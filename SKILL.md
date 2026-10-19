---
name: app-ui-slopless
description: Visual design and UX for native mobile app screens in SwiftUI, Jetpack Compose and Compose Multiplatform (KMP). Use whenever the user wants to design, build, restyle, redesign, theme or audit how an iOS or Android screen, flow, component or design system looks and feels — e.g. a screen that looks generic, boring, stock Material or "AI-made"; picking a type scale, colour palette or theme code; giving an app a style (warm premium, neo-brutalist, playful, editorial); or a UX critique of a mobile screen or screenshot (hierarchy, tap targets, thumb reach, contrast, error states). Trigger even if "design" is never said ("make it less ugly", "give it personality", "is this memorable or generic?"). Grounded in Apple HIG, Material 3 and UX research (Norman, Nielsen, Fitts, Hoober). Not for web/React/HTML pages, Figma tool how-tos, pixel-identical XML-to-Compose ports, or non-visual mobile work (crashes, scroll performance, navigation/deep links, tests, backend, CI/release).
---

# app-ui-slopless

Make mobile UI that people remember, on top of interaction design that holds up to the research.

Two failure modes to avoid, equally:
- **Slop**: the generic look an AI produces by default. Grey-on-white cards with soft shadows, a purple-blue gradient, one sans everywhere at timid sizes, emoji as icons, everything rounded the same. It's forgettable, and the research says it costs you: people judge visual appeal in ~50 ms (Lindgaard 2006), rate attractive interfaces as more usable (Kurosu & Kashimura 1995; Tractinsky 2000), and flat, signifier-poor screens take ~22% longer to use (NN/g, Moran 2017).
- **Pretty but broken**: bold styling on a flow that's hard to use. Tuch et al. (2012) found poor usability *lowers* perceived beauty. Google's M3 Expressive research reached the same place: expressive works *through* familiar patterns, and breaking them hurts.

So the job is: **studied bones, unmistakable skin.**

## Workflow

Work out which mode the user wants. A request can combine several (e.g. audit → redesign).

| Mode | Trigger | Output |
|---|---|---|
| **Build** | "make me a … screen" | Brief → code |
| **Redesign** | existing screen + "make it better/bolder" | Brief → code + short "what changed and why" |
| **Audit** | "review / critique / what's wrong" | Findings report (see `references/audit.md`) |
| **Spec** | "design system", "tokens", "style guide" | Brief expanded into a token file |

### 1. Inventory the product

Before any style decision, write **8–12 things that belong to this product and to no competitor** as a short bulleted list in your reply, not only in your head: the user should see what the design is built from, and can correct a wrong assumption before it shapes every screen. This list is where the owned idea comes from in step 3, and it's what you hold the dealt directions against in step 2. Look for:
- **Its name** and what the name means or sounds like.
- **Its numbers:** the streak, the price, the minutes, the seat count, the 66 levels, the 21:00 deadline.
- **Its constraint:** one ferry a day, a weekly budget that resets on Monday, a habit that only counts before noon.
- **Its objects and materials:** what the thing physically is or touches (a ticket, a jar of coins, a running shoe, a seed packet).
- **Its rituals and hours:** when people open it and what they do in what order (the morning check-off, the Sunday plan, the boarding-gate glance).
- **Its printed artefacts:** what paper or signage already exists in its world (a receipt, a boarding pass, a logbook, a score sheet, a seed catalogue, a departure board).
- **Its place:** where it's used (on a bike, at the counter, in bed, on a platform) and what that place looks like.

If the request is thin, infer plausible items from the domain, mark them as assumptions, and carry on. "Clean", "modern" and "fun" are not inventory items.

**Gate:** don't run `deal.py` until the list is in your reply. It also opens the brief in step 3, so it can't get lost between steps.

### 2. Deal and pick the direction (+ dials)

The user chooses the style; never silently default to something safe.

**Deal the directions; don't invent them.** Asked to choose a look, a model picks the category default every time (every fintech app gets the same warm premium). So a script deals researched directions, each anchored in shipped apps, and you choose among them:

First name the screen's **content shapes**: what the user came to see or do, primary first. One of `list` (rows to scan: departures, spends, habits), `number` (one figure that answers the screen: a balance, a countdown), `detail` (one item in depth), `collection` (many items to browse), `canvas` (a map, calendar or chart as the screen), `story` (one moment per screen, in sequence), `progression` (a path or levels), `action` (one verb dominates). A ferry home is `list,number`; a room page `detail,canvas`; a habit home `action,list`.

```bash
python3 <skill>/scripts/deal.py --options 3 --content <primary>[,<secondary>] [--preset <name>] [--sector <e.g. finance, health, kids>] [--have photography]
```

- `--content`: only directions whose composition can show the primary shape are dealt, and within each preset the ones that also hold the secondary shapes come first. A poster of colour blocks can't show a timetable, so it isn't dealt for one.
- `--preset`: only when the user named one; the deal then stays inside it. Without it, the three options come from different presets.
- `--sector`: drops directions marked wrong for it (neo-brutalist for finance, for example).
- `--have photography`: only when the product really has photographs: its own photos in the project, or photos it shows at runtime (listings, products, places, people's uploads). Without it, directions that depend on photographs are not dealt, so a screen never ends up built around grey placeholder boxes. Drawn art never needs `--have`: it is made in code.

**Fit test: reject options that don't fit.** For each dealt option, answer three questions in one line each:
1. **Content at rest:** does its composition show the primary shape in the first screen, at the density the brief needs (the next few departures, not one)?
2. **Owned idea:** can it carry something from the inventory, something only this product has?
3. **Costume test:** would someone who uses this kind of product every day read the style as belonging to their world, or as a trend put on top of it? Name the reason it belongs (a timetable board for a ferry, a receipt for a shared kitty). "It's bold" or "it's not a bank" is not a reason.

Drop every option that fails any of the three. If none survives, redeal with a new seed (`--seed` any other number) and say so in the report. Then, among the survivors:
- **If you can ask,** show the surviving options in one line each (name, composition, the inventory item it would carry) and let the user pick. They may also name a reference app instead; map it to the nearest direction.
- **If you can't ask** (non-interactive run), choose, and write one line on why it beats the others for *this* product. Not the most familiar one: the familiar one is what this step exists to prevent.

Then print the full sheet and adopt it. Don't blend it with the layout you would have made anyway:

```bash
python3 <skill>/scripts/deal.py --direction <id> --seed <seed from the deal>
```

The sheet gives the composition, the idea slot, a dealt type system and palette (light and dark, with measured contrast), shape, signature moves, motion and the way the direction goes wrong. If the brand already fixes colours or typefaces, pass `--keep palette,type` and map the brand onto the roles. Redeal only for a reason you can state (it contradicts the brand, or needs an asset that doesn't exist), and say so in the report. If the script can't run, read `library/directions.json` and pick by the same rules.

The four presets behind the directions:

| Preset | One-liner | Real-world anchors | File |
|---|---|---|---|
| **Warm premium** | Photo-led, confident type, rich but controlled | Airbnb, Uber, Revolut, Flighty | `references/presets/warm-premium.md` |
| **Neo-brutalist** | Thick strokes, hard offset shadows, flat clashing colour, raw type | Gumroad, Figma, Nothing, Teenage Engineering | `references/presets/neo-brutalist.md` |
| **Playful / toy** | Chunky pressable shapes, springy motion, characters, rewards | Duolingo, Headspace, Finch | `references/presets/playful.md` |
| **Editorial** | Huge display type, magazine grids, stark contrast | Arc, Spotify Wrapped, Nike, NYT | `references/presets/editorial.md` |

Then read **only** the chosen direction's preset file. It holds the wider rules for that style: palette strategy, type, shape, depth, motion, more signature moves, real examples, and how cheap imitations go wrong. Where the sheet and the preset file differ, the sheet wins for this build.

Then set the **dials** (1–10). The sheet gives this direction's defaults; the user can override any of them.

| Dial | 1 | 10 |
|---|---|---|
| `BOLDNESS` | quiet, mostly neutral | loud, saturated, oversized |
| `MOTION` | instant, fades only | springy, choreographed, celebratory |
| `DENSITY` | airy, one idea per screen | packed, dashboard-like (Flighty, Bloomberg) |
| `COLOR` | near-monochrome + one accent | full multi-hue palette |
| `FIDELITY` | fully native look (stock HIG/M3 components) | fully bespoke components |

`FIDELITY` controls the *look* of components. Platform *mechanics* (back behaviour, safe areas, text scaling, system gestures) stay native at every setting unless there's a written reason. See "Breaking conventions".

### 3. Find the idea, then write the brief (before any code)

**The owned idea** is what makes the app belong to this product and no other. Look at what recent Apple Design Award winners share: not polish, but *one strong idea carried through every surface*. Flighty is an airport departure board. Tide Guide's palette follows the sky. Duolingo has its cast of characters. Halide is a film camera.

Write it as one sentence, and don't start the brief until both blanks are filled:

> In this app, **[an item from the inventory]** becomes **[the device the direction calls for]**.

For example: "In this app, the 21:00 last-ferry constraint becomes the departure-board countdown that every screen hangs from." Or: "In this app, the seed packet becomes the card shape of every habit, with the sowing date as its stamp."

**The competitor test.** Put the nearest real competitor's name into the sentence. If it still works, the idea belongs to the category, not the product: "a check mark becomes a celebration" fits every habit app, so it fails. Go back to the inventory and pick something only this product has.

**One live thing.** From the idea, make one interaction that is different every time or reacts to real state: the mascot that panics as the deadline nears (Duolingo's widget), the progress ring that keeps counting with no connection (Flighty), the budget jar that visibly empties as you spend. It uses the product's real data, works one-handed, has an accessible and reduce-motion fallback, and is one thing, not a playground. It is usually one of the signature moves.

Then write the brief. A short brief keeps the style coherent across every screen, and it's what turns "make it fun" into decisions. Keep it under ~30 lines, and put it in your reply (or in `DESIGN.md` for Spec mode or multi-screen work).

```
Inventory: <the 8–12 items from step 1, comma-separated; mark assumptions with (assumed)>
Direction: <dealt id verbatim, e.g. pl-persona, then its name> (seed <n>, or "user-picked preset")   Dials: B<n> M<n> D<n> C<n> F<n>
Owned idea: In this app, <one item from the Inventory line> becomes <device>. Competitor test: <competitor> → fails/passes
Live thing: <the one interaction made from the idea, and the real state it reacts to>
Persona: <one sentence: who the app is, as a character>
This, not that: <3 pairs, e.g. "confident, not shouty · warm, not cute · fast, not frantic">
Primary user + goal on this screen: <who, what they came to do, how often>
Type: display <face, use> / text <face> / scale <4–6 sizes>
Colour: <roles: surface, ink, primary, accent, success/warn/error; light + dark>
Shape & depth: <radius language, stroke, elevation/shadow model>
Icons: <which glyphs are custom-designed (the core verb, hero, categories) vs system family for utility chrome>
Motion: <spring/easing + the motion list for this MOTION level (see "Motion budget")>
Signature moves: <2–3 things someone would recognise in a screenshot>
```

The **owned idea** and **signature moves** are the antidote to slop. Carry the idea into every surface you build, including the empty state, settings, errors and the paywall: the commonest failure is a distinctive home screen followed by stock screens. Pick signature moves as concrete, transferable mechanics from the direction sheet or preset file (e.g. "every pressable has a 4dp bottom lip that compresses on press"), not adjectives.

Want more real examples than the preset file has? See `research/real-ui-references.md`: award winners, design-team case studies, font alternatives, all from shipped apps.

**Commit to the direction.** The dials are a promise to the user. A playful screen at `BOLDNESS 8` should look unmistakably playful in a screenshot. If a principle seems to argue for toning it down, look for a way to satisfy the principle *inside* the style (e.g. make a signifier louder, not the style quieter). Restraint is a dial setting, not a default.

### Icons are part of the signature

Stock icon sets are plumbing: fine for utility chrome (back, close, settings, share, search), and they make everything else look like every other app. Design these glyphs instead of importing them:
- **The core verb's icon:** the check in a habit app, the heart in a dating app, the ticket in a transit app. It's the most-seen glyph in the product, so it gets the most care: a custom shape in the preset's language (chunky rounded stroke, thick square cap, fine serif-like detail…) and an animated state change (draw-on, morph, stamp, pop).
- **Hero and category icons:** tab icons at `BOLDNESS` ≥7, categories, empty-state art, the mascot. Draw them as one family: same stroke weight, corner treatment and fill/duotone logic, all made in code (`Canvas`/`ImageVector` in Compose, `Shape`/`Path` in SwiftUI) or from one commissioned set.
- **System symbols done well count too.** SF Symbols with `.symbolEffect` and variable colour, or Material Symbols with fill/weight axes animated, are legitimate when `FIDELITY` is low. Stock and static, with no styling, is the default look.

The platform files show how to draw and animate custom glyphs.

### 4. Build

Read `references/platform-swiftui.md` or `references/platform-compose.md` (Compose Multiplatform uses the Compose file plus its CMP section). They show how to implement tokens, custom fonts that still scale, press states, springs, haptics, reduce-motion, and insets idiomatically.

Each platform file ends with a **code baseline** (§8b): stable list identity, state that survives, animating transforms rather than layout, and so on. Follow it, because bold UI that janks reads as broken.

Put tokens first (one theme/token file or block), then components, then the screen. Hard-coded colours and sizes scattered through the screen are how a style decays into slop on screen three.

Apply the core rules below while building. `references/principles.md` has the full rule set with sources; read it for Audit mode or when a judgement call needs backing.

**Real content at real density.** A screen built on "Alex", "Lorem ipsum" and three tidy rows looks finished in code and thin on a phone. The design has to be judged with the content it will actually carry:
- **Domain-real sample data.** Names, items, amounts and dates that belong to this product's world and its users (a varied, international set of names; real-sounding habit names, routes, dishes, merchants). No "Acme", "John Doe", "Item 1", "Lorem", "Good morning, Alex 👋".
- **Full density.** Enough rows to scroll, the longest realistic name, the widest number ("365", "€12,480.50"), two-line titles, a missing photo. Design for those, not the happy average.
- **Every state.** Empty, loading, error, offline and first-run, each carrying the owned idea, not a grey icon and "Nothing here yet".
- **No invented proof.** No made-up ratings, reviews, testimonials, user counts, press logos or "Trusted by 10,000+". Placeholder business facts (prices, plan names) are fine; list them in the report so the user can replace them.
- **Words named for what they do.** Buttons say the action ("Book for €84", "Mark as done"), not "Submit" or "Continue"; errors say what happened and how to fix it.

**Pictures: where they come from.** Photo-led directions (warm premium, story cards, type-as-image with photography) depend on imagery, and models skip finding it because it's work. Use this order and never stop at a grey box:
1. **The product's own:** user content, product photos, real maps or screenshots the project already has. In an app most images are runtime content, so design the slot: a fixed aspect ratio (no layout jump on load), a loading state that is a tone step in the palette, and a designed fallback (initials, a glyph from the icon family), never a grey rectangle or a broken-image icon.
2. **Generated,** if you have an image tool and the user is fine with it. Never present a generated picture as a real person, product, place or customer.
3. **Openly licensed pictures of the product's world,** for onboarding, empty states, category art and sample content: Wikimedia Commons, Openverse, and museum open-access collections (the Met, the Art Institute of Chicago, the Rijksmuseum), NASA. Search the inventory, not the category: the product's object up close, its city in an old postcard, a botanical plate, a timetable, an engraving of its trade. Use only licences that allow commercial use, download the file into the project's assets, and list title, creator, licence and source in the report. A found picture shows the world around the product, never the product's own team, customers or goods.
   **Never send the user's identity to outside services.** Searching and downloading pictures (or fonts, or anything else) must not carry the user's email, name, account, organisation or machine details: not in a User-Agent header, a query string, an API key field or a "contact" parameter, even when a service's etiquette asks for contact details. Use a generic identifier such as `User-Agent: app-ui-slopless/1.0 (+https://github.com/massipetro/app-ui-slopless)`. If a service refuses requests without personal contact details, skip it and say so in the report.
4. **Drawn in code from the inventory** (`Canvas` / `Path` / `ImageVector`): the product's objects in one consistent flat graphic language, in the palette's real colours. Better than a placeholder, an enlarged SF Symbol, or an abstract blob.
5. **Type and colour alone,** for directions built on them.

Never: stock photos of laughing people, AI images passed off as real, illustration from mixed packs, a decorative blob standing in for a picture.

**The brief at rest.** Before styling, list the brief's must-haves for this screen (for a ferry home: next departures, a countdown, buying a ticket) and design so every one is visible in the resting frame, or reachable from a visible control there. Two limits keep the hero honest:
- When the screen's content shapes include `list`, at least three rows (or the whole list, if shorter) show at rest, and the hero takes no more than about 45% of the screen's height.
- Make the key number big inside its region (48–72 pt), not by growing the region. A huge hero that pushes what the user came for below the fold loses to a plainer screen that answers the brief at a glance: it's the most common way a stronger idea lost in our blind evals.

**Removing slop leaves space. Don't fill it with another ornament.** Fill it with scale (make the main thing bigger, within the limits above), with the full content, or with the owned idea. One deliberate empty moment per screen at most.

### 5. Look at it, fix it, then report

**Gate first: compile, then lint.** Code that doesn't build is not a deliverable, however good the render looks.

- **SwiftUI:** typecheck every Swift file you wrote, together, against the iOS simulator SDK:

  ```bash
  python3 <skill>/scripts/typecheck.py <changed .swift files or folder> [--ios <deployment target, default 17.0>]
  ```

  Fix every error and run it again until it passes. It needs no Xcode project, so there's no excuse to skip it on a Mac. If it can't run (exit 3: no Xcode, or files that import third-party packages), say so under "Not verified"; never report Swift as compiled when it wasn't.
- **Compose / CMP:** if the project has a Gradle build, compile the module you changed (`./gradlew :<module>:compileKotlin`, or `compileKotlinIosSimulatorArm64` / `compileDebugKotlinAndroid` for a CMP target) and fix every error. Without a project, Kotlin can't be compiled here: say "Kotlin not compiled" under "Not verified".

Then lint the files you wrote:

```bash
python3 <skill>/scripts/lint.py <changed .swift / .kt files or folder> [--allow <rule>,<rule>]
```

It flags the slop tells and craft defects the code itself shows (violet accents, stock greys, 5%-black shadows, fixed font sizes, placeholder-only fields, sub-44/48 targets, unlabelled icon buttons, emoji, placeholder data, animation without Reduce Motion) and the code-baseline patterns from the platform files (index-based list identity, `AnyView`, `DispatchQueue` delays, `ObservableObject`, `@MainActor` models in default arguments, lazy `items` without keys, a `LazyColumn` inside `verticalScroll`, `collectAsState()`, typed text in plain `remember`). `--list-rules` shows them all. Fix every `FAIL`. Treat each `WARN` as wrong unless you can defend it in one sentence. `--allow` is for deliberate style choices only (e.g. `blur-shadow` for a warm premium floating sheet); list each one in the report. It's a regex heuristic, so a clean lint proves nothing about taste: that's what the passes below are for.

**Render what you built and look at the image before handing over.** Code that reads well often renders badly: a number clipped by a fixed-width box, a token stretched into a pill by its parent, a tick off-centre, a bar covering content. The user sees those first, and one of them makes a bold design look broken (Tuch et al. 2012: poor execution lowers perceived beauty). Use the best render path available:
1. **Real render:** Compose `@Preview` screenshot tests (Roborazzi/Paparazzi), SwiftUI previews or snapshot tests, or the app on an emulator/simulator (`adb exec-out screencap -p > s.png`, `xcrun simctl io booted screenshot s.png`).
2. **Faithful mock:** if you can't run the platform, write an HTML/CSS mock with the same tokens, sizes and layout, and screenshot it headless at phone size with motion settled (e.g. Chromium-based `--headless=new --force-prefers-reduced-motion --window-size=390,844 --screenshot=s.png file.html`).
3. **Neither possible:** say clearly in the report that the layout was never seen rendered.

**Render every scrolling screen twice: at rest and scrolled to the end.** The resting frame is what people and screenshots see first; the end frame proves the last row clears the pinned bar. On a simulator, swipe to the bottom and screenshot again; in a Compose screenshot test, render a second preview with the list state scrolled to the last item. In the HTML mock, give the scroll container an id and end the file with one line, `<script>if (location.hash === '#end') { const s = document.getElementById('scroll'); s.scrollTop = s.scrollHeight; }</script>`, then render `mock.html` and `mock.html#end` as two frames.

Judge only the pictures, never the code: you wrote the code, so you'll read your intentions into it. If a problem is visible in the screenshot, it's real.

**Craft pass.** Read the image like a picky designer:
- Text clipped, truncated or overflowing its container, especially the biggest numbers at their widest value ("12" vs "365").
- Elements stretched or squashed by their parent (fill-height, flex stretch, `fillMaxSize` in a `Row`).
- Icons and ticks off-centre in their circles or tiles; misaligned baselines.
- Overlaps, content hidden under top or bottom bars, and uneven gaps that break the spacing scale.
- **Anything cut off by a pinned bottom element** (a CTA bar, tab bar, sheet handle or home indicator): a list row sliced in half behind the button is the commonest defect in generated screens, and it was the one most often penalised in our blind evals. Fix it in two places:
  - **Structure, so the last row can scroll clear.** SwiftUI: pin the bar with `.safeAreaInset(edge: .bottom) { bar }` on the `ScrollView`/`List`, not a `ZStack(alignment: .bottom)` or `.overlay(alignment: .bottom)` over it. Compose: put the bar in `Scaffold(bottomBar = …)` and pass the `innerPadding` bottom into the list's `contentPadding`, not a `Box` with `Alignment.BottomCenter` over it. `lint.py` warns (`pinned-bottom-overlap`) when it sees the overlay pattern.
  - **The resting frame, which is what people and screenshots see first.** Content that continues under the bar must read as scroll, not as cut: the bar is opaque with a visible top edge (a tone step, or the platform's scroll-edge effect), and either the fold lands in a gap between rows or a short fade of the page colour (16–24 pt) sits above the bar. A row whose text is cut mid-line at rest is a defect even when the code scrolls correctly; shorten or reorder what's above it, or move the fade.
  - **Fold check, row by row.** In the resting frame, name every row whose box comes within 24 pt of the bar's top edge, and say for each one: whole above the bar, under the fade with no text cut, or cut. "Cut" includes a row's text, avatar or card border sliced by the bar. Any "cut" is a defect: move the fold into a gap (tighten or reorder what's above, or change a row height; never grow the hero to push the list down) and render again. In the end frame, the last row must sit fully above the bar with at least 8 pt clear.
- Depth signifiers (lips, shadows, strokes) that are invisible at their real colours.

**Taste pass.** Passing the craft pass means nothing is broken. It doesn't mean the screen is good. Critique the same screenshots with `references/critique.md`: the one-second glance, the squint, the cover-the-logo test, idea reach, sameness, fullness, the thumb, the bottom edge. Score them, and **write the critique in your reply** in its format, including the scores line. The critique is part of the deliverable, not private working: a run that ends without it hasn't finished step 5. If you couldn't render at all, say so in the reply in place of the critique ("Critique: not run, the screen was never rendered") rather than leaving it out.

Then fix the top three problems across both passes, render again and look again. **Two rounds at most**; report what still falls short instead of looping.

Then run the checks at the end of this file. For each failed check, fix it or, if the style choice deliberately trades it off, keep it and **warn** the user (see Accessibility stance). **End with the report block.** Your final message ends with the block below, filled in. It is a fixed format, not a suggestion: copy the 15 labels exactly, in this order, one per line, inside the fenced block, starting with the `app-ui-slopless report` line. Don't rename, merge, reorder or drop a label, and don't restate it as prose or under your own headings. Fill every field; if one doesn't apply, write `n/a` and why. You may write anything you like before the block (what you built, notes for the user), but the block comes last and stands on its own: some hosts (headless runs, some models) show only the last message, so a step that only appeared mid-run is invisible to the reader. Don't claim a check you didn't run.

```
app-ui-slopless report
Inventory: <the 8–12 items from step 1, comma-separated; (assumed) where inferred>
Direction: <dealt id, e.g. pl-persona> (seed <n>); redeals: <none, or which and why>
Owned idea: In this app, <inventory item> becomes <device>.
Competitor test: <competitor> → <why the idea fails for them>
Live thing: <the interaction and the real state it reacts to>
Built: <files, screens, states; the brief's must-haves visible at rest>
Signature moves: <2–3>
Lint: <compile: pass / FAIL / not run and why; lint n FAIL, n WARN; each --allow and each kept WARN with its reason>
Critique (final round): Idea n · Hierarchy n · Craft n · Substance n · Platform n → overall n (caps: <which, or none>)
Bottom edge: rest frame <each row at the fold: whole / under fade / cut>; end frame <last row clear by n pt>
Still short: <what the critique found and you didn't fix>
Sample content to replace: <names, prices, dates, photos>
Pictures: <each found picture: title, creator, licence, source; or "none, drawn in code">
Warnings: <accessibility trade-offs with criterion, value and fix>
Not verified: <e.g. not compiled, not run on device, large text not checked>
```

## Core rules (the studied bones)

These hold in every preset. Each one exists because ignoring it measurably hurts people. The sources are in `references/principles.md`.

**Signifiers and feedback**
- Every tappable thing looks tappable: a container, a fill, a stroke, an underline, or an icon *plus* a label. Non-interactive things must not borrow the *same* look; give them a quieter version of the style's depth instead of none (Norman; Gestalt similarity; NN/g flat-UI study).
- A signifier only exists if people can see it. Lips, strokes and hard shadows need ≥3:1 contrast against the surface they sit on (WCAG 1.4.11). A white-on-white lip is no lip.
- Acknowledge every tap within 100 ms with a pressed state (plus a haptic where it means something). Show progress past ~1 s, and determinate, cancellable progress past ~10 s (Nielsen response-time limits).
- Put feedback at the point of action. Toasts far from the thumb get missed (Johnson: peripheral vision is poor).

**Reach and targets**
- Content goes in the centre. Primary actions go low (bottom bar, bottom-anchored CTA, FAB, sheet). Rare and navigational actions go high. Never put the only primary CTA in a top corner (Hoober; Clark).
- Targets are ≥44 pt on iOS and ≥48 dp on Android, with ≥8 dp between them. Make the whole row tappable. Keep destructive actions physically apart from frequent ones (Fitts; HIG; M3).

**Structure and memory**
- One obvious primary action per screen. Fewer, more prominent choices beat many equal ones (Hick–Hyman).
- Keep context visible (selected item, totals, active filters). Working memory holds ~4 chunks, not 7 (Cowan 2001). Chunk long numbers in groups of 3–4.
- Show 3–5 top destinations in a visible tab or navigation bar. Hidden navigation cut discoverability by >20% (NN/g 2016).
- Spacing *is* grouping. Make gaps within a group clearly smaller than gaps between groups (Gestalt proximity).

**Forms and errors**
- Use persistent labels above the field, never placeholder-only labels (NN/g 2014; Wroblewski). Use the right keyboard, autofill hints and sensible defaults, and validate when the field is finished.
- Prefer undo to "Are you sure?". Confirm only destructive, irreversible actions (Norman; Shneiderman rule 6; Cooper's excise).
- Error messages say what happened and how to fix it, next to the field (Nielsen #9).
- A completed flow ends in a closure state, not a silent pop back (Shneiderman rule 4).

**Type, colour, hierarchy**
- Use 4–6 type sizes with real jumps between them. Make the key number big (a price, time or streak at 34–60 pt). A timid 15/16/17 ladder has no hierarchy (Bringhurst; Lupton).
- Change one variable per hierarchy level. Use tabular figures for numbers that update or align.
- **Caps budget: at most two small uppercase labels per screen, in every preset.** "Small" means under about 20 pt, tracked or not, monospace or not: eyebrows, section labels, metadata, units, badges, button text. Uppercase earns its place at display size (a one- or two-word hero, a giant section header); everywhere else use sentence case at a readable size and let size, weight or colour carry the hierarchy. Neo-brutalist and editorial directions are where this goes wrong most: both ferry screens in our round-4 eval were capped for it. `lint.py` warns (`caps-labels`) when the code uppercases more than two labels, counting every call of a helper that does it.
- Never use colour alone to carry meaning. Pair it with shape, icon or text (Johnson; WCAG 1.4.1).
- Judge colour in context, in both light and dark, never as a lone swatch (Albers). Build ramps in OKLCH, then check contrast with WCAG (and APCA for dark mode).

**Motion** (how much is set by the dial; see "Motion budget" below)
- Things travel; they don't teleport. Ease every movement, and use springs for anything gesture-driven so it stays interruptible (Chang & Ungar; M3 motion).
- The research limits *duration and blocking* on frequent paths, not the presence of motion. A 120 ms squish on every tap is great. A 2 s celebration on every tap is not. Frequent feedback stays ≤300 ms, is interruptible, and never blocks input (HIG; NN/g surface vs deep delight).
- Honour Reduce Motion / Remove animations: swap movement for fades and drop looping animation.

**Delight**
- Function → reliable → usable → pleasurable (Walter). Personality sits on top and is required, not optional.
- Put personality where it's cheap and safe: empty states, success moments, microinteractions (toggles, favourites, pull-to-refresh), and copy voice (Saffer).
- Tone it down on serious surfaces such as money, health, safety and bad news.

## Motion budget (by `MOTION` dial)

Motion is how a static mock becomes an app people want to touch. A high `MOTION` setting is a request for *more life*, so deliver it.

| `MOTION` | What to build |
|---|---|
| **1–3** | Pressed states, simple fades and slides, numbers that change without animation. Nothing loops. |
| **4–6** | Everything above, plus spring presses, shared-element / container transitions, numbers that roll when they change, a staggered entrance when a screen first loads (30–50 ms per item), and an animated state change on the core verb (check draws on, heart fills). |
| **7–10** | Everything above, plus: **ambient life** (a mascot that blinks and breathes, gently bobbing hero art, a flame that flickers, cycling 2–3 frames of "boil" on illustrations), **press squish on every pressable** (scale ~0.94 plus the lip/shadow collapse), **animated icons** (draw-on checks with overshoot, morphing tab icons, a bouncing selected tab), **choreographed celebrations** on milestones (particles, scale burst, sound and haptic), playful page transitions, and pull-to-refresh with character. |

At every level:
- Ambient loops are subtle (small amplitude, ≥2 s cycles), never on text, and stop under Reduce Motion (WCAG 2.2.2, 2.3.3).
- Frequent paths stay quick: ≤300 ms, interruptible, never blocking input. Big celebrations are for milestones, not routine taps.
- Pair motion with haptics on meaningful moments (light on press, success on completion).
- Under Reduce Motion, keep the *information* (state change, colour, haptic, sound) and drop the movement.

## Platform fidelity

Shared across platforms (the brand layer): colour, display type, iconography style, illustration, shape language, motion personality.

Native per platform (the mechanics):
- **Back:** iOS uses a top-left back button plus edge swipe. Android uses system and predictive back; never hijack it except to dismiss your own transient UI.
- **Insets:** iOS safe areas; Android edge-to-edge is enforced from SDK 35 (handle `WindowInsets`).
- **Text scaling:** iOS Dynamic Type up to the AX sizes. Android `sp` up to 200% with nonlinear scaling.
- **Sheets, pickers, date/time inputs, haptics, share sheets:** use each platform's own.
- **Tab bar vs navigation bar:** both bottom, 3–5 labelled destinations, never hidden or disabled.

In Compose Multiplatform, one shared UI is fine. Branch with `expect/actual` (or a platform flag) for the mechanics above when they differ visibly: back affordance, haptics, sheet style, system font fallbacks.

## Breaking conventions

The user is allowed to break platform conventions when the style calls for it, for example a custom bottom bar shaped like a ticket stub, or a bespoke toggle. When you break one:
1. Say which convention, and why the style needs it, in one line in the brief.
2. Keep the *function* the convention protected. A custom tab bar still shows labels, stays visible, and has 44/48 targets. A custom toggle still announces its state to VoiceOver and TalkBack.
3. Never break hard requirements silently: safe areas and insets, system back, text scaling, screen-reader labels. Breaking one of these gets a ⚠️ warning in the report.

## Accessibility stance: warn, don't block

Bold choices sometimes trade against accessibility, such as neon-on-black contrast, a 9 pt caption in an editorial layout, or non-stop motion. The user decides, but always with the information in front of them:
- Default to compliant (WCAG 2.2 AA: 4.5:1 text, 3:1 large text and UI components, 44/48 targets, scalable text, reduce-motion fallback).
- If the style needs a trade-off, make it, and list it under **⚠️ Accessibility warnings** with the criterion, the measured or estimated value, and the compliant fix (e.g. "Caption #8A8A8A on #FFF = 3.5:1, fails 1.4.3; #6B6B6B gives 5.3:1").
- Never drop screen-reader labels, text scaling or the reduce-motion fallback to get a look. These cost nothing visually.

## Slop tells (as of 2026-10; check before handing over)

Models produce slop because they sample the statistical average of their training data, which is mostly templates and tutorials (Anthropic calls it "distributional convergence"). If the output shows any of these without a deliberate reason, it has drifted back to that average. Fix it. (Compiled from Anthropic, impeccable.style, taste-skill and designers' write-ups; see `research/real-ui-references.md` §6.) `scripts/lint.py` catches the ones visible in code.

**This list is dated, on purpose.** Tells move: each published "use this instead" becomes the next wave of defaults within months (Inter was replaced by Space Grotesk, Geist and Instrument Serif, which are now tells themselves; purple gradients were replaced by cream and terracotta). So the fix for a tell is a *procedure*, never a named replacement: deal a direction, take colour and type from the sheet or from the product's own material, and derive the idea from the inventory. Don't treat the font names in the preset files or the research notes as a new default list either; they're what the deal draws from. When you notice a new tell spreading, add it here with its date.

**Colour**
- Purple/indigo-to-violet gradients, gradient text, a gradient FAB or app bar.
- Cream/beige base with terracotta/rust accents as an unexamined default (the newer "tasteful AI" look).
- Grey-on-white secondary text below contrast. Dark mode that's just inverted grey with the same accent.

**Type**
- One sans (Inter/Roboto/SF) at timid sizes for everything, with no display moment.
- Second-order defaults when Inter is banned: Space Grotesk, Geist, Instrument Serif. Fine with a reason; slop as a reflex.
- A tiny letter-spaced uppercase "eyebrow" above every heading. An italic serif "accent word" in a headline.
- Monospace for "techy vibes" outside data or code.

**Layout and components**
- "Good morning, Alex 👋" + a 2×2 grid of pastel stat cards + a card list: every app as the same dashboard.
- Every surface a white rounded-16 card with a 5%-black soft shadow on light grey; cards nested in cards.
- A coloured left-edge stripe on cards. SF Symbols / Material icons in pastel rounded-square tiles on every row.
- Everything centred, the same radius on chips, cards, sheets, buttons *and* images, every gap 16.
- Glassmorphism or blur as decoration, or a glass tab bar over flat white content.
- A centred hero, then three equal icon-topped feature cards, then a big pill button.

**Icons and imagery**
- Emoji standing in for icons, or a mix of icon families. Stock 3D blobs. Free-pack Lottie checkmarks that clash with the rest.
- The core verb drawn with a stock, static icon (a default Material/SF checkmark for "done" in a habit app).
- *Pastel* tiles with stock symbols on every row. (Vivid, custom-drawn icon tiles with a role, such as each habit owning a hue and a glyph, are a playful signature, not slop. The tell is generic-and-pastel-everywhere.)

**Motion and feel**
- No motion at all, or one fade on everything. Bouncy easing on routine dialogs.
- Confetti on routine actions. No haptics anywhere, or `.heavy` on everything.

**Craft**
- Default `Color.gray` / `Color(0xFF888888)` and stock `.shadow(radius: 8)`.
- Missing empty, loading and error states.
- Copy like "Unlock your potential", "Seamless experience" or "Supercharge your…".

## Final checklist

- [ ] Inventory of 8–12 product-only items written in the reply before `deal.py` ran, and repeated as the brief's first line.
- [ ] Content shapes named and passed to `deal.py --content`; every dealt option put through the fit test (content at rest, owned idea, costume test), misfits dropped, redeal stated if none survived; direction id and seed in the report.
- [ ] Owned-idea sentence passes the competitor test; the live thing is built and reacts to real state.
- [ ] Brief written: direction, dials, owned idea, live thing, persona, 2–3 signature moves.
- [ ] Swift typechecked with `scripts/typecheck.py` (or Kotlin compiled with Gradle) and passing; if it couldn't run, the report says so.
- [ ] `scripts/lint.py` run on the changed files: no `FAIL`, every `WARN` and `--allow` defended in the report.
- [ ] Scrolling screens rendered at rest and scrolled to the end; the row-by-row fold check found no cut row, and the last row clears the bar.
- [ ] Rendered and looked at: no clipped, stretched, off-centre or overlapping elements (or the report says it couldn't be rendered).
- [ ] Taste pass written in the reply in `references/critique.md` format (or "Critique: not run" with the reason), top three fixed, at most two rounds; final scores reported.
- [ ] Real content at real density, every state designed, no invented proof; sample content to replace is listed.
- [ ] The brief at rest: every must-have visible or reachable in the resting frame; with a `list`, three rows show and the hero stays under about 45% of the height.
- [ ] No request to an outside service carried the user's email, name or account; found pictures are credited.
- [ ] Tokens defined once; no stray hex values or magic numbers in the screen.
- [ ] Every interactive element has a visible signifier and a pressed state.
- [ ] Primary action is in the thumb zone; targets are 44/48; destructive actions are isolated.
- [ ] Type scale of 4–6 sizes, a real display moment, and custom fonts that scale with Dynamic Type / `sp`.
- [ ] Contrast checked in light and dark (or a warning given); colour never carries meaning alone.
- [ ] Core-verb icon and hero glyphs are custom-designed and animated; stock icons only for utility chrome.
- [ ] Motion matches the `MOTION` dial's row in the motion budget (at 7+: ambient life, press squish everywhere, animated icons); frequent paths ≤300 ms; reduce-motion fallback present.
- [ ] Depth signifiers (lips, strokes, shadows) visible at ≥3:1 against their surface.
- [ ] Native mechanics intact (back, insets, text scaling, screen-reader labels), or the break is justified.
- [ ] None of the slop tells.
- [ ] The final message ends with the `app-ui-slopless report` block from step 5: all 15 labels verbatim, in order, every field filled (or `n/a` with a reason).
