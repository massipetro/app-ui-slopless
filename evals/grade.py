"""Programmatic grader for app-ui-slopless evals.

Usage: python3 grade.py <iteration-dir>
Writes grading.json into every <eval>/<config>/ run dir.
Checks are regex heuristics over the produced code/markdown: they catch presence
of craft (haptics, reduce-motion, semantics, labels...) and absence of slop tells.
Visual taste is judged by the human in the viewer, not here.
"""
import json, re, sys
from pathlib import Path


def read(d, *names):
    out = ""
    for n in names:
        for p in d.glob(n):
            out += p.read_text(errors="ignore") + "\n"
    return out


def check(text, pattern, flags=re.I | re.S | re.M):
    m = re.search(pattern, text, flags)
    return bool(m), (m.group(0)[:120] if m else "no match")


def absent(text, pattern, flags=re.I | re.S | re.M):
    ok, ev = check(text, pattern, flags)
    return (not ok), ("not found" if not ok else f"found: {ev}")


def eval1(d):
    kt = read(d, "**/*.kt")
    resp = read(d, "response.md")
    return with_compile([
        ("Brief states a style with concrete signature moves", *check(resp, r"signature|owned idea")),
        ("Text sized in sp", *check(kt, r"\d+(\.\d+)?\.sp")),
        ("Pressed state driven by interaction source", *check(kt, r"collectIsPressedAsState|isPressed|detectTapGestures\([^)]*onPress|onPress\s*=")),
        ("Haptic feedback on check-off", *check(kt, r"HapticFeedback|performHapticFeedback")),
        ("Reduce-motion handled", *check(kt, r"reduceMotion|ReduceMotion|ANIMATOR_DURATION_SCALE|animationsEnabled|MotionDurationScale")),
        ("Spring motion used", *check(kt, r"spring\(")),
        ("Check-off exposes semantics (toggleable/role/stateDescription)", *check(kt, r"toggleable|Role\.Checkbox|Role\.Switch|stateDescription")),
        ("Touch targets >= 48dp enforced", *check(kt, r"minimumInteractiveComponentSize|(heightIn|size|height)\(\s*(min\s*=\s*)?(4[89]|[5-9]\d)\.dp|\w*(Min|Target)\w*\s*(:\s*Dp)?\s*=\s*(4[89]|[5-9]\d)\.dp")),
        ("Tokens defined once (theme / token object)", *check(kt, r"(object|class)\s+\w*(Token|Palette|Color|Brand|Theme)\w*|^\s*(private |internal )?object\s+\w+\s*\{|staticCompositionLocalOf|MaterialTheme\(")),
        ("No purple/indigo gradient slop", *absent(kt, r"(Gradient[^\n]{0,120}0xFF(6A5AE0|7C3AED|8B5CF6|6366F1|9C6BFF|A855F7))")),
        ("Check glyph is custom-drawn, not a stock Icons.*.Check", *check(kt, r"PathMeasure|getSegment|drawPath|ImageVector\.Builder|PathParser")),
        ("Ambient/idle motion present (infinite transition)", *check(kt, r"rememberInfiniteTransition|infiniteRepeatable")),
        ("Lazy list items keyed (stable identity)", *check(kt, r"items\([^)]*key\s*=|itemsIndexed\([^)]*key\s*=|key\(\s*\w+\.id\s*\)")),
    ], d)


def eval2(d):
    sw = read(d, "**/ProfileView.swift")
    return with_compile([
        ("Keeps NavigationStack (native mechanics)", *check(sw, r"NavigationStack")),
        ("Hard shadow is an offset shape, not blurred .shadow", *check(sw, r"\.offset\(\s*x:\s*\w+[^)]*y:")),
        ("No blurred .shadow(radius > 0)", *absent(sw, r"\.shadow\([^)]*radius:\s*[1-9]")),
        ("Thick strokes (lineWidth >= 2)", *check(sw, r"(lineWidth:\s*([2-9]|\d{2}))|stroke\([^)]*,\s*([2-9])\)|border\([^)]*width:\s*[2-9]")),
        ("Small radii (no corner radius > 8, literal or token)", *absent(sw, r"cornerRadius[:(]\s*(9|[1-9]\d)|[Rr]adius\w*\s*(:\s*CGFloat)?\s*=\s*(9|[1-9]\d)\b|\bradius:\s*(9|[1-9]\d)\b")),
        ("Fonts scale with Dynamic Type", *check(sw, r"relativeTo:|\.font\(\.(largeTitle|title|title2|title3|headline|body|callout|subheadline|footnote|caption)")),
        ("Custom controls/buttons have a ButtonStyle (pressed state)", *check(sw, r"ButtonStyle")),
        ("Accessibility labels/values on custom elements", *check(sw, r"accessibility(Label|Value|Element|AddTraits)")),
        ("44pt minimum targets", *check(sw, r"minHeight:\s*(4[4-9]|[5-9]\d)|height:\s*(4[4-9]|[5-9]\d)|frame\(minWidth:\s*44|(?i:height|target)\w*\s*:\s*CGFloat\s*=\s*(4[4-9]|[5-9]\d)")),
        ("No default Color.gray slop", *absent(sw, r"Color\.gray|\.foregroundColor\(\.gray\)")),
        ("Reduce Motion respected", *check(sw, r"accessibilityReduceMotion")),
        ("No index-based ForEach identity", *absent(sw, r"ForEach\([^)]*\.indices|id:\s*\\\.offset")),
    ], d)


def eval3(d):
    audit = read(d, "**/audit.md")
    kt = read(d, "**/CheckoutScreen.kt")
    # named sources or rule IDs from references/principles.md (R-FORM-1 etc.)
    principles = len(set(m.lower() for m in re.findall(
        r"Nielsen|Fitts|Hoober|Norman|Shneiderman|Wroblewski|WCAG|Hick|Cowan|Gestalt|Tractinsky|Clark|Saffer|Cooper|HIG|Material|Baymard|R-[A-Z0-9]+-\d+", audit)))
    return with_compile([
        ("Audit cites >= 5 distinct named principles/sources", principles >= 5, f"{principles} distinct"),
        ("Audit gives measured contrast ratios", *check(audit, r"\d(\.\d+)?\s*:\s*1")),
        ("Audit rates severity", *check(audit, r"sev|severity|critical|major|minor")),
        ("Audit points at code lines", *check(audit, r"(line|L|\.kt:)\s*\d+")),
        ("Redesign uses persistent labels (label =), not placeholder-only", *check(kt, r"label\s*=\s*(\{|\"[A-Z])")),
        ("Numeric keyboard for card fields", *check(kt, r"KeyboardType\.(Number|NumberPassword)")),
        ("Handles insets / IME", *check(kt, r"imePadding|WindowInsets|navigationBarsPadding|safeDrawing|Scaffold")),
        ("Purple gradient removed", *absent(kt, r"0xFF6A5AE0|0xFF9C6BFF|verticalGradient\(listOf\(Color\(0xFF6A")),
        ("Checkbox target >= 48dp (no 20dp checkbox)", *absent(kt, r"Checkbox\([^)]*size\(20\.dp\)")),
        ("Autofill / content type hints for card", *check(kt, r"ContentType\.CreditCard|autofill|AutofillType|contentType")),
        ("User input survives rotation (rememberSaveable / TextFieldState / ViewModel)", *check(kt, r"rememberSaveable|rememberTextFieldState|TextFieldState|SavedStateHandle")),
    ], d)


sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import lint  # noqa: E402  (the skill's own gate, so "no FAIL" means the same thing here)


def lint_fails(d):
    fails = [f"{r}:{n}" for f in sorted(d.rglob("*")) if f.suffix in (".swift", ".kt")
             for r, n, _ in lint.lint_file(f) if lint.RULES[r][0] == "FAIL"]
    return (not fails), ("no FAIL" if not fails else ", ".join(fails[:6]))


LIBRARY = json.loads((Path(__file__).resolve().parent.parent / "library" / "directions.json").read_text())["directions"]


def direction_stated(resp):
    """A dealt direction counts when a seed (only deal.py makes one) sits near the direction's id,
    its library name, or plain words like 'direction' / 'style' (runs often paraphrase the id)."""
    names = [re.escape(d["id"]) for d in LIBRARY] + [re.escape(d["name"]) for d in LIBRARY]
    named = r"(" + "|".join(names) + r"|\bdirections?\b|\bstyles?\b)"
    near = named + r"[\s\S]{0,240}?seed\D{0,5}\d+|seed\D{0,5}\d+[\s\S]{0,240}?" + named
    return check(resp, near)


REPORT_LABELS = ["Inventory", "Direction", "Owned idea", "Competitor test", "Live thing", "Built",
                 "Signature moves", "Lint", "Critique (final round)", "Bottom edge", "Still short",
                 "Sample content to replace", "Pictures", "Warnings", "Not verified"]


def report_block(resp):
    """The skill's fixed report block: header line, then all 15 labels at line starts, in order."""
    i = resp.rfind("app-ui-slopless report")
    if i < 0:
        return False, "no 'app-ui-slopless report' block"
    block, pos, missing = resp[i:], 0, []
    for label in REPORT_LABELS:
        m = re.compile(r"^\s*" + re.escape(label) + r"\s*:", re.M).search(block, pos)
        if m:
            pos = m.end()
        else:
            missing.append(label)
    return (not missing), ("all 15 labels in order" if not missing else "missing or out of order: " + ", ".join(missing))


def swift_typechecks(d):
    """Typecheck the run's Swift with scripts/typecheck.py. None when there's no Xcode here (check skipped)."""
    import subprocess
    files = [str(f) for f in sorted(d.rglob("*.swift"))]
    if not files:
        return None
    tc = Path(__file__).resolve().parent.parent / "scripts" / "typecheck.py"
    # Pinned: a run can't pass by writing its own Package.swift with a newer platform.
    proc = subprocess.run([sys.executable, str(tc), *files, "--ios", "17.0"], capture_output=True, text=True)
    if proc.returncode == 3:
        return None
    last = (proc.stdout.strip().splitlines() or ["no output"])[-1]
    first_error = next((l for l in proc.stdout.splitlines() if ": error:" in l), "")
    return proc.returncode == 0, (last if proc.returncode == 0 else first_error.split("error:")[-1].strip()[:110] or last)


def kotlin_compiles(d):
    """Compile the run's Kotlin with scripts/compile_kotlin.py. None when it can't run here (check skipped)."""
    import subprocess
    files = [str(f) for f in sorted(d.rglob("*.kt"))]
    if not files:
        return None
    ck = Path(__file__).resolve().parent.parent / "scripts" / "compile_kotlin.py"
    proc = subprocess.run([sys.executable, str(ck), *files], capture_output=True, text=True)
    if proc.returncode == 3:
        return None
    last = (proc.stdout.strip().splitlines() or ["no output"])[-1]
    first_error = next((l for l in proc.stdout.splitlines() if ": error:" in l), "")
    return proc.returncode == 0, (last if proc.returncode == 0 else first_error.split("error:")[-1].strip()[:110] or last)


def with_compile(checks, d):
    tc = swift_typechecks(d)
    kc = kotlin_compiles(d)
    return (checks + ([("Swift typechecks (iOS 17 simulator SDK)", *tc)] if tc is not None else [])
            + ([("Kotlin compiles (Compose MP 1.9.0, JVM + Android)", *kc)] if kc is not None else []))


def process_checks(resp):
    # The no-preset evals test the workflow itself: inventory, deal, idea, critique.
    return [
        ("Report block: all 15 labels, in order", *report_block(resp)),
        ("Inventory of product-only items listed", *check(resp, r"inventory")),
        ("Direction dealt: named (id, name or plain words) with its seed", *direction_stated(resp)),
        ("Owned-idea sentence written", *check(resp, r"In this app,[^\n]{0,200}becomes")),
        ("Competitor test applied", *check(resp, r"competitor")),
        ("Critique scored (Idea / Hierarchy / overall)", *check(resp, r"Idea\s*\d+[\s\S]{0,80}Hierarchy\s*\d+|overall\s*\d")),
        ("Lint gate run", *check(resp, r"lint\.py|\d+ FAIL")),
        ("Motion recorded as a filmstrip, or stated as not recorded", *check(resp, r"filmstrip|motion not recorded")),
        ("Signature moves pointed at in the resting frame", *check(resp, r"^\s*Signature moves\s*:[^\n]*(→|->|not visible)[^\n]*stock layout")),
    ]


def eval4(d):
    sw = read(d, "**/*.swift")
    resp = read(d, "response.md")
    return with_compile(process_checks(resp) + [
        ("lint.py: no FAIL in the produced Swift", *lint_fails(d)),
        ("Live countdown driven by time (TimelineView / Timer / Date math)", *check(sw, r"TimelineView|Timer\.publish|\.timeIntervalSince|Date\.now|countdown")),
        ("Real place names, no placeholder data", *check(sw, r"Procida|Ischia|Napoli|Naples|Molo|Beverello|Pozzuoli")),
        ("Fonts scale with Dynamic Type", *check(sw, r"relativeTo:|\.font\(\.(largeTitle|title|title2|title3|headline|body|callout|subheadline|footnote|caption)")),
        ("VoiceOver labels on custom elements", *check(sw, r"accessibility(Label|Value|Element|AddTraits)")),
        ("Reduce Motion respected", *check(sw, r"accessibilityReduceMotion")),
    ], d)


def eval5(d):
    kt = read(d, "**/*.kt")
    resp = read(d, "response.md")
    return with_compile(process_checks(resp) + [
        ("lint.py: no FAIL in the produced Kotlin", *lint_fails(d)),
        ("Weekly reset modelled (Monday / week start)", *check(kt, r"MONDAY|Monday|weekStart|startOfWeek|resetsOn")),
        ("Over-budget or empty-week state designed", *check(kt, r"over ?budget|overBudget|isEmpty|EmptyWeek|empty state", re.I)),
        ("Text sized in sp", *check(kt, r"\d+(\.\d+)?\.sp")),
        ("Semantics on custom elements", *check(kt, r"semantics|contentDescription|stateDescription")),
        ("Reduce-motion handled", *check(kt, r"reduceMotion|ReduceMotion|ANIMATOR_DURATION_SCALE|animationsEnabled|MotionDurationScale")),
    ], d)


def eval6(d):
    sw = read(d, "**/*.swift")
    html = read(d, "**/*.html")
    resp = read(d, "response.md")
    return with_compile(process_checks(resp) + [
        ("lint.py: no FAIL in the produced Swift", *lint_fails(d)),
        ("Photo slots keep a fixed aspect ratio", *check(sw, r"aspectRatio\(")),
        ("Remote photos handle loading and failure (AsyncImage phases or placeholder)", *check(sw, r"AsyncImage[\s\S]{0,600}(phase|placeholder:|\.failure|\.empty)")),
        ("No grey placeholder boxes standing in for photos", *absent(sw + html, r"Rectangle\(\)\s*\.fill\(\s*(Color\.)?(gray|secondary)|fill\(Color\(\.system(Gray|Fill)|background:\s*#(ccc|ddd|e0e0e0|d9d9d9)\b")),
        ("Picture sourcing is honest (licence / credit stated, or drawn)", *check(resp, r"licen[cs]e|public domain|CC[ -]BY|CC0|Wikimedia|Openverse|credit|drawn in code|illustrat")),
        ("Fonts scale with Dynamic Type", *check(sw, r"relativeTo:|\.font\(\.(largeTitle|title|title2|title3|headline|body|callout|subheadline|footnote|caption)")),
    ], d)


GRADERS = {"playful-habit-home-cmp": eval1, "neobrutalist-profile-swiftui": eval2, "checkout-audit-warm-premium": eval3,
           "ferry-home-no-preset-swiftui": eval4, "flat-budget-no-preset-cmp": eval5,
           "guesthouse-photos-no-preset-swiftui": eval6}

if __name__ == "__main__":
    it = Path(sys.argv[1])
    # layout: <iteration>/eval-<id>-<name>/<config>/run-<n>/outputs
    for name, fn in GRADERS.items():
        for run in sorted(it.glob(f"eval-*-{name}/*/run-*")):
            cfg = run.parent.name
            if not (run / "outputs").exists():
                continue
            res = fn(run / "outputs")
            exp = [{"text": t, "passed": bool(p), "evidence": e} for t, p, e in res]
            passed = sum(x["passed"] for x in exp)
            (run / "grading.json").write_text(json.dumps({
                "expectations": exp,
                "summary": {"passed": passed, "failed": len(exp) - passed, "total": len(exp),
                            "pass_rate": round(passed / len(exp), 2)},
            }, indent=2))
            print(f"{name:32} {cfg:14} {passed}/{len(exp)}")
