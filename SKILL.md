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

### 1. Pick the style (preset + dials)

The user chooses the style; never silently default to something safe.

If they named a preset, use it. If not and you can ask, offer the four presets with one line each and let them pick (or name a reference app; map it to the nearest preset and adjust dials). If you can't ask (non-interactive run), pick the preset that best fits the product and audience, state the choice and why in one line, and carry on.

| Preset | One-liner | Real-world anchors | File |
|---|---|---|---|
| **Warm premium** | Photo-led, confident type, rich but controlled | Airbnb, Uber, Revolut, Flighty | `references/presets/warm-premium.md` |
| **Neo-brutalist** | Thick strokes, hard offset shadows, flat clashing colour, raw type | Gumroad, Figma, Nothing, Teenage Engineering | `references/presets/neo-brutalist.md` |
| **Playful / toy** | Chunky pressable shapes, springy motion, characters, rewards | Duolingo, Headspace, Finch | `references/presets/playful.md` |
| **Editorial** | Huge display type, magazine grids, stark contrast | Arc, Spotify Wrapped, Nike, NYT | `references/presets/editorial.md` |

Read **only** the chosen preset's file. It holds the palette strategy, type, shape, depth, motion, signature moves, real examples, and how cheap imitations of that style go wrong.

Then set the **dials** (1–10). Each preset file gives its defaults; the user can override any of them.

| Dial | 1 | 10 |
|---|---|---|
| `BOLDNESS` | quiet, mostly neutral | loud, saturated, oversized |
| `MOTION` | instant, fades only | springy, choreographed, celebratory |
| `DENSITY` | airy, one idea per screen | packed, dashboard-like (Flighty, Bloomberg) |
| `COLOR` | near-monochrome + one accent | full multi-hue palette |
| `FIDELITY` | fully native look (stock HIG/M3 components) | fully bespoke components |

`FIDELITY` controls the *look* of components. Platform *mechanics* (back behaviour, safe areas, text scaling, system gestures) stay native at every setting unless there's a written reason. See "Breaking conventions".

### 2. Write the design brief (before any code)

A short brief keeps the style coherent across every screen, and it's what turns "make it fun" into decisions. Keep it under ~30 lines, and put it in your reply (or in `DESIGN.md` for Spec mode or multi-screen work).

```
Preset: <name>   Dials: B<n> M<n> D<n> C<n> F<n>
Owned idea: <the one metaphor carried through every surface: an airport board, a sky, a character, a camera, a ticket stub>
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

The **owned idea** and **signature moves** are the antidote to slop. Look at what recent Apple Design Award winners share: not polish, but *one strong idea carried through every surface*. Flighty is an airport departure board. Tide Guide's palette follows the sky. Duolingo has its cast of characters. Halide is a film camera. Find the idea in the product's own domain (a transit app might borrow from ticket stubs, platform signage or a split-flap board). Then pick concrete, transferable moves from the preset file (e.g. "every pressable has a 4dp bottom lip that compresses on press"), not adjectives.

Want more real examples than the preset file has? See `research/real-ui-references.md`: award winners, design-team case studies, font alternatives, all from shipped apps.

**Commit to the preset.** The dials are a promise to the user. A playful screen at `BOLDNESS 8` should look unmistakably playful in a screenshot. If a principle seems to argue for toning it down, look for a way to satisfy the principle *inside* the style (e.g. make a signifier louder, not the style quieter). Restraint is a dial setting, not a default.

### Icons are part of the signature

Stock icon sets are plumbing: fine for utility chrome (back, close, settings, share, search), and they make everything else look like every other app. Design these glyphs instead of importing them:
- **The core verb's icon:** the check in a habit app, the heart in a dating app, the ticket in a transit app. It's the most-seen glyph in the product, so it gets the most care: a custom shape in the preset's language (chunky rounded stroke, thick square cap, fine serif-like detail…) and an animated state change (draw-on, morph, stamp, pop).
- **Hero and category icons:** tab icons at `BOLDNESS` ≥7, categories, empty-state art, the mascot. Draw them as one family: same stroke weight, corner treatment and fill/duotone logic, all made in code (`Canvas`/`ImageVector` in Compose, `Shape`/`Path` in SwiftUI) or from one commissioned set.
- **System symbols done well count too.** SF Symbols with `.symbolEffect` and variable colour, or Material Symbols with fill/weight axes animated, are legitimate when `FIDELITY` is low. Stock and static, with no styling, is the default look.

The platform files show how to draw and animate custom glyphs.

### 3. Build

Read `references/platform-swiftui.md` or `references/platform-compose.md` (Compose Multiplatform uses the Compose file plus its CMP section). They show how to implement tokens, custom fonts that still scale, press states, springs, haptics, reduce-motion, and insets idiomatically.

Each platform file ends with a **code baseline** (§8b): stable list identity, state that survives, animating transforms rather than layout, and so on. Follow it, because bold UI that janks reads as broken.

Put tokens first (one theme/token file or block), then components, then the screen. Hard-coded colours and sizes scattered through the screen are how a style decays into slop on screen three.

Apply the core rules below while building. `references/principles.md` has the full rule set with sources; read it for Audit mode or when a judgement call needs backing.

### 4. Look at it, fix it, then report

**Render what you built and look at the image before handing over.** Code that reads well often renders badly: a number clipped by a fixed-width box, a token stretched into a pill by its parent, a tick off-centre, a bar covering content. The user sees those first, and one of them makes a bold design look broken (Tuch et al. 2012: poor execution lowers perceived beauty). Use the best render path available:
1. **Real render:** Compose `@Preview` screenshot tests (Roborazzi/Paparazzi), SwiftUI previews or snapshot tests, or the app on an emulator/simulator (`adb exec-out screencap -p > s.png`, `xcrun simctl io booted screenshot s.png`).
2. **Faithful mock:** if you can't run the platform, write an HTML/CSS mock with the same tokens, sizes and layout, and screenshot it headless at phone size with motion settled (e.g. Chromium-based `--headless=new --force-prefers-reduced-motion --window-size=390,844 --screenshot=s.png file.html`).
3. **Neither possible:** say clearly in the report that the layout was never seen rendered.

Then read the image like a picky designer:
- Text clipped, truncated or overflowing its container, especially the biggest numbers at their widest value ("12" vs "365").
- Elements stretched or squashed by their parent (fill-height, flex stretch, `fillMaxSize` in a `Row`).
- Icons and ticks off-centre in their circles or tiles; misaligned baselines.
- Overlaps, content hidden under top or bottom bars, and uneven gaps that break the spacing scale.
- Depth signifiers (lips, shadows, strokes) that are invisible at their real colours.

Fix what you find and render again. Two passes is normal.

Then run the checks at the end of this file. For each failed check, fix it or, if the style choice deliberately trades it off, keep it and **warn** the user (see Accessibility stance). End with a short list: what you built, the signature moves, any warnings, and anything you couldn't verify (e.g. "not run on device").

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

## Slop tells (check before handing over)

Models produce slop because they sample the statistical average of their training data, which is mostly templates and tutorials (Anthropic calls it "distributional convergence"). If the output shows any of these without a deliberate reason, it has drifted back to that average. Fix it. (Compiled from Anthropic, impeccable.style, taste-skill and designers' write-ups; see `research/real-ui-references.md` §6.)

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

- [ ] Rendered and looked at: no clipped, stretched, off-centre or overlapping elements (or the report says it couldn't be rendered).
- [ ] Brief written: preset, dials, persona, 2–3 signature moves.
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
- [ ] Report lists what was built, the signature moves, warnings, and what wasn't verified.
