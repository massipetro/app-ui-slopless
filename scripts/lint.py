#!/usr/bin/env python3
"""Lint SwiftUI (.swift) and Compose / CMP (.kt) source for slop tells and craft defects.

  lint.py <file or folder> [...] [--platform ios|macos] [--allow rule,rule] [--a11y] [--list-rules]

Swift files are linted as macOS when --platform macos is given, or when the project (Package.swift,
.xcodeproj) or the file itself (AppKit, MenuBarExtra, NSViewRepresentable ...) says so. On macOS the
touch and Dynamic Type rules are relaxed (22 pt controls, fixed text styles) and Mac rules apply
(hover states, menu commands, window sizing, phone-sized frames). Everything else is shared.

Prints FAIL / WARN findings as file:line. Exit code 1 if any FAIL remains.
A FAIL is a tell or defect with no good default reason; a WARN needs a one-sentence
defence (e.g. hard offset shadows are the point of neo-brutalist). Use --allow for
deliberate style choices and say so in the report.

Accessibility rules carry the WCAG 2.2 criterion they are evidence against in brackets (CRITERIA
maps each rule to its criteria for scripts/acr.py); --a11y reports only those, for an accessibility
audit of an existing app. A clean a11y lint is not conformance: it can't hear VoiceOver.

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
    "missing-animate-import": ("FAIL", "transition.animateFloat/animateColor/animateDp called without importing the extension (doesn't compile)", "import androidx.compose.animation.core.animateFloat (animateDp, animateValue) or androidx.compose.animation.animateColor"),
    "wrong-import": ("FAIL", "import from a package the symbol isn't in (doesn't compile)", "rememberSaveable lives in androidx.compose.runtime.saveable"),
    "index-identity": ("WARN", "list identity from indices or offsets", "SwiftUI: ForEach over Identifiable with a stored id; Compose: items(rows, key = { it.id })"),
    "anyview": ("WARN", "AnyView erases identity and costs diffing", "@ViewBuilder, a generic, or an enum-driven switch"),
    "dispatch-delay": ("WARN", "DispatchQueue delay used to sequence UI", "withAnimation { } completion: { }, .task with Task.sleep, or a phase/keyframe animator"),
    "observableobject": ("WARN", "ObservableObject / @Published / @StateObject in new code", "@Observable model held in @State; children get let, @Bindable or @Environment"),
    "mainactor-default-arg": ("WARN", "@MainActor model created in a default argument (fails to compile)", "Pass the model from the caller, or create it in @State private var model = Model()"),
    "lazy-items-no-key": ("WARN", "lazy list items without a stable key", "items(rows, key = { it.id }, contentType = { it.kind })"),
    "nested-scroll": ("WARN", "LazyColumn inside a verticalScroll container", "One scroll container per axis: put headers in as item { }"),
    "collect-no-lifecycle": ("WARN", "flow collected with collectAsState()", "collectAsStateWithLifecycle()"),
    "text-in-remember": ("WARN", "typed text held in remember { mutableStateOf(\"\") }", "rememberTextFieldState(), or rememberSaveable for anything the user typed"),
    "caps-labels": ("WARN", "more than two uppercase labels on one screen", "Caps budget: two small uppercase labels at most; sentence case elsewhere, caps only at display size"),
    "pinned-bottom-overlap": ("WARN", "bottom bar laid over the scrolling content instead of insetting it", "SwiftUI: .safeAreaInset(edge: .bottom) on the ScrollView/List; Compose: Scaffold(bottomBar) with innerPadding in the list's contentPadding"),
    "mac-no-hover": ("WARN", "clickable custom control with no hover state (macOS)", "Add .onHover / a hovered fill; on a Mac hover is the first signifier that it is live"),
    "mac-no-commands": ("WARN", "App with no .commands { } (macOS)", "Put every action in the menu bar with a keyboard shortcut for the daily ones"),
    "mac-window-size": ("WARN", "WindowGroup without a minimum or default size (macOS)", ".frame(minWidth:minHeight:) on the root view, .defaultSize and .windowResizability(.contentMinSize)"),
    "mac-phone-frame": ("WARN", "iPhone-sized fixed frame in a Mac app", "Let the window size the layout: .frame(maxWidth:) for a reading column, adaptive grids, NavigationSplitView"),
    "mac-ios-api": ("FAIL", "iOS-only API in a macOS target (doesn't compile)", "AppKit equivalent, or guard with #if os(iOS)"),
    "mac-haptics": ("WARN", "haptic feedback on a Mac", "Trackpad haptics only for alignment/snapping; use a hover or pressed state and, rarely, a short sound"),
    "no-reduce-motion": ("WARN", "animation with no Reduce Motion / Remove animations handling", "Read accessibilityReduceMotion / animator scale and swap travel for fades"),
    "unshipped-font": ("WARN", "custom font with no font file in the project, so the system font shows in its place", "Ship the .ttf/.otf next to the code or in Fonts/ (listed in UIAppFonts / ATSApplicationFontsPath, or in res/font / composeResources/font), or use a system face"),
    # Accessibility (WCAG 2.2 AA as WCAG2ICT applies it to native apps; criterion in brackets).
    "tap-no-role": ("FAIL", "tap gesture on a plain view: VoiceOver/TalkBack get no button role, and keyboard and Switch users may not reach it [4.1.2, 2.1.1]", "SwiftUI: a Button with a custom ButtonStyle, or .accessibilityAddTraits(.isButton) on the same view; Compose: Modifier.clickable(role = Role.Button, onClickLabel = …) instead of pointerInput"),
    "clickable-no-role": ("WARN", "clickable/toggleable/selectable with no role: TalkBack says only \"double-tap to activate\" [4.1.2]", "role = Role.Button / Checkbox / Switch / RadioButton / Tab, and onClickLabel for what it does"),
    "toggle-no-state": ("WARN", "custom toggle that never tells assistive tech whether it is on [4.1.2]", "SwiftUI: .accessibilityValue(on ? \"On\" : \"Off\") or .accessibilityAddTraits(.isSelected / .isToggle); Compose: Modifier.toggleable(value, role = Role.Switch) or stateDescription"),
    "image-no-label": ("WARN", "picture or drawing with no text alternative and no decorative marking [1.1.1]", "Label what it shows (.accessibilityLabel / contentDescription / semantics { contentDescription }), or mark it decorative (Image(decorative:), .accessibilityHidden(true))"),
    "a11y-hidden-control": ("FAIL", "interactive control hidden from assistive tech [4.1.2]", "Hide only decoration; a control hidden from VoiceOver/TalkBack is unusable for their users"),
    "label-in-name": ("WARN", "accessible name doesn't contain the visible label, so Voice Control / Voice Access can't call it by what it shows [2.5.3]", "Start the accessibilityLabel / contentDescription with the visible words"),
    "colour-only-state": ("WARN", "a state shown only by a change of colour [1.4.1]", "Pair the colour with a shape, icon, weight or text that changes too (and an accessibilityValue / stateDescription)"),
    "fixed-text-frame": ("WARN", "text inside a fixed-height frame: it clips or truncates at the largest text sizes [1.4.4, 1.4.10]", "minHeight / heightIn(min =), @ScaledMetric, or let the row grow; switch HStack→VStack at accessibility sizes"),
    "dynamic-type-capped": ("WARN", "text scaling capped below the accessibility sizes [1.4.4]", "Let text reach the AX sizes / fontScale 2.0; cap only a display number that already fills its region, and say so"),
    "gesture-no-alternative": ("WARN", "drag, swipe, pinch or rotate gesture with no accessibility action [2.5.1, 2.5.7]", "Add .accessibilityAction(named:) / .accessibilityAdjustableAction (Compose: customActions or a progressBarRangeInfo + setProgress) and a visible single-tap control"),
    "overlay-not-modal": ("WARN", "custom overlay (scrim + panel) that leaves the content behind it reachable to VoiceOver/TalkBack and the keyboard [2.4.3]", "Use .sheet / .alert / Dialog / ModalBottomSheet, or add .accessibilityAddTraits(.isModal) (Compose: hide the content behind with clearAndSetSemantics or use Dialog/Popup)"),
    "heading-missing": ("WARN", "titled sections with no heading marked, so screen-reader users can't jump between them [1.3.1, 2.4.6]", "SwiftUI: .accessibilityAddTraits(.isHeader); Compose: Modifier.semantics { heading() }"),
    "no-reduce-transparency": ("WARN", "translucent material with no Reduce Transparency fallback [508 503.2, EN 301 549 11.7]", "@Environment(\\.accessibilityReduceTransparency): swap the material for an opaque surface token"),
}

# Which WCAG 2.2 criteria each rule is evidence against (scripts/acr.py reads this).
CRITERIA = {
    "unlabelled-icon-button": ["1.1.1", "4.1.2"], "placeholder-only-field": ["3.3.2", "1.3.1"], "small-target": ["2.5.8"],
    "fixed-font-size": ["1.4.4"], "no-reduce-motion": ["2.2.2"], "pinned-bottom-overlap": ["2.4.11"],
    "tap-no-role": ["4.1.2", "2.1.1"], "clickable-no-role": ["4.1.2"], "toggle-no-state": ["4.1.2"],
    "image-no-label": ["1.1.1"], "a11y-hidden-control": ["4.1.2"], "label-in-name": ["2.5.3"],
    "colour-only-state": ["1.4.1"], "fixed-text-frame": ["1.4.4", "1.4.10"], "dynamic-type-capped": ["1.4.4"],
    "gesture-no-alternative": ["2.5.1", "2.5.7"], "overlay-not-modal": ["2.4.3"], "heading-missing": ["1.3.1", "2.4.6"],
    "no-reduce-transparency": ["503.2"],
}

HEX_KT = re.compile(r"Color\(\s*0x([0-9A-Fa-f]{8}|[0-9A-Fa-f]{6})\s*\)")
HEX_STR = re.compile(r"\"#?([0-9A-Fa-f]{6})\"")
RGB_SWIFT = re.compile(r"Color\(\s*(?:\.sRGB,\s*)?red:\s*([\d.]+)\s*,\s*green:\s*([\d.]+)\s*,\s*blue:\s*([\d.]+)")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF☀-➿⭐⭕]")
STRING = re.compile(r"\"((?:[^\"\\\n]|\\.)*)\"")
TOKEN_FILE = re.compile(r"(Theme|Token|Palette|Colou?rs?|Brand|DesignSystem|Style)", re.I)
TOKEN_DECL = re.compile(r"(object|enum|struct|extension)\s+\w*(Tokens?|Palette|Colou?rs?|Theme)\b|extension\s+Color\b|ColorScheme\(|lightColorScheme|darkColorScheme")
ANIMATION = re.compile(r"withAnimation|\.animation\(|animate\w*AsState|spring\(|rememberInfiniteTransition|AnimatedVisibility|AnimatedContent|\.transition\(|phaseAnimator|keyframeAnimator|updateTransition")
FONT_FILES = (".ttf", ".otf", ".ttc")
# Faces that ship with iOS and macOS, so naming them needs no font file.
SYSTEM_FACES = ("sfpro", "sfcompact", "sfmono", "newyork", "applesystemuifont", "helvetica", "avenir", "georgia", "courier",
                "menlo", "timesnewroman", "palatino", "futura", "gillsans", "americantypewriter", "didot", "baskerville",
                "hoefler", "optima", "rockwell", "chalkboard", "markerfelt", "noteworthy", "copperplate", "arial", "verdana",
                "trebuchet", "charter", "iowan", "seravek", "kohinoor", "damascus", "snellroundhand", "zapfino", "papyrus",
                "bodoni", "superclarendon", "monaco", "andalemono", "sanfrancisco", "geneva", "lucidagrande",
                "pingfang", "hiragino", "applesdgothic", "applecoloremoji", "symbol", "skia", "silom")
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


OPEN, CLOSE = "({[", ")}]"


def match_back(text: str, j: int) -> int:
    """Index of the opener that matches the closer at text[j]."""
    depth = 0
    for k in range(j, -1, -1):
        if text[k] in CLOSE:
            depth += 1
        elif text[k] in OPEN:
            depth -= 1
            if depth == 0:
                return k
    return 0


def match_fwd(text: str, i: int) -> int:
    """Index just past the closer that matches the opener at text[i]."""
    depth = 0
    for k in range(i, len(text)):
        if text[k] in OPEN:
            depth += 1
        elif text[k] in CLOSE:
            depth -= 1
            if depth == 0:
                return k + 1
    return len(text)


def swift_chain(text: str, at: int) -> tuple[int, int]:
    """(start, end) of the SwiftUI expression whose modifier chain includes the `.modifier` at `at`:
    back to the head view (`HStack { … }`, `Image("x")`), forward over every `.modifier(…) { … }`."""
    start = at
    p = at if text[at:at + 1] == "." else -1
    while p >= 0:  # backward from a `.link`: [groups] identifier, and on while a '.' precedes it
        j = p - 1
        while j >= 0 and text[j].isspace():
            j -= 1
        while j >= 0 and text[j] in CLOSE:  # the previous link's ( ) and { } groups
            j = match_back(text, j) - 1
            while j >= 0 and text[j] in " \t":
                j -= 1
        k = j
        while k >= 0 and (text[k].isalnum() or text[k] == "_"):
            k -= 1
        start = k + 1
        if k == j:  # no identifier: a closure or a leading-dot expression
            break
        while k >= 0 and text[k].isspace():
            k -= 1
        p = k if k >= 0 and text[k] == "." else -1
    m = re.match(r"\.?[\w]+", text[at:])
    k = at + (m.end() if m else 0)
    while True:  # forward: groups after this link (and labelled trailing closures), then more `.links`
        while True:
            g = re.match(r"[ \t]*([({])", text[k:]) or re.match(r"\s*[a-z]\w*:\s*(\{)", text[k:])
            if not g:
                break
            k = match_fwd(text, k + g.start(1))
        nxt = re.match(r"\s*\.[A-Za-z_]\w*", text[k:])
        if not nxt:
            break
        k += nxt.end()
    return start, k


def kotlin_call(text: str, at: int) -> tuple[str, int, int]:
    """(name, start, end) of the innermost call whose argument list contains `at`, with its trailing lambda."""
    depth = 0
    for k in range(at - 1, -1, -1):
        c = text[k]
        if c in CLOSE:
            depth += 1
        elif c in OPEN:
            if depth:
                depth -= 1
                continue
            m = re.search(r"([A-Za-z_]\w*)\s*$", text[:k]) if c == "(" else None
            if not m:
                return "", 0, 0
            end = match_fwd(text, k)
            lam = re.match(r"\s*\{", text[end:])
            if lam:
                end = match_fwd(text, end + lam.end() - 1)
            return m.group(1), m.start(1), end
    return "", 0, 0


SWIFT_A11Y_ROLE = re.compile(r"accessibilityAddTraits\([^)]*\.is(Button|Link|Toggle|Selected|Tab)|accessibilityAction\b|accessibilityRepresentation|accessibilityAdjustableAction|accessibilityHidden\(\s*true")
SWIFT_COLOUR_CALL = re.compile(r"\.(foregroundStyle|foregroundColor|fill|background|tint|stroke|strokeBorder|border|shadow)\(\s*!?\(?\s*([A-Za-z_][\w.]*)\s*\)?\s*\?(?!\?)")
KT_COLOUR_CALL = re.compile(r"\b(color|containerColor|contentColor|tint|background|borderColor|backgroundColor|targetValue)\s*=\s*if\s*\(\s*!?\s*([A-Za-z_][\w.]*)\s*\)|\.background\(\s*(?:color\s*=\s*)?if\s*\(\s*!?\s*([A-Za-z_][\w.]*)\s*\)|animateColorAsState\(\s*(?:targetValue\s*=\s*)?if\s*\(\s*!?\s*([A-Za-z_][\w.]*)\s*\)")
NOT_AX = ("xSmall", "small", "medium", "large", "xLarge", "xxLarge", "xxxLarge")


def labelled_around(text: str, at: int, swift: bool) -> bool:
    """True when the view or composable that contains `at` sets an accessible name or hides itself,
    or every call site of it does (a drawing inside `fun Gauge(modifier)` is labelled where it's used)."""
    decl = r"\bstruct\s+(\w+)\s*(?::[^{]*)?\{" if swift else r"\bfun\s+(\w+)\s*\("
    marks = r"accessibility(Label|Value|Hidden|Element|Representation)" if swift else r"semantics|contentDescription"
    owner = None
    for m in re.finditer(decl, text[:at]):
        s, e = brace_block(text, m.end() - 1)
        if s <= at < e:
            owner = (m.group(1), s, e)
    if not owner:
        return False
    name, s, e = owner
    if re.search(marks, text[s:e]):
        return True
    sites = [c.start() for c in re.finditer(r"(?<![\w.])" + name + r"\s*\(", text) if not (s - 200 < c.start() < e)]
    for c in sites:
        span = text[swift_chain(text, c)[0]:swift_chain(text, c)[1]] if swift else text[c:c + len(call_span(text, c))]
        if not re.search(marks, span):
            return False
    return bool(sites)


def norm_words(s: str) -> str:
    return " ".join(re.sub(r"[^\w\s]", " ", s.lower()).split())


def a11y_findings(text: str, swift: bool, mac: bool, add, line_of) -> None:
    """Accessibility rules (WCAG 2.2 AA as WCAG2ICT applies it to native apps). Heuristic, like the rest."""
    if swift:
        # Tap gestures on plain views. A Button keeps its role, focus and keyboard activation; a gesture doesn't.
        for m in re.finditer(r"\.onTapGesture\b|\.(simultaneous|highPriority)?[gG]esture\(\s*TapGesture", text):
            s, e = swift_chain(text, m.start())
            chain = text[s:e]
            body = text[m.start():e]
            if re.match(r"\s*(Button|Toggle|Link|NavigationLink|Menu)\b", chain) or SWIFT_A11Y_ROLE.search(chain):
                continue
            body = body[:match_fwd(body, body.find("{"))] if "{" in body else body
            if re.search(r"(?i)focus|keyboard|endEditing|resignFirstResponder", body):  # tap-outside to dismiss the keyboard
                continue
            if re.match(r"\s*Image\(\s*systemName:", chain) and "accessibilityLabel" not in chain:
                add("unlabelled-icon-button", line_of(m.start()), "Image(systemName:) with a tap gesture")
            add("tap-no-role", line_of(m.start()))
        # Custom toggles: a Button that flips a Bool must say which way it is.
        for m in re.finditer(r"\bButton\s*(\(action:|\{)", text):
            s, e = swift_chain(text, m.start())
            chain = text[s:e]
            action = text[m.start():match_fwd(text, m.end() - 1)] if m.group(1) == "{" else call_span(text, m.start())
            flip = re.search(r"([\w.]+)\.toggle\(\)|(\b[\w.]+)\s*=\s*!\s*\2\b", action)
            if not flip:
                continue
            var = (flip.group(1) or flip.group(2)).split(".")[-1]
            label = chain[len(action):] if chain.startswith(action) else chain
            # Showing a panel is a plain button (the panel is the state); a label that changes with it (Play/Pause) says it.
            if re.match(r"(?i)(show|isShowing|is\w*Presented|present|expand|isExpanded)", var) and "expand" not in var.lower() \
                    or re.search(r"(Text\(|Label\(|systemName:|systemImage:)[^\n]*\b" + re.escape(var) + r"\b", label):
                continue
            if not re.search(r"accessibilityValue|\.is(Selected|Toggle)\b|accessibilityRepresentation|\bToggle\(", chain):
                add("toggle-no-state", line_of(m.start()), var)
        # Label in name: the accessible name must contain the words the button shows.
        for m in re.finditer(r"\bButton\b", text):
            s, e = swift_chain(text, m.start())
            chain = text[s:e]
            shown = re.match(r"\s*Button\(\s*\"([^\"\\]{3,60})\"", chain) or re.search(r"\bText\(\s*\"([^\"\\]{3,60})\"", chain)
            named = re.search(r"\.accessibilityLabel\(\s*(?:Text\()?\s*\"([^\"\\]+)\"", chain)
            if shown and named and norm_words(shown.group(1)) not in norm_words(named.group(1)):
                add("label-in-name", line_of(named.start()), f"shows '{shown.group(1)}', named '{named.group(1)}'")
        # Pictures and drawings: a text alternative, or marked decorative.
        for m in re.finditer(r"\bImage\(\s*\"|\bImage\(\s*(uiImage|nsImage):|\bAsyncImage\(|\bCanvas\s*[({]", text):
            s, e = swift_chain(text, m.start())
            chain = text[s:e]
            if not re.search(r"accessibilityLabel|accessibilityHidden|accessibilityValue|accessibilityRepresentation|accessibilityElement|\bLabel\(", chain) \
                    and not labelled_around(text, m.start(), True):
                add("image-no-label", line_of(m.start()), m.group(0).strip("({ \""))
        # Controls hidden from assistive tech.
        for m in re.finditer(r"\.accessibilityHidden\(\s*true\s*\)", text):
            s, e = swift_chain(text, m.start())
            chain = text[s:m.start()]
            if re.search(r"\bButton\b|\bToggle\(|\bLink\(|NavigationLink|\bTextField\(|\.onTapGesture", chain) and \
                    not re.match(r"\s*(Color|Rectangle|Circle)\b", chain):
                add("a11y-hidden-control", line_of(m.start()))
        if not mac:
            # Fixed-height frames around text clip at the accessibility sizes (AX5 body is about 3x the default).
            scaled = set(re.findall(r"@ScaledMetric[^\n]*?var\s+(\w+)", text))
            for m in re.finditer(r"\.frame\(([^()]*)\)", text):
                h = re.search(r"(?<![A-Za-z])height:\s*([A-Za-z_][\w.]*|\d+(?:\.\d+)?)", m.group(1))
                if not h or h.group(1).split(".")[-1] in scaled:
                    continue
                s, _ = swift_chain(text, m.start())
                head = text[s:m.start()]
                if re.match(r"\s*(ScrollView|List|Map|Chart|Canvas|Image|Color|Rectangle|Circle|Spacer|Divider|GeometryReader|TabView|VideoPlayer)\b", head):
                    continue
                if re.search(r"\b(Text|Label|TextField)\(", head):
                    add("fixed-text-frame", line_of(m.start()), f"height: {h.group(1)}")
            for m in re.finditer(r"\.dynamicTypeSize\(([^)]*)\)", text):
                arg = m.group(1)
                cap = re.search(r"(?:\.\.\.|\.\.<)\s*(?:DynamicTypeSize)?\.(\w+)", arg) or re.fullmatch(r"\s*(?:DynamicTypeSize)?\.(\w+)\s*", arg)
                if cap and cap.group(1) in NOT_AX:
                    add("dynamic-type-capped", line_of(m.start()), f"capped at .{cap.group(1)}")
        # Path, drag and multi-touch gestures need an accessible and a single-tap alternative.
        g = re.search(r"\bDragGesture\((?!\s*minimumDistance:\s*0\b)|\bMagnif(y|ication)Gesture\b|\bRotat(e|ion)Gesture\b", text)
        if g and not re.search(r"accessibilityAction|accessibilityAdjustableAction|accessibilityScrollAction|accessibilityZoomAction|accessibilityRepresentation", text):
            add("gesture-no-alternative", line_of(g.start()), g.group(0).rstrip("("))
        # A home-made modal: a full-screen scrim with no .isModal leaves the content behind it reachable.
        for m in re.finditer(r"(Color\.black|\.black|Color\(\s*\.black\s*\))\s*\.opacity\(\s*0?\.[1-9]|\b\w*[Ss]crim\b(?!\w*\()", text):
            s, e = swift_chain(text, m.start())
            if re.search(r"ignoresSafeArea|onTapGesture", text[s:e]) and ".isModal" not in text:
                add("overlay-not-modal", line_of(m.start()))
                break
        # Section titles with no heading trait.
        titles = re.findall(r"\bText\([^\n]*\)\s*\n?\s*\.font\(\s*(?:\.(?:largeTitle|title|title2|title3|headline)\b|[\w.]*(?i:title|heading|section)\w*)", text)
        if len(titles) >= 2 and ".isHeader" not in text:
            add("heading-missing", line_of(text.find(titles[1])), f"{len(titles)} titles")
        b = re.search(r"\.blur\(\s*radius:\s*[1-9]", text)
        if b and "accessibilityReduceTransparency" not in text:
            add("no-reduce-transparency", line_of(b.start()))
        colour_calls = [(m.start(), m.start() + len(call_span(text, m.start()) or m.group(0)), m.group(2)) for m in SWIFT_COLOUR_CALL.finditer(text)]
        colour_calls += [(m.start(), m.end(), m.group(1)) for m in re.finditer(r":\s*Color\s*=\s*!?([A-Za-z_][\w.]*)\s*\?", text)]
    else:
        # Taps detected by hand are invisible to TalkBack and unreachable by Switch Access and the keyboard.
        for m in re.finditer(r"\bpointerInput\(", text):
            block = text[m.start():match_fwd(text, text.find("{", m.start()))] if "{" in text[m.start():m.start() + 120] else ""
            if "detectTapGestures" not in block or re.search(r"\bonPress\b", block) and "onTap" not in block:
                continue
            name, s, e = kotlin_call(text, m.start())
            span = text[s:e] if name else text[max(0, m.start() - 300):m.start() + 300]
            if not re.search(r"\bsemantics\b|\bclickable\b|\btoggleable\b|\bselectable\b|onClick\s*=", span):
                add("tap-no-role", line_of(m.start()), "pointerInput { detectTapGestures }")
        for m in re.finditer(r"\.(clickable|combinedClickable|toggleable|selectable|triStateToggleable)\b\s*(\(|\{)", text):
            span = call_span(text, m.start()) if m.group(2) == "(" else ""
            args = span[:span.find("{")] if "{" in span else span
            if "role" not in args:
                add("clickable-no-role", line_of(m.start()), m.group(1))
            if m.group(1) in ("clickable", "combinedClickable"):
                lam = text[m.start():match_fwd(text, text.find("{", m.start()))] if "{" in text[m.start():m.start() + 200] else ""
                if re.search(r"(\b[\w.]+)\s*=\s*!\s*\1\b|\.toggle\(\)", lam):
                    name, s, e = kotlin_call(text, m.start())
                    if not re.search(r"stateDescription|toggleable|\bselected\s*=|Role\.(Switch|Checkbox)", text[s:e] if name else lam):
                        add("toggle-no-state", line_of(m.start()))
        for m in re.finditer(r"\bclearAndSetSemantics\s*\{\s*\}|\binvisibleToUser\(\)|\bhideFromAccessibility\(\)", text):
            name, s, e = kotlin_call(text, m.start())
            if name and re.search(r"\bclickable\b|\bonClick\s*=|\btoggleable\b|\bButton\(|IconButton\(", text[s:e]):
                add("a11y-hidden-control", line_of(m.start()))
        for m in re.finditer(r"clearAndSetSemantics\s*\{[^}]*contentDescription\s*=\s*\"([^\"\\]+)\"", text):
            name, s, e = kotlin_call(text, m.start())
            shown = re.search(r"\bText\(\s*(?:text\s*=\s*)?\"([^\"\\]{3,60})\"", text[s:e]) if name else None
            if shown and norm_words(shown.group(1)) not in norm_words(m.group(1)):
                add("label-in-name", line_of(m.start()), f"shows '{shown.group(1)}', named '{m.group(1)}'")
        for m in re.finditer(r"\bCanvas\(", text):
            args = call_span(text, m.start())
            args = args[:args.find("{")] if "{" in args else args
            if not re.search(r"semantics|contentDescription", args) and not labelled_around(text, m.start(), False):
                add("image-no-label", line_of(m.start()), "Canvas")
        for m in re.finditer(r"\.(height|size|requiredHeight|requiredSize)\(\s*\d+(\.\d+)?\.dp\s*\)", text):
            name, s, e = kotlin_call(text, m.start())
            if name in ("Text", "Row", "Box", "Column", "Surface", "Card", "Button", "OutlinedButton", "TextButton", "FilledTonalButton", "ElevatedButton", "LazyRow", "FlowRow") \
                    and re.search(r"\bText\(", text[s:e]):
                add("fixed-text-frame", line_of(m.start()), f"{name} with a fixed {m.group(1)}")
        for m in re.finditer(r"fontScale\s*=\s*1(\.0)?f\b|fontScale\.coerceAtMost\(|fontScale\s*=\s*min\(|/\s*(LocalDensity\.current\.)?fontScale\b", text):
            add("dynamic-type-capped", line_of(m.start()), m.group(0)[:30])
        g = re.search(r"\bdetect(Horizontal|Vertical)?DragGestures(AfterLongPress)?\b|\bdetectTransformGestures\b|\.(draggable|anchoredDraggable|swipeable|transformable)\(|\bSwipeToDismissBox\(", text)
        if g and not re.search(r"customActions|CustomAccessibilityAction|setProgress|progressBarRangeInfo", text):
            add("gesture-no-alternative", line_of(g.start()), g.group(0).strip(".("))
        for m in re.finditer(r"Color\.Black\.copy\(\s*alpha\s*=\s*0?\.[1-9]|\b\w*[Ss]crim\w*\b", text):
            name, s, e = kotlin_call(text, m.start())
            span = text[s:e] if name else ""
            if "fillMaxSize" in span and re.search(r"clickable|pointerInput", span) and \
                    not re.search(r"clearAndSetSemantics|isTraversalGroup|traversalIndex|paneTitle|hideFromAccessibility|invisibleToUser", text):
                add("overlay-not-modal", line_of(m.start()))
                break
        titles = re.findall(r"style\s*=\s*(?:MaterialTheme\.typography\.(?:title|headline|display)\w*|[\w.]*(?i:title|heading|section)\w*)", text)
        if len(titles) >= 2 and "heading()" not in text:
            add("heading-missing", line_of(text.find(titles[1])), f"{len(titles)} titles")
        colour_calls = []
        for m in KT_COLOUR_CALL.finditer(text):
            var = next(v for v in m.groups()[1:] if v)
            colour_calls.append((m.start(), text.find(")", m.end() - 1) + 1 if m.group(0).endswith(")") else m.end(), var))
            # an `if (x) A else B` colour expression runs to the end of its line
            colour_calls[-1] = (m.start(), text.find("\n", m.start()) if text.find("\n", m.start()) > 0 else len(text), var)

    # Colour as the only signal: the Bool that picks a colour changes nothing else people can see.
    # Only status hues count (green for on time, red for late): a zebra band or an inverted selected fill
    # changes lightness too, so it isn't the colour-alone case WCAG 1.4.1 is about.
    status = re.compile(r"(?i)\b(red|green|orange|yellow|amber)\b|success|error|danger|warn|alert|positive|negative|late|overdue|delay|ontime|onTime|good|bad|ok\b|critical|urgent|status")
    reported = set()
    for start, end, var in colour_calls:
        name = var.split(".")[-1]
        if not status.search(text[start:end].replace(var, "", 1)):
            continue
        if name in reported or name in ("isEnabled", "enabled", "colorScheme", "isDark", "dark", "darkTheme", "isPressed", "pressed", "isHovered", "hovering", "configuration"):
            continue
        visible = False
        for u in re.finditer(r"(?<![\w.])(?:[\w]+\.)*" + re.escape(name) + r"\b", text):
            if any(s <= u.start() < e for s, e, _ in colour_calls):
                continue
            ln = text[text.rfind("\n", 0, u.start()) + 1:text.find("\n", u.start()) if text.find("\n", u.start()) > 0 else len(text)]
            if re.search(r"\b(var|let|val)\s+" + re.escape(name) + r"\b|" + re.escape(name) + r"\s*:\s*\w|" + re.escape(name) + r"\s*=[^=]|" + re.escape(name) + r"\.toggle\(\)", ln):
                continue
            if re.search(r"accessibility|semantics|stateDescription|contentDescription|Description\s*=", ln):
                continue
            visible = True
            break
        if not visible:
            reported.add(name)
            add("colour-only-state", line_of(start), f"'{var}' changes only a colour")


MAC_FILE = re.compile(r"^\s*import\s+AppKit\b|\bNSViewRepresentable\b|\bNSWindow\b|\bNSApp\b|\bNSColor\b|\bNSImage\b|\bMenuBarExtra\b|\.windowStyle\(|\.inspector\(isPresented", re.M)
IOS_FILE = re.compile(r"^\s*import\s+UIKit\b|\bUIViewRepresentable\b|\bUIColor\b|\bUIImage\b|\bUIApplication\b|\.navigationBarTitleDisplayMode\b", re.M)


def project_is_mac(path: Path) -> bool | None:
    """True/False when the enclosing project declares only macOS / only iOS; None when it says nothing."""
    for d in [path.resolve().parent, *path.resolve().parents]:
        pkg = d / "Package.swift"
        if pkg.exists():
            t = pkg.read_text(errors="ignore")
            if (".macOS(" in t) != (".iOS(" in t):
                return ".macOS(" in t
        for proj in d.glob("*.xcodeproj/project.pbxproj"):
            t = proj.read_text(errors="ignore")
            mac, ios = "MACOSX_DEPLOYMENT_TARGET" in t, "IPHONEOS_DEPLOYMENT_TARGET" in t
            if mac != ios:
                return mac
        if (d / ".git").exists():
            break
    return None


def is_mac(path: Path, text: str, forced: str | None) -> bool:
    if path.suffix != ".swift":
        return False
    if forced:
        return forced == "macos"
    if MAC_FILE.search(text) and not IOS_FILE.search(text):
        return True
    if IOS_FILE.search(text):
        return False
    return bool(project_is_mac(path))


def project_fonts(path: Path) -> list[str]:
    """Normalised names of the font files the project ships: from the project root (Package.swift, an
    .xcodeproj or Gradle settings, walking up) or, with no project, the file's own folder."""
    root = path.parent
    for d in [path.parent, *path.parent.parents][:6]:
        if any((d / m).exists() for m in ("Package.swift", "settings.gradle", "settings.gradle.kts")) or any(d.glob("*.xcodeproj")):
            root = d
            break
    skip = {"build", ".build", "DerivedData", "node_modules", ".git", "Pods", ".gradle"}
    names = []
    for f in root.rglob("*"):
        if f.suffix.lower() in FONT_FILES and not skip & set(f.parts):
            names.append(re.sub(r"[^a-z0-9]", "", f.stem.lower()))
            if len(names) > 400:
                break
    return names


def lint_file(path: Path, platform: str | None = None) -> list[tuple[str, int, str]]:
    raw = path.read_text(errors="ignore")
    lines = [strip_comment(l) for l in raw.splitlines()]
    text = "\n".join(lines)
    swift = path.suffix == ".swift"
    mac = is_mac(path, raw, platform)
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
                and re.search(r"Material|blur|containerColor|background", line) \
                and not (mac and re.search(r"(?i)sidebar|inspector|toolbar|titlebar|for:\s*\.window|containerBackground|menu", line)):
            add("glass", n)

        # Type
        if swift:
            if not mac:  # macOS has no Dynamic Type; fixed sizes are how its text styles work
                if re.search(r"\.system\(size:", line) and "relativeTo" not in line:
                    add("fixed-font-size", n, ".system(size:) does not scale with Dynamic Type")
                if re.search(r"\.custom\([^)]*size:", line) and "relativeTo" not in line and "fixedSize" not in line:
                    add("fixed-font-size", n, ".custom(_, size:) without relativeTo:")
            for m in re.finditer(r"size:\s*(\d+(?:\.\d+)?)", line):
                if "font" in line.lower() or ".system(" in line or ".custom(" in line:
                    if float(m.group(1)) < (10 if mac else 12):
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
            if m and int(m.group(2)) < (20 if mac else 44):
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
            if "LabeledContent" not in text and not (mac and re.search(r"\bForm\b", text)) and not re.search(r"\bText\(", before):
                add("placeholder-only-field", line_of(m.start()), "the title is only a placeholder" + ("" if mac else " on iOS"))
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

    # Code baseline (platform files, section 8b): patterns that hurt what users feel, or don't compile.
    if swift:
        for m in re.finditer(r"ForEach\([^\n]*?(\.indices\b|id:\s*\\\.offset|\.enumerated\(\)[^\n]*id:\s*\\\.offset)", text):
            add("index-identity", line_of(m.start()))
        for m in re.finditer(r"\bAnyView\(", text):
            add("anyview", line_of(m.start()))
        for m in re.finditer(r"DispatchQueue\.main\.asyncAfter", text):
            add("dispatch-delay", line_of(m.start()))
        for m in re.finditer(r":\s*ObservableObject\b|@Published\b|@StateObject\b|@ObservedObject\b", text):
            add("observableobject", line_of(m.start()))
        # Classes isolated to the main actor (@Observable alone is not).
        actor_types = set(re.findall(r"@MainActor\b(?:\s*@\w+(?:\([^)]*\))?)*\s*(?:(?:final|public|private|fileprivate|internal)\s+)*class\s+(\w+)", text))
        for m in re.finditer(r"\binit\(([^)]*)\)", text):
            for t in re.findall(r":\s*(\w+)\??\s*=\s*(\w+)\(", m.group(1)):
                if t[1] in actor_types:
                    add("mainactor-default-arg", line_of(m.start()), t[1])
    else:
        # Transition extensions need their own import; animateFloatAsState doesn't bring them in.
        ext_pkg = {"animateFloat": "androidx.compose.animation.core", "animateDp": "androidx.compose.animation.core",
                   "animateValue": "androidx.compose.animation.core", "animateOffset": "androidx.compose.animation.core",
                   "animateColor": "androidx.compose.animation"}
        for fn, pkg in ext_pkg.items():
            call = re.search(r"\.\s*" + fn + r"\s*\(", text)
            if call and not re.search(r"^\s*import\s+" + re.escape(pkg) + r"\.(" + fn + r"\b|\*)", raw, re.M):
                add("missing-animate-import", line_of(call.start()), fn)
        for m in re.finditer(r"^\s*import\s+androidx\.compose\.runtime\.rememberSaveable\b", raw, re.M):
            add("wrong-import", raw.count("\n", 0, m.start()) + 1, "androidx.compose.runtime.rememberSaveable")
        for m in re.finditer(r"(?<![\w.])(items|itemsIndexed)\(", text):
            span = call_span(text, m.start())
            args = span[:span.find(")") + 1] if ")" in span else span
            depth, end = 0, len(span)
            for k, ch in enumerate(span):
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if depth == 0:
                        end = k
                        break
            args = span[:end]
            if re.search(r"\bLazy(Column|Row|VerticalGrid|HorizontalGrid|VerticalStaggeredGrid)\b", text) and "key" not in args:
                add("lazy-items-no-key", line_of(m.start()))
        for m in re.finditer(r"verticalScroll\(", text):
            block = brace_block(text, m.end())
            inner = text[block[0]:block[1]]
            if re.search(r"\bLazyColumn\b", inner):
                add("nested-scroll", line_of(m.start()))
        for m in re.finditer(r"\.collectAsState\(", text):
            add("collect-no-lifecycle", line_of(m.start()))
        for m in re.finditer(r"(?<!Saveable)\bremember\s*\{\s*mutableStateOf\(\s*\"\"\s*\)", text):
            add("text-in-remember", line_of(m.start()))

    # macOS: pointer, keyboard and window rules.
    if mac:
        for m in re.finditer(r"UIKit|\bUI(Color|Image|Screen|Application|Device|ImpactFeedbackGenerator|NotificationFeedbackGenerator)\b|\.navigationBarTitleDisplayMode|\.fullScreenCover\(|\.navigationViewStyle\(\s*\.stack|\.tabViewStyle\(\s*\.page|\.statusBar", text):
            add("mac-ios-api", line_of(m.start()), m.group(0)[:30])
        for m in re.finditer(r"UIScreen|\.frame\([^)]*width:\s*(320|360|375|390|393|402|412|414|428|430|440)\b", text):
            add("mac-phone-frame", line_of(m.start()), m.group(0)[:40])
        for m in re.finditer(r"\.sensoryFeedback\(|UIImpactFeedbackGenerator|NSHapticFeedbackManager", text):
            add("mac-haptics", line_of(m.start()))
        custom = re.search(r"\bButtonStyle\b|\.onTapGesture\b", text)
        if custom and not re.search(r"\.onHover\b|\.hoverEffect\b|isHovered|isHovering|\bhovering\b", text):
            add("mac-no-hover", line_of(custom.start()))
        if re.search(r"@main\b", text) and re.search(r"\bWindowGroup\b|\bwindow\b", text) and not re.search(r"\.commands\s*\{", text):
            add("mac-no-commands", line_of(re.search(r"@main\b", text).start()))  # type: ignore[union-attr]
        wg = re.search(r"\bWindowGroup\b", text)
        if wg and not re.search(r"minWidth:|\.defaultSize\(|\.windowResizability\(|\.windowMinSize|\.defaultWindowPlacement", text):
            add("mac-window-size", line_of(wg.start()))

    a11y_findings(text, swift, mac, add, line_of)

    # Caps budget: uppercase transforms plus ALL-CAPS text literals (2+ words or 4+ letters).
    caps_sites = []
    for m in re.finditer(r"\.textCase\(\s*\.uppercase\s*\)|\.uppercased\(\)|\.uppercase\(\)|textTransform\s*=", text):
        # Inside a helper (func / fun), count the helper's call sites instead of the one transform.
        helper = re.findall(r"\b(?:func|fun)\s+(\w+)", text[max(0, m.start() - 600):m.start()])
        calls = [c.start() for c in re.finditer(r"(?<!\w)" + re.escape(helper[-1]) + r"\s*\(", text)
                 if not re.search(r"\b(?:func|fun)\s+$", text[max(0, c.start() - 12):c.start()])] if helper else []
        caps_sites += calls if calls else [m.start()]
    for m in re.finditer(r"\bText\(\s*\"([^\"\n]{2,40})\"", text):
        lit = m.group(1)
        letters = re.sub(r"[^A-Za-z]", "", lit)
        if letters and letters.isupper() and (len(letters) >= 4 or " " in lit.strip()):
            caps_sites.append(m.start())
    if len(caps_sites) > 2:
        add("caps-labels", line_of(sorted(caps_sites)[2]), f"{len(caps_sites)} uppercase labels")

    # A bar pinned over a scroll view (ZStack/overlay/Box-align) hides the last rows unless padded by hand.
    if swift:
        scrolls = re.search(r"\bScrollView\b|\bList\s*[({]", text)
        pinned = re.search(r"ZStack\(alignment:\s*\.bottom\w*\)|\.overlay\(alignment:\s*\.bottom\)\s*\{[^}]{0,400}?Button", text)
        if scrolls and pinned and "safeAreaInset(edge: .bottom" not in text:
            add("pinned-bottom-overlap", line_of(pinned.start()))
    else:
        scrolls = re.search(r"\bLazy(Column|VerticalGrid)\b|verticalScroll\(", text)
        pinned = re.search(r"Alignment\.BottomCenter", text)
        uses_inset = re.search(r"bottomBar\s*=", text) and re.search(r"calculateBottomPadding|innerPadding|paddingValues|contentPadding\s*=\s*\w*[Pp]adding\b", text)
        if scrolls and pinned and not uses_inset:
            add("pinned-bottom-overlap", line_of(pinned.start()))

    radii = re.findall(r"cornerRadius[:(]\s*(\d+)|RoundedRectangle\(cornerRadius:\s*(\d+)|RoundedCornerShape\(\s*(\d+)\.dp", text)
    values = [next(v for v in g if v) for g in radii]
    if len(values) >= 3 and len(set(values)) == 1:
        add("same-radius", line_of(text.find(values[0])), f"{len(values)} shapes, all radius {values[0]}")

    # Custom fonts the project never ships: in a real build they quietly fall back to the system font
    # (round 21: four of six Mac builds designed with faces they didn't include).
    shipped = None
    if swift:
        uses = [(m.group(1), m.start()) for m in re.finditer(r'(?:\.custom|NSFont|UIFont)\(\s*(?:name:\s*)?"([^"]+)"', text)]
        for m in re.finditer(r'(?:\.custom|NSFont|UIFont)\(\s*(?:name:\s*)?([A-Za-z_][\w.]*)\s*[,)]', text):
            decl = re.search(rf'\b(?:let|var)\s+{re.escape(m.group(1).split(".")[-1])}\s*(?::\s*String)?\s*=\s*"([^"]+)"', text)
            if decl:
                uses.append((decl.group(1), m.start()))
    else:
        uses = [(m.group(1), m.start()) for m in re.finditer(r"\b(?:Res|R)\.font\.(\w+)", text)]
    reported = set()
    for name, at in sorted(uses, key=lambda u: u[1]):
        key = re.sub(r"[^a-z0-9]", "", name.lower())
        if not key or key in reported or key.startswith(SYSTEM_FACES) or name.startswith("."):
            continue
        shipped = project_fonts(path) if shipped is None else shipped
        if not any(f.startswith(key) for f in shipped):
            reported.add(key)
            add("unshipped-font", line_of(at), f"'{name}'")

    if ANIMATION.search(text) and not REDUCE_MOTION.search(text):
        add("no-reduce-motion", line_of(ANIMATION.search(text).start()))  # type: ignore[union-attr]

    return found


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--platform", choices=["ios", "macos"], help="lint Swift files as this platform (default: detected from the project and the file)")
    ap.add_argument("--allow", default="", help="comma-separated rules to skip, for deliberate style choices")
    ap.add_argument("--a11y", action="store_true", help="report only the accessibility rules (Accessibility audit mode)")
    ap.add_argument("--list-rules", action="store_true")
    args = ap.parse_args()

    if args.list_rules:
        for rule, (sev, what, fix) in RULES.items():
            if not args.a11y or rule in CRITERIA:
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
        for rule, lineno, detail in lint_file(f, args.platform):
            if rule in allow or args.a11y and rule not in CRITERIA:
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
