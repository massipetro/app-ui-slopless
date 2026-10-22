---
name: app-ui-slopless
description: Visual design and UX for native app screens in SwiftUI (iOS and macOS), Jetpack Compose and Compose Multiplatform (KMP). Use whenever the user wants to design, build, restyle, redesign, theme or audit how an iOS, Android or Mac screen, window, flow, component or design system looks and feels — e.g. a screen that looks generic, boring, stock Material or "AI-made"; picking a type scale, colour palette or theme code; giving an app a style (warm premium, neo-brutalist, playful, editorial); or a UX critique of a mobile or Mac screen or screenshot (hierarchy, tap targets, thumb reach, sidebar and toolbar layout, hover and keyboard use, contrast, error states). Trigger even if "design" is never said ("make it less ugly", "give it personality", "is this memorable or generic?"). Grounded in Apple HIG (iOS and macOS), Material 3 and UX research (Norman, Nielsen, Fitts, Hoober). Not for web/React/HTML pages, Figma tool how-tos, pixel-identical XML-to-Compose ports, or non-visual app work (crashes, scroll performance, navigation/deep links, tests, backend, CI/release, notarization and App Store packaging).
---

# app-ui-slopless

Make native app UI (iPhone, Android, Mac) that people remember, on top of interaction design that holds up to the research.

**Platform first.** Decide which platform(s) the screen ships on before anything else, from the project (`Package.swift` platforms, the `.xcodeproj`'s deployment targets, `import AppKit`) or the request, and state it in your reply. The study-backed bones and the directions' brand layer are shared; the mechanics and the window composition are not. On a Mac, deal with `--platform macos` (step 2), read `references/platform-macos.md` and apply the **macOS** variants of the rules marked that way below (pointer and keyboard instead of thumb, windows and sidebars instead of one screen, fixed 13 pt text instead of Dynamic Type). Never ship an iPhone layout in a bigger window.

Two failure modes to avoid, equally:
- **Slop**: the generic look an AI produces by default. Grey-on-white cards with soft shadows, a purple-blue gradient, one sans everywhere at timid sizes, emoji as icons, everything rounded the same. It's forgettable, and the research says it costs you: people judge visual appeal in ~50 ms (Lindgaard 2006), rate attractive interfaces as more usable (Kurosu & Kashimura 1995; Tractinsky 2000), and flat, signifier-poor screens take ~22% longer to use (NN/g, Moran 2017).
- **Pretty but broken**: bold styling on a flow that's hard to use. Tuch et al. (2012) found poor usability *lowers* perceived beauty. Google's M3 Expressive research reached the same place: expressive works *through* familiar patterns, and breaking them hurts.

So the job is: **studied bones, unmistakable skin.**

## Workflow

Work out which mode the user wants. A request can combine several (e.g. audit → redesign).

| Mode | Trigger | Output |
|---|---|---|
| **Build** | "make me a … screen" | Intake → brief → code |
| **Redesign** | existing screen + "make it better/bolder" | Intake (read what exists, then ask) → brief → code + short "what changed and why" |
| **Audit** | "review / critique / what's wrong" | Findings report (see `references/audit.md`) |
| **Spec** | "design system", "tokens", "style guide" | Intake → brief expanded into a token file |

### 1. Intake: read what exists, then inventory the product

A direction that ignores the product, or throws away a brand people already recognise, is the most expensive mistake this skill can make, because everything after it is built on top. So look before you deal.

#### 1a. Read what exists (Redesign, Audit, and Build inside an existing app)

Before proposing anything, take stock of the current visual language from the theme/token files, font and drawable resources, and a screenshot if you can get one:
- **Type:** which faces, and how they feel (rounded and friendly, geometric, serif, condensed).
- **Colour:** brand colour, surfaces, how status colours are used.
- **Shape and depth:** radius language, cards vs rules, shadows.
- **Identity assets:** mascot or characters, illustrations, photography, a custom logo or font. These carry recognition. **Keep them by default**; dropping one is the user's call, asked in step 2.
- **Closest preset:** name the family the app already sits in (e.g. "rounded faces + mascot + illustrated heroes = already near Playful / Warm premium").

Write it in your reply in a few lines; the identity assets also go into the inventory below.

#### 1b. Inventory the product

After 1a and before any style decision, write **8–12 things that belong to this product and to no competitor** as a short bulleted list in your reply, not only in your head: the user should see what the design is built from, and can correct a wrong assumption before it shapes every screen. This list is where the owned idea comes from in step 3, and it's what you hold the dealt directions against in step 2. Look for:
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

First name the screen's **content shapes**: what the user came to see or do, primary first. One of `list` (rows to scan: departures, spends, habits), `number` (one figure that answers the screen: a balance, a countdown), `detail` (one item in depth), `collection` (many items to browse), `canvas` (a map, calendar or chart as the screen), `story` (one moment per screen, in sequence), `progression` (a path or levels), `action` (one verb dominates); on a Mac also `table` (sortable columns of records: files, orders, cues) and `document` (text the user writes or edits at length). A ferry home is `list,number`; a room page `detail,canvas`; a habit home `action,list`.

```bash
python3 <skill>/scripts/deal.py --options 3 --content <primary>[,<secondary>] [--preset <name>] [--sector <e.g. finance, health, kids, hobby>] [--have photography] [--platform macos]
```

Every deal ends with a `Deal:` line: the command with its flags and seed that deals the same options again. Copy it, and each redeal's, into the report's Direction line, so a reader can replay what you were offered.

- `--content`: only directions whose composition can show the primary shape are dealt, and within each preset the ones that also hold the secondary shapes come first. A poster of colour blocks can't show a timetable, so it isn't dealt for one.
- `--preset`: only when the user named one; the deal then stays inside it. Without it, the three options come from different presets. **Retro** is dealt only this way: when the user asks for a pixel, 8-bit, terminal, CRT or old-desktop look, pass `--preset retro`; the open deal never offers it.
- `--sector`: drops directions marked wrong for it (neo-brutalist for finance, for example). `hobby` covers collectors' and enthusiasts' apps. Some directions also drop out when a content shape anywhere in `--content` is one they don't suit (quiet native for `collection`).
- `--platform macos`: for a Mac app. Each direction is dealt in its Mac form: a window composition (sidebar, content, inspector, toolbar, menu bar extra) instead of the phone screen, pointer-and-keyboard signature moves, Mac-scale shape, Mac dial defaults (usually denser), and a **window chrome** line that says what stays system (translucent sidebar, the user's accent colour, the title bar) and what carries the palette. Directions with no Mac form (`ed-story-cards`) are not dealt. Three **Mac-only presets** (native craft, pro instrument, document first) join the deal, and two of the three options come from them whenever two can show the content (one when only one can), because Mac users reward Mac-native craft (`research/macos-references.md`). In the fit test, prefer a Mac-native option; pick a phone-first direction only when its owned idea is clearly stronger and its Mac form keeps Mac density, and say why. In round 18, `pl-persona`'s Mac form became a stock grid of rounded cards and lost both pairs, while `nc-owned-chrome` swept both. Without the flag they are never dealt. Pass the same flag when printing the sheet. When the working directory's project or code says macOS (`Package.swift`, the `.xcodeproj`, AppKit APIs), `deal.py` deals for the Mac on its own and says so; a brief that only *says* "Mac app" still needs the flag. The fit test reads the Mac composition: "content at rest" means in a 1280×800 window, not a phone.
- `--have photography`: only when the product really has photographs: its own photos in the project, or photos it shows at runtime (listings, products, places, people's uploads). Without it, directions that depend on photographs are not dealt, so a screen never ends up built around grey placeholder boxes. Drawn art never needs `--have`: it is made in code.

**Fit test: reject options that don't fit.** For each dealt option, answer four questions in one line each:
1. **Content at rest:** does its composition show the primary shape in the first screen, at the density the brief needs (the next few departures, not one)?
2. **Owned idea:** can it carry something from the inventory, something only this product has?
3. **Costume test:** would someone who uses this kind of product every day read the style as belonging to their world, or as a trend put on top of it? Name the reason it belongs (a timetable board for a ferry, a receipt for a shared kitty). "It's bold" or "it's not a bank" is not a reason.
4. **Category fit:** find the product's row in the table below. An option from a poor-fit preset fails, unless the app already sits in that preset (1a) or the user named it.

| Product category | Good fit | Poor fit (offer only with the warning) |
|---|---|---|
| Navigation, transit, mobility, maps, travel | Warm premium; Playful if the app already has a mascot or illustrations | Editorial (utility screens have little content to set), Neo-brutalist (reads unreliable when people depend on it) |
| Utilities (weather, scanners, calculators, settings-heavy tools) | Warm premium at low `BOLDNESS`; Neo-brutalist for indie or dev tools | Editorial |
| Finance, banking, insurance | Warm premium; Playful only for beginner/teen finance | Neo-brutalist (reads untrustworthy) |
| Health, medical | Warm premium, calm dials | Neo-brutalist, loud Playful |
| Wellbeing, habits, fitness, learning, kids, games | Playful | Editorial, Neo-brutalist (except indie games) |
| Social, messaging, dating | Playful; Neo-brutalist for Gen-Z or creator-led | Editorial for chat-heavy screens |
| Media, news, reading, music, podcasts, sports stats | Editorial | Playful on news (bad-news surfaces) |
| Commerce, marketplaces, food, hospitality | Warm premium; Editorial for drops and fashion | Neo-brutalist for mass-market retail |
| Creator tools, dev tools, events, portfolios | Neo-brutalist, Editorial | none strong |
| Productivity, enterprise, form-heavy flows | Warm premium at low `BOLDNESS` | Editorial, Playful |

**On a Mac** the three Mac presets join the table. *Native craft* fits every category except kids and games. *Pro instrument* fits creator, developer and pro tools, finance trading and monitoring, data and admin; it is a poor fit for casual consumer apps. *Document first* fits writing, notes, reading, translation and scripts; it is a poor fit wherever the content isn't text people make or read at length.

The table says which *presets* can belong; it doesn't pick the direction. Good fit is the floor, and the owned idea still decides among the survivors. Each preset file's "Fits / Doesn't fit" lines go into more detail.

Drop every option that fails any of the first three. A category misfit (question 4) is dropped in a non-interactive run; when you can ask, it may stay on the menu with its warning from the table. If none survives, redeal with a new seed (`--seed` any other number) and say so in the report. Then, among the survivors, recommend one: the option that carries an owned idea from the inventory and keeps the identity assets found in 1a. When 1a and the table point to the same preset, prefer its survivor; when they disagree, recommend the category fit and say which existing assets carry over into it, unless the user asked for a rethink. The app's own identity is not the "familiar default" this step guards against; the category's stock look is.
- **If you can ask,** ask once, at most four questions. Put the recommended option first, labelled "(Recommended)", with its one-line reason; every option says, in one line, its composition, the inventory item it would carry, and how it treats the app's existing assets ("keeps the rabbit and the city art", "replaces the rounded faces"). Skip any question the request or the code already answers.
  - **Redesign:** 1. **Direction:** the survivors, recommended first; a poor fit carries its warning. 2. **Keep** (multi-select): the identity assets found in 1a, plus the current layout order. 3. **Scope:** *reskin* (same layout and flow, new skin) · *restructure* (rethink this screen's hierarchy and layout) · *rethink* (question what the screen is for and what belongs on it). 4. **Focus:** what bothers them today, which state matters most (the key alert or error state, empty, loading), or dial overrides next to the sheet's defaults; pick whichever the code leaves least clear.
  - **Build:** 1. **Direction**, recommended first. 2. **Reference app:** "an app whose look you like" instead; map it to the nearest direction. 3. **Dials:** the sheet's defaults, or "louder / calmer / denser / airier". 4. **Audience,** only if the request doesn't say: who it's for, how often they use it, and where (on the move, at a desk).
  - **Spec:** the Build questions, plus which platforms the tokens are for.
- **If you can't ask** (non-interactive run), take the recommendation, keep every identity asset, use *restructure* scope for a Redesign, and state each assumption in one line before the brief, with one line on why the chosen direction beats the others for *this* product. Not the most familiar one: the category default is what this step exists to prevent.

If the user named a preset, deal inside it (`--preset`), even a poor fit: warn them once, in one line, then commit to it.

Then print the full sheet and adopt it. Don't blend it with the layout you would have made anyway:

```bash
python3 <skill>/scripts/deal.py --direction <id> --seed <seed from the deal> [--platform macos]
```

The sheet gives the composition, the idea slot, a dealt type system and palette (light and dark, with measured contrast), shape, signature moves, motion and the way the direction goes wrong. If the brand already fixes colours or typefaces, pass `--keep palette,type` and map the brand onto the roles. Redeal only for a reason you can state (it contradicts the brand, or needs an asset that doesn't exist), and say so in the report. If the script can't run, read `library/directions.json` and pick by the same rules.

The presets behind the directions (native craft, pro instrument and document first are Mac-only; retro is dealt only when the user names it):

| Preset | One-liner | Real-world anchors | File |
|---|---|---|---|
| **Warm premium** | Photo-led, confident type, rich but controlled | Airbnb, Uber, Revolut, Flighty | `references/presets/warm-premium.md` |
| **Neo-brutalist** | Thick strokes, hard offset shadows, flat clashing colour, raw type | Gumroad, Figma, Nothing, Teenage Engineering | `references/presets/neo-brutalist.md` |
| **Playful / toy** | Chunky pressable shapes, springy motion, characters, rewards | Duolingo, Headspace, Finch | `references/presets/playful.md` |
| **Editorial** | Huge display type, magazine grids, stark contrast | Arc, Spotify Wrapped, Nike, NYT | `references/presets/editorial.md` |
| **Native craft** (Mac) | Mac-assed: Mac behaviour everywhere, identity concentrated in one control or owned chrome | Panic Nova/Transmit, NetNewsWire, Things 3, Ivory | `references/presets/native-craft.md` |
| **Pro instrument** (Mac) | Dense, keyboard-first, content centre and controls at the edges, exact readouts | Raycast, Linear app, Logic Pro, iStat Menus | `references/presets/pro-instrument.md` |
| **Document first** (Mac) | The document's typography is the design; chrome disappears while you work | iA Writer, Ulysses, Bear | `references/presets/document-first.md` |
| **Retro** (named only) | A past machine made usable: phosphor terminal, pixel sprites, 1-bit desktop; one grid, integer type sizes, effects off under Reduce Motion | Fallout's Pip-Boy, Balatro, Shovel Knight, Playdate, Obra Dinn | `references/presets/retro.md` |

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
Inventory: <the 8–12 items from step 1b, comma-separated; mark assumptions with (assumed)>
Direction: <dealt id verbatim, e.g. pl-persona, then its name> (seed <n>, or "user-picked preset")   Dials: B<n> M<n> D<n> C<n> F<n>
Kept from the current app: <identity assets carried over and the scope (reskin / restructure / rethink) for a Redesign, or "new app">
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

Want more real examples than the preset file has? See `research/real-ui-references.md`: award winners, design-team case studies, font alternatives, all from shipped apps. For a Mac app, `research/macos-references.md`.

**Commit to the direction.** The dials are a promise to the user. A playful screen at `BOLDNESS 8` should look unmistakably playful in a screenshot. If a principle seems to argue for toning it down, look for a way to satisfy the principle *inside* the style (e.g. make a signifier louder, not the style quieter). Restraint is a dial setting, not a default.

### Icons are part of the signature

Stock icon sets are plumbing: fine for utility chrome (back, close, settings, share, search), and they make everything else look like every other app. Design these glyphs instead of importing them:
- **The core verb's icon:** the check in a habit app, the heart in a dating app, the ticket in a transit app. It's the most-seen glyph in the product, so it gets the most care: a custom shape in the preset's language (chunky rounded stroke, thick square cap, fine serif-like detail…) and an animated state change (draw-on, morph, stamp, pop).
- **Hero and category icons:** tab icons at `BOLDNESS` ≥7, categories, empty-state art, the mascot. Draw them as one family: same stroke weight, corner treatment and fill/duotone logic, all made in code (`Canvas`/`ImageVector` in Compose, `Shape`/`Path` in SwiftUI) or from one commissioned set.
- **System symbols done well count too.** SF Symbols with `.symbolEffect` and variable colour, or Material Symbols with fill/weight axes animated, are legitimate when `FIDELITY` is low. Stock and static, with no styling, is the default look.

- **A mascot: the mascot kit is the required path, not an option.** This applies whenever the screen has a character or creature: one the brief asks for, one implied by "Duolingo-level fun", or one you add as the live thing. Don't draw it freehand in `Canvas`, `Path` or CSS; a freehand mascot comes out as a different drawing on each platform and in the mock, and it can't pass the kit's checks. Instead:
  1. Draw it once as an SVG rig from the direction's primitives and palette (`references/mascot.md`), and save it with the code (e.g. `mascot/dot.svg`).
  2. Generate the code: `python3 <skill>/scripts/mascot.py svg2code mascot/dot.svg --compose|--swift -o <DotMascot.kt|.swift>`. **When the brief names one file for the code** ("put the code in HabitHomeScreen.kt"), use `--into HabitHomeScreen.kt` instead of `-o`: the imports are merged, the code lands in a marked block at the end of that file, and rerunning replaces the block. Animate it by changing the generated pose (`rememberDotPainter(pose)` / `DotMascot(pose:)`), driven by the real state it reacts to.
  3. In the HTML mock, paste the same SVG inline and animate its groups with CSS (`transform-origin` at each `data-pivot`), so the mock shows the drawing that ships.
  4. Run `mascot.py check` (24 px silhouette, squint) and filmstrip its states (step 5). Use `lottie` when the project plays Lottie or the states are authored keyframes (an idle loop, a celebration).

  If the kit can't run here, say so under "Not verified" with the reason; never fall back to a freehand drawing without saying so. An animated hero glyph (the streak flame, the core verb's check) may use the kit the same way. Flat, geometric characters work; painterly or detailed ones don't, and Rive's `.riv` can't be generated, so say so instead of faking it.

The platform files show how to draw and animate custom glyphs.

### 4. Build

Read `references/platform-swiftui.md` or `references/platform-compose.md` (Compose Multiplatform uses the Compose file plus its CMP section). **For a Mac app, read `references/platform-macos.md` as well**: it replaces the thumb-zone, 44 pt and Dynamic Type guidance with window anatomy (`NavigationSplitView`, toolbar, inspector), hover and cursor states, menu-bar commands and shortcuts, Mac type density, vibrancy and the accent colour, plus a macOS code baseline. They show how to implement tokens, custom fonts that still scale, press states, springs, haptics, reduce-motion, and insets idiomatically.

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
4. **Drawn in code from the inventory** (`Canvas` / `Path` / `ImageVector`): the product's objects in one consistent flat graphic language, in the palette's real colours. Better than a placeholder, an enlarged SF Symbol, or an abstract blob. For empty-state art, a character or a hero object, draw it once as SVG and convert it with `scripts/mascot.py svg2code` (`references/mascot.md`), so both platforms get the same drawing; run `mascot.py check` for the 24 px silhouette and squint tests.
5. **Type and colour alone,** for directions built on them.

Never: stock photos of laughing people, AI images passed off as real, illustration from mixed packs, a decorative blob standing in for a picture.

**The brief at rest.** Before styling, list the brief's must-haves for this screen (for a ferry home: next departures, a countdown, buying a ticket) and design so every one is visible in the resting frame, or reachable from a visible control there. Two limits keep the hero honest:
- When the screen's content shapes include `list`, at least three rows (or the whole list, if shorter) show at rest, and the hero takes no more than about 45% of the screen's height.
- Make the key number big inside its region (48–72 pt), not by growing the region. A huge hero that pushes what the user came for below the fold loses to a plainer screen that answers the brief at a glance: it's the most common way a stronger idea lost in our blind evals.

**Ambient screens get one dominant readout.** When the brief says the screen stays open and is glanced at from a distance (a kitchen counter, a desk, a wall, a shop floor), one live value answers the glance: sized to read from two or three metres (64–120 pt in a Mac window, the hero size on a phone) and at least three times the size of anything else live. Never two timers or figures of equal weight, and never a mascot competing with the readout. In round 18 the bake-day screens that lost split attention between two timers, or between a timer and a talking starter; the winners had one huge elapsed timer.

**One moment in time.** Sample data is a single moment. Define one `now` and one data set, and derive every live value from them: timers, countdowns, "since" and "until" times, progress bars, counters, totals. Do this in the preview data and in the mock's script; never type a derived number by hand. Then read the resting frame as the user would: does every number agree with every other (the elapsed time with its bar, "fed 6 h ago" with the clock, "1 of 5 watered" with the rows)? A pair was lost in round 18 to a progress bar, a countdown and a "since fed" that implied three different times of day, and round 17's counter disagreed with its own list.

**Removing slop leaves space. Don't fill it with another ornament.** Fill it with scale (make the main thing bigger, within the limits above), with the full content, or with the owned idea. One deliberate empty moment per screen at most.

### 5. Look at it, fix it, then report

**Gate first: compile, then lint.** Code that doesn't build is not a deliverable, however good the render looks.

- **SwiftUI (iOS or macOS):** typecheck every Swift file you wrote, together, against the iOS simulator SDK, or the macOS SDK for a Mac app (the script detects which from the project and the code; `--platform macos` forces it):

  ```bash
  python3 <skill>/scripts/typecheck.py <changed .swift files or folder>
  ```

  Fix every error and run it again until it passes. **Keep the deployment target.** The script reads it from the project (`Package.swift` platforms, or `IPHONEOS_DEPLOYMENT_TARGET` / `MACOSX_DEPLOYMENT_TARGET` in the `.xcodeproj`) and uses iOS 17 (macOS 14 for a Mac app) when there's neither. An error like "'Tab' is only available in iOS 18.0 or newer" means the code is wrong for the target, not that the target is wrong: wrap the newer API in `if #available(iOS 18, *)` with an iOS 17 fallback, or use the older API (`references/platform-swiftui.md` rule 17). Never pass `--ios` / `--macos` to get past an availability error. Pass it only when the user or the project states a different target, and then name the target and where it came from on the report's Lint line. It needs no Xcode project, so there's no excuse to skip it on a Mac. If it can't run (exit 3: no Xcode, or files that import third-party packages), say so under "Not verified"; never report Swift as compiled when it wasn't.
- **Compose / CMP:** if the project has a Gradle build, compile the module you changed there (`./gradlew :<module>:compileKotlin`, or `compileKotlinIosSimulatorArm64` / `compileDebugKotlinAndroid` for a CMP target). Without one, compile in the skill's throwaway project:

  ```bash
  python3 <skill>/scripts/compile_kotlin.py <changed .kt files or folder>
  ```

  It compiles against Kotlin 2.2.21 and Compose Multiplatform 1.9.0 (Material 3 1.4) for JVM and Android; shared code must compile for both, so Android-only APIs in `commonMain` code fail as they would in a real CMP module. Compose `Res` and Android `R` resources are stubbed, and listed so you can check the real files exist. Fix every error and run it again until it passes. The first run downloads what isn't in `~/.gradle`; if it can't run (exit 3: no JDK 17+, no Gradle, offline), say "Kotlin not compiled" under "Not verified".

Then lint the files you wrote:

```bash
python3 <skill>/scripts/lint.py <changed .swift / .kt files or folder> [--platform ios|macos] [--allow <rule>,<rule>]
```

It flags the slop tells and craft defects the code itself shows (violet accents, stock greys, 5%-black shadows, fixed font sizes, placeholder-only fields, sub-44/48 targets, unlabelled icon buttons, emoji, placeholder data, animation without Reduce Motion) and the code-baseline patterns from the platform files (index-based list identity, `AnyView`, `DispatchQueue` delays, `ObservableObject`, `@MainActor` models in default arguments, lazy `items` without keys, a `LazyColumn` inside `verticalScroll`, `collectAsState()`, typed text in plain `remember`). `--list-rules` shows them all. On macOS (detected, or `--platform macos`) it drops the Dynamic Type and 44 pt checks and adds Mac ones: custom controls with no hover state, an `App` with no `.commands`, a `WindowGroup` with no size limits, iPhone-sized fixed frames, iOS-only APIs and haptics. Fix every `FAIL`. Treat each `WARN` as wrong unless you can defend it in one sentence. `--allow` is for deliberate style choices only (e.g. `blur-shadow` for a warm premium floating sheet); list each one in the report. It's a regex heuristic, so a clean lint proves nothing about taste: that's what the passes below are for.

**Render what you built and look at the image before handing over.** Code that reads well often renders badly: a number clipped by a fixed-width box, a token stretched into a pill by its parent, a tick off-centre, a bar covering content. The user sees those first, and one of them makes a bold design look broken (Tuch et al. 2012: poor execution lowers perceived beauty). Use the best render path available:
1. **Real render:** Compose `@Preview` screenshot tests (Roborazzi/Paparazzi), SwiftUI previews or snapshot tests, or the app on an emulator/simulator (`adb exec-out screencap -p > s.png`, `xcrun simctl io booted screenshot s.png`). **A Mac app:** render the real window from its `#Preview`, with no Xcode project: `python3 <skill>/scripts/render_swiftui.py <files or folder> --out window.png [--size 1280x800] [--appearance dark]`. It compiles your files with a small host, shows the view in a window behind the others for about two seconds, and captures it from the window server (title bar, toolbar, sidebar materials, real controls). Give the screen a `#Preview` that builds it with its sample data, so it can render. Put the font files the design uses next to the code (a `Fonts` folder works): the renderer registers them first, and names any face passed to `Font.custom` that it can't find, because the render then shows the system font in its place. When it and your HTML mock disagree, the render is the truth: in our evals it showed step text truncated with "…", locale-dependent numbers and a detail column pushed off-screen, all of which the mocks hid. Give the render, not the mock, to the blind judge. A built app works too: launch it and capture its window only (`screencapture -o -l <windowID> s.png`, with the id from `osascript -e 'tell application "<App>" to get id of window 1'`), which needs the Screen Recording permission for the terminal; if it is denied, say so under "Not verified". Render it at its **minimum** window size, at a typical size (about 1280×800), and at full screen, in light and dark; a Mac layout that is only good at one size is not done.
2. **Faithful mock:** if you can't run the platform, write an HTML/CSS mock with the same tokens, sizes and layout, and screenshot it headless at phone size (a Mac window: 1280×800, plus the minimum size) with motion settled (e.g. Chromium-based `--headless=new --force-prefers-reduced-motion --window-size=390,844 --screenshot=s.png file.html`; `--size 1280x800` for `filmstrip.py`).
3. **Neither possible:** say clearly in the report that the layout was never seen rendered.

**Render every scrolling screen twice: at rest and scrolled to the end** (on a Mac, also check that the last row isn't hidden by a status bar or bottom toolbar, and that a resized window reflows rather than clips). The resting frame is what people and screenshots see first; the end frame proves the last row clears the pinned bar. On a simulator, swipe to the bottom and screenshot again; in a Compose screenshot test, render a second preview with the list state scrolled to the last item. In the HTML mock, give the scroll container an id and end the file with one line, `<script>if (location.hash === '#end') { const s = document.getElementById('scroll'); s.scrollTop = s.scrollHeight; }</script>`, then render `mock.html` and `mock.html#end` as two frames.

**Record the motion whenever there is some to judge.** Stills can't show motion: a stuck, janky or clipped animation passes every check above, and a good one earns nothing. When `MOTION` is 4 or more, or the core verb or the live thing animates, turn the motion into a filmstrip (frames over time in one image) and look at it:
- **HTML mock:** build the motion with CSS animations or the Web Animations API (motion on `requestAnimationFrame` or timers can't be stepped), and start the motion under test on `#play`, the way `#end` scrolls: `<script>if (location.hash === '#play') document.body.classList.add('play');</script>`. Then run `python3 <skill>/scripts/filmstrip.py mock.html`. It pauses every animation at 0–800 ms (`--times` to change), crops the frames to the area that moves (`--crop x,y,w,h` to choose it yourself), renders them in light mode whatever the machine uses (`--scheme dark` for the dark frames), tiles them into one PNG, and prints how many animations run, the longest finite one in ms and how many loop forever. The two still frames above stay the Reduce Motion view.
- **Compose:** in a UI or screenshot test, set `composeTestRule.mainClock.autoAdvance = false`, trigger the action, and capture a frame after each `mainClock.advanceTimeBy(40)` (`captureRoboImage` with Roborazzi); then `filmstrip.py frames/*.png`.
- **SwiftUI on a Mac:** `screencapture -v -V 3 -l <windowID> motion.mov` (or QuickTime), then the same `ffmpeg` and `filmstrip.py` steps as below.
- **SwiftUI on a simulator:** `xcrun simctl io booted recordVideo motion.mov`, do the action, stop it with Ctrl-C, then `ffmpeg -i motion.mov -vf fps=15 frames/f%03d.png` and `filmstrip.py` on the frames around the action.
- **Mascot or hero glyph (Lottie):** `mascot.py lottie rig.svg motion.json -o m.json`, then `mascot.py preview m.json` and `filmstrip.py m.preview.html --crop 0,0,240,240` once for the reaction (`#play`) and once with `--hash state=idle` for the loop. The preview drives lottie-web from a Web Animations clock, so the strip's numbers are real. Native mascot code animates like any other view: use the Compose or SwiftUI route above. `references/mascot.md` §7 says what to look for.
- **None possible:** write "motion not recorded" under "Not verified".

Read the strip with `references/critique.md` pass 14, and put the numbers on the report's "Live thing" line.

Judge only the pictures, never the code: you wrote the code, so you'll read your intentions into it. If a problem is visible in the screenshot, it's real.

**Craft pass.** Read the image like a picky designer:
- Text clipped, truncated or overflowing its container, especially the biggest numbers at their widest value ("12" vs "365").
- Elements stretched or squashed by their parent (fill-height, flex stretch, `fillMaxSize` in a `Row`).
- Icons and ticks off-centre in their circles or tiles; misaligned baselines.
- Overlaps, content hidden under top or bottom bars, and uneven gaps that break the spacing scale.
- **Anything cut off by a pinned bottom element** (a CTA bar, tab bar, sheet handle or home indicator): a list row sliced in half behind the button is the commonest defect in generated screens, and it was the one most often penalised in our blind evals. Fix it in two places:
  - **Structure, so the last row can scroll clear.** SwiftUI: pin the bar with `.safeAreaInset(edge: .bottom) { bar }` on the `ScrollView`/`List`, not a `ZStack(alignment: .bottom)` or `.overlay(alignment: .bottom)` over it. Compose: put the bar in `Scaffold(bottomBar = …)` and pass the `innerPadding` bottom into the list's `contentPadding`, not a `Box` with `Alignment.BottomCenter` over it. `lint.py` warns (`pinned-bottom-overlap`) when it sees the overlay pattern.
  - **The resting frame, which is what people and screenshots see first.** Content that continues under the bar must read as scroll, not as cut: the bar is opaque with a visible top edge (a tone step, or the platform's scroll-edge effect), and the fold lands in a gap between rows: every row is either fully above the bar or fully under it. A row half-showing above the bar (a "peek"), even 1 pt of a card's top edge, reads as cut, with or without a fade. Our blind judges capped every one of them in four rounds, including a 38-of-72 pt peek with its title intact. A row whose text is cut mid-line at rest is a defect even when the code scrolls correctly; shorten or reorder what's above it.
  - **Fold check: measured, not eyeballed.** A few pixels of card above a tab bar are easy to miss in a screenshot, so for the HTML mock run the gate:

    ```bash
    python3 <skill>/scripts/fold.py mock.html
    ```

    It loads the mock at 390×844 with motion settled and fonts loaded, finds the pinned bar (a buy bar stacked on a tab bar counts as one) and the scrolling container. Every row that comes within 24 pt of the bar's top edge is either **whole** (fully above the bar, or fully under it) or **cut** (any part of it shows above the bar while the rest is under it: a sliver of card, a row sliced through its icon or text). A plain divider line peeking out is fine. It also scrolls to the end and checks that the last row clears the bar by 8 pt, and that the mock scrolls at all. Treat it like the compile gate: fix every `CUT` and `FAIL` and rerun until it says `fold pass`. To fix, move the fold into a gap by tightening or reordering what's above, or by changing a row height or the gap between rows; never grow the hero to push the list down. Pass `--bar` or `--scroll` if it picks the wrong element. Without an HTML mock (a native render only), apply the same rule by eye, row by row, and say in the report that the fold was not measured.
- Depth signifiers (lips, shadows, strokes) that are invisible at their real colours.

**Signature check: does the screen show the direction?** A dealt direction can come out as the category's stock layout in the direction's colours, and nothing above catches that. Using the resting frame only:
- **Point at each signature move from the brief:** name the element and where it sits ("the departure time set at 120 pt fills the top third"), or write "not visible". A move that exists only in code, in another state or after an interaction doesn't count here. At least two must be visible at rest.
- **Stock-layout test.** In one line, describe the screen a competent team would ship by default for this product and category, block by block (for a ferry home: route header, next-departure card, timetable list, buy button). Then write the built screen's blocks in the same way. If the order and proportions match and the only differences are colour, type and corners, the direction is a costume: rebuild the composition from the sheet around a signature move (change what leads, its scale and how the list is set), not the paint.

Fix this before the taste pass, and put both results on the report's "Signature moves" line.

**Blind pass first.** Your own critique knows what you meant to build, so it reads intent into the pixels: in our evals the builds' own critiques passed a stock layout, an orphaned heading, a counter that disagreed with its list and live numbers implying three times of day, and blind judges capped every one. So before your own critique, hand the resting frame (and any other frames you rendered) to a judge that has never seen your code, brief notes or report:

```bash
python3 <skill>/scripts/blind_critique.py screenshot.png [more.png] --brief "<the user's brief in one or two sentences>" --platform ios|android|macos
```

It copies only the images, the brief and `references/critique.md` into an empty folder and runs a fresh headless `claude` judge on them (about a minute, about $0.30). Without a `claude` CLI it prints the hand-off instead: give exactly those files and that prompt to a fresh subagent with no other context. Never judge "blind" yourself; you can't unsee your intent. Treat its three fixes as the first items of your top three, unless one contradicts the brief (say which and why). Put its overall on the report's Critique line.

**Taste pass.** Passing the craft pass means nothing is broken. It doesn't mean the screen is good. Critique the same screenshots with `references/critique.md`: the one-second glance, the squint, the cover-the-logo test, idea reach, sameness, fullness, the thumb, the bottom edge, the motion. Score them, and **write the critique in your reply** in its format, including the scores line. The critique is part of the deliverable, not private working: a run that ends without it hasn't finished step 5. If you couldn't render at all, say so in the reply in place of the critique ("Critique: not run, the screen was never rendered") rather than leaving it out.

Then fix the top three problems across both passes, render again and look again. **Two rounds at most**; report what still falls short instead of looping.

Then run the checks at the end of this file. For each failed check, fix it or, if the style choice deliberately trades it off, keep it and **warn** the user (see Accessibility stance). **End with the report block.** Your final message ends with the block below, filled in. It is a fixed format, not a suggestion: copy the 15 labels exactly, in this order, one per line, inside the fenced block, starting with the `app-ui-slopless report` line. Don't rename, merge, reorder or drop a label, and don't restate it as prose or under your own headings. Fill every field; if one doesn't apply, write `n/a` and why. You may write anything you like before the block (what you built, notes for the user), but the block comes last and stands on its own: some hosts (headless runs, some models) show only the last message, so a step that only appeared mid-run is invisible to the reader. Don't claim a check you didn't run.

```
app-ui-slopless report
Inventory: <the 8–12 items from step 1b, comma-separated; (assumed) where inferred>
Direction: <dealt id, e.g. pl-persona> (seed <n>); deal: <deal.py's Deal line, verbatim>; redeals: <none, or each redeal's Deal line and why>
Owned idea: In this app, <inventory item> becomes <device>.
Competitor test: <competitor> → <why the idea fails for them>
Live thing: <the interaction and the real state it reacts to>; filmstrip: <n animations, longest n ms, n looping, and what the frames show; or "not recorded" and why>
Built: <files, screens, states; the brief's must-haves visible at rest>
Signature moves: <each move → where it shows at rest, or "not visible">; stock layout: <the default screen's blocks> → <what this screen does instead>
Lint: <compile: pass / FAIL / not run and why, at <iOS or macOS> <target> (<from the project / default>); lint n FAIL, n WARN; each --allow and each kept WARN with its reason>
Critique (final round): Idea n · Hierarchy n · Craft n · Substance n · Platform n → overall n (caps: <which, or none>); blind judge before fixes: overall n (or "not run" and why)
Bottom edge: <fold.py: pass / FAIL, or "not measured: no HTML mock">; rest frame <each row at the fold: whole / cut>; end frame <last row clear by n pt>
Still short: <what the critique found and you didn't fix>
Sample content to replace: <names, prices, dates, photos>
Pictures: <each found picture: title, creator, licence, source; the mascot: its .svg and the mascot.py command that made the code; or "none, drawn in code">
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
- **macOS variant (pointer and keyboard):** there is no thumb zone. Primary actions live in the toolbar, in the content, and in the menu bar with a shortcut. A standard control is 22 pt tall (never below 20, and ≥24×24 for icon buttons including padding, WCAG 2.5.8); the whole row is still the click target. Every clickable thing has a hover state, a right-click menu where it has actions, and is reachable by keyboard. Destructive items stay out of the default (Return) action.

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
- **macOS:** a sidebar (`NavigationSplitView`) for top-level navigation and a toolbar for window actions, not a bottom tab bar; hover, cursor and right-click states; a real menu bar with keyboard shortcuts; resizable windows with a declared minimum; fixed system text styles (body 13 pt) and an in-app zoom for content-heavy views instead of Dynamic Type; light, dark and the user's accent colour; translucent sidebars; Settings in ⌘,; undo instead of confirmation. Details: `references/platform-macos.md`.

In Compose Multiplatform, one shared UI is fine. Branch with `expect/actual` (or a platform flag) for the mechanics above when they differ visibly: back affordance, haptics, sheet style, system font fallbacks.

## Breaking conventions

The user is allowed to break platform conventions when the style calls for it, for example a custom bottom bar shaped like a ticket stub, or a bespoke toggle. When you break one:
1. Say which convention, and why the style needs it, in one line in the brief.
2. Keep the *function* the convention protected. A custom tab bar still shows labels, stays visible, and has 44/48 targets. A custom toggle still announces its state to VoiceOver and TalkBack.
3. Never break hard requirements silently: safe areas and insets, system back, text scaling, screen-reader labels (on macOS: visible traffic lights and a draggable title area, a menu bar with the standard commands, keyboard access, VoiceOver labels, Reduce Motion and Reduce Transparency). Breaking one of these gets a ⚠️ warning in the report.

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
- [ ] Intake done: existing look and identity assets read (Redesign, or Build inside an existing app); questions asked once, or assumptions stated.
- [ ] Content shapes named and passed to `deal.py --content` (plus `--platform macos` for a Mac app); every dealt option put through the fit test (content at rest, owned idea, costume test, category fit), misfits dropped, redeal stated if none survived; direction id, seed and the `Deal:` line in the report.
- [ ] Owned-idea sentence passes the competitor test; the live thing is built and reacts to real state.
- [ ] Brief written: direction, dials, what's kept from the current app, owned idea, live thing, persona, 2–3 signature moves.
- [ ] Swift typechecked with `scripts/typecheck.py` on the right platform at the project's deployment target (iOS 17 / macOS 14 when the project sets none), newer APIs behind `if #available`, `--ios` / `--macos` never raised to get a pass; Kotlin compiled with the project's Gradle build or `scripts/compile_kotlin.py`; both passing, or the report says why not.
- [ ] `scripts/lint.py` run on the changed files: no `FAIL`, every `WARN` and `--allow` defended in the report.
- [ ] Scrolling screens rendered at rest and scrolled to the end; `scripts/fold.py` passes on the mock (no cut row, no sliver behind a fade, no section heading orphaned above the bar, the last row clears the bar by 8 pt), or the report says the fold was checked by eye and why.
- [ ] Signature check done on the resting frame: at least two signature moves pointed at, and the screen is not the category's stock layout in new colours.
- [ ] Motion recorded as a filmstrip (`scripts/filmstrip.py`, or test / simulator frames) when `MOTION` ≥ 4 or the core verb animates: it moves, settles on the rest state, clips nothing, and frequent paths finish within 300 ms.
- [ ] Rendered and looked at: no clipped, stretched, off-centre or overlapping elements (or the report says it couldn't be rendered).
- [ ] Blind pass run with `scripts/blind_critique.py` (or a fresh subagent given only the images, the brief and `critique.md`) before your own critique; its fixes taken first.
- [ ] Taste pass written in the reply in `references/critique.md` format (or "Critique: not run" with the reason), top three fixed, at most two rounds; final scores reported.
- [ ] Real content at real density, every state designed, no invented proof; sample content to replace is listed.
- [ ] One moment in time: every live value derived from one `now` and one data set, and the resting frame read for numbers that disagree.
- [ ] An ambient screen (kept open, glanced at from a distance) has one dominant readout at least three times the size of anything else live.
- [ ] Every meter, bar, gauge or pip row shows its own value at rest: different values look different (fill, segments lit, colour step). Three urgencies drawn as the same empty bar is decoration (round 14).
- [ ] The brief at rest: every must-have visible or reachable in the resting frame; with a `list`, three rows show and the hero stays under about 45% of the height.
- [ ] No request to an outside service carried the user's email, name or account; found pictures are credited.
- [ ] Tokens defined once; no stray hex values or magic numbers in the screen.
- [ ] Every interactive element has a visible signifier and a pressed state.
- [ ] Primary action is in the thumb zone; targets are 44/48; destructive actions are isolated. (macOS: primary action in the toolbar and menu bar with a shortcut; controls ≥22 pt; every clickable thing has a hover state and a right-click or keyboard path.)
- [ ] macOS only: root view has a minimum window size and the layout was rendered at minimum, typical and full-screen sizes; sidebar/toolbar/inspector follow `references/platform-macos.md` §2-3; menu commands and shortcuts exist for the daily actions; light, dark and a non-default accent colour checked; no iPhone layout stretched into a window.
- [ ] Type scale of 4–6 sizes, a real display moment, and custom fonts that scale with Dynamic Type / `sp` (macOS: the system text styles, body 13 pt, plus in-app zoom where content is dense).
- [ ] Contrast checked in light and dark (or a warning given); colour never carries meaning alone.
- [ ] Core-verb icon and hero glyphs are custom-designed and animated; stock icons only for utility chrome.
- [ ] A mascot, if the screen has one, was drawn as an SVG rig and generated with `mascot.py svg2code` (`--into` for a single-file brief), never freehand; it passed `mascot.py check` (24 px silhouette, squint) and its states were filmstripped and read with pass 14.
- [ ] Motion matches the `MOTION` dial's row in the motion budget (at 7+: ambient life, press squish everywhere, animated icons); frequent paths ≤300 ms; reduce-motion fallback present.
- [ ] Depth signifiers (lips, strokes, shadows) visible at ≥3:1 against their surface.
- [ ] Native mechanics intact (back, insets, text scaling, screen-reader labels; on macOS: window chrome, menu bar, keyboard access, VoiceOver), or the break is justified.
- [ ] None of the slop tells.
- [ ] The final message ends with the `app-ui-slopless report` block from step 5: all 15 labels verbatim, in order, every field filled (or `n/a` with a reason).
