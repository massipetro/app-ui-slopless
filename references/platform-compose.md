# Jetpack Compose / Compose Multiplatform implementation patterns

How to turn a design brief into idiomatic Compose (Material 3, Compose 1.7+ / CMP 1.7+). Copy the shapes of these snippets, not their values. The values come from the brief.

## Contents
1. Tokens and theme
2. Custom fonts (and scaling)
3. Press states and indications
4. Depth: hard shadows, lips, strokes
5. Motion: springs, reduce motion, number changes
6. Haptics
7. Layout: insets, thumb zone, large text, back
8. Accessibility semantics for custom controls
9. Compose Multiplatform specifics

---

## 1. Tokens and theme

Map the brief onto `MaterialTheme`, so stock components (TextField, Switch, NavigationBar) pick up the style. Add a small `CompositionLocal` for tokens M3 doesn't have (stroke width, hard-shadow offset, lip height).

```kotlin
@Immutable data class Brand(
    val stroke: Dp = 3.dp, val shadowOffset: Dp = 6.dp, val lip: Dp = 4.dp,
    val accent: Color, val success: Color,
)
val LocalBrand = staticCompositionLocalOf<Brand> { error("No Brand") }

@Composable fun AppTheme(dark: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {
    val scheme = if (dark) darkScheme else lightScheme          // hand-tuned, not inverted
    CompositionLocalProvider(LocalBrand provides if (dark) brandDark else brandLight) {
        MaterialTheme(colorScheme = scheme, typography = appTypography, shapes = appShapes, content = content)
    }
}
```

Dynamic colour (Material You): offer it only if the preset allows (warm premium can, the others usually shouldn't, since the palette *is* the identity).

## 2. Custom fonts

Android: put fonts in `res/font`. CMP: put them in `composeResources/font` and load them with `Font(Res.font.x)` inside a `@Composable`.

```kotlin
val Display = FontFamily(Font(Res.font.bricolage_extrabold, FontWeight.ExtraBold))
val Text    = FontFamily(Font(Res.font.instrument_sans_regular), Font(Res.font.instrument_sans_semibold, FontWeight.SemiBold))

val appTypography = Typography(
    displayLarge = TextStyle(fontFamily = Display, fontSize = 57.sp, lineHeight = 60.sp, letterSpacing = (-1.5).sp),
    headlineMedium = TextStyle(fontFamily = Display, fontSize = 28.sp, lineHeight = 32.sp),
    bodyLarge = TextStyle(fontFamily = Text, fontSize = 17.sp, lineHeight = 24.sp),
    labelLarge = TextStyle(fontFamily = Text, fontWeight = FontWeight.SemiBold, fontSize = 15.sp),
)
```

- Size text and line height in `sp` so they scale to 200%. Size padding and boxes in `dp`. Never size a text container with a fixed height.
- Use tabular figures for numbers that change: `fontFeatureSettings = "tnum"`.
- Test at 200%: `@Preview(fontScale = 2f)`.

## 3. Press states

Collect `isPressed` from an `InteractionSource` and drive the visual from it. Keep the semantic `onClick`.

```kotlin
@Composable fun LipButton(text: String, onClick: () -> Unit, fill: Color, lip: Color, modifier: Modifier = Modifier) {
    val source = remember { MutableInteractionSource() }
    val pressed by source.collectIsPressedAsState()
    val lipHeight = LocalBrand.current.lip
    val drop by animateDpAsState(if (pressed) lipHeight else 0.dp, spring(dampingRatio = 0.6f, stiffness = 800f))
    val shape = RoundedCornerShape(16.dp)
    Box(
        modifier
            .heightIn(min = 52.dp).fillMaxWidth()
            .padding(bottom = lipHeight)                       // reserve room for the lip
            .clickable(interactionSource = source, indication = null, role = Role.Button, onClick = onClick)
            .drawBehind {                                      // lip: same shape, shifted down, stays put
                drawRoundRect(lip, topLeft = Offset(0f, lipHeight.toPx()), size = size, cornerRadius = CornerRadius(16.dp.toPx()))
            }
            .offset { IntOffset(0, drop.roundToPx()) }         // face drops onto the lip when pressed
            .background(fill, shape),
        contentAlignment = Alignment.Center,
    ) { Text(text, style = MaterialTheme.typography.labelLarge, color = Color.White) }
}
```

The `drawBehind` comes before `.offset`, so the lip stays still while the face moves down onto it.

`indication = null` is only acceptable when your own visual *is* the pressed state. Otherwise keep the ripple, or replace it with a custom `IndicationNodeFactory`.

## 4. Depth

Hard offset shadow (neo-brutalist): draw the ink shape behind, then translate it on press.

```kotlin
fun Modifier.hardShadow(offset: Dp, radius: Dp, ink: Color, stroke: Dp) = this
    .drawBehind {
        val o = offset.toPx()
        drawRoundRect(ink, topLeft = Offset(o, o), size = size, cornerRadius = CornerRadius(radius.toPx()))
    }
    .border(stroke, ink, RoundedCornerShape(radius))
```

Soft tinted elevation (warm premium): use `Modifier.shadow(elevation, shape, ambientColor = primary.copy(.15f), spotColor = primary.copy(.25f))`. Tint it with a brand colour, not black.

Shape morphing (M3 Expressive / playful): `androidx.graphics.shapes` `RoundedPolygon` + `Morph` for pressed or selected shapes (e.g. square → cookie). Available on Android. On CMP, check availability, and fall back to animating the corner radius.

## 5. Motion

Use springs for spatial moves. The M3 Expressive tokens are spatial default (damping 0.8, stiffness 380), fast (0.6, 800) and slow (0.8, 200). Never bounce colour or alpha changes; use damping 1.0 for those.

```kotlin
val scale by animateFloatAsState(if (done) 1f else 0.9f, spring(dampingRatio = 0.6f, stiffness = 800f))
AnimatedContent(targetState = streak, transitionSpec = {
    (slideInVertically { -it } + fadeIn()) togetherWith (slideOutVertically { it } + fadeOut())
}) { Text("$it", style = MaterialTheme.typography.displayLarge) }
```

- **Reduce motion:** Android's "Remove animations" scales animator durations to 0, and Compose honours it through `MotionDurationScale`. Infinite or looping animations and `basicMarquee` still need a manual check. Read the setting on Android with `Settings.Global.getFloat(contentResolver, Settings.Global.ANIMATOR_DURATION_SCALE, 1f) == 0f`. On iOS (CMP), read `UIAccessibilityIsReduceMotionEnabled()` via `expect/actual` (see §9).
- Shared elements: `SharedTransitionLayout` + `Modifier.sharedElement(...)` for list → detail.
- Lottie or Rive for character animation (playful). Pause it under reduce motion, and keep it out of high-frequency paths.

### Custom glyphs, draw-on and ambient life

Draw the core verb's glyph yourself, and animate it with a path trim:

```kotlin
@Composable fun DrawOnCheck(done: Boolean, color: Color, modifier: Modifier = Modifier, reduceMotion: Boolean = false) {
    val progress by animateFloatAsState(
        if (done) 1f else 0f,
        if (reduceMotion) snap() else tween(220, easing = FastOutSlowInEasing), label = "check")
    val pop by animateFloatAsState(if (done) 1f else 0.6f, spring(dampingRatio = 0.45f, stiffness = 600f), label = "pop")
    Canvas(modifier.size(28.dp).graphicsLayer { scaleX = pop; scaleY = pop }) {
        val path = Path().apply {                          // chunky, slightly asymmetric tick
            moveTo(size.width * .18f, size.height * .54f)
            lineTo(size.width * .42f, size.height * .76f)
            lineTo(size.width * .84f, size.height * .26f)
        }
        val measure = PathMeasure().apply { setPath(path, false) }
        val partial = Path().also { measure.getSegment(0f, measure.length * progress, it, true) }
        drawPath(partial, color, style = Stroke(width = size.width * .14f, cap = StrokeCap.Round, join = StrokeJoin.Round))
    }
}
```

- **Glyph families:** build icons as `ImageVector` with `ImageVector.Builder` / `materialPath` (or draw them in `Canvas`) and keep stroke width, caps and corner rounding identical across the set.
- **Ambient loops** (blink, breathe, flicker) use `rememberInfiniteTransition()`. Guard every one with the reduce-motion flag and render a static frame instead:

```kotlin
val breathe = if (reduceMotion) 1f else rememberInfiniteTransition(label = "idle")
    .animateFloat(1f, 1.03f, infiniteRepeatable(tween(1200, easing = FastOutSlowInEasing), RepeatMode.Reverse), label = "b").value
```

- **Staggered entrance:** keep a `visible` flag per item, set from `LaunchedEffect(Unit)` with `delay(index * 40L)`, and wrap each item in `AnimatedVisibility(enter = scaleIn(spring(0.6f)) + fadeIn())`. Do this only on first load, not on every recomposition.
- **Particles:** a `Canvas` drawing N small shapes whose positions come from one `Animatable(0f → 1f)`, which is cheap and needs no library.
- **Rive / Lottie:** use `rive-android` or Lottie Compose on Android. On CMP, wrap the native views per platform or use Compottie (Lottie for Compose Multiplatform).

## 6. Haptics

```kotlin
val haptics = LocalHapticFeedback.current
haptics.performHapticFeedback(HapticFeedbackType.Confirm)   // Compose 1.8+; LongPress/TextHandleMove on older
```

For richer Android haptics use `View.performHapticFeedback(HapticFeedbackConstants.CONFIRM)`. On CMP iOS, `LocalHapticFeedback` maps to UIKit feedback generators.

## 7. Layout

- **Edge-to-edge is mandatory** when targeting SDK 35+. Call `enableEdgeToEdge()` and let `Scaffold` hand you `innerPadding`. For custom screens use `Modifier.windowInsetsPadding(WindowInsets.safeDrawing)`, and `imePadding()` on forms.
- Pin the bottom CTA with `Scaffold(bottomBar = { … })` plus `navigationBarsPadding()`.
- Targets: M3 components enforce 48 dp via `minimumInteractiveComponentSize()`. Add it to custom clickables too.
- **Back:** use `BackHandler` only to close your own sheet, search or selection mode. Predictive back is on by default for apps targeting API 36, so use `PredictiveBackHandler` if you animate the dismissal. Don't put horizontal swipe content flush against the screen edges, because both edges are back gestures.
- Large text: use `FlowRow` / `FlowColumn`, or switch `Row` → `Column` when `LocalDensity.current.fontScale > 1.3f`.

## 8. Semantics for custom controls

```kotlin
Modifier
    .toggleable(value = on, role = Role.Switch, onValueChange = { on = it })
    .semantics { contentDescription = "Notifications" }
```

- Hide decorative images and mascots: `contentDescription = null`.
- Merge stat tiles into one element: `Modifier.semantics(mergeDescendants = true) {}`.
- State in text, not only colour: `stateDescription = "Completed"`.

## 8b. Code baseline (what users feel)

A bold screen that janks reads as broken (Tuch et al. 2012). These rules cover only what's visible: smooth scrolling, steady animation, state that survives. Sources and the full list of 20 are in `../research/code-baseline.md`; rules 13–14 come from compile failures in our own evals. Where third-party skills disagree, the official docs win.

1. **Stable keys in lazy lists:** `items(rows, key = { it.id }, contentType = { it.kind })`. Never an index. That's what makes `Modifier.animateItem()` and per-row saved state work.
2. **Reserve space for async content:** images get a fixed size or `aspectRatio` plus a placeholder, so rows don't jump.
3. **One scroll container per axis:** no `LazyColumn` inside `verticalScroll`. Put headers in as `item {}`.
4. **Cheap composable bodies:** sort, filter and format in the ViewModel or in `remember(input) {}`.
5. **`derivedStateOf` only to turn fast state into slower state** (scroll index → show FAB). Use `remember(keys)` for mapping parameters.
6. **Defer fast reads into lambda modifiers:** `Modifier.offset { … }`, `drawBehind {}`, `graphicsLayer { scaleX = s }`. Animate transforms and alpha, not size, padding or `offset(dp)`. This is what keeps press squish and ambient loops at 60/120 fps.
7. **Don't chase stability by reflex.** Strong skipping is the default (Kotlin 2.0.20+). Check Layout Inspector recomposition counts before adding `@Stable` or `ImmutableList`.
8. **Choose each state's lifespan on purpose:** `remember` for transient UI; `rememberSaveable` for anything the user did (typed text, selection, tab, expanded); ViewModel + `SavedStateHandle` for screen state that must survive process death. Save IDs, not objects.
9. **Text fields use the state-based API:** `TextField(state = rememberTextFieldState())`. No dropped characters or cursor jumps, and it survives rotation. This needs Material 3 1.4 (Compose Multiplatform: `org.jetbrains.compose.material3:material3:1.9.0` or later; the `compose.material3` accessor in CMP 1.9.0 still pins the older 1.8.2). On an older Material 3, use `value`/`onValueChange` with `rememberSaveable` and say so.
10. **`collectAsStateWithLifecycle()`** for flows (common code via `org.jetbrains.androidx.lifecycle`). Hoist state: the screen collects, children get values and lambdas, and the ViewModel is never passed down.
11. **Preview every state** (loading, empty, error, longest real string) with fake `UiState` and `@PreviewLightDark` / `@PreviewFontScales`.
12. **Judge smoothness in a release build (R8) on a real device**, and ship a Baseline Profile for startup and the main scroll. CMP: the iOS side needs Instruments on a release framework, and `CADisableMinimumFrameDurationOnPhone = YES` in Info.plist for 120 Hz.
13. **Compile before you hand over.** With a Gradle project, `./gradlew :<module>:compileKotlin` (CMP: the `compileKotlinIosSimulatorArm64` and Android compile tasks) must pass. Without one, run `scripts/compile_kotlin.py` on the files you wrote. Only if neither can run, say "Kotlin not compiled" in the report.
14. **Import transition extensions explicitly.** `infiniteTransition.animateFloat(…)`, `animateDp`, `animateValue` (`androidx.compose.animation.core`) and `animateColor` (`androidx.compose.animation`) are extension functions with their own imports; importing `animateFloatAsState` doesn't bring them in. `rememberSaveable` is in `androidx.compose.runtime.saveable`. These two caused most of the compile failures in our evals; `lint.py` fails both.

**Companion skill:** for deeper Compose and CMP correctness, suggest that users install [aldefy/compose-skill](https://github.com/aldefy/compose-skill) (MIT): `/plugin marketplace add aldefy/compose-skill`. Where it conflicts with the rules above (stability/`ImmutableList`, CMP `rememberSaveable`), these rules win.

## 9. Compose Multiplatform specifics

One shared UI is fine. Make the brand layer common. Branch the *mechanics* where iOS users would notice:

```kotlin
// commonMain
expect val isIos: Boolean
expect fun reduceMotionEnabled(): Boolean

// iosMain
actual val isIos = true
actual fun reduceMotionEnabled() = platform.UIKit.UIAccessibilityIsReduceMotionEnabled()
```

- **Back affordance:** on iOS, show a top-left back chevron in your top bar (there is no system back button), and keep edge-swipe enabled. Compose Navigation on CMP iOS supports the swipe in recent versions; verify it on your version. On Android, rely on system back.
- **Sheets:** M3 `ModalBottomSheet` works on both. On iOS, consider medium/large detent-like sizing, and drag-to-dismiss is expected.
- **Pickers and date inputs:** M3 pickers on Android. On iOS, consider `UIKitView` wrapping `UIDatePicker` if the M3 look feels foreign at your `FIDELITY` level.
- **Text scaling on iOS:** CMP maps the iOS content-size category into `fontScale`. Check it at the largest accessibility size, because some versions cap or skip it, so verify on device.
- **Fonts:** load from `composeResources`. Ship OFL fonts so the same face renders on both platforms.
- **Ripples on iOS** look Android-ish. At `FIDELITY` ≤ 5, replace the ripple with a press-scale/opacity indication on iOS.
