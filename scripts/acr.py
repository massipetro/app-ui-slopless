#!/usr/bin/env python3
"""Draft an Accessibility Conformance Report (ACR) for the screens a build made, in VPAT 2.5Rev form.

  acr.py <.swift / .kt files or folder> [...] [--report response.md] [--product "Ferry, home screen"]
         [--platform ios|android|macos] [--out acr.md]

It reads two things and writes a Markdown ACR (WCAG 2.2 edition: Table 1 Level A, Table 2 Level AA,
then notes for Revised Section 508 chapter 5 and EN 301 549 clause 11):
  - the report's "Accessibility:" line (SKILL.md step 5), where the build states, per criterion,
    "Supports", "Partially supports", "Does not support" or "Not applicable", each with a reason;
  - scripts/lint.py's accessibility rules over the code, each mapped to the criteria it is evidence
    against (lint.CRITERIA).

A lint FAIL on a criterion the report claims to support turns the claim into "Partially Supports" and
names the file and line. A WARN is listed in the remarks to review. A criterion the report doesn't
mention, and no rule settles, is marked "To evaluate": VPAT 2.5 allows "Not Evaluated" only for
Level AAA, so a person has to answer it before the report goes out. The criteria WCAG2ICT says apply
only to sets of software (2.4.1, 2.4.5, 3.2.3, 3.2.6) default to "Not Applicable" with that reason.

This is a draft from code, lint and renders. Nothing here has been tested with VoiceOver, TalkBack,
Switch Control, Voice Control or a keyboard, and the Evaluation Methods section says so. Publish it
only after that testing.

Standard library only; works on Python 3.9.
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint  # noqa: E402

# WCAG 2.2 Level A and AA (4.1.1 Parsing is obsolete in 2.2 and left out, as ITI's WCAG edition marks it).
CRITERIA = [
    ("1.1.1", "Non-text Content", "A"), ("1.2.1", "Audio-only and Video-only (Prerecorded)", "A"),
    ("1.2.2", "Captions (Prerecorded)", "A"), ("1.2.3", "Audio Description or Media Alternative (Prerecorded)", "A"),
    ("1.3.1", "Info and Relationships", "A"), ("1.3.2", "Meaningful Sequence", "A"), ("1.3.3", "Sensory Characteristics", "A"),
    ("1.4.1", "Use of Color", "A"), ("1.4.2", "Audio Control", "A"), ("2.1.1", "Keyboard", "A"), ("2.1.2", "No Keyboard Trap", "A"),
    ("2.1.4", "Character Key Shortcuts", "A"), ("2.2.1", "Timing Adjustable", "A"), ("2.2.2", "Pause, Stop, Hide", "A"),
    ("2.3.1", "Three Flashes or Below Threshold", "A"), ("2.4.1", "Bypass Blocks", "A"), ("2.4.2", "Page Titled", "A"),
    ("2.4.3", "Focus Order", "A"), ("2.4.4", "Link Purpose (In Context)", "A"), ("2.5.1", "Pointer Gestures", "A"),
    ("2.5.2", "Pointer Cancellation", "A"), ("2.5.3", "Label in Name", "A"), ("2.5.4", "Motion Actuation", "A"),
    ("3.1.1", "Language of Page", "A"), ("3.2.1", "On Focus", "A"), ("3.2.2", "On Input", "A"), ("3.2.6", "Consistent Help", "A"),
    ("3.3.1", "Error Identification", "A"), ("3.3.2", "Labels or Instructions", "A"), ("3.3.7", "Redundant Entry", "A"),
    ("4.1.2", "Name, Role, Value", "A"),
    ("1.2.4", "Captions (Live)", "AA"), ("1.2.5", "Audio Description (Prerecorded)", "AA"), ("1.3.4", "Orientation", "AA"),
    ("1.3.5", "Identify Input Purpose", "AA"), ("1.4.3", "Contrast (Minimum)", "AA"), ("1.4.4", "Resize Text", "AA"),
    ("1.4.5", "Images of Text", "AA"), ("1.4.10", "Reflow", "AA"), ("1.4.11", "Non-text Contrast", "AA"),
    ("1.4.12", "Text Spacing", "AA"), ("1.4.13", "Content on Hover or Focus", "AA"), ("2.4.5", "Multiple Ways", "AA"),
    ("2.4.6", "Headings and Labels", "AA"), ("2.4.7", "Focus Visible", "AA"), ("2.4.11", "Focus Not Obscured (Minimum)", "AA"),
    ("2.5.7", "Dragging Movements", "AA"), ("2.5.8", "Target Size (Minimum)", "AA"), ("3.1.2", "Language of Parts", "AA"),
    ("3.2.3", "Consistent Navigation", "AA"), ("3.2.4", "Consistent Identification", "AA"), ("3.3.3", "Error Suggestion", "AA"),
    ("3.3.4", "Error Prevention (Legal, Financial, Data)", "AA"), ("3.3.8", "Accessible Authentication (Minimum)", "AA"),
    ("4.1.3", "Status Messages", "AA"),
]
SETS_ONLY = {"2.4.1", "2.4.5", "3.2.3", "3.2.6"}
NO_SPACING_OVERRIDE = {"1.4.12"}
TERMS = {"supports": "Supports", "partially supports": "Partially Supports", "does not support": "Does Not Support",
         "not applicable": "Not Applicable"}
SC = re.compile(r"(\d\.\d{1,2}\.\d{1,2})(?:\s*\(((?:[^()]|\([^()]*\))*)\))?")


def parse_line(text: str) -> dict[str, tuple[str, str]]:
    """{criterion: (term, reason)} from the last 'Accessibility:' line of a report."""
    lines = [l for l in text.splitlines() if re.match(r"\s*Accessibility\s*:", l)]
    if not lines:
        return {}
    line = lines[-1].split(":", 1)[1]
    out: dict[str, tuple[str, str]] = {}
    # Split at each conformance term, longest first so "partially supports" isn't read as "supports".
    marks = sorted(TERMS, key=len, reverse=True)
    pattern = re.compile(r"(?i)\b(" + "|".join(re.escape(m) for m in marks) + r")\b\s*:?")
    hits = list(pattern.finditer(line))
    for i, h in enumerate(hits):
        if h.start() and re.search(r"(?i)partially\s*$|does\s*$|not\s*$", line[:h.start()]):
            continue
        chunk = line[h.end():hits[i + 1].start() if i + 1 < len(hits) else len(line)]
        term = TERMS[h.group(1).lower()]
        for m in SC.finditer(chunk):
            out.setdefault(m.group(1), (term, (m.group(2) or "").strip()))
    return out


def lint_by_criterion(paths: list[Path], platform: str | None) -> dict[str, list[tuple[str, str, str]]]:
    files: list[Path] = []
    for p in paths:
        files += sorted(f for f in p.rglob("*") if f.suffix in (".swift", ".kt") and "build" not in f.parts) if p.is_dir() else [p]
    found: dict[str, list[tuple[str, str, str]]] = {}
    swift_platform = "macos" if platform == "macos" else ("ios" if platform == "ios" else None)
    for f in files:
        for rule, n, _ in lint.lint_file(f, swift_platform):
            for sc in lint.CRITERIA.get(rule, []):
                found.setdefault(sc, []).append((lint.RULES[rule][0], rule, f"{f.name}:{n}"))
    return found


def cell(term: str, reason: str, findings: list[tuple[str, str, str]]) -> tuple[str, str]:
    fails = [f for f in findings if f[0] == "FAIL"]
    warns = [f for f in findings if f[0] == "WARN"]
    remarks = [reason] if reason else []
    if fails:
        where = ", ".join(f"`{r}` {loc}" for _, r, loc in fails[:4]) + (" …" if len(fails) > 4 else "")
        if term in ("Supports", "To evaluate", ""):
            term = "Partially Supports"
        remarks.append(f"Lint FAIL: {where}.")
    if warns:
        remarks.append("To review (lint WARN): " + ", ".join(f"`{r}` {loc}" for _, r, loc in warns[:4]) + (" …" if len(warns) > 4 else "") + ".")
    return term or "To evaluate", " ".join(remarks)


def build(paths: list[Path], report: str, product: str, platform: str | None) -> str:
    claims = parse_line(report)
    found = lint_by_criterion(paths, platform)
    plat = {"ios": "iOS (SwiftUI)", "android": "Android (Jetpack Compose)", "macos": "macOS (SwiftUI)"}.get(platform or "", "native app")
    out = [f"# Accessibility Conformance Report (draft): {product}", "",
           "Based on VPAT® 2.5Rev (ITI), WCAG edition. **Draft, not for publication**: see Evaluation Methods Used.", "",
           f"- **Name of product / version:** {product}",
           f"- **Report date:** {datetime.date.today().isoformat()}",
           f"- **Product description:** {plat} screens built with the app-ui-slopless skill.",
           "- **Contact information:** (fill in)",
           "- **Notes:** Scope is the screens in the files listed below, not the whole app. Conformance terms follow ITI's definitions. "
           "\"To evaluate\" is not a VPAT term: it marks criteria nobody has answered yet, and every one must be answered before publishing.",
           "- **Evaluation methods used:** Source review and `scripts/lint.py --a11y` (heuristic rules mapped to WCAG criteria), "
           "renders at default and largest text sizes, and the build's own critique. **Not tested with VoiceOver, TalkBack, Switch Control, "
           "Voice Control, Voice Access or a hardware keyboard on a device.** Complete that testing and update this report before use.",
           f"- **Files:** {', '.join(p.name for p in paths)}", "",
           "## Applicable standards / guidelines", "",
           "| Standard / guideline | Included in report |", "|---|---|",
           "| WCAG 2.2 Level A | Yes |", "| WCAG 2.2 Level AA | Yes |", "| WCAG 2.2 Level AAA | No |",
           "| Revised Section 508 (36 CFR 1194), Chapter 5 Software | Notes below |",
           "| EN 301 549 V3.2.1 / V4.1.1, Clause 11 Software | Notes below |", "",
           "## Terms", "",
           "- **Supports**: the functionality has at least one method that meets the criterion without known defects, or meets it with equivalent facilitation.",
           "- **Partially Supports**: some functionality does not meet the criterion.",
           "- **Does Not Support**: the majority of functionality does not meet the criterion.",
           "- **Not Applicable**: the criterion is not relevant to the product.",
           "- **Not Evaluated**: allowed only for Level AAA (not used here).", ""]
    counts: dict[str, int] = {}
    for level, title in (("A", "Table 1: Success Criteria, Level A"), ("AA", "Table 2: Success Criteria, Level AA")):
        out += [f"## {title}", "", "| Criteria | Conformance Level | Remarks and Explanations |", "|---|---|---|"]
        for sc, name, lv in CRITERIA:
            if lv != level:
                continue
            term, reason = claims.get(sc, ("", ""))
            if not term and sc in SETS_ONLY:
                term, reason = "Not Applicable", "WCAG2ICT applies this only to sets of software programs; this is one program."
            if not term and sc in NO_SPACING_OVERRIDE:
                term, reason = "Not Applicable", "The platform offers no mechanism to override text spacing (WCAG2ICT; WCAG2Mobile draft)."
            term, remarks = cell(term, reason, found.get(sc, []))
            counts[term] = counts.get(term, 0) + 1
            out.append(f"| {sc} {name} (Level {lv}) | {term} | {remarks.replace('|', '/')} |")
        out.append("")
    out += ["## Revised Section 508 and EN 301 549", "",
            "- **508 E207.2 / EN 301 549 clause 11.1–11.4:** the WCAG tables above, read with WCAG2ICT (\"software\" for \"web page\"; pt or dp for CSS px).",
            "- **508 502 / EN 11.5 Interoperability with assistive technology:** the evidence for 4.1.2 above (platform accessibility APIs: labels, traits/roles, values, actions).",
            "- **508 503.2 / EN 11.7 User preferences** (colour, contrast, font size, focus cursor): "
            + ("Lint findings: " + ", ".join(f"`{r}` {loc}" for _, r, loc in found.get("503.2", [])[:4]) + "." if found.get("503.2") else
               "to evaluate: Dynamic Type / font scale, Increase Contrast, Reduce Transparency, Bold Text and dark appearance followed."),
            "- **508 503.4 / EN 11.7–7.x captions and audio description controls:** Not Applicable unless the screens play video.",
            "- **EN 301 549 V4.1.1** (published 2026-09, prepared for the European Accessibility Act) adds 11.2.4.2 (each screen or window titled) "
            "and 11.3.2.4 (consistent identification within one program); answer 3.2.4 and 2.4.2 above with that in mind.", "",
            "## Legal disclaimer", "", "(fill in)", "",
            "---", "Summary: " + ", ".join(f"{v} {k}" for k, v in sorted(counts.items(), key=lambda kv: -kv[1])) + "."]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--report", help="the build's reply (response.md) holding the Accessibility: line")
    ap.add_argument("--product", default="", help="product and screen name for the header")
    ap.add_argument("--platform", choices=["ios", "android", "macos"])
    ap.add_argument("--out", help="write the Markdown here (default: stdout)")
    args = ap.parse_args()
    paths = [Path(p) for p in args.paths]
    missing = [p for p in paths if not p.exists()]
    if missing:
        print(f"acr: not found: {', '.join(map(str, missing))}", file=sys.stderr)
        return 2
    report = Path(args.report).read_text(errors="ignore") if args.report else ""
    if args.report and not parse_line(report):
        print("acr: no 'Accessibility:' line in the report; every criterion starts as 'To evaluate'", file=sys.stderr)
    md = build(paths, report, args.product or paths[0].stem, args.platform)
    if args.out:
        Path(args.out).write_text(md)
        print(f"acr: draft written to {args.out} ({md.splitlines()[-1]})")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
