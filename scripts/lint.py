#!/usr/bin/env python3
"""Lint SwiftUI (.swift) and Compose / CMP (.kt) source for slop tells and craft defects.

  lint.py <file or folder> [...] [--allow rule,rule] [--list-rules]

Prints FAIL / WARN findings as file:line. Exit code 1 if any FAIL remains.
A FAIL is a tell or defect with no good default reason; a WARN needs a one-sentence
defence (e.g. hard offset shadows are the point of neo-brutalist). Use --allow for
deliberate style choices and say so in the report.

Heuristic regexes, not a parser: it catches the common defaults, not everything.
Standard library only; works on Python 3.9.
"""
from __future__ import annotations

import argparse
import colorsys
import re
import sys
from pathlib import Path

RULES = {
    "violet-accent": ("FAIL", "violet/indigo colour: the AI default accent", "Use the direction's palette; give the accent a reason"),
    "gradient-fill": ("WARN", "decorative gradient", "Flat colour; a gradient only as a scrim under text on a photo"),
    "default-grey": ("FAIL", "stock system grey", "A tuned ink2 token that passes 4.5:1 on its surface"),
    "soft-shadow": ("FAIL", "faint black blurred shadow (the 5%-black card shadow)", "Separate surfaces by tone, or use the direction's depth model"),
    "blur-shadow": ("WARN", "blurred shadow", "Fine for one tinted floating element; never on every card"),
    "glass": ("WARN", "translucent / blurred surface", "Opaque surface one tone step from the ground, unless it is the system material"),
    "hex-outside-tokens": ("WARN", "colour literal outside the theme/token file", "Define colours once as tokens and reference them"),
    "same-radius": ("WARN", "every shape uses the same corner radius", "Vary radius by role (image, card, button, chip)"),
    "fixed-font-size": ("FAIL", "font size that ignores Dynamic Type / text scaling", "SwiftUI: a text style or .custom(_, size:, relativeTo:); Compose: sp"),
    "tiny-text": ("WARN", "text under 12pt/sp", "12+ for anything people must read; warn if the style needs smaller"),
    "slop-font": ("WARN", "font that is an AI default", "The direction's dealt type system, or a stated reason"),
    "emoji": ("FAIL", "emoji in UI text", "A custom glyph in the direction's icon language, or words"),
    "placeholder-only-field": ("FAIL", "text field labelled only by its placeholder", "A persistent label above the field"),
    "small-target": ("FAIL", "tap target under 44pt / 48dp", "Make the whole row tappable, or minimumInteractiveComponentSize / frame(minHeight: 44)"),
    "unlabelled-icon-button": ("FAIL", "icon-only button with no accessible name", "contentDescription / accessibilityLabel"),
    "placeholder-data": ("FAIL", "placeholder sample data", "Domain-real names, items and amounts at full density"),
    "generic-button-label": ("WARN", "button not named for its action", "Name the action: \"Pay €642\", \"Mark as done\""),
    "slop-copy": ("WARN", "generic marketing copy", "Say the specific thing this product does"),
    "stock-check": ("WARN", "core verb drawn with a stock check icon", "Custom-draw and animate the core verb's glyph"),
    "no-reduce-motion": ("WARN", "animation with no Reduce Motion / Remove animations handling", "Read accessibilityReduceMotion / animator scale and swap travel for fades"),
}

HEX_KT = re.compile(r"Color\(\s*0x([0-9A-Fa-f]{8}|[0-9A-Fa-f]{6})\s*\)")
HEX_STR = re.compile(r"\"#?([0-9A-Fa-f]{6})\"")
RGB_SWIFT = re.compile(r"Color\(\s*(?:\.sRGB,\s*)?red:\s*([\d.]+)\s*,\s*green:\s*([\d.]+)\s*,\s*blue:\s*([\d.]+)")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF☀-➿⭐⭕]")
STRING = re.compile(r"\"((?:[^\"\\\n]|\\.)*)\"")
TOKEN_FILE = re.compile(r"(Theme|Token|Palette|Colou?rs?|Brand|DesignSystem|Style)", re.I)
TOKEN_DECL = re.compile(r"(object|enum|struct|extension)\s+\w*(Tokens?|Palette|Colou?rs?|Theme)\b|extension\s+Color\b|ColorScheme\(|lightColorScheme|darkColorScheme")
ANIMATION = re.compile(r"withAnimation|\.animation\(|animate\w*AsState|spring\(|rememberInfiniteTransition|AnimatedVisibility|AnimatedContent|\.transition\(|phaseAnimator|keyframeAnimator|updateTransition")
REDUCE_MOTION = re.compile(r"accessibilityReduceMotion|ReduceMotion|reduceMotion|ANIMATOR_DURATION_SCALE|MotionDurationScale|isReduceMotionEnabled|areAnimationsEnabled")


def is_violet(r: float, g: float, b: float) -> bool:
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return 235 <= h * 360 <= 300 and s >= 0.4 and 0.25 <= l <= 0.85


def hex_rgb(h: str) -> tuple[float, float, float]:
    h = h[-6:]
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def strip_comment(line: str) -> str:
    # Drop // comments, but not the // inside "https://..." strings.
    out, in_str = [], False
    i = 0
    while i < len(line):
        c = line[i]
        if c == '"' and (i == 0 or line[i - 1] != "\\"):
            in_str = not in_str
        if not in_str and line.startswith("//", i):
            break
        out.append(c)
        i += 1
    return "".join(out)


def call_span(text: str, start: int) -> str:
    """Text of the call starting at the '(' at or after start, plus a trailing { } lambda."""
    i = text.find("(", start)
    if i < 0:
        return ""
    depth, j = 0, i
    while j < len(text):
        if text[j] == "(":
            depth += 1
        elif text[j] == ")":
            depth -= 1
            if depth == 0:
                break
        j += 1
    end = j + 1
    rest = text[end:end + 2].lstrip()
    if rest.startswith("{"):
        k = text.find("{", end)
        depth = 0
        while k < len(text):
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        end = k + 1
    return text[start:end]


def brace_block(text: str, start: int) -> tuple[int, int]:
    """(start, end) of the { } block whose opening brace is at or after start."""
    i = text.find("{", start)
    if i < 0:
        return (len(text), len(text))
    depth = 0
    for j in range(i, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return (i, j + 1)
    return (i, len(text))


def lint_file(path: Path) -> list[tuple[str, int, str]]:
    raw = path.read_text(errors="ignore")
    lines = [strip_comment(l) for l in raw.splitlines()]
    text = "\n".join(lines)
    swift = path.suffix == ".swift"
    found: list[tuple[str, int, str]] = []

    def add(rule: str, lineno: int, detail: str = "") -> None:
        found.append((rule, lineno, detail))

    def line_of(offset: int) -> int:
        return text.count("\n", 0, offset) + 1

    token_file = bool(TOKEN_FILE.search(path.stem)) or bool(TOKEN_DECL.search(text))

    for n, line in enumerate(lines, 1):
        # Colours
        colours = [hex_rgb(m.group(1)) for m in HEX_KT.finditer(line)]
        colours += [hex_rgb(m.group(1)) for m in HEX_STR.finditer(line) if "Color" in line or "color" in line]
        colours += [tuple(float(x) for x in m.groups()) for m in RGB_SWIFT.finditer(line)]  # type: ignore[misc]
        if any(is_violet(*c) for c in colours):
            add("violet-accent", n, line.strip()[:80])
        if colours and not token_file:
            add("hex-outside-tokens", n, line.strip()[:80])
        if re.search(r"LinearGradient\(|RadialGradient\(|AngularGradient\(|\.linearGradient\(|Brush\.(vertical|horizontal|linear|radial|sweep)Gradient", line) \
                and not re.search(r"scrim|Scrim", line):
            add("gradient-fill", n)
        if re.search(r"Color\.gray\b|\(\s*\.gray\s*\)|Color\(\.systemGray\d?\)|Color\.(Gray|LightGray|DarkGray)\b|0xFF(888888|9E9E9E|BDBDBD|757575)", line):
            add("default-grey", n)

        # Depth
        if swift and ".shadow(" in line:
            if re.search(r"\.shadow\([^)]*\.black\.opacity\(0?\.(0\d|1\d?)\)[^)]*radius:\s*[1-9]", line):
                add("soft-shadow", n)
            elif re.search(r"\.shadow\([^)]*radius:\s*[1-9]", line):
                add("blur-shadow", n)
        if not swift and re.search(r"Modifier\.shadow\(|\.shadow\(\s*\d|cardElevation\(\s*(defaultElevation\s*=\s*)?[1-9]", line) \
                and not re.search(r"ambientColor|spotColor", line):
            add("soft-shadow", n)
        if re.search(r"\.(ultraThin|thin|regular|thick)Material\b|Modifier\.blur\(|\.blur\(radius:\s*[1-9]|\.copy\(alpha\s*=\s*0?\.[0-3]\d*f?\)\s*[,)]", line) \
                and re.search(r"Material|blur|containerColor|background", line):
            add("glass", n)

        # Type
        if swift:
            if re.search(r"\.system\(size:", line) and "relativeTo" not in line:
                add("fixed-font-size", n, ".system(size:) does not scale with Dynamic Type")
            if re.search(r"\.custom\([^)]*size:", line) and "relativeTo" not in line and "fixedSize" not in line:
                add("fixed-font-size", n, ".custom(_, size:) without relativeTo:")
            for m in re.finditer(r"size:\s*(\d+(?:\.\d+)?)", line):
                if "font" in line.lower() or ".system(" in line or ".custom(" in line:
                    if float(m.group(1)) < 12:
                        add("tiny-text", n, f"{m.group(1)}pt")
        else:
            if re.search(r"fontSize\s*=\s*\d+(\.\d+)?\.dp|TextStyle\([^)]*\d+\.dp", line):
                add("fixed-font-size", n, "text sized in dp does not scale")
            for m in re.finditer(r"fontSize\s*=\s*(\d+(?:\.\d+)?)\.sp", line):
                if float(m.group(1)) < 12:
                    add("tiny-text", n, f"{m.group(1)}sp")
        if re.search(r"\b(Inter|SpaceGrotesk|Space Grotesk|space_grotesk|Geist|InstrumentSerif|Instrument Serif|instrument_serif)\b", line) \
                and re.search(r"[Ff]ont|custom\(|R\.font", line):
            add("slop-font", n)

        # Strings: emoji, placeholder data, copy
        for m in STRING.finditer(line):
            s = m.group(1)
            if EMOJI.search(s):
                add("emoji", n, s[:40])
            if re.search(r"\b(Lorem|ipsum|Acme|John Doe|Jane Doe|Test User|User Name|Sample text|Item \d+|Foo|Bar Baz)\b", s):
                add("placeholder-data", n, s[:40])
            if re.search(r"(?i)unlock your|seamless|supercharge|elevate your|next-gen|world-class|game[- ]changer", s):
                add("slop-copy", n, s[:40])
        if re.search(r"(Button\(\s*\"|Text\(\s*\")(Submit|Continue|OK|Ok|Click here|Get Started|Get started)\"", line):
            add("generic-button-label", n)

        # Targets
        if not swift:
            m = re.search(r"(Checkbox|RadioButton|IconButton|Switch|clickable|toggleable|selectable)[^\n]*\.size\(\s*(\d+)\.dp", line)
            if m and int(m.group(2)) < 48:
                add("small-target", n, f"{m.group(2)}dp")
        else:
            m = re.search(r"(Button|onTapGesture|Toggle)[^\n]*\.frame\([^)]*height:\s*(\d+)", line)
            if m and int(m.group(2)) < 44:
                add("small-target", n, f"{m.group(2)}pt")

        if re.search(r"Icons\.\w+\.(Check|Done)\b|systemName:\s*\"checkmark(\.circle)?(\.fill)?\"", line):
            add("stock-check", n)

    # Multi-line constructs
    if not swift:
        for m in re.finditer(r"\b(Outlined)?TextField\(", text):
            span = call_span(text, m.start())
            if "placeholder" in span and not re.search(r"\blabel\s*=", span):
                add("placeholder-only-field", line_of(m.start()))
        for m in re.finditer(r"\bIconButton\(", text):
            span = call_span(text, m.start())
            if re.search(r"contentDescription\s*=\s*null", span):
                add("unlabelled-icon-button", line_of(m.start()))
    else:
        for m in re.finditer(r"\bTextField\(", text):
            before = "\n".join(lines[max(0, line_of(m.start()) - 3):line_of(m.start()) - 1])
            if "LabeledContent" not in text and not re.search(r"\bText\(", before):
                add("placeholder-only-field", line_of(m.start()), "the title is only a placeholder on iOS")
        for m in re.finditer(r"\bButton\s*(\(action:[^)]*\))?\s*\{", text):
            first = brace_block(text, m.end() - 1)
            if m.group(1):
                label = first  # Button(action: ...) { label }
            else:
                after = re.match(r"\s*label:\s*\{", text[first[1]:])
                if not after:
                    continue
                label = brace_block(text, first[1] + after.end() - 1)
            body = text[label[0]:label[1]]
            trailing = text[label[1]:label[1] + 200].split("\n")[:3]
            named = re.search(r"\bText\(|\bLabel\(|accessibilityLabel", body) or "accessibilityLabel" in "\n".join(trailing)
            if "Image(systemName:" in body and not named:
                add("unlabelled-icon-button", line_of(m.start()))

    radii = re.findall(r"cornerRadius[:(]\s*(\d+)|RoundedRectangle\(cornerRadius:\s*(\d+)|RoundedCornerShape\(\s*(\d+)\.dp", text)
    values = [next(v for v in g if v) for g in radii]
    if len(values) >= 3 and len(set(values)) == 1:
        add("same-radius", line_of(text.find(values[0])), f"{len(values)} shapes, all radius {values[0]}")

    if ANIMATION.search(text) and not REDUCE_MOTION.search(text):
        add("no-reduce-motion", line_of(ANIMATION.search(text).start()))  # type: ignore[union-attr]

    return found


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--allow", default="", help="comma-separated rules to skip, for deliberate style choices")
    ap.add_argument("--list-rules", action="store_true")
    args = ap.parse_args()

    if args.list_rules:
        for rule, (sev, what, fix) in RULES.items():
            print(f"{sev:4} {rule:24} {what}. Instead: {fix}.")
        return 0
    if not args.paths:
        ap.print_help()
        return 2

    allow = {a.strip() for a in args.allow.split(",") if a.strip()}
    unknown = allow - set(RULES)
    if unknown:
        print(f"unknown rule(s) in --allow: {', '.join(sorted(unknown))}; see --list-rules", file=sys.stderr)
        return 2

    files: list[Path] = []
    for p in map(Path, args.paths):
        if p.is_dir():
            files += sorted(f for f in p.rglob("*") if f.suffix in (".swift", ".kt") and "build" not in f.parts)
        elif p.suffix in (".swift", ".kt"):
            files.append(p)

    fails = warns = 0
    for f in files:
        for rule, lineno, detail in lint_file(f):
            if rule in allow:
                continue
            sev, what, fix = RULES[rule]
            fails += sev == "FAIL"
            warns += sev == "WARN"
            extra = f" ({detail})" if detail else ""
            print(f"{sev} {rule} {f}:{lineno}: {what}{extra}. Instead: {fix}.")
    print(f"{len(files)} file(s): {fails} FAIL, {warns} WARN" + (f" (allowed: {', '.join(sorted(allow))})" if allow else ""))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
