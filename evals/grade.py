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
    kt = read(d, "*.kt")
    resp = read(d, "response.md")
    return [
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
    ]


def eval2(d):
    sw = read(d, "ProfileView.swift")
    return [
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
    ]


def eval3(d):
    audit = read(d, "audit.md")
    kt = read(d, "CheckoutScreen.kt")
    # named sources or rule IDs from references/principles.md (R-FORM-1 etc.)
    principles = len(set(m.lower() for m in re.findall(
        r"Nielsen|Fitts|Hoober|Norman|Shneiderman|Wroblewski|WCAG|Hick|Cowan|Gestalt|Tractinsky|Clark|Saffer|Cooper|HIG|Material|Baymard|R-[A-Z0-9]+-\d+", audit)))
    return [
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
    ]


GRADERS = {"playful-habit-home-cmp": eval1, "neobrutalist-profile-swiftui": eval2, "checkout-audit-warm-premium": eval3}

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
