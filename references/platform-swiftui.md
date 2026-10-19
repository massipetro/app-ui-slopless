# SwiftUI implementation patterns

How to turn a design brief into idiomatic SwiftUI (iOS 17+, with notes for iOS 26). Copy the shapes of these snippets, not their values. The values come from the brief.

## Contents
1. Tokens
2. Custom fonts that still scale (Dynamic Type)
3. Press states and button styles
4. Depth: hard shadows, lips, strokes
5. Motion: springs, reduce motion, number changes
6. Haptics
7. Layout: safe areas, thumb zone, large text
8. Accessibility labels for custom controls
9. iOS 26 Liquid Glass

---

## 1. Tokens

Keep one file. Use asset-catalog colours (or `Color(light:dark:)`) so dark mode is designed, not inverted.

```swift
enum Ink {
    static let surface   = Color("Surface")      // asset with Any/Dark variants
    static let ink       = Color("Ink")
    static let primary   = Color("Primary")
    static let accent    = Color("Accent")
    static let success   = Color("Success")
}

enum Space { static let xs: CGFloat = 4, s: CGFloat = 8, m: CGFloat = 16, l: CGFloat = 24, xl: CGFloat = 40 }
enum Radius { static let chip: CGFloat = 999, card: CGFloat = 20, control: CGFloat = 14 }
```

No asset catalog (e.g. a single-file deliverable)? Build a dynamic colour:

```swift
extension Color {
    init(light: UIColor, dark: UIColor) {
        self.init(UIColor { $0.userInterfaceStyle == .dark ? dark : light })
    }
}
```

## 2. Custom fonts that still scale

Custom fonts must follow Dynamic Type (HIG). Pass `relativeTo:` so they scale with a text style.

```swift
extension Font {
    static func display(_ size: CGFloat, relativeTo style: Font.TextStyle = .largeTitle) -> Font {
        .custom("BricolageGrotesque-ExtraBold", size: size, relativeTo: style)
    }
    static func body(_ size: CGFloat = 17) -> Font { .custom("InstrumentSans-Regular", size: size, relativeTo: .body) }
}
```

For non-text metrics that should grow with text, such as icon size or row height, use `@ScaledMetric`:

```swift
@ScaledMetric(relativeTo: .body) private var iconSize: CGFloat = 24
```

Big display numbers: use `.monospacedDigit()` for values that change. If a giant number must not wrap, add `.minimumScaleFactor(0.5)` and `.lineLimit(1)`, but check it at AX5. Use `ViewThatFits` to swap to a stacked layout at large sizes.

Font files: add them to the target, then list them under `UIAppFonts` in Info.plist. Prefer OFL fonts from Google Fonts so the user can ship them.

## 3. Press states and button styles

Every custom button gets a `ButtonStyle`, so the pressed state comes for free and stays consistent.

```swift
struct LipButtonStyle: ButtonStyle {            // playful: 3D lip that compresses
    var fill: Color, lip: Color
    func makeBody(configuration: Configuration) -> some View {
        let pressed = configuration.isPressed
        configuration.label
            .font(.body(17).weight(.bold))
            .foregroundStyle(.white)
            .frame(maxWidth: .infinity, minHeight: 52)
            .background(RoundedRectangle(cornerRadius: 16).fill(fill))
            .background(RoundedRectangle(cornerRadius: 16).fill(lip).offset(y: pressed ? 0 : 4))
            .offset(y: pressed ? 4 : 0)
            .animation(.spring(response: 0.18, dampingFraction: 0.6), value: pressed)
            .contentShape(Rectangle())
    }
}
```

Use `.contentShape(Rectangle())` so the whole row or card is the target, not just the text (Fitts).

## 4. Depth: hard shadows, lips, strokes

A hard offset shadow (neo-brutalist) is a second shape behind the first, not `.shadow()`:

```swift
struct HardShadow: ViewModifier {
    var offset: CGFloat = 6, radius: CGFloat = 12, stroke: CGFloat = 3, ink: Color = .black
    func body(content: Content) -> some View {
        content
            .clipShape(RoundedRectangle(cornerRadius: radius))
            .overlay(RoundedRectangle(cornerRadius: radius).stroke(ink, lineWidth: stroke))
            .background(RoundedRectangle(cornerRadius: radius).fill(ink).offset(x: offset, y: offset))
    }
}
```

When pressed, translate the content by `offset` and set the shadow offset to 0, so it "clicks in".

Soft elevation (warm premium): use one layered shadow with a tinted colour, never black at 5%. For example: `.shadow(color: Ink.ink.opacity(0.08), radius: 1, y: 1)` + `.shadow(color: Ink.primary.opacity(0.12), radius: 16, y: 8)`.

## 5. Motion

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion

withAnimation(reduceMotion ? .easeOut(duration: 0.2) : .spring(response: 0.35, dampingFraction: 0.7)) {
    isDone.toggle()
}
```

- Transitions: under Reduce Motion, `.transition(reduceMotion ? .opacity : .move(edge: .bottom).combined(with: .opacity))`.
- Number changes: `.contentTransition(.numericText(value: streak))` with `withAnimation`.
- Symbol effects: `.symbolEffect(.bounce, value: count)` for one-off celebrations. It respects Reduce Motion automatically.
- Phased celebration: use `PhaseAnimator` / `KeyframeAnimator` (iOS 17) for a streak flame or stamp. Run it once per event, never looping on a frequent path.
- Shared-element continuity: `matchedGeometryEffect` within a screen, `.navigationTransition(.zoom(sourceID:in:))` (iOS 18) for card-to-detail navigation.

### Custom glyphs, draw-on and ambient life

Draw the core verb's glyph as a `Shape`, and animate `.trim`:

```swift
struct Tick: Shape {                                  // chunky, slightly asymmetric
    func path(in r: CGRect) -> Path {
        var p = Path()
        p.move(to: CGPoint(x: r.width * 0.18, y: r.height * 0.54))
        p.addLine(to: CGPoint(x: r.width * 0.42, y: r.height * 0.76))
        p.addLine(to: CGPoint(x: r.width * 0.84, y: r.height * 0.26))
        return p
    }
}

Tick()
    .trim(from: 0, to: done ? 1 : 0)
    .stroke(color, style: StrokeStyle(lineWidth: 4, lineCap: .round, lineJoin: .round))
    .frame(width: 28, height: 28)
    .scaleEffect(done ? 1 : 0.6)
    .animation(reduceMotion ? nil : .spring(response: 0.25, dampingFraction: 0.45), value: done)
```

- **Glyph families:** draw them as `Shape`s, or as a custom SF Symbol template (export from the SF Symbols app, edit, and import into the asset catalog). The custom symbol then gets `.symbolEffect` for free.
- **Ambient loops:** use `PhaseAnimator` with `repeating`, or `TimelineView(.animation)` for continuous motion (flicker, bob). Gate both on `accessibilityReduceMotion`:

```swift
mascot
    .phaseAnimator(reduceMotion ? [1.0] : [1.0, 1.03]) { v, s in v.scaleEffect(s) }
        animation: { _ in .easeInOut(duration: 1.2) }
```

- **Staggered entrance:** `.transition(.scale(scale: 0.9).combined(with: .opacity))` plus `.animation(.spring(response: 0.35, dampingFraction: 0.6).delay(Double(index) * 0.04), value: appeared)`, triggered once from `.onAppear`.
- **Particles:** a `Canvas` + `TimelineView` drawing N shapes, or `KeyframeAnimator` per sparkle. No library is needed.
- **Rive / Lottie:** `RiveRuntime` or `lottie-ios` via SwiftPM.
- **Check it frame by frame:** record the simulator (`xcrun simctl io booted recordVideo motion.mov`), split it with `ffmpeg -i motion.mov -vf fps=15 frames/f%03d.png`, and tile the frames around the action with `scripts/filmstrip.py` (SKILL.md step 5). A `KeyframeAnimator` / `PhaseAnimator` whose last frame doesn't match the resting view snaps at the end; the strip shows it.

## 6. Haptics

```swift
.sensoryFeedback(.success, trigger: completedCount)      // iOS 17
.sensoryFeedback(.impact(weight: .light), trigger: isPressed)
```

Match haptic weight to action weight (Shneiderman: modest for frequent actions, substantial for major ones). Don't buzz on scroll or on every keystroke.

## 7. Layout

- Backgrounds extend under bars with `.ignoresSafeArea()` on the *background only*. Content stays inside the safe area.
- Keep the bottom CTA in the thumb zone: `.safeAreaInset(edge: .bottom) { PrimaryCTA() }` keeps it above the home indicator and lets scroll content pass under it.
- Large text: test with `.dynamicTypeSize(.accessibility3)` in previews. Use `@Environment(\.dynamicTypeSize)` to switch `HStack` → `VStack`, or wrap in `ViewThatFits`.
- Keep the system `NavigationStack` back button. A custom back must keep the edge-swipe (don't hide it with `.navigationBarBackButtonHidden` unless you rebuild the gesture).
- Use the system `TabView` for top-level navigation. Restyle it with `.tint`, custom symbols and labels. If you build a custom bar, keep labels, 44 pt targets and `.accessibilityAddTraits(.isSelected)`.

## 8. Accessibility for custom controls

```swift
CustomToggle(isOn: $on)
    .accessibilityElement(children: .ignore)
    .accessibilityLabel("Notifications")
    .accessibilityValue(on ? "On" : "Off")
    .accessibilityAddTraits(.isButton)
    .accessibilityAction { on.toggle() }
```

- Decorative images and mascots: `.accessibilityHidden(true)`.
- Combine stat tiles into one element: `.accessibilityElement(children: .combine)`.

## 8b. Code baseline (what users feel)

A bold screen that hitches reads as broken (Tuch et al. 2012). These rules cover only what's visible: smooth scrolling, animations that don't reset, state that survives. Sources and the full list of 20 are in `../research/code-baseline.md`; rules 15–17 come from compile failures and drift in our own evals.

1. **`@Observable` models** (add `@MainActor` when the model drives UI state, then see rule 15 for where it may be created). The owner holds `@State private var model = Model()`. Children get `let`, `@Bindable` or `@Environment(Model.self)`. No `ObservableObject` in new code.
2. **`@State` is `private` and never mirrors a parent value** (it would freeze on the first value). Use `let` or `@Binding`.
3. **Stable identity:** `ForEach` over `Identifiable` with a stored `id`. Never `indices`, `\.offset`, or a `UUID()` made in `body`, because they reset row state and break insert/delete animations.
4. **Same view shape per `ForEach` element:** filter before the loop, and wrap conditional content in a `VStack`.
5. **Change modifier values, not branches:** `.opacity(hidden ? 0 : 1)` keeps identity, so animations and state survive. No `.if {}` helpers. Avoid `AnyView` in rows.
6. **`List` / `LazyVStack` for long feeds.** Lazy rows lose `@State` off-screen, so keep row state in the model.
7. **Trivial `init`/`body`:** no sorting, filtering or formatter construction. Use `Text(date, format: …)`.
8. **Async work in `.task {}` / `.task(id:)`**, which cancels automatically and restarts when the input changes.
9. **Never block the main actor:** decode JSON and images off-main, and downsample large images to display size.
10. **Give rows their element** (`Row(item:)`), not the store plus an id, so one change doesn't redraw every row.
11. **Fast-changing values stay out of broad state:** use `scrollTransition` / `visualEffect` for scroll-driven visuals and `onScrollGeometryChange` (iOS 18, so behind `#available`; see rule 17) thresholded to a Bool for logic.
12. **Animate transforms and opacity, not `frame`/`padding`.** Attach `.animation(_:value:)` to the smallest subtree, and sequence with `withAnimation {} completion: {}`, not `DispatchQueue` delays.
13. **Per-window state** (tab, selection, `NavigationPath`) goes in `@SceneStorage`. Navigate by value with `navigationDestination(for:)`, and present with `sheet(item:)`.
14. **One `#Preview` per state** (loading, empty, error, longest string) plus dark and AX sizes. Profile a release build on device with the Instruments SwiftUI template.
15. **Create `@MainActor` models only where the main actor runs.** `View` is main-actor isolated, so `@State private var model = Model()` is fine. A default argument is not: `init(model: Model = Model())` fails to compile with "call to main actor-isolated initializer in a synchronous nonisolated context", and so does a `static let` or a global. Pass the model in from the caller, or create it in the `@State` initializer.
16. **Keep each view expression small enough to typecheck.** When the compiler reports "failed to produce diagnostic" or "unable to type-check this expression in reasonable time", it gave up on one expression: extract parts into small subviews or computed properties until it names the real error. Don't put conditionals inside result builders that don't support them (`keyframes:`, `ShapeStyle` chains): branch outside the builder, e.g. `trigger: reduceMotion ? 0 : stamp`, or apply the modifier conditionally on a value. Typecheck with `scripts/typecheck.py` before you render.
17. **Build for the project's deployment target, not the newest SDK.** Read it from the project (`IPHONEOS_DEPLOYMENT_TARGET`, or `platforms: [.iOS(...)]` in `Package.swift`); with none, target iOS 17. Use newer APIs only behind a check, with a fallback that still looks designed:
    - iOS 18: `Tab(...)` in `TabView` (use `.tabItem` on 17), `onScrollGeometryChange`, `MeshGradient`, `.navigationTransition(.zoom(...))`, `ScrollPosition`, `.presentationSizing`. iOS 26: `.glassEffect()`, `GlassEffectContainer`.
    - Inside a body: `if #available(iOS 18, *) { MeshGradient(...) } else { LinearGradient(...) }`. For a modifier, wrap it in a small `ViewModifier` that branches, so the call site stays one line. For a whole type, mark it `@available(iOS 18, *)` and branch where it's used.
    - Never raise the target (or `typecheck.py --ios`) to make an availability error go away. If the project really targets something newer, say so in the report.

**Companion skill:** for deeper SwiftUI correctness, suggest that users install [twostraws/swiftui-agent-skill](https://github.com/twostraws/swiftui-agent-skill) (SwiftUI Pro, MIT): `/plugin marketplace add twostraws/SwiftUI-Agent-Skill`, and tell it the real deployment target. Use [avdlee/swiftui-agent-skill](https://github.com/avdlee/swiftui-agent-skill) (MIT) instead if Instruments trace analysis is needed.

## 9. iOS 26 Liquid Glass

In iOS 26, system bars, tab bars and toolbars are glass automatically when you use the system components.
- In **warm premium** and **editorial**, let the system glass float over rich content (photos, big type). That's where it looks right.
- In **neo-brutalist**, glass conflicts with the flat, opaque look. Use `.toolbarBackgroundVisibility(.visible, for: .navigationBar)` with a solid colour, or build an opaque custom bar (and note it as a convention break).
- `.glassEffect()` on custom controls (iOS 26, so behind `if #available(iOS 26, *)` unless the project targets 26; rule 17): only over real content, never as decoration on a flat background (a slop tell).
