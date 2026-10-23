# Accessibility: audit and build to WCAG 2.2 AA, ready for an ACR

Two uses:
- **Accessibility mode.** Audit an existing iOS, Android or Mac app (code, screenshots, or both) for conformance. There is no intake, no deal and no direction: the app keeps its look. The output is findings, the Accessibility line and a draft ACR. Section 2 is the process.
- **Build and Redesign, step 5.** The Access pass (`critique.md` pass 15) and the report's Accessibility line use the checks in section 3.

Sources for every rule here, and the gap audit that produced this file, are in `../research/accessibility-references.md`. Rule ids are in `principles.md` (R-A11Y-*).

## Contents
1. What conformance means for an app
2. Accessibility mode: the process
3. The checks
4. The Accessibility line
5. The draft ACR
6. Style trade-offs

## 1. What conformance means for an app

- **The standard is WCAG 2.2 Level A and AA, read through WCAG2ICT** (W3C Group Note, Dec 2025):
  - "web page" means the screen or window;
  - a CSS pixel is a pt on iOS and macOS and a dp on Android;
  - 1.4.4 asks for text "up to the text sizing capabilities of the platform".
  - Criteria that apply only to *sets of software* are Not Applicable to one app: 2.4.1, 2.4.5, 3.2.3, 3.2.6.
  - 1.4.12 is Not Applicable where the platform can't override text spacing.
- **Section 508** incorporates WCAG 2.0 AA (E207.2). It adds chapter 5:
  - 502: interoperability with assistive technology;
  - 503.2: follow the user's platform settings for colour, contrast, font size and focus cursor;
  - 503.4: caption controls next to the volume control.
- **EN 301 549.** V3.2.1 is WCAG 2.1. V4.1.1 (Sept 2026) is WCAG 2.2 and is prepared for the European Accessibility Act.
  - Its clause 11 mirrors WCAG for software.
  - It adds two requirements: every screen or window has a title (11.2.4.2), and consistent identification applies within one program (11.3.2.4).
- **An ACR is the VPAT 2.5Rev template filled in.** Each criterion gets one of five terms (ITI's definitions):
  - **Supports**, **Partially Supports**, **Does Not Support**, **Not Applicable**, each with a remark that justifies it;
  - **Not Evaluated**, which is allowed only at Level AAA. Every A and AA criterion needs a real answer.
- **Apple's Accessibility Nutrition Labels** follow the same rule: a feature (VoiceOver, Voice Control, Larger Text, Dark Interface, Differentiate Without Color Alone, Sufficient Contrast, Reduced Motion, Captions, Audio Descriptions) may be declared only when *all common tasks* work with it:
  - primary function;
  - first launch;
  - login;
  - purchase;
  - settings.

  Google Play has no equivalent declaration. Its pre-launch report flags four kinds of issue: content labels, touch targets (48 dp), contrast (4.5:1, or 3:1 for large text and images), and implementation.
- **What this skill can claim, and what it can't.** Its evidence is code review, lint and renders.
  - That is enough to find most failures and to draft an ACR.
  - It is not a test with VoiceOver, TalkBack, Switch Control, Voice Control, Voice Access or a keyboard on a device.
  - Every Accessibility line and every draft ACR says so. Never present a draft as a finished ACR, and never claim a Nutrition Label for an app you saw one screen of.

## 2. Accessibility mode: the process

**Platform first**, as in every mode: iOS, iPadOS, Android, macOS, or a Compose Multiplatform app on several of them. Name it in the reply.

1. **Scope.** List the screens and the common tasks the audit covers: Apple's list (primary function, onboarding, login, purchase, settings), or what the user names. If the request is thin, audit what the code or screenshots contain and say what's left out.
2. **Lint, accessibility rules only:**
   ```bash
   python3 <skill>/scripts/lint.py <source folder> --a11y [--platform ios|macos]
   ```
   Every finding names its WCAG criterion. A FAIL is a failure unless the code around it proves otherwise (a trait applied by a parent the regex can't see). A WARN is a lead to check by reading the code.

   The rules cover SwiftUI and Compose only. For UIKit, AppKit or XML Views, do the same checks by reading the code: `isAccessibilityElement`, `accessibilityLabel` / `accessibilityTraits`, `contentDescription`, `importantForAccessibility`, `android:labelFor`, `adjustsFontForContentSizeCategory`.
3. **Render at the default and the largest text size**, light and dark. Look at every frame with section 3.3.
   - **iOS (SwiftUI):** `python3 <skill>/scripts/render_swiftui.py <files> --platform ios --out ax5.png --dynamic-type ax5`. Run it again without `--dynamic-type` for the default frame. It needs a `#Preview` that builds the screen with sample data.

     For a built app on a simulator: `xcrun simctl ui booted content_size accessibility-extra-extra-extra-large`, then `xcrun simctl io booted screenshot ax5.png`. Set it back with `content_size large`. `xcrun simctl ui booted increase_contrast enabled` shows the Increase Contrast frame.
   - **Android (Compose):** a screenshot test or preview at `fontScale = 2f` (`@Preview(fontScale = 2f)`, or `@PreviewFontScale` for 85–200%) rendered with Roborazzi or Paparazzi. On an emulator: `adb shell settings put system font_scale 2.0`, then `adb exec-out screencap -p > fs2.png`, and set it back to `1.0`.
   - **macOS:** there is no Dynamic Type to render. Apple documents that `dynamicTypeSize` doesn't change text size on a Mac, and a render with it is identical. Render the window at its minimum size, and with the app's own zoom (⌘+) if it has one (`platform-macos.md` §6).
   - **HTML mock** (when nothing native can run): `python3 <skill>/scripts/fold.py mock.html --text-scale ax5 --shot ax5.png` (or `android2`). It maps every font size through the platform's own large-text table and reruns the fold check at that size.
4. **Read the code for what a picture can't show** (section 3.1–3.2): names, roles, values, reading order, actions, announcements, focus.
5. **If a device or simulator with assistive tech is available, use it** and say so in the report. That is the only way to move a criterion from "from code" to "tested".
   - Accessibility Inspector's audit (Xcode > Open Developer Tool) on a simulator build.
   - VoiceOver: swipe through the common tasks.
   - Voice Control: "Show names".
   - Android Accessibility Scanner, and TalkBack.
   - A hardware keyboard: Full Keyboard Access on iOS, Tab on Android and the Mac.
6. **Report:**

```markdown
# Accessibility audit: <app or screens> (<platform>)

**Scope:** <screens and common tasks covered; what wasn't>
**Evidence:** <lint --a11y, renders at default and <largest size>, code review; AT testing: none / what was tested on what device>
**Verdict:** <2–3 sentences: where the app stands against WCAG 2.2 AA and the worst barriers>

## Findings
| # | Sev | Criterion | Finding | Where | Fix |
|---|---|---|---|---|---|
| 1 | 4 | 4.1.2 | Habit check-off is an `onTapGesture` on a circle: VoiceOver hears no button and no state | `HabitRow.swift:42` | `Button` with a `ButtonStyle`, `.accessibilityValue(done ? "Done" : "Not done")` |
| 2 | 3 | 1.4.4 | At AX5 the departure time truncates to "06:…" inside a 44 pt fixed row | `ax5.png`, `DepartureRow.swift:18` | `minHeight`, stack the time above the name when `isAccessibilitySize` |

## Large text
<what the largest-size render shows, frame by frame>

Accessibility: <the line from section 4>
```

Severity uses the 0–4 scale from `audit.md`:
- **4** blocks a task for some users: no name or role on a control, a modal that leaves the content behind it reachable, text clipped at large sizes so its meaning is lost.
- **3** is frequent friction.
- **2** and **1** as in `audit.md`.

Order the findings by severity, then by how often the screen is used. Then draft the ACR (section 5) when the user needs one.

## 3. The checks

Each heading names its criteria. The lint rule that catches part of it is in brackets; the rest is judgement from the code and the renders.

### 3.1 Names, roles, values (1.1.1, 1.3.1, 4.1.2, 2.5.3)
- **Use the real control.** A `Button`, `Toggle`, `Slider` or `Picker` with a custom style keeps its name, role, state and keyboard activation for free. SwiftUI's `ButtonStyle` and `ToggleStyle` keep the control's accessibility; Compose's `Modifier.clickable(role =, onClickLabel =)` and `toggleable` / `selectable` merge the children and expose the action. A tap gesture on a shape keeps none of it [`tap-no-role`]. In Compose, `pointerInput { detectTapGestures }` is invisible to TalkBack, Switch Access and the keyboard.
- **Name:** short, the purpose, no control type ("Buy ticket", not "Buy ticket button"); the trait or role says the type. Icon-only controls always need one [`unlabelled-icon-button`].
- **Label in name:** the name starts with the visible words, so Voice Control and Voice Access can call it by what it shows [`label-in-name`]. SwiftUI's `.accessibilityInputLabels([...])` adds spoken synonyms. Keep the visible text first.
- **Role and state:**
  - Custom toggles report their state [`toggle-no-state`]: SwiftUI `.accessibilityValue("On")` or `.accessibilityAddTraits(.isSelected / .isToggle)`; Compose `toggleable(role = Role.Switch)` or `stateDescription`.
  - Selected tabs and segments carry `.isSelected` / `selected = true`.
  - Headings carry `.isHeader` / `heading()` [`heading-missing`].
- **Pictures:**
  - Each one has a text alternative that says what it means ("Bulk ferment, 62%"), or is marked decorative [`image-no-label`]: SwiftUI `Image(decorative:)` or `.accessibilityHidden(true)`; Compose `contentDescription = null`.
  - A drawn gauge, chart or mascot that shows state carries a label and a value. A chart has an audio graph or a text summary.
  - Never hide a control [`a11y-hidden-control`].
- **Grouping:** a row reads as one element with one name. SwiftUI: `.accessibilityElement(children: .combine)` (or `.ignore` with your own label). Compose: `semantics(mergeDescendants = true) {}`, which `clickable` already does. Its secondary actions become custom actions: `.accessibilityAction(named:)` / `customActions`.

### 3.2 Order and focus (1.3.2, 2.4.3, 2.4.7, 2.4.11, 2.1.1, 2.1.2)
- **Reading order.** VoiceOver and TalkBack follow reading order: top to bottom, then left to right in a left-to-right language. Read the screen in that order and check it still makes sense: the hero number before its caption, a row's name before its time.
  - Overlays drawn in a `ZStack` or a `Box` can put a floating element out of place. Pin the order with SwiftUI `.accessibilitySortPriority` (higher first) inside an `.accessibilityElement(children: .contain)` group, or Compose `isTraversalGroup` + `traversalIndex` (lower first).
  - SwiftUI's exact order for overlapping `ZStack` children isn't documented. Check it with VoiceOver when you can, and say "from code" when you can't.
- **Modals.**
  - A custom overlay (scrim + panel) traps assistive focus inside it [`overlay-not-modal`]: SwiftUI `.accessibilityAddTraits(.isModal)` on the panel; Compose `Dialog` / `ModalBottomSheet`, or `clearAndSetSemantics {}` on the content behind.
  - Escape dismisses it: `.accessibilityAction(.escape)` / `onExitCommand` on a Mac, `BackHandler` on Android (2.1.2).
- **Keyboard and switch.** Every action is reachable with Full Keyboard Access, Switch Control, a hardware keyboard and a D-pad (2.1.1). A gesture-only control isn't.
  - Single-key shortcuts need a modifier or must only work while a view has focus [`character-key-shortcut`, 2.1.4].
- **Focus visible.** Keep the system focus ring; if you replace it, draw your own [`focus-ring-removed`]. In Compose, `indication = null` also removes the focus indication.
- **Focus not obscured.** Pinned bars and FABs never cover the focused row completely. `.safeAreaInset` / `Scaffold` padding does it; check the end frame (`fold.py`) at large text too [`pinned-bottom-overlap`].

### 3.3 Text size and reflow (1.4.4, 1.4.10, 1.4.5)
- **What "largest" means:**
  - iOS AX5: Body 17 → 53 pt, Caption 2 11 → 40 pt, Large Title 34 → 60 pt. Apple's Larger Text label asks for at least 200%.
  - Android at font scale 2.0, nonlinear: 14 sp → 26 dp, 24 sp → 36 dp, 30 sp → 38 dp.
  - macOS: no Dynamic Type; an in-app zoom where content is dense.
- **The defects to look for in the large-text render:**
  - Text that clips, truncates into "…", or overlaps a neighbour. A truncated row is allowed only if the full text is one tap away.
  - A row that keeps its height.
  - Columns that stay side by side when they should stack.
  - Horizontal scrolling to read a line (1.4.10).
- **Fixes:**
  - SwiftUI: text styles, or `.custom(_:size:relativeTo:)` [`fixed-font-size`]; `@ScaledMetric` for sizes that sit next to text; `minHeight`, not `height` [`fixed-text-frame`]; at `dynamicTypeSize.isAccessibilitySize` switch `HStack` to `VStack` (or use `ViewThatFits`).
  - Compose: `sp` for text, `heightIn(min =)` not `height()` around text [`fixed-text-frame`], `FlowRow`.
- **Caps.** Don't cap scaling below the accessibility sizes [`dynamic-type-capped`]. The only defensible cap is a display number that already fills its region (a 96 pt countdown at `...accessibility2`). Say so on the line. Tab bars and other chrome that can't grow use the Large Content Viewer (`.accessibilityShowsLargeContentViewer()`).
- **Images of text.** No type baked into images, SVG rigs or sprites (1.4.5). A mascot's speech bubble is real `Text`.

### 3.4 Colour and contrast (1.4.1, 1.4.3, 1.4.11)
- **Colour is never the only signal** [`colour-only-state`]. "Late" in red also has an icon, a word or a strike-through. Squint at a grayscale copy of the render: every state still reads. Honour Differentiate Without Colour (`accessibilityDifferentiateWithoutColor`) by adding shapes or glyphs.
- **Text contrast** is 4.5:1, or 3:1 at 18 pt and up, or 14 pt bold and up. Controls' boundaries and states, and meaningful graphics, are 3:1 against what's next to them (1.4.11).
  - Measure the pairs the render actually shows, in light and dark, with the formula in `audit.md`; `deal.py` measured only the palette.
  - Text over photos or materials: composite first, check the worst spot.
- **Increase Contrast.** Offer higher-contrast colours when it is on: SwiftUI `colorSchemeContrast == .increased`, Asset Catalog high-contrast variants; Android `UiModeManager.getContrast()` on API 34+, or M3's medium and high contrast schemes. Apple's Sufficient Contrast label wants the default colours to pass without it.

### 3.5 Motion, time and flashing (2.2.1, 2.2.2, 2.3.1)
- **Reduce Motion / Remove animations:** swap travel for fades and stop loops [`no-reduce-motion`]. The motion budget in SKILL.md already says how.
- **Pause, Stop, Hide.** Anything that moves on its own for more than 5 s next to other content has a pause control, or stops within 5 s (2.2.2). A system setting alone is a weak answer: say "Partially supports" if that's all there is.
- **Flashing.** Nothing flashes more than three times a second, whatever the settings (2.3.1). Check CRT flicker and celebration strobes in the filmstrip.
- **Timeouts.** A toast with an Undo button stays up while a screen reader is on. Compose's `SnackbarHost` already does this; a hand-made toast must too (2.2.1). On Android, use `AccessibilityManager.getRecommendedTimeoutMillis`.

### 3.6 Pointer and gestures (2.5.1, 2.5.2, 2.5.4, 2.5.7, 2.5.8)
- **Gestures.** Every swipe, drag, pinch or rotate has a single-tap alternative on screen and an accessibility action [`gesture-no-alternative`]:
  - SwiftUI: `.accessibilityAction(named:)`, `.accessibilityAdjustableAction`;
  - Compose: `customActions`.
  - SwiftUI `List` `.swipeActions` are exposed to VoiceOver already.
- **Pointer cancellation.** Actions fire on release, not on touch-down. A press state built from `DragGesture(minimumDistance: 0)` or `onPress` must not trigger the action.
- **Targets.** 44×44 pt on iOS, 48×48 dp on Android, 24×24 pt minimum on a Mac with 22 pt controls [`small-target`]. WCAG's floor is 24×24, so the platform sizes pass with room.
- **Motion actuation.** Shake or tilt features have an on-screen equivalent and can be turned off (2.5.4).

### 3.7 Input and errors (1.3.5, 3.3.1–3.3.4, 3.3.7, 3.3.8)
- **Labels.** Persistent labels, not placeholders [`placeholder-only-field`].
- **Content types** on personal data, so autofill and password managers work [`field-no-content-type`]:
  - SwiftUI: `.textContentType(.emailAddress)`, `.password`, `.oneTimeCode`;
  - Compose: `semantics { contentType = ContentType.EmailAddress }`, `KeyboardOptions`.
  - This also serves 3.3.7 and 3.3.8: never block paste into a password field, and offer a non-memory way to log in.
- **Errors** are text next to the field, say how to fix it, and are announced (4.1.3).
- **Payments and bookings** have a review step or an undo (3.3.4).

### 3.8 Status, titles, language (4.1.3, 2.4.2, 2.4.6, 3.1.2)
- **Status messages** reach assistive tech without moving focus [`status-not-announced`]: "Saved", "Timer done", "3 results". SwiftUI: `AccessibilityNotification.Announcement("Saved").post()`. Compose: `semantics { liveRegion = LiveRegionMode.Polite }`, or `SnackbarHost`.
- **Titles.** Every screen and window has a title, even when a custom header replaces the visible one. Set `.navigationTitle` anyway; a hidden navigation bar's title may not be announced, so check that with VoiceOver (unverified). Compose has `paneTitle`. EN 301 549 V4.1.1 requires a title for each screen or window (11.2.4.2).
- **Language.** Text in another language says so (3.1.2). SwiftUI: an `AttributedString` with `accessibilitySpeechLanguage` set (API name unverified). Compose: `SpanStyle(localeList = LocaleList("it"))`. A translator's source column is the common case.

### 3.9 Platform settings (508 503.2, EN 301 549 11.7)
Follow the user's settings, read them, and render the ones that change the look:

| Setting | SwiftUI | Android / Compose |
|---|---|---|
| Text size | text styles, `relativeTo:`, `@ScaledMetric` | `sp`, `LocalDensity.current.fontScale` for layout only |
| Bold Text | `legibilityWeight == .bold` (custom fonts must handle it) | `Configuration.fontWeightAdjustment` (API 31) |
| Increase Contrast | `colorSchemeContrast == .increased` | `UiModeManager.getContrast()` (API 34) |
| Reduce Transparency | `accessibilityReduceTransparency`: opaque surfaces. System materials adapt; a home-made blur doesn't [`no-reduce-transparency`] | — |
| Reduce Motion | `accessibilityReduceMotion` | animator duration scale, `MotionDurationScale` |
| Differentiate Without Colour | `accessibilityDifferentiateWithoutColor` | no setting: always pair colour with a shape |
| Smart Invert | `.accessibilityIgnoresInvertColors()` on photos and video | — |
| Button Shapes | `accessibilityShowButtonShapes`: give text buttons an edge | — |
| Dark appearance | both appearances designed | both appearances designed |

### 3.10 Media (1.2.x, 508 503.4)
With video or audio: captions, audio description, a transcript for audio-only content, and caption controls next to the volume control. Without media, these are Not Applicable.

## 4. The Accessibility line

The report's line states conformance the way an ACR does: per criterion, one term and a reason. Write it on one line, grouped by term:

```
Accessibility: WCAG 2.2 AA, from code, lint and renders at <default and AX5 / font scale 2.0 / minimum window>; not tested with assistive technology. Supports: 1.1.1 (every glyph labelled, the gull hidden), 1.4.1 (late shows a strike-through and "late", not only red), …; Partially supports: 1.4.4 (countdown capped at AX2 because it fills its region; everything else reaches AX5, rendered); Does not support: none; Not applicable: 1.2.1–1.2.5 (no media), 2.4.1, 2.4.5, 3.2.3, 3.2.6 (sets of software only), 1.4.12 (no platform spacing override)
```

**Which criteria.** Every build answers the core set, because every screen can fail it: 1.1.1, 1.3.1, 1.3.2, 1.3.4, 1.4.1, 1.4.3, 1.4.4, 1.4.10, 1.4.11, 2.1.1, 2.2.2, 2.4.3, 2.4.6, 2.4.7, 2.4.11, 2.5.1, 2.5.3, 2.5.7, 2.5.8, 4.1.2 and 4.1.3. Add:
- 1.3.5, 3.3.1, 3.3.2 and 3.3.3 when the screen takes input;
- 3.3.4 when it takes money;
- 3.3.8 for login;
- 1.2.x for media;
- 2.1.4 for shortcuts;
- 3.1.2 for mixed languages;
- 2.3.1 for flicker or strobe.

**The terms:**
- **Supports** only with evidence: the code does it and the render shows it, or lint has no finding and the code was read. If the only evidence is that nothing contradicts it, write the reason that way ("from code: …").
- **Partially supports** when part of the screen falls short (one capped number, one unlabelled chart); name the part.
- **Does not support** when most of the screen falls short.
- **Not applicable** with the reason.
- A lint FAIL on a criterion means it can't be Supports.
- Keep it honest: a line full of "Supports" with no renders behind it is worse than a short line that says what was checked.

## 5. The draft ACR

```bash
python3 <skill>/scripts/acr.py <files or folder> --report response.md --product "<app, screens>" --platform ios|android|macos --out acr.md
```

It fills VPAT 2.5Rev's WCAG tables (55 criteria at A and AA):
- each criterion gets the term and reason from the Accessibility line;
- the lint findings for each criterion go into its remarks, and a FAIL lowers a "Supports" claim;
- the sets-of-software criteria are marked Not Applicable with WCAG2ICT's reason;
- everything else is marked "To evaluate". That is not a VPAT term on purpose: someone must answer it before the report goes out.

It closes with the 508 chapter 5 and EN 301 549 clause 11 notes. The Evaluation Methods field says what the evidence was and that no assistive-technology testing was done. Hand it over as a draft.

## 6. Style trade-offs

The skill's stance is "warn, don't block" for *style* (SKILL.md): a 3.8:1 neon caption can ship with a warning, the measured value and the compliant fix. That stance applies only to contrast, type size and motion intensity, where a style choice costs some users some ease.

It never covers the things that cost nothing visually and lock people out:
- names and roles;
- states;
- reading order;
- modal focus;
- text scaling;
- accessibility actions for gestures;
- announcements;
- the Reduce Motion fallback.

Those are built in at every setting. In the Accessibility line, a style trade-off is "Partially supports" with the reason and the fix, never "Supports".
