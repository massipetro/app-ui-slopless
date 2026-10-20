# macOS implementation patterns (SwiftUI, with AppKit where SwiftUI stops)

How to turn a design brief into a Mac app that looks owned and still behaves like a Mac app. Read `platform-swiftui.md` first: tokens, press states, motion, and the code baseline (§8b) apply unchanged. This file covers what differs on a Mac. Copy the shapes of these snippets, not their values. Targets macOS 14+ with notes for macOS 15 and 26; read the real target from the project (rule 9).

A Mac app is used for hours, with a pointer and a keyboard, in a window the user resizes. Everything below follows from that.

## Contents
1. What changes from iOS
2. Window anatomy: sidebar, content, inspector
3. Toolbars and window chrome
4. Pointer: hover, cursor, click targets
5. Keyboard, menus and commands
6. Density and type (no Dynamic Type)
7. Colour, materials and vibrancy
8. Motion and feedback
9. Code baseline for macOS
10. Beyond the main window: settings, menu bar extras, multiple windows
11. Accessibility

---

## 1. What changes from iOS

| iOS rule | On macOS |
|---|---|
| Thumb zone, primary action low (R-TOUCH-1/2) | Pointer and keyboard. Primary actions live in the toolbar, the content, or a keyboard shortcut. Nothing is "low for reach". |
| 44 pt targets | A standard control is 22 pt tall (regular), 28 pt (large). Hover and click precision are high. Keep ≥ 24×24 pt (WCAG 2.5.8) and give small icon buttons a larger `contentShape`. |
| Tab bar, 3-5 destinations | Sidebar, or toolbar segmented control for 2-4 views. Sidebars hold many items. |
| Dynamic Type | None. Text styles are fixed sizes; the user zooms with the system or your own zoom command. |
| One screen at a time | Several panes visible at once; the window is resizable, with a minimum and no maximum. |
| Tap | Click, double-click, right-click (context menu), drag, hover, scroll, trackpad gestures. |
| Haptics | Rare: trackpad haptics only for alignment and snapping (`NSHapticFeedbackManager`). Sound is quieter than on a phone. |
| Sheets slide up | Sheets drop from the title bar; popovers anchor to a control; alerts are modal windows. |

Do **not** ship an iPhone layout in a bigger window. The test: shrink the window to its minimum and stretch it to a full 5K display; both must look composed, not scaled.

## 2. Window anatomy: sidebar, content, inspector

Use `NavigationSplitView` as the skeleton. It gives the standard sidebar behaviour, collapse, and resize for free.

```swift
struct RootView: View {
    @State private var selection: Voyage.ID?
    @State private var showInspector = true

    var body: some View {
        NavigationSplitView {
            Sidebar(selection: $selection)
                .navigationSplitViewColumnWidth(min: 200, ideal: 240, max: 320)
        } detail: {
            VoyageDetail(id: selection)
                .inspector(isPresented: $showInspector) {               // macOS 14+
                    VoyageInspector(id: selection)
                        .inspectorColumnWidth(min: 240, ideal: 280, max: 360)
                }
        }
        .frame(minWidth: 820, minHeight: 520)                          // always set a minimum
    }
}
```

- **Sidebar:** `List(selection:)` with `Section`s, `Label` rows and `.listStyle(.sidebar)`. Selection state is the system's; restyle it with `.tint` and `listRowBackground`, but keep the sidebar translucent unless the direction demands otherwise (see §7).
- **Content width:** cap reading text at 45-75 characters (R-VIS-2). In a wide window, centre a column with `.frame(maxWidth: 680)` rather than stretching text across 1800 pt.
- **Inspector** for properties of the selection, never for primary content. It toggles from the toolbar and a shortcut (⌥⌘I).
- **Grids and lists adapt:** `LazyVGrid(columns: [GridItem(.adaptive(minimum: 220))])` so a wider window shows more columns, not bigger tiles.
- **Resizing contract:** set `.frame(minWidth:minHeight:)` on the root; save the window frame (the system does it for `WindowGroup`); test at the minimum size and at full screen.
- **Information density:** a Mac list shows 15-30 rows, not 4. A phone-style card list with 8 pt gaps and 20 pt radii wastes the screen and is the commonest sign of an iOS port.

## 3. Toolbars and window chrome

```swift
.toolbar {
    ToolbarItem(placement: .navigation) { SidebarToggle() }
    ToolbarItemGroup(placement: .primaryAction) {
        Button { newVoyage() } label: { Label("New Voyage", systemImage: "plus") }
            .keyboardShortcut("n")
        Toggle(isOn: $showInspector) { Label("Inspector", systemImage: "sidebar.trailing") }
    }
}
.navigationTitle(voyage.name)
.navigationSubtitle("Departs 21:00")
```

- **Primary action goes in the toolbar** (`.primaryAction`), with a keyboard shortcut and a menu command. An in-content "big CTA" belongs to empty states and onboarding only.
- **Icon-only toolbar buttons need `Label`** (title + icon) so the text shows in "Icon and Text" mode and in VoiceOver and tooltips (`.help("New voyage")`).
- **Title bar:** `.windowStyle(.hiddenTitleBar)` or `.containerBackground(.thinMaterial, for: .window)` (macOS 15) when the direction's art runs under the title bar. Keep the traffic lights visible and clear of content (≈ 70 × 28 pt top-left). Custom title bars that hide them are a hard-requirement break (§11).
- **Window background:** `.containerBackground(for: .window) { Ink.surface }` (macOS 15) for a branded ground. On macOS 14 use `NSWindow.backgroundColor` via a small `NSViewRepresentable` that sets it on `viewDidMoveToWindow`.
- **Window size:** `WindowGroup { }.defaultSize(width: 980, height: 640).windowResizability(.contentMinSize)`.
- **Full-bleed hero art** goes behind the toolbar with `.ignoresSafeArea(edges: .top)` on the background only, as on iOS.

## 4. Pointer: hover, cursor, click targets

Every clickable thing needs a hover state. Hover is the Mac's "pressed-before-pressed", and it is the signifier that the element is live (R-COG-1).

```swift
struct HoverRow: ViewModifier {
    @State private var hovering = false
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    func body(content: Content) -> some View {
        content
            .padding(.horizontal, 8).padding(.vertical, 5)
            .background(RoundedRectangle(cornerRadius: 6).fill(hovering ? Ink.hover : .clear))
            .contentShape(Rectangle())                                  // the whole row is the target
            .onHover { hovering = $0 }
            .animation(reduceMotion ? nil : .easeOut(duration: 0.12), value: hovering)
    }
}
```

- **Button styles get three states**: rest, hover, pressed (`configuration.isPressed`), plus the focus ring for keyboard focus. Do not remove `.focusEffectDisabled()` unless you draw an equal replacement.
- **Cursor:** `.onHover { $0 ? NSCursor.pointingHand.push() : NSCursor.pop() }` for link-like controls only. Don't make every button a pointing hand; the Mac reserves it for links. Draggable edges use `resizeLeftRight`, draggable items `openHand`.
- **Right-click:** `.contextMenu { }` on every row and card that has actions. It is the Mac's long-press, and users will try it.
- **Double-click** opens or edits. Keep single-click = select.
- **Drag and drop:** `.draggable` / `.dropDestination` with the real transferable, and a visible drop target highlight. Support dragging files from Finder when files are the domain.
- **Scroll:** trackpad inertia and mouse wheels both work. Never hijack scroll for custom paging unless the direction is a canvas.
- **Tooltips:** `.help("…")` on icon-only controls. They appear after a hover delay and are the Mac's label of last resort.
- **Small targets are fine, but not tiny.** A 22 pt row is normal; a 14 pt icon button with no hover and no padding is not.

## 5. Keyboard, menus and commands

A Mac app without a menu bar and shortcuts feels like a web page in a frame.

```swift
@main
struct VoyageApp: App {
    var body: some Scene {
        WindowGroup { RootView() }
            .commands {
                CommandGroup(replacing: .newItem) {
                    Button("New Voyage") { Store.shared.newVoyage() }.keyboardShortcut("n")
                }
                CommandMenu("Voyage") {
                    Button("Mark as Boarded") { Store.shared.markBoarded() }
                        .keyboardShortcut("b", modifiers: [.command, .shift])
                    Divider()
                    Button("Show Timetable") { openTimetable() }.keyboardShortcut("t", modifiers: [.command, .option])
                }
            }
        Settings { SettingsView() }
    }
}
```

- **Standard shortcuts are not yours to reuse:** ⌘N, ⌘O, ⌘S, ⌘W, ⌘Q, ⌘,, ⌘Z/⇧⌘Z, ⌘X/C/V, ⌘A, ⌘F, ⌘P, ⌘M, ⌘H, ⌘`, ⌘⌥I (inspector). Keep their system meaning.
- **Every command in a menu**, with a shortcut for anything used daily. The menu bar is the discoverability layer (R-COG-5): users find features there before they find them anywhere else.
- **Return/Escape:** `.keyboardShortcut(.defaultAction)` on the primary button in a sheet or dialog, `.cancelAction` for Cancel. Escape dismisses popovers and sheets.
- **Focus:** Tab moves through controls in a sensible order, arrow keys navigate lists, Space triggers the focused button. Use `@FocusState` and `.focusable()` for custom controls, and `.onKeyPress` (macOS 14) for single keys (a calendar, a board, a player).
- **Undo:** reversible actions register with `UndoManager` (`@Environment(\.undoManager)`). This is the Mac's R-FORM-4: no confirmation dialogs for reversible actions.
- **Text fields:** a `TextField` is already labelled on the left in a `Form`; use `LabeledContent` or `Form { TextField("Name", text: $n) }.formStyle(.grouped)`. Placeholders are hints, never labels (R-FORM-1).

## 6. Density and type (no Dynamic Type)

macOS has no Dynamic Type. System text styles are fixed point sizes, so `.font(.system(size: 13))` is not a defect here, but a design system still needs a scale.

| Style | Size (pt) | Use |
|---|---|---|
| `.largeTitle` | 26 | Empty states, onboarding |
| `.title` / `.title2` / `.title3` | 22 / 17 / 15 | Window and section headers |
| `.headline` | 13 bold | Row titles |
| `.body` | 13 | Default text; this is the Mac's 17 pt |
| `.callout` | 12 | Secondary |
| `.subheadline` / `.footnote` | 11 | Metadata |
| `.caption` / `.caption2` | 10 | Smallest allowed; never for primary content |

- **Body is 13 pt, not 17.** Port a phone scale unchanged and the app looks enlarged and sparse. A display moment (R-VIS-1) is still wanted: set one number or heading at 40-96 pt; the rest stays at 11-15.
- **Custom fonts** still use one display face + one text face (R-VIS-4). `.custom("Name", size: 13, relativeTo: .body)` is harmless on macOS and keeps one code path; `relativeTo` simply has no scaling effect. Register fonts under `ATSApplicationFontsPath` in Info.plist, or with `CTFontManagerRegisterFontsForURL`.
- **Monospaced digits** for any changing number: `.monospacedDigit()`.
- **Row heights:** 22-28 pt for dense lists, 32-44 pt for comfortable ones, via `.environment(\.defaultMinListRowHeight, 28)`. `controlSize(.small/.regular/.large)` changes all control heights consistently.
- **Offer zoom for content-heavy apps:** a ⌘+ / ⌘− / ⌘0 command that scales a `@AppStorage("zoom")` factor applied through `.environment(\.dynamicTypeSize, …)` on your own text, or a `scaleEffect` for canvases. Accessibility for low-vision users on macOS is system zoom plus your own zoom.

## 7. Colour, materials and vibrancy

- **Light and dark are both first-class**, and so is **accent colour**: users set a system accent and expect controls to follow it. Decide deliberately: follow it (`Color.accentColor`) for standard controls and use your brand colour for the owned idea and key surfaces, or set `.tint(Ink.primary)` app-wide and say so in the brief.
- **Dynamic colours:** asset-catalog colours, or in code:

```swift
extension Color {
    init(light: NSColor, dark: NSColor) {
        self.init(nsColor: NSColor(name: nil) { $0.bestMatch(from: [.darkAqua, .aqua]) == .darkAqua ? dark : light })
    }
}
```

- **Materials:** sidebars and inspectors are translucent (vibrancy) on purpose: they show the desktop's tint behind the window and mark the chrome layer. In **warm premium** and **editorial** keep the system sidebar material and put the brand in the content pane. In **neo-brutalist** replace it with an opaque tone and a hard divider, and note it as a convention break (§ Breaking conventions in SKILL.md). `lint.py`'s `glass` rule is demoted on macOS for `.sidebar`/`.windowBackground` materials.
- **Semantic colours** (`Color(nsColor: .labelColor)`, `.secondaryLabelColor`, `.separatorColor`, `.controlBackgroundColor`) adapt to contrast settings. Hard-coded greys do not, and they also fail the `default-grey` lint.
- **Selection colour:** the system draws selection in the accent colour (blue by default), greying out when the window is inactive. A custom selection background must also dim when `controlActiveState != .key`.
- **Inactive windows** (`@Environment(\.controlActiveState)`): dim toolbar icons and selections slightly; a whole app that looks identical when inactive feels off.
- **Increase contrast / Reduce transparency:** `@Environment(\.colorSchemeContrast)` and `accessibilityReduceTransparency`. Swap material for an opaque fill when set.

## 8. Motion and feedback

- Keep durations short: 120-220 ms for hover and press, 250-350 ms for layout. Mac users repeat actions hundreds of times; a 500 ms bounce on a frequent action is a defect (R-EMO-3).
- Springs work as on iOS (`platform-swiftui.md` §5). Respect `accessibilityReduceMotion`, and note that the Mac's setting is "Reduce motion" in Accessibility > Display.
- **Window and sheet transitions belong to the system.** Don't animate the window frame yourself except for a deliberate hero (a mini player expanding), and then use `NSWindow.animator()` or `.windowResizability`.
- **Sound** is optional and short; honour the system's alert volume and offer a toggle.
- **Progress:** a determinate `ProgressView(value:)` in the toolbar or status bar for long work, with Cancel; Dock icon badge or `NSApp.dockTile.badgeLabel` for background counts.
- **Drag feedback:** the dragged item follows the pointer 1:1 (R-TOUCH-4) with a drop highlight and a spring-back on a cancelled drop.

## 9. Code baseline for macOS

Rules 1-16 of `platform-swiftui.md` §8b hold. Additions and replacements:

1. **Per-window state with `@SceneStorage`**, and app-wide state in an `@Observable` store passed with `.environment`. Each window gets its own selection; two windows must not fight over one global.
2. **Large collections use `Table` (sortable columns) or `List`**, not `ScrollView { VStack }`. Give rows stable ids and `selection:`. `Table` is the right shape for data (R-VIS-7 applies to its chart cousins).
3. **Never block the main thread.** File I/O, parsing and image decoding run off-main; a spinning beachball is the Mac's worst failure. Downsample images to display size, and use `NSImage`/`CGImage` thumbnails with `ImageIO` for big files.
4. **Platform branching without `#if` sprawl:** keep shared views platform-neutral and isolate AppKit bridging in small `NSViewRepresentable` wrappers. Guard with `#if os(macOS)` / `#if canImport(AppKit)` at the file or type level; do not scatter `#if` through bodies.
5. **Bridge sparingly.** Prefer SwiftUI (`TextEditor`, `Table`, `Canvas`, `inspector`, `MenuBarExtra`) before `NSViewRepresentable`. When bridging (an `NSTextView` for rich text, an `NSOutlineView` for a huge tree, a `WKWebView`), keep the representable small, forward bindings in `updateNSView` without feedback loops, and own the `Coordinator`.
6. **Type-check expression size** (rule 16) applies equally; huge `Table` column builders are a common cause.
7. **Deployment target:** read `MACOSX_DEPLOYMENT_TARGET` or `platforms: [.macOS(...)]` and use newer APIs only behind `if #available(macOS N, *)`: macOS 14 `inspector`, `@Observable`, `onKeyPress`, `Table` improvements; macOS 15 `containerBackground(for: .window)`, `WindowDragGesture`, `windowResizability` refinements; macOS 26 `glassEffect()` and the scroll-edge effect. With no declared target, use macOS 14. Never raise the target to clear an availability error (`typecheck.py --macos` reports it).
8. **App Sandbox and entitlements:** file access goes through `fileImporter`/`fileExporter` or security-scoped bookmarks; do not hard-code paths. Mention required entitlements in the report if the design needs them (network client, user-selected files).

## 10. Beyond the main window

- **Settings** (`Settings { }` scene, ⌘,): a `TabView` of panes with icons, `Form` + `.formStyle(.grouped)`. Controls apply immediately, with no Save button. Brand it lightly; this is system territory.
- **Menu bar extra** (`MenuBarExtra`): `.menuBarExtraStyle(.window)` for a custom popover. Keep it glanceable (R-NAV-5), ≤ 360 pt wide, one live number or state, and a template-style monochrome icon (`Image(systemName:)` or a template `NSImage`). This is where an owned idea can shine on a Mac: Flighty-style countdown in the menu bar. It must show the real state.
- **Multiple windows:** `WindowGroup(for: Voyage.ID.self)` plus `openWindow(value:)`. Detail windows are real windows with their own toolbars, not modal sheets.
- **Dock and notifications:** badge counts, `UNUserNotificationCenter` for deadlines, and `NSApp.dockTile` for a live state (rarely).
- **Widgets, Control Center and Shortcuts** carry the brand layer too: reuse tokens through a shared Swift package.

## 11. Accessibility

Hard requirements on macOS (breaking one gets a ⚠️ warning in the report, as with safe areas on iOS):
- **VoiceOver:** `accessibilityLabel` on every icon-only control, `accessibilityElement(children:)` grouping on composite rows, `.accessibilityAddTraits(.isButton)` on custom clickable shapes, and logical focus order. Test with VoiceOver (⌘F5) and navigate with the keyboard only.
- **Full keyboard access:** every action reachable without a pointer (Tab, arrows, Space/Return, menu commands). A custom control that only responds to clicks fails.
- **Contrast** (R-A11Y-1) in light, dark, and with Increase Contrast on. Check text over vibrancy against the worst wallpaper (composite first).
- **Reduce motion, Reduce transparency, Differentiate without colour** are all honoured.
- **Targets:** WCAG 2.5.8 (24×24 CSS px) is the floor; the Mac standard is a 22 pt control with generous padding and hover, not 44 pt.
- **Traffic lights and title bar** stay visible and clickable; the window remains movable by dragging an obvious area.
- **Text:** macOS has no Dynamic Type, so offer in-app zoom for content-heavy views (§6) and make sure the layout survives it without clipping.
