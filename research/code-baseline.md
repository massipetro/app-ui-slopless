# app-ui-slopless: code baseline research

This is the research behind the short "code baseline" section planned for `references/platform-compose.md` and `references/platform-swiftui.md`. It covers only the code practices a user can **see**: smooth scrolling, jank-free motion, state that survives rotation, process death and navigation, a responsive main thread, and previews that catch large-text and dark-mode breakage. Architecture, testing and style rules are out of scope.
Compiled 2026-10-18 from the repos below (shallow clones at HEAD on that date) and official docs.

**Verification tags** (same scheme as `literature.md`)
- **[V]**: checked this session against official docs (developer.android.com, kotlinlang.org, developer.apple.com).
- **[S]**: checked only against a skill repo that cites a primary source (for example a WWDC session), or against a secondary page.
- **[U]**: not verified this session. Treat it as a pointer, not a citation.

All rule text is paraphrased. Quotes are kept under 15 words. No text is copied from the repos.

**Already in the reference files, so not repeated here:** `@Preview(fontScale = 2f)` and `.dynamicTypeSize(.accessibility3)` previews, reduce-motion handling, edge-to-edge and safe-area insets, predictive back, haptics, `@ScaledMetric`, springs and motion tokens. The baseline should point to those sections, not restate them.

---

## 1. Repos reviewed

Stars and last push are from the GitHub API on 2026-10-18. Licences were read from each repo's `LICENSE` file.

| Repo | Licence (from LICENSE) | Focus | Verdict as a companion |
|---|---|---|---|
| [aldefy/compose-skill](https://github.com/aldefy/compose-skill) (`compose-expert` v2.4.0, ~600★, pushed 2026-07) | **MIT** (© 2026 Adit Lal). Bundled AOSP source excerpts in `references/source-code/` are **Apache-2.0**, which is why GitHub shows "NOASSERTION". | The broadest Compose skill: state, side effects, performance, lists, animation, navigation 2 and 3, Paging, Material 3 and M3 Expressive, CMP (iOS, Desktop, Web), TV, PR-review mode and a crash playbook. It bundles androidx source excerpts and has a claim-verification Gradle module. | **Yes, with caveats.** It is the best depth and CMP coverage available. But I found errors in exactly this baseline's area: it says `rememberSaveable` is Android-only in CMP (it is common code); it pushes `ImmutableList` for stability, which the official stability page now discourages under strong skipping; it shows `derivedStateOf` wrapped in `remember(items, query)` for plain filtering (a misuse); its strong-skipping config snippet is outdated; its CMP notes on `collectAsStateWithLifecycle` contradict each other; and one `graphicsLayer` example uses the non-lambda form. Where they disagree, the baseline below wins. |
| [anhvt52/jetpack-compose-skills](https://github.com/anhvt52/jetpack-compose-skills) (`modern-jetpack-compose` v1.0, ~100★, pushed 2026-03) | **MIT** (© 2026 Anh Vu) | A compact review checklist (11 short refs) for state, effects, recomposition, navigation, M3, accessibility and performance, with before/after output. Its structure mirrors SwiftUI Pro. | **Optional, lightweight alternative.** Mostly correct and easy to read. Some advice is dated: it says to `remember` lambdas, to use `ImmutableList`, and never to use `mutableStateOf` in a ViewModel, which is stricter than Google. It has no CMP coverage and looks unmaintained since March. |
| [hamen/material-3-skill](https://github.com/hamen/material-3-skill) (v1.1.1, ~1.5k★, pushed 2026-07) | **MIT** (© 2026 CWTI Ltd) | The Material Design 3 system: tokens, 30+ components, theming and dynamic colour, adaptive layout, M3 Expressive, Flutter and web notes, and an MD3 compliance audit. | **No.** It is a design-system skill, not a code baseline, and it has almost no performance or state content. It treats Roboto, dynamic colour and "MD3 compliance" as defaults, which fights the slopless presets where the palette and type *are* the identity. It also still shows the deprecated `calculateWindowSizeClass`. |
| [twostraws/swiftui-agent-skill](https://github.com/twostraws/swiftui-agent-skill) (SwiftUI Pro v2.0.0 by Paul Hudson, ~6.2k★, pushed 2026-10-16) | **MIT** (© 2026 Paul Hudson) | A concise review skill with 12 short refs: deprecated API, views, data flow, navigation, HIG design, resizability (iPhone Duo), accessibility, localization, performance (plus an opt-in "performance-plus"), Swift and hygiene. It knows Xcode 27 and iOS 27, and gates advice on the deployment target. | **Yes, the primary SwiftUI companion.** It is tight, current and precise about identity, Observation dependencies and `ForEach` row shape, and it sticks to code quality without dictating visual style. It defaults to iOS 27 for *new* apps, so tell it the real deployment target (iOS 17+). |
| [avdlee/swiftui-agent-skill](https://github.com/avdlee/swiftui-agent-skill) (`swiftui-expert-skill` by Antoine van der Lee, ~3.7k★, pushed 2026-10-06) | **MIT** (© 2026 Antoine van der Lee) | Broad coverage (34 refs): state, environment, view structure, performance, lists, scroll, animation, previews, images, Liquid Glass, macOS and iPhone Duo. Includes Python scripts to record and analyse Instruments `.trace` files. Many rules cite WWDC23 and WWDC25 sessions. | **Yes, as the alternative or as the profiling tool.** It has the best "why is this view updating" tooling and good WWDC sourcing. It overlaps heavily with SwiftUI Pro, so install one of the two by default. Its "adopt Liquid Glass only when asked" rule is compatible with slopless §9. |
| [dpearson2699/swift-ios-skills](https://github.com/dpearson2699/swift-ios-skills) (~1.2k★, pushed 2026-07) | **PolyForm Perimeter 1.0.0** (source-available, **not** OSI open source; its noncompete clause bars use in any product that competes with it) | A large collection of iOS 26+ / Swift 6.3 skills with evals. The relevant ones are `swiftui-performance` (evidence-first triage, Instruments lanes, lazy-container guardrails), `swiftui-patterns` (Observation ownership, preview isolation), `swiftui-animation`, `swiftui-layout-components` and `swiftui-navigation`. | **No for bundling or adapting; fine for personal use.** The quality is high, especially the "hypothesis until a trace confirms" discipline. The licence makes it unsafe to adapt into a distributed skill, and app-ui-slopless could arguably count as a competing product. It was used here only to cross-check coverage, and no content was derived from it. Users may install it themselves. |
| [Wholiver/swiftui-design-skill](https://github.com/Wholiver/swiftui-design-skill) (v1.0.0, ~210★, pushed 2026-05) | **MIT** (© 2026 wholiver) | SwiftUI *visual design*: six anti-slop rules, a design-direction workflow, brand-spec template, layout, type and colour, and a five-dimension review. It sends performance questions to swiftui-expert-skill. | **No.** It overlaps directly with app-ui-slopless, so the two would compete for the same triggers. It has almost no code-baseline content (a `LazyVStack` hint and `@ScaledMetric`). |
| [FloWritesCode/fwc-swiftui-skills](https://github.com/FloWritesCode/fwc-swiftui-skills) (~430★, pushed 2026-10-08) | **MIT** (© 2026 FloWritesCode) | Two niche skills: `swiftui-liquid-glass` (iOS 26 native glass APIs, `GlassEffectContainer`, `safeAreaBar`, no glass inside scrolling rows, no pre-enclosed symbols) and `swiftui-iphone-duo` (Xcode/iOS 27.1 adaptive layout and hinge APIs). | **Situational yes.** It is not a code baseline. The Liquid Glass skill pairs well with slopless §9 for the warm-premium and editorial presets, and the Duo skill matters only if the app targets iOS 27.1. |

---

## 2. Compose code baseline

Targets Compose 1.7+ / CMP 1.7+ (the current Compose BOM). **Source keys:** [D-perf](https://developer.android.com/develop/ui/compose/performance) · [D-best](https://developer.android.com/develop/ui/compose/performance/bestpractices) · [D-stab](https://developer.android.com/develop/ui/compose/performance/stability) · [D-phases](https://developer.android.com/develop/ui/compose/phases) · [D-lists](https://developer.android.com/develop/ui/compose/lists) · [D-save](https://developer.android.com/develop/ui/compose/state-saving) · [D-life](https://developer.android.com/develop/ui/compose/state-lifespans) · [D-hoist](https://developer.android.com/develop/ui/compose/state-hoisting) · [D-text](https://developer.android.com/develop/ui/compose/text/user-input) · [D-bp](https://developer.android.com/topic/performance/baselineprofiles/overview) · [D-prev](https://developer.android.com/develop/ui/compose/tooling/previews) · [K-life](https://kotlinlang.org/docs/multiplatform/compose-lifecycle.html) · [K-prev](https://kotlinlang.org/docs/multiplatform/compose-previews.html) · A1 = aldefy · A2 = anhvt52.

**Measure honestly**
1. **Judge smoothness only in a release build with R8 on, on a real device.** Debug Compose is much slower, so jank seen there means little. — [D-perf V] A1, A2
2. **Ship an app-specific Baseline Profile** covering startup and the main scroll and navigation journeys. Compose ships a default profile; Google cites about 30% faster code from first launch. `./gradlew :app:generateBaselineProfile` — [D-bp V, D-perf V] A1, A2. *CMP:* Android only. On iOS, profile a **release** framework in Instruments, because Kotlin/Native debug binaries are unoptimised [U].
3. **Find hot spots before "fixing stability".** Strong skipping is the default since Kotlin 2.0.20: unstable parameters are compared by instance, so skipping already works. Don't reflexively wrap lists in `ImmutableList` or add `@Stable` everywhere. Look at Layout Inspector recomposition counts first, then the compiler stability reports. — [D-stab V] (A1 and A2 still give the older `ImmutableList` advice.)

**Smooth lists**
4. **Give every lazy item a stable, unique key of a Bundle-able type.** Never use an index or a random value. It keeps per-item `rememberSaveable` state and makes `Modifier.animateItem()` work. `items(rows, key = { it.id }) { … }` — [D-lists V, D-best V] A1, A2
5. **Mixed lists declare a `contentType`**, so compositions are reused only between rows of the same type. `contentType = { it.kind }` — [D-lists V] A1, A2
6. **Reserve space for async content.** A 0-px row that grows when its image loads makes the list compose everything, then jump. Give images a fixed size or `aspectRatio` and a placeholder. — [D-lists V]
7. **Use one scroll container per axis.** No `LazyColumn` inside `verticalScroll`. Fold headers and sections into the same `LazyColumn` with `item {}`. — [D-lists V] A1

**Jank-free frames**
8. **Keep the composable body cheap.** Sort, filter and format in the ViewModel, or at least in `remember(input) { … }`, never inline on each recomposition. — [D-best V] A1, A2
9. **Use `derivedStateOf` only to turn fast state into a slower result**, for example scroll position into show/hide FAB: `val showFab by remember { derivedStateOf { list.firstVisibleItemIndex > 0 } }`. For mapping plain parameters use `remember(keys)`. — [D-best V] A2 (A1's filtering example misuses it.)
10. **Defer high-frequency reads into lambda modifiers**, so scroll- or animation-driven changes skip composition: `Modifier.offset { IntOffset(0, scroll()) }`, `drawBehind { … }`. Pass `() -> Int` providers down instead of raw values. — [D-best V, D-phases V] A1, A2
11. **Animate transforms and alpha in the `graphicsLayer {}` lambda, not size, padding or `offset(dp)`.** `Modifier.graphicsLayer { scaleX = s; scaleY = s; alpha = a }` with `s` and `a` from `animateFloatAsState` (`by` delegates), so the read happens at draw time. — [D-phases V for the principle; lambda-form guidance S via the API KDoc and A2] A1
12. **Never write state that was already read earlier in the same composition** (a "backwards write"). It loops recomposition forever. Write state only in event callbacks. — [D-best V]

**State that survives**
13. **Pick each state's lifespan on purpose.** Use `remember` for transient UI such as animation helpers. Use `rememberSaveable` for anything the user did: typed text, selection, tab, expanded, scroll. Use `retain` (Compose 1.10+) for non-saveable objects that must survive rotation, such as a player or cache. Use the ViewModel for screen state, and `SavedStateHandle` for business state that must survive process death. User input in plain `remember` is lost on rotation. — [D-save V, D-life V] A1, A2
14. **Save IDs, not objects.** Saved state goes into a size-limited `Bundle`, and large lists cause `TransactionTooLargeException`. Restore the ID, then reload from the data layer. Don't `retain` a Context, Activity or View. — [D-save V, D-life V]
15. **Use `rememberSerializable` for `@Serializable` types** (runtime-saveable 1.11, common source set) instead of hand-writing a `Saver`. This is handy in CMP, where `@Parcelize` isn't available. — [D-life V, S for the version] *CMP:* `rememberSaveable` works in common code. Whether saved state survives an iOS app being terminated is not documented [U], so test it.
16. **Text fields use the state-based API:** `TextField(state = rememberTextFieldState())`. It survives configuration change and process death, and removes the async `onValueChange` round-trip that causes dropped characters and cursor jumps. — [D-text V for save/restore and the async rationale; U for the symptom wording]
17. **Collect flows with `collectAsStateWithLifecycle()`**, so hidden screens stop collecting. — [D-hoist V] A2. *CMP:* available in `commonMain` through `org.jetbrains.androidx.lifecycle:lifecycle-runtime-compose`; reportedly 2.8+, so check your version [S]. iOS lifecycle events map onto `ON_START`/`ON_STOP` etc. [K-life V]. Otherwise fall back to `collectAsState()`.
18. **Hoist state.** The screen composable collects state and passes values and lambdas to stateless children. Never pass the ViewModel down. Hoist `LazyListState` to where it's shared. Run `animateScrollToItem` and other UI suspend calls in a composition-scoped coroutine: from `viewModelScope` they throw. — [D-hoist V] A1, A2
19. **When the layout changes with window size, fold posture or rotation**, keep stateful composables at a stable call site, or move them with `movableContentOf`. Otherwise scroll position and input reset on the switch. — [D-life V] A1

**Previews**
20. **Preview the stateless screen with fake `UiState`** in every meaningful state (loading, empty, error, longest real string), stacked with `@PreviewLightDark`, `@PreviewFontScales` and `@PreviewScreenSizes`. This complements §2's `fontScale = 2f` tip. — [D-prev V] A1. *CMP:* from CMP 1.10 the AndroidX `@Preview` is multiplatform and the JetBrains one is deprecated [K-prev S]. Whether the multipreview annotations render from `commonMain` is unverified [U].

**Other CMP caveats**
- For 120 Hz on ProMotion iPhones, CMP apps need `CADisableMinimumFrameDurationOnPhone = YES` in Info.plist. — A1 [U this session; the Info.plist key is Apple's]
- Baseline Profiles, Macrobenchmark and Layout Inspector are Android-only. iOS jank needs Instruments on a device. — A1 [S]

---

## 3. SwiftUI code baseline

Targets iOS 17+ with iOS 26 notes. **Source keys:** [AP-obs](https://developer.apple.com/documentation/swiftui/migrating-from-the-observable-object-protocol-to-the-observable-macro) · [AP-lazy](https://developer.apple.com/documentation/swiftui/creating-performant-scrollable-stacks) · [AP-state](https://developer.apple.com/documentation/swiftui/state) · [AP-scene](https://developer.apple.com/documentation/swiftui/scenestorage) · AP-task (`task(priority:_:)` / `task(id:priority:_:)` docs; the JSON wasn't fetchable this session) · W21 = WWDC21 "Demystify SwiftUI" · W23 = WWDC23 "Demystify SwiftUI performance" · W25 = WWDC25 "Optimize SwiftUI performance with Instruments" (306) and "What's new in SwiftUI" (256) · S1 = SwiftUI Pro (twostraws) · S2 = swiftui-expert-skill (avdlee) · S3 = dpearson2699 (cross-check only, nothing derived).

**Data flow and state**
1. **New models are `@Observable` (and `@MainActor`) classes.** The owning view holds `@State private var model = Model()`. Children take a plain `let`, use `@Bindable` when they need bindings, or read `@Environment(Model.self)`. Views then redraw only for properties their `body` reads. Avoid `ObservableObject` in new code. — [AP-obs V] S1, S2
2. **`@State` is always `private`, and never mirrors a parent-owned value.** A `@State var item` initialised from the parent keeps showing the first value forever. Use `let` or `@Binding`. With Xcode 27, `@State` becomes a macro, so seed it once in `init` and give the declaration no default. — [AP-state V for private and the Xcode 27 macro] S1, S2
3. **Make value types `Equatable` and skip no-op writes in hot callbacks** (`if new != current { current = new }`), so repeated identical values don't redraw. — S1, S2 [S]
4. **Keep per-window UI state (tab, selection, a Codable `NavigationPath`) in `@SceneStorage`**, so it comes back after the system kills the app. Store small values only. Don't use `@AppStorage` for it: two iPad windows would fight over it. — [AP-scene V] S1
5. **Navigate by value:** `NavigationStack(path:)` with `navigationDestination(for:)` registered once per type. Never mix it with `NavigationLink(destination:)` in one stack. Value paths are what make restoration and deep links possible. — S1, S2 [S]
6. **Present from data:** use `sheet(item:)` / `alert(_:item:)` rather than a Bool plus a separate optional, so the sheet never opens empty or stale. — S1 [S]

**Identity (smooth lists, animations that don't reset)**
7. **`ForEach` identity comes from the element:** `Identifiable` with a stored `id`. Never use `indices`, `\.offset`, `id: \.self` on large structs, or a `UUID()` made in `body`. Each of those resets row state and breaks insert and delete animations. — [AP-lazy V for unique ids] S1, S2; S3 agrees
8. **Each `ForEach` element yields the same number and kind of views.** Filter before the `ForEach`, and wrap conditional row content in a `VStack` (not `Group`). Otherwise SwiftUI evaluates every row to work out identity. Debug with the `-LogForEachSlowPath YES` launch argument. — W23 [S] S1, S2; S3 agrees
9. **Change modifier values, not view branches:** `.opacity(isHidden ? 0 : 1)` keeps one view identity, so state and animations survive. `if/else` swaps identity. Don't write a `.if {}` view helper. — W21 [S] S1; S3 agrees
10. **Avoid `AnyView` in rows and hot paths.** Use `@ViewBuilder`, generics or an extracted view. — W23 [S] S1, S2

**Scrolling and the main thread**
11. **Use `List` or a `LazyVStack` for long or unbounded feeds.** Apple's advice is to start with a plain stack and switch when profiling shows a gain. Lazy rows lose their `@State` when scrolled off, so keep row state in the model, and don't make `onAppear` the only setup point. *iOS 26:* lazy stacks nested in scroll views (e.g. a carousel in a feed) now defer loading too. — [AP-lazy V] W25 [S] S1, S2; S3 agrees
12. **Keep `init` and `body` trivial:** no sorting, filtering or formatter construction. Let `Text` format: `Text(date, format: .dateTime.day().month())`. — S1, S2 [S]; S3 agrees
13. **Load async work in `.task {}`**, which is cancelled when the view goes away. Use `.task(id: query)` to restart on input change; it replaces `onAppear { Task { … } }` and hand-made debounce state. — AP-task [U this session; long-standing documented behaviour] S1, S2
14. **Never block the main actor.** JSON parsing, image decoding and file I/O go off-main, and large images are downsampled to display size before rendering. These are the usual causes of hangs and scroll hitches. — S2, S3 [S]
15. **Give each row its element (`Row(item: item)`), not the store plus an id.** A row that looks itself up depends on the whole collection, so one change redraws every row. If rows change independently, give each its own `@Observable` model, created once. — W25 [S] S1, S2
16. **Keep fast-changing values (scroll offset, drag position, timer ticks) out of the environment and out of broad state.** For visual effects use `scrollTransition` or `visualEffect`, which don't re-run `body`. For logic, use `onScrollGeometryChange` (iOS 18) and threshold to a Bool. — W25 [S] S1, S2

**Motion**
17. **Animate transforms (`scaleEffect`, `offset`, `rotationEffect`, `opacity`), not `frame` or `padding`.** Attach `.animation(_:value:)` to the smallest subtree, and always pass `value:`. — S2, S1 [S]; S3 agrees
18. **Sequence animations with `withAnimation { … } completion: { … }`** (iOS 17), not `DispatchQueue` delays, which drift out of sync under load. — S1 [S]

**Previews and checking**
19. **Write one `#Preview` per meaningful state** (loading, empty, error, longest real string) with self-contained mock data and no network, plus the dark and AX-size variants from §7. Use `@Previewable @State` (iOS 18+) for interactive previews; below that, use a small wrapper view. — S2, S1 [S]; S3 agrees
20. **Profile a release build on a real device** with the Instruments SwiftUI template. Apple says never to profile in the simulator. Use `let _ = Self._printChanges()` (debug only) to see why a view redrew. — [AP-lazy V for device and template] S2, S3

---

## 4. Companion skills

**Compose.** Install **aldefy/compose-skill** (`compose-expert`) alongside app-ui-slopless for depth on lists, effects, navigation, Paging and especially Compose Multiplatform. Tell the agent that the slopless baseline (official docs) overrides it on stability, CMP `rememberSaveable` and `collectAsStateWithLifecycle`. Claude Code: `/plugin marketplace add aldefy/compose-skill` then `/plugin install compose-expert`. If you want only a lightweight review checklist, **anhvt52/jetpack-compose-skills** is the alternative: `npx skills add https://github.com/anhvt52/jetpack-compose-skills`. Skip hamen/material-3-skill, which would pull designs back toward stock MD3.

**SwiftUI.** Install **twostraws/swiftui-agent-skill** (SwiftUI Pro) as the default, and state the real deployment target, since it assumes iOS 27 for new apps. Claude Code: `/plugin marketplace add twostraws/SwiftUI-Agent-Skill` then `/plugin install swiftui-pro@swiftui-agent-skill`, or `npx skills add https://github.com/twostraws/swiftui-agent-skill --skill swiftui-pro`. Pick **avdlee/swiftui-agent-skill** instead of SwiftUI Pro (not on top of it, the two overlap heavily) if you want Instruments trace recording and analysis: `/plugin marketplace add AvdLee/SwiftUI-Agent-Skill` then `/plugin install swiftui-expert@swiftui-expert-skill`. For iOS 26 glass in the warm-premium or editorial presets, add `npx skills add FloWritesCode/fwc-swiftui-skills --skill swiftui-liquid-glass`. Don't recommend Wholiver (duplicate scope). Don't vendor or adapt dpearson2699 (PolyForm Perimeter); individuals may install it for their own use.

---

## 5. Notes for writing the reference-file sections

- Keep each platform's section to about 10–12 one-liners in the reference file, and leave the full list above for this research note. Strongest picks: Compose 1, 2, 4, 6, 9, 10, 11, 13, 16, 19, 20; SwiftUI 1, 2, 7, 8, 9, 11, 13, 14, 16, 17, 19.
- Point to existing sections instead of repeating them: Compose §2 (fontScale preview), §5 (reduce motion), §7 (insets, back); SwiftUI §2 (`@ScaledMetric`), §5 (reduce motion), §7 (AX preview).
- Where the official docs and the skills disagree (Compose stability and `ImmutableList`, CMP saveable), the official docs win. Section 1 notes each case.
