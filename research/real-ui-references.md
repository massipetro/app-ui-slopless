# Real, shipped, human-designed mobile UI: reference pack for `app-ui-slopless`

Researched 2026-10-18 with WebSearch and WebFetch. Every URL below was checked with `curl -L` on that date.

**How to read the markers**
- ✅ **Verified.** The URL returned 200 and its content was read (by WebFetch or in search excerpts).
- 🔒 **Bot-blocked.** The URL exists and shows up in search results with matching content, but returns 403/406 to scripted clients. Open it in a browser to check it.
- ⚠️ **Unverified.** The claim comes only from secondary or AI-generated "DESIGN.md"-style pages (shadcn.io/design, open-design.ai, webdesignhot, opendesigner.io), or sources disagree. Treat these as plausible, not fact.
- 🛠 **Implementation suggestion.** The numbers are my starting values for a coding agent. They are **not** measured from the real app.

Quotes are kept under 15 words. Everything else is paraphrased.

---

## 0. Where to look at real screens (not AI concept shots)

| Gallery | What it is | Notes |
|---|---|---|
| **Mobbin** (https://mobbin.com/) ✅ | A searchable library of screenshots and flows from **real shipped** iOS, Android and web apps. The homepage claims ~621k screens. It began as a founder's Dropbox folder of screenshots. | It is the best source for "show me how Airbnb/Duolingo actually does X". It also has an MCP integration for agents. |
| **Page Flows** (https://pageflows.com/) ✅ | Annotated screen *recordings* of real user flows (onboarding, checkout, login) on iOS, Android, web and email. Paid, with a $2.95 3-day trial. | Use it for motion and flow, not just static screens. |
| **Screenlane** (https://screenlane.com/) ✅ | **It now 301-redirects to pageflows.com**, so it has been absorbed into Page Flows. | Don't cite it as a separate source anymore. |
| **Refero** (https://refero.design/) ✅ | A UI/UX reference library. Its homepage doesn't say whether the content is real apps or how much there is. Its sister site `styles.refero.design` publishes per-brand "style references". | Use the screenshots. Treat its generated style write-ups as ⚠️. |
| **Apple "Behind the Design"** (https://developer.apple.com/design/) ✅ | Apple's own long-form interviews with ADA winners and finalists. It is the most reliable primary source for *why* a shipped app looks the way it does. | Cited heavily below. |
| **Apple new-design gallery** (https://developer.apple.com/design/new-design-gallery/) ✅ (redirects to /design/) | Shipped apps adopting Liquid Glass (e.g. Tide Guide). | |

> **Warning about "DESIGN.md" sites.** Many search results for "Brand X design system" are generated token files (shadcn.io/design/*, open-design.ai, webdesignhot.com/design.md, opendesigner.io, blakecrosley.com guides). They often disagree with each other on hex values, fonts and sizes. Don't treat their numbers as ground truth. This file uses them only where marked ⚠️.

---

## 1. Award winners: real apps, with Apple's or Google's stated reasons

### Apple Design Awards (ADA). Official pages verified ✅

| Year | App winners worth studying (category): Apple's stated reason, paraphrased | Source |
|---|---|---|
| **2026** | **grug** (Delight & Fun): daily affirmations written as caveman grunts, with a scribbled, hand-drawn UI and a custom status bar. **Tide Guide** (Visuals & Graphics): Liquid Glass, custom animation, and **palettes that match the sky** through the day. **Moonlitt** (Interaction): SwiftUI moon tracker with deep Liquid Glass integration. **Guitar Wiz** (Inclusivity). **Primary: News in Depth** (Social Impact). Finalists include **(Not Boring) Camera**, praised for a tactile, retro-inspired camera UI. | https://developer.apple.com/design/awards/ ✅ · https://www.apple.com/newsroom/2026/06/apple-reveals-winners-of-the-2026-apple-design-awards/ ✅ |
| **2025** | **CapWords** (Delight & Fun): turns photos of objects into flashcards, with fun animations and real-world sounds. **Feather: Draw in 3D** (Visuals). **Watch Duty** (Social Impact). **Play** (Innovation). Finalist **Vocabulary** was cited for consistent illustration, balanced type and tasteful haptics. Finalist **Denim** was cited for custom haptics and depth effects. | https://developer.apple.com/design/awards/2025/ ✅ |
| **2024** | **Bears Gratitude** (Delight & Fun): huggable characters. **NYT Games** (Delight & Fun, game): redesigned navigation. **Crouton** (Interaction): a recipe app you can use at the counter. **Gentler Streak** (Social Impact): encouraging, non-pushy tone. **Rooms** (Visuals): a nostalgic 8-bit canvas. | https://developer.apple.com/design/awards/2024/ ✅ |
| **2023** | **Duolingo** (Delight & Fun): redesign, quests and leaderboards. **Flighty** (Interaction): Live Activities and Dynamic Island. **Headspace** (Social Impact). **Any Distance** (Visuals): shareable data viz, 3D maps and AR. | https://developer.apple.com/design/awards/2023/ ✅ |
| **2022** | **(Not Boring) Habits** (Delight & Fun): playful haptics and a gamified journey. **Halide Mark II** (Visuals): an uncluttered UI inspired by film cameras. **Slopes** (Interaction). | https://developer.apple.com/design/awards/2022/ ✅ |
| **2021** | **CARROT Weather** (Interaction): humorous forecasts and distinctive visuals. **Pok Pok Playroom** (Delight & Fun): beautiful animation with subtle haptics and sound. **Loóna** (Visuals): type, colour, animation and 3D all tuned to calm. | https://developer.apple.com/design/awards/2021/ ✅ |
| 2017 | **Things 3** won its second ADA (its first was in 2009). | https://en.wikipedia.org/wiki/Things_(software) ✅ |

**Pattern across ADA winners.** What wins is *a single strong idea carried through every surface*: a character, a metaphor such as an airport board, a camera or a sky, or a sound and haptic signature. Polish alone doesn't win. Award text keeps returning to **haptics + sound + custom animation** as the "delight" layer.

### Google Material Design Awards

| Year | Winners | Source |
|---|---|---|
| 2016 | Asana (Brand Infusion), Fabulous (Charming Engagement), C Channel (Creative Navigation) | https://9to5google.com/2016/10/19/google-material-design-awards-for-2016-winning-android-apps/ ✅ |
| 2018 | KptnCook (Expression), Lyft (Innovation), Simple Habit (Experience), Anchor | https://www.phonearena.com/news/Google-names-four-apps-as-its-2018-Material-Design-Award-winners_id110613 🔒 |
| 2019 | Trip.com (Universality), Ruff (Theming), Reflectly (Innovation), Scripts (Experience) | https://www.androidcentral.com/here-are-winners-2019-google-material-design-awards ✅ |
| 2021 | Todoist (large screens). The 2021 round had awards for large screens, dark theme and motion. | https://www.xda-developers.com/material-design-award-winners-2021/ ✅ |

⚠️ I found no Material Design Award rounds after 2021. The programme appears to be dormant (unverified).

### Webby and Awwwards
- **Webby** has "Best Mobile Visual Design – Aesthetic/Function" categories (https://winners.webbyawards.com/ ✅). I couldn't confirm a specific 2025 *native app* winner in those categories from search results. Browse the winners site directly. One example: Tappytoon was a Webby Honoree in Best Visual Design – Function in 2026 (via a BusinessWire release, not opened).
- **Awwwards** (https://www.awwwards.com/ ✅) is overwhelmingly web, not native mobile. Use it for editorial and brutalist type ideas, not for mobile patterns.

---

## 2. Preset 1: Warm premium (photo-led, confident type, rich but controlled)

### Exemplar apps

**1. Airbnb (2025 Summer Release, "dimensional" redesign)**
- **What's distinctive:** Airbnb brought in a dimensional design system: an animated interface plus new **3D iconography** made in-house. The team built up the icons over roughly two years. VP of Design Teo Connor called them utility-rich, "a universal language", and playful. The edges are rounder and softer and the motion is subtle. Coverage frames it as a deliberate move back toward depth and texture, away from flat design. A July 2025 follow-up previewed a new system covering typeface, navigation, layout, colour, cards and icons. Back in 2024, Connor stressed prototyping on device early. His point was that you only know a design works when you play with it on a phone.
- **Category bar (2022 onward):** a horizontally scrolling row of illustrated category icons (Castles, Design, Beach…) heads search. Airbnb launched it with 50+ categories in the 2022 Summer Release.
- **Type:** **Airbnb Cereal**, custom-made with Dalton Maag in 2018. It has six weights (Light→Black), a tall x-height, and a Book weight tuned for small UI text. The team said they wanted it "playful, open, and simple".
- Sources: https://www.itsnicethat.com/articles/airbnb-app-redesign-140525 ✅ · https://news.airbnb.com/product-releases/airbnb-2025-summer-release/ ✅ · https://designcompass.org/en/2025/07/04/airbnb-new-design-system/ ✅ · https://dive-club.beehiiv.com/p/shiny-grills ✅ (2024 interview summary) · https://news.airbnb.com/2022-summer-release/ ✅ · Cereal: https://www.itsnicethat.com/news/airbnb-cereal-typeface-font-dalton-maag-graphic-design-150518 ✅, https://eyeondesign.aiga.org/airbnbs-new-typeface-is-a-case-study-in-unified-accessible-design/ ✅
- Note: the classic Airbnb Design essays (`airbnb.design/building-a-visual-language`, `airbnb.design/working-type`) now 302-redirect to airbnb.com and **return 404**. Don't link them.

**2. Uber (2018 brand redesign + Base design system)**
- **What's distinctive:** near-monochrome black and white, with colour used sparingly. The custom **Uber Move** typeface comes in Display (headlines) and Text (body) cuts. It was drawn by MCKL/Jeremy Mickel under Wolff Olins direction (⚠️ attribution comes from a secondary source). The brand system has 9 named elements, including type, colour and motion. The map does the visual work, and the chrome stays quiet.
- Sources: Uber's design page `https://www.uber.com/<locale>/careers/design/work/2018-redesign/` 🔒 (it is in the search index across many locales, but returns 404/406 to scripted fetches). Base Web, Uber's open-source React implementation of Base: https://baseweb.design/ ✅ · https://github.com/uber/baseweb ✅. Token values (e.g. accent blue #276EF1, motion durations of ~100/200/350 ms) ⚠️ come from Base Web/third-party reconstructions.

**3. Monzo (2024–25 visual refresh)**
- **What's distinctive:** **hot coral** leads, with deep navy and soft white in support and teal/pink/blue/yellow-green/orange as accents. **Oldschool Grotesk** is the hero face, picked for its warm, bold curves. **Monzo Sans**, a custom cut of Universal Sans, handles functional text. Photography uses warm hues, sunny light flares and dramatic shadows. Illustrations replaced generic flat corporate people with characters: a coral circle, an exclamation mark, a googly-eyed star. They also deliberately **"exaggerate" app UI elements** (trend charts, budget controls, bill split) in marketing to add impact.
- Sources: https://monzo.com/blog/weve-had-a-little-makeover ✅ · https://community.monzo.com/t/we-ve-given-our-visual-brand-a-refresh-q-a-w-jesse-senior-brand-designer/139681 ✅ (designer Q&A: coral = warmth/empathy)

**4. Revolut (Revolut 10, Oct 2023)**
- **What's distinctive:** Revolut called Revolut 10 its biggest redesign. It added a customisable home screen with widgets, themes and custom backgrounds, plus "Pockets" sub-accounts. The look is dark and confident, with heavy display type and photography or cards as hero.
- Sources: https://www.revolut.com/news/revolut_launches_revolut_10_as_it_targets_primary_accounts_and_passes_35m_customers_worldwide 🔒. ⚠️ Type (Aeonik Pro for display, Inter for body, 136 px hero) comes only from third-party DESIGN.md pages. Revolut publishes no official design system.

**5. Robinhood (2024 rebrand, by Porto Rocha)**
- **What's distinctive:** a serif (**Martina Plantijn**) for headlines balances a new sans (**RH Phonic**) whose ink traps add character. One electric yellow-green, **Robin Neon**, pops against black, white and muted neutrals. That is a deliberate rejection of competitors' rainbow palettes. Photography is **luxury-fashion-style close-up still lifes** of single objects (an egg for returns, chains for crypto), shot by Lauren Bamford. Illustration is a technical style drawn from financial charts.
- Source: https://www.portorocha.com/robinhood ✅ (agency case study). ⚠️ COLLINS' earlier work calls the sans "Capsule Sans", so naming is inconsistent across eras.

**6. Flighty (ADA 2023 Interaction)**
- **What's distinctive:** it borrows airport-signage conventions. Founder Ryan Jones points out that departure boards use **one line per flight** and have refined what matters over ~50 years. Key information is always visible through Live Activities, the Dynamic Island and widgets. Once the plane pushes back, the Island switches to a **simple circular progress timer** that keeps working with no connectivity. The team sketches **20 concepts** per feature to avoid reaching for stock assets. Jones's goal: work so well it feels "almost boringly obvious".
- Source: https://developer.apple.com/news/?id=970ncww4 ✅ · award: https://developer.apple.com/design/awards/2023/ ✅

**7. Things 3 (Cultured Code, ADA 2017)**
- **What's distinctive:** restrained, white, typographic, and very calm. The signature interaction is the draggable **Magic Plus** button. Drop it into a list to insert a to-do at that exact spot, or onto a day to schedule it. Motion is quick, with little friction.
- Source: https://en.wikipedia.org/wiki/Things_(software) ✅ (Magic Plus details come from 9to5Mac/MacStories coverage cited in search results).

**8. Tide Guide (ADA 2026 Visuals & Graphics winner)**
- **What's distinctive:** a polished data app whose aqua palette **shifts to match the sky through the day**. It uses full-screen hour-by-hour charts and Liquid Glass reacting to chart interaction.
- Source: https://developer.apple.com/design/awards/ ✅

### Transferable design moves (agent-implementable)
1. **One hero image or object per screen, edge to edge.** It is photography in Airbnb/Robinhood, the map in Uber. UI chrome sits on top in neutral black and white and never competes with it. 🛠 Image corner radius 12–20 dp with type *below* the image, not overlaid. Use overlay text only with a real scrim.
2. **A custom-feeling display face with a tall x-height, one family, 2–3 weights.** That's Cereal, Uber Move, Oldschool Grotesk. Pair it with a quiet text cut. Don't mix 3 families.
3. **One owned accent colour, used like a signature.** Monzo coral, Robin Neon, Uber's near-absence of colour. 🛠 Put the accent on ≤10% of pixels: primary CTA, selected state, one data highlight.
4. **Dimensional, custom icons for *navigation categories only*** (Airbnb 3D icons, 2022 category bar). Keep system icons (SF Symbols / Material Symbols) for utility actions. 🛠 Horizontally scrolling category row: 24–32 dp illustrated icon over an 11–12 sp label. The selected item gets a 2 dp underline and full-opacity label, the rest sit at 60–70% opacity.
5. **Light and shadow as warmth.** Monzo's flares and dramatic shadows, Airbnb's soft depth. 🛠 Use one directional, low-blur, slightly tinted shadow. Avoid generic `0 4 12 rgba(0,0,0,.1)` on everything.
6. **"Exaggerated UI" moments.** Blow up the one number or control that matters, like Monzo's budget control or Cash App's amount. 🛠 Make the key numeral 48–72 sp in a tabular-figure display weight.
7. **The airport-board rule for dense status (Flighty).** One row per entity, fixed columns, status as colour plus word. Use tabular figures, and keep the layout identical when data changes.
8. **Prototype the motion on device** (Airbnb). 🛠 Use spring-based transitions that keep spatial continuity: a card expands into the detail screen with a shared element.
9. **Draggable creation affordance** (Things' Magic Plus). It shows that a premium feel can come from an interaction, not ornament.

### Anti-patterns: what makes a fake "premium" feel cheap
- Stock photos of laughing people, or AI-generated photography. The style relies on *specific, art-directed* imagery: Robinhood's single-object still lifes, Monzo's warm flares.
- Gradient-on-everything "luxury" (purple→blue, gold gradients). Real examples use **flat colour plus photography**.
- Three or more accent colours. That breaks the "one owned colour" rule.
- 3D icons used everywhere, including utility actions, or mismatched 3D packs from different sources. Airbnb confines them to a consistent, in-house set.
- Thin, light-grey body text to look "elegant". It kills contrast, and these brands keep body text dark.
- Glass or blur cards on top of photos for every surface. One glass layer reads as intentional. Five reads as a template.
- Even, monotonous spacing with every card the same height. Premium layouts vary scale: one big hero, then dense supporting rows.

---

## 3. Preset 2: Neo-brutalist (thick borders, hard offset shadows, clashing flat colour, raw type)

> **Honest finding:** *fully* neo-brutalist **native mobile apps** are rare among well-documented shipped products. Most canonical examples are web or brand (Gumroad, Figma). The mobile references below are a mix of true neo-brutalist work and **adjacent "raw/industrial"** apps that share the ethos: honest controls, monospace or dot type, hard edges, no soft shadows. I flagged which is which. To find real mobile screens, search Mobbin for the brands below.

### Exemplar apps and products

**1. Gumroad (2021 relaunch; web + iOS/Android apps): true neo-brutalist**
- **What's distinctive:** it moved from polished SaaS to **thick black outlines, flat pastel or hot-pink fills, hard unblurred offset shadows**, and oversized type. The redesign was polarising, and it made the brand instantly recognisable.
- Sources: https://madegooddesigns.com/neobrutalism-web-design/ ✅ · live product: https://gumroad.com/ ✅. ⚠️ The specific fonts (ABC Favorit) and a 2021 credit to a designer come from generated style pages. One guide reports the *current* gumroad.com homepage no longer serves box-shadows, so check it live.

**2. Figma (2019 brand refresh, led by Tori Hinn per UX Collective): neo-brutalist brand**
- **What's distinctive:** it drops shadows for **sharp dark outlines around flat shapes**, clashing orange and yellow, and high-contrast colour blocks. It is often credited as one of the first big design-tool brands to adopt the look.
- Sources: https://uxdesign.cc/neubrutalism-is-taking-over-the-web-e9d09e0fe441 🔒 · https://madegooddesigns.com/neobrutalism-web-design/ ✅

**3. Nothing (Nothing OS / Nothing X app): industrial-raw**
- **What's distinctive:** the **dot-matrix typeface Ndot (Ndot55/Ndot57)** with a monochrome base. Dot-built widgets and a dot unlock animation. Widgets act as controls, not decoration. When OS 3.0 removed the dot font from much of the UI, users pushed back. Nothing staff admitted they "went a bit too hard" and restored it as an option. OS 4.0 reportedly moves system text to Geist and keeps dot type for character moments (⚠️ from a community post).
- Sources: https://nothing.community/d/104-ndot57-the-nothing-typeface ✅ · https://nothing.community/d/15941-nothing-os-30-dont-remove-the-dot-font ✅ · https://nothing.community/d/61774-nothing-os-evolution ✅ · https://www.androidauthority.com/nothing-os-3-hands-on-3488739/ 🔒

**4. Teenage Engineering (OP-1 / field UIs, companion apps, website): industrial-raw**
- **What's distinctive:** **monospace type everywhere** (product, packaging, web, docs). Chrome is black, white and a few greys, and the *product* supplies the colour. Mode screens take over the full display, with no permanent nav chrome. The constraint of a small screen plus 4 knobs drives the interface.
- Sources: https://teenage.engineering/ ✅ · https://teenage.engineering/products/op-1 ✅. ⚠️ The analysis of the type system and greys comes from third-party guides (blakecrosley.com), not TE.

**5. grug (ADA 2026 Delight & Fun winner): raw/anti-polish**
- **What's distinctive:** a **scribbled, hand-drawn, childlike interface** with a custom status bar. The copy is caveman grunts. It shows raw, unpolished visuals can win Apple's top award when they're fully committed. It was made by Ocho (Netherlands), a tiny team.
- Sources: https://developer.apple.com/design/awards/ ✅ · https://www.apple.com/newsroom/2026/06/apple-reveals-winners-of-the-2026-apple-design-awards/ ✅

**6. Halide Mark II (ADA 2022 Visuals): industrial/tool-honest (adjacent)**
- **What's distinctive:** Lux framed it as a camera, not an app. Gestures become muscle memory, like camera dials. Controls are reachable one-handed and look like physical controls. Halide Mark III (2026) moved to Liquid Glass, but the Mark II design stays selectable.
- Sources: https://developer.apple.com/design/awards/2022/ ✅ · https://www.lux.camera/introducing-halide/ ✅

**7. Rooms (ADA 2024 Visuals): pixel-raw (adjacent)**
- **What's distinctive:** a nostalgic **8-bit** building canvas. It commits to low-res as an aesthetic.
- Source: https://developer.apple.com/design/awards/2024/ ✅

Implementation kit reference: **neobrutalism.dev** (https://neobrutalism.dev/ ✅), an open-source component set. It is useful for exact border and shadow conventions on web.

### Transferable design moves
1. **Hard offset shadow, zero blur, and press equals "squash into the shadow".** 🛠 Border 2–3 dp solid #000. Shadow offset 4–6 dp x and y, blur 0, colour #000 *or* an accent. On press, translate the element +4 dp x/y and set the shadow to 0, so it visibly sinks. In Compose, draw a solid offset rect behind the element. On iOS, use a background shape offset by 4 pt.
2. **Every interactive thing *looks* like a control** (madegooddesigns): visible borders on inputs, toggles and checkboxes drawn as graphic objects. Controls never fade into flat text.
3. **Flat, saturated, clashing fills on an off-white base**, no gradients and no transparency. 🛠 Use a base #FFFDF5 or pure white, black ink, and 2–3 accents from different hue families (e.g. #FF90E8 pink, #FFC900 yellow, #23A094 green). Assign them per section, not randomly.
4. **Radius 0 to 4 dp.** Adding big radii is the #1 way the style gets diluted.
5. **Type: an oversized grotesque or condensed display, plus monospace for metadata** (JetBrains Mono, IBM Plex Mono, Space Mono). Teenage Engineering-style: monospace for *everything* in tool UIs. Nothing-style: a dot-matrix display face reserved for numbers, clocks and hero labels.
6. **Full-screen modes with no persistent chrome** (Teenage Engineering). On mobile, that means one task per screen and a big, bordered back or close button.
7. **Visible grid, honest structure.** Use 2 dp rules between rows instead of soft cards. Lists look like tables.
8. **Raw hand-drawn layer** (grug). If you go raw, make *everything* hand-drawn, including the status bar, so it reads as committed and not unfinished.

### Anti-patterns: cheap imitation
- **Rounded-xl cards plus a blurred shadow plus a black border.** That's "soft brutalism", the most common fake. Blur is the giveaway.
- Neo-brutalist *skin* on a generic layout: three bordered feature cards in a row and a centred hero.
- Random clashing colour with no system (a different colour per card for no reason). Real examples assign colour by role or section.
- Unreadable contrast: white text on #FFC900, or pink on yellow. madegooddesigns flags saturated combos failing WCAG.
- Using it in the wrong context. The source calls it untrustworthy for finance, aggressive for anxious health users, and alienating for government.
- Monospace for long body copy on mobile. Teenage Engineering gets away with it because the copy is terse labels.
- Dot-matrix type for running text. Nothing itself retreated from that, and it reads as gimmick.

---

## 4. Preset 3: Playful / toy-like (chunky shapes, bouncy motion, mascots, gamification)

### Exemplar apps

**1. Duolingo (ADA 2023 Delight & Fun)**
- **Shape language (Duolingo's art blog):** shapes are built from a *few* simple vector forms, rounded and friendly rather than pointy, using "the fewest details needed". Exaggeration is combined with **rhythm**, a deliberate variety of shape sizes. Colours are bright and vibrant, framed by white negative space so art never fights the UI.
- **Characters:** a recurring cast (Duo, Lily, Oscar, Eddy…). VP of design Ryan Sims: "Fun is the most important part of the work we do." Small character reactions reward correct answers.
- **Rive state machines:** characters are animated in **Rive**, with 20+ mouth shapes (visemes) per character driven by phoneme timing from the speech models. Idle states blink, nod and move eyebrows, and final states react to right or wrong. For Lily's video call, 8 head × 8 body idle animations give 64+ neutral variations, so loops don't repeat. Reactions include a lean-in when listening and an exaggerated eye-roll when unimpressed.
- **Celebration:** for streak milestones, Duo transforms into a **phoenix**, like a video-game power-up. They replaced number balloons, which they judged too low-energy, and tuned the timing over several rough animation passes.
- **Widget:** Duo looks increasingly panicked as midnight approaches with the lesson undone. A set of ~25 exaggerated poses is planned. The widget shows **only** the streak and whether it's at risk.
- **Core tabs refresh:** they dropped most containers in favour of whitespace and used bold, high-contrast header bars with tiered header sizes.
- **Sound and haptics:** the app ships "Sound effects" and "Haptic feedback" toggles under Lesson experience. The design team lists micro-interactions, copy and **sound** as part of personality.
- **Signature 3D button "lip":** ⚠️ widely described (a darker bottom edge of ~4 px that disappears as the button moves down 4 px on press), but I found **no official Duolingo source**. The descriptions come from generated design-system pages. It's observable in the shipped app via Mobbin.
- Sources: https://blog.duolingo.com/shape-language-duolingos-art-style/ ✅ · https://developer.apple.com/news/?id=jhkvppla ✅ · https://blog.duolingo.com/world-character-visemes/ ✅ · https://rive.app/blog/duolingo-s-ai-powered-video-call-brings-lily-to-life ✅ · https://blog.duolingo.com/streak-milestone-design-animation/ ✅ · https://blog.duolingo.com/widget-feature/ ✅ · https://blog.duolingo.com/core-tabs-redesign/ ✅ · https://blog.duolingo.com/duologues-design-conversations/ ✅
- Note: `design.duolingo.com` (the old public brand guidelines) now **redirects to the blog's design hub**. The old typography and colour pages are gone.

**2. Headspace (ADA 2023 Social Impact; 2024 rebrand with Italic Studio)**
- **What's distinctive:** signature **orange**, warm friendly illustration, and an orange smiley that now shows **a range of moods** (stress, sadness, contentment), not just joy. Breath-driven animation is central. The custom typeface is a "Headspace-ified" **Aperçu** by Colophon, built to flex "from playful to clinical". Navigation was simplified to a **Today** tab with morning, afternoon and night one-tap activities: "simplicity at the surface".
- Sources: https://developer.apple.com/news/?id=fkfnhq8u ✅ · https://www.itsnicethat.com/articles/italic-studio-headspace-graphic-design-project-250424 ✅

**3. (Not Boring) Habits by Andy Works (ADA 2022 Delight & Fun)**
- **What's distinctive:** the checkbox is an **explosive 3D event**. You must press and hold longer than expected, with a hold-progress cue added after testing. It stacks ~6–7 effects, custom **sound** and custom **haptics**. Animations are authored in Blender and rendered in SceneKit, while standard controls stay off-the-shelf. The habit journey is framed as a 66-level game with a "Summit" and a "final battle". Andy Allen: "We went all out."
- Source: https://developer.apple.com/news/?id=9ab1g4r3 ✅

**4. CARROT Weather (ADA 2021 Interaction)**
- **What's distinctive:** a sarcastic robot persona with selectable personality levels (Professional → Snarky → Overkill) and political "views". Dense, serious weather data sits under humorous copy. One developer (Brian Mueller) designs, illustrates and writes the jokes.
- Source: https://developer.apple.com/design/awards/2021/ ✅. Persona details come from reviews in search results.

**5. Pok Pok Playroom (ADA 2021 Delight & Fun)**
- **What's distinctive:** art that is **hand-drawn and hand-animated, not vector**. There's a rule that everything may "jitter a little", which hides imperfection and adds life. Every sound was recorded from real objects (wooden blocks, kitchen pots). The musical section has a consistent mapping, e.g. blue = C, circle = sine wave. Apple credits its "subtle haptics".
- Sources: https://developer.apple.com/news/?id=5bcex7xf ✅ · https://developer.apple.com/design/awards/2021/ ✅

**6. Bears Gratitude (ADA 2024 Delight & Fun)**
- **What's distinctive:** the **art came first**: the app was built around hundreds of existing hand-drawn bear illustrations. Journaling prompts are **flip cards** swiped left and right, which the team admits is nonstandard but users did it instinctively. There's **no sign-in screen**, prompts are written in the user's voice, and it uses a beige base. "The art is the heart of everything we do."
- Source: https://developer.apple.com/news/?id=i74v3f4r ✅

**7. Gentler Streak (ADA 2024 Social Impact)**
- **What's distinctive:** an abstract mascot, **Yorhart** ("your heart"), and colourful, approachable charts. The copy encourages rather than pushes, and you compare against your own history, not other people's.
- Source: https://developer.apple.com/news/?id=3m0ht22s ✅

**8. Opal (screen-time app; ADA 2025 Social Impact finalist per its own job listing ⚠️)**
- **What's distinctive:** a **gem** metaphor. Users are called "gems", and the gem is meant to grow brighter and more intricate as focus improves, with a milestone "reveal" moment. They note iOS Screen Time sandboxing limited the animation.
- Sources: https://opalapp.com/blog/the-milestone-reveal-moment ✅ · https://opalapp.com/blog/designing-for-wellbeing ✅

### Transferable design moves
1. **The 3D "lip" button that compresses on press** (Duolingo-observed ⚠️). 🛠 Fill colour with a bottom "lip" of the same hue at ~20% darker, 4 dp tall, radius 12–16 dp. On press, translate y +4 dp and collapse the lip to 0 over 60–80 ms, plus a light haptic (`UIImpactFeedbackGenerator(.light)` / `HapticFeedbackType.LongPress` or `performHapticFeedback(KEYBOARD_TAP)`). Release with a slight overshoot spring (damping ~0.6).
2. **Shapes from 3 primitives** (rounded rect, circle, rounded triangle), all corners rounded, and **rhythm**: vary sizes deliberately (one big, two medium, many small).
3. **A mascot with a state machine, not a GIF** (Duolingo, Rive). 🛠 Define inputs like `isCorrect`, `isIdle`, `streakAtRisk` and `celebrate`, and give it ≥3 idle variants so loops don't feel canned. Use Rive's iOS/Android runtimes. Tie mascot mood to *real app state* (Duolingo's widget panics as the deadline nears).
4. **Make the core verb a celebration** (Not Boring checkbox, Duolingo phoenix). Pick ONE primary action and give it layered feedback: scale burst, particles, sound and haptic. Keep everything else calm. 🛠 A press-and-hold with a visible progress ring (≈400–600 ms), then a confetti or particle burst, a success sound, and `.success` notification haptics.
5. **Sound design as a first-class asset.** Record real objects (Pok Pok). Ship **several slightly different variants of each click**, a game-audio trick Andy Allen discusses, so repetition doesn't grate. Always give the user a toggle (Duolingo has separate sound and haptics toggles).
6. **Hand-drawn jitter** (Pok Pok): a subtle frame-to-frame wobble on illustrated elements gives life cheaply. 🛠 Cycle 2–3 hand-drawn frames at 8–12 fps ("boiling line").
7. **Personality in copy, scaled by user choice** (CARROT's personality slider, Gentler Streak's gentle tone).
8. **Gamified structure that maps to real progress**: Duolingo's single path, Not Boring's 66 levels, Opal's growing gem. Not points for points' sake.
9. **Let illustration lead the IA** (Bears Gratitude): design screens around the art you have, not the reverse.

### Anti-patterns: cheap imitation
- **Generic emoji or stock 3D blobs as "mascot".** A mascot needs a defined personality, expressions and states.
- Bounce or elastic easing on *every* element, including routine dialogs and navigation. impeccable.style lists it as an AI tell. Real apps reserve big motion for the celebration moment.
- Confetti on trivial actions. It dilutes the reward (Duolingo celebrates milestones, not every tap).
- Rounded everything with the same radius *and* pastel-only palettes. That reads as children's template. Duolingo uses **vibrant** saturated colour with strong contrast.
- Lottie files from different artists mixed together. Styles clash, so one illustration system is mandatory.
- Sounds with no off switch, or the same sample replayed identically 50 times.
- Guilt-trip copy pretending to be playful. Gentler Streak's success comes from *not* pushing.

---

## 5. Preset 4: Editorial / expressive type (huge display type, magazine layouts)

### Exemplar apps

**1. Spotify: Wrapped + Spotify Mix typeface**
- **Spotify Mix (2024, with Dinamo):** a variable typeface with a **width axis from condensed to extended**, plus weight. It has a "transmitter" shape in the counters of p/b/d, subtle flicks and diagonal cuts, four numeral sets, and straight alternates for stricter tone. Condensed suits tall, narrow screens and extended suits wide ones. It is designed to animate, and it replaced Circular across app, web and wordmark.
- **Wrapped 2022:** interlocking "monogram" shapes on a **16×16 grid** act as backgrounds and as containers for data and imagery.
- **Wrapped 2023:** free-flowing, layered forms, including pixelated early-internet shapes, with a layering system that turns elements up or down. It was described as untamed and playful.
- **Criticism worth learning from:** Wrapped 2021 was called out for squashed text and imagery that didn't integrate.
- Sources: https://www.itsnicethat.com/articles/spotify-dinamo-new-typeface-spotify-mix-project-230524 ✅ · https://www.itsnicethat.com/features/spotify-wrapped-campaign-identity-2022-graphic-design-301122 ✅ · https://www.itsnicethat.com/features/spotify-wrapped-campaign-identity-2023-graphic-design-301123 ✅ · https://fontsinuse.com/uses/63891/spotify-2024-redesign ✅

**2. NYT Games (ADA 2024 Delight & Fun winner)**
- **What's distinctive:** the 2024 redesign turned a crossword app into a games hub. New game cards show **progress state** (Spelling Bee, Wordle, Crossword, Mini) and surface archives in the feed, with streamlined typography and clearer per-game brand icons. Each game has its own colour and glyph identity inside one editorial frame. It inherits NYT's serif heritage (Cheltenham, Karnak, Franklin). ⚠️ Exact app fonts weren't confirmed by any source.
- Sources: https://developer.apple.com/design/awards/2024/ ✅ · https://techcrunch.com/2024/03/07/nyt-games-redesigned-app-boost-discovery-simplify-navigation/ ✅

**3. Nike SNKRS**
- **What's distinctive:** product drops presented as **editorial stories**: full-bleed hero photography, a near-monochrome UI where the product supplies the colour, and huge condensed uppercase headlines. Instrument stripped the experience back to the shoe to speed up checkout.
- Sources: https://www.instrument.com/work/snkrs ✅. ⚠️ Fonts conflict across sources ("Nike Futura ND" vs "Trade Gothic" for SNKRS). Rally's case study domain no longer resolves.

**4. Wise (2023 rebrand, by Ragged Edge)**
- **What's distinctive:** it rejected fintech blue for **green as the core colour**. **Wise Sans**, a bespoke typeface inspired by scripts from around the world, is used very heavy and large for display. The Fast Flag icon was recrafted, and the icon and illustration library was rebuilt from scratch and tested globally.
- Sources: https://www.creativereview.co.uk/wise-rebrand-ragged-edge/ ✅ · https://raggededge.com/work/wise/ ✅ (redirects to /partnerships/wise). ⚠️ Hex values (#9FE870 bright green, #163300 forest) and "weight 900 display" come from secondary pages.

**5. Cash App (late-2025 design language + "Moneybot")**
- **What's distinctive:** a brighter, **fluorescent green**, a custom **Cash Sans**, 650+ new icons, 3D graphic elements on a structured grid, user-specific visuals on payment and card screens, and custom micro-animations. The amount-entry screen with giant numerals is the archetypal "exaggerated number" move.
- Sources: https://designcompass.org/en/2025/12/03/cash-apps-new-design-language-and-ai-moneybot/ ✅ · https://www.abduzeedo.com/cash-apps-new-design-language-and-ai-assistant-moneybot ✅. ⚠️ The Cash Sans designer credit and hex values are unverified.

**6. Any Distance (ADA 2023 Visuals & Graphics)**
- **What's distinctive:** workouts become **shareable poster cards**: the route and stats in a "fun font", the user's photo in an **oval mask** (which became a brand trait), and animated 3D route maps (ARKit/SceneKit/MapKit). Route clipping is on by default for privacy. The background is a Metal-rendered gradient "swirly thing". Founder Luke Beard on SF Symbols: Apple's greatest contribution to design.
- Source: https://developer.apple.com/news/?id=uiiopcl8 ✅

**7. Arc Search (The Browser Company)**
- **What's distinctive:** "Browse for Me" generates a **custom article page** for each query: image carousel, then a short answer, then a summary of the top results, then a detailed breakdown. Navigation is swipe-first and the keyboard is up immediately on launch. Lead designer Karla Mickens framed the goal as cutting clutter.
- Source: https://www.inverse.com/tech/arc-search-ios-app-interview-lead-designer-engineer ✅. ⚠️ The Browser Company shifted focus to Dia in 2025 (secondary source), so Arc Search's future is uncertain.

**8. Robinhood** (also in Warm Premium): serif **Martina Plantijn** headlines plus the Phonic sans, luxury still-life photography, one neon accent. https://www.portorocha.com/robinhood ✅

### Transferable design moves
1. **Type is the image.** 🛠 Hero headline at 48–96 sp, line-height 0.9–1.0, tracking −2% to −4% for heavy grotesques. Let it **break onto 2–4 lines deliberately**, setting manual line breaks per screen size, and allow it to bleed off the edge or crop.
2. **Use a variable width axis as an expressive tool** (Spotify Mix). Condensed for tall phone layouts, extended for short wide moments, and animate width or weight on transitions. OFL options with width axes: **Bricolage Grotesque** (wdth + opsz), **Anybody** (wdth), **Big Shoulders Display** (condensed).
3. **Strict grid plus one rule-breaker per screen** (Wrapped's 16×16 monogram grid). Background shapes double as text containers.
4. **Serif plus grotesk contrast for authority** (Robinhood, NYT). Serif for headlines and pull numbers, grotesk for UI.
5. **Huge numerals for the one number that matters** (Cash App amount, Wrapped minutes, Any Distance stats). 🛠 72–120 sp, tabular figures, with the unit in a tiny caps label beside it, not above it.
6. **Story-card format for shareable moments** (Wrapped, Any Distance). 9:16 full-bleed cards, one stat per card, tap to advance, and a photo in a distinctive mask shape (oval, arch).
7. **Full-bleed photography with the UI reduced to monochrome** (Nike SNKRS). The product or photo carries all colour.
8. **Per-section identity inside one frame** (NYT Games: each game gets a colour plus a glyph, while the typography stays shared).
9. **Generated editorial layout for content** (Arc Search): when showing aggregated info, lay it out like an article (lede, carousel, sections) rather than as a card list.

### Anti-patterns: cheap imitation
- **Italic serif display headline as decoration.** impeccable.style flags it as an AI tell, and taste-skill bans italic or coloured accent words in headlines. Real editorial work uses serif for *structure*, not one fancy word.
- **"Oversized hero headline" with nothing behind it.** Big type needs a real idea and real content (Wrapped has your data).
- Crushed letter spacing applied to *body* text, or tracking so tight letters collide (another impeccable tell).
- Squashed or distorted type to fit (Wrapped 2021's main criticism). Use a real condensed cut or the width axis, never `scaleX`.
- Five type sizes per screen. Editorial means *contrast*: one huge, one small, little in between. taste-skill caps it at about five per page.
- Tiny uppercase letter-spaced labels above every heading (eyebrows), and numbered sections (01/02/03). Both are flagged by impeccable.style and taste-skill.
- Magazine layout that breaks Dynamic Type or accessibility. Huge type must still reflow.

---

## 6. What "AI slop UI" looks like, according to designers

### Sources
| Source | Who | URL |
|---|---|---|
| *Improving frontend design through Skills* | Anthropic (Nov 2025). It names the cause **"distributional convergence"**. | https://claude.com/blog/improving-frontend-design-through-skills ✅ (redirects to /resources/articles/…) |
| *The visible tells of AI design* | Paul Bakaus (Impeccable). A catalogue of ~46 patterns. | https://impeccable.style/slop ✅ |
| *Spot the Slop: a UI designer's guide to fixing AI defaults* | Kosta Canatselis | https://world.hey.com/kostac/spot-the-slop-a-ui-designer-s-guide-to-fixing-ai-defaults-4c448c9c ✅ |
| *Why Your AI Keeps Building the Same Purple Gradient Website* | prg.sh (likely Pragnesh Gajjar; no byline) | https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website ✅ |
| Adam Wathan's Aug 2025 apology for making every Tailwind UI button `bg-indigo-500` | Tailwind creator | https://x.com/adamwathan/status/1953510802159219096 ✅ (200, content via prg.sh) |
| *AI Slop Fonts and Gradients* | 925Studios (an AI design agency, so a vendor source) | https://www.925studios.co/blog/ai-slop-design-tells ✅ |
| **taste-skill** (`design-taste-frontend`) | leonxlnx | https://github.com/leonxlnx/taste-skill ✅ · rules: https://github.com/leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md ✅ |

**Why it happens:** models sample the statistical average of their training data (Anthropic's "distributional convergence"). That data is dominated by Tailwind tutorials and templates. Tailwind UI's indigo default is the commonly cited origin of the purple (prg.sh, Wathan).

### Consolidated tell list (with who flags it)
**Typography**
- Inter everywhere, or Roboto, Arial, Open Sans, Lato or system defaults (Anthropic, prg.sh, Kosta, 925, impeccable).
- **Second-order defaults** that appear when Inter is banned: Geist, Space Grotesk, Instrument Serif (impeccable). Anthropic notes Space Grotesk is still a fallback the model reaches for.
- One family for everything, flat hierarchy (headings look like body), crushed tracking (impeccable).
- A tiny letter-spaced uppercase label or pill badge above every heading (impeccable, taste-skill).
- An italic serif or coloured "accent word" in the headline (impeccable, taste-skill).
- Monospace used for "techy" vibes outside actual code (taste-skill).

**Colour**
- Purple→blue/indigo gradients on white, used decoratively with no meaning (all sources).
- Gradient text. Neon glows and cyan-on-dark. A radial "spotlight" halo behind content (impeccable).
- Default cream/beige grounds, or cream + rust/terracotta, the newer "tasteful" default (impeccable, taste-skill).
- Soft grey body text, i.e. low contrast (taste-skill: running text must use full ink).

**Layout and components**
- Centred hero, then a CTA, then **three identical icon-topped feature cards** (prg.sh, 925, impeccable, taste-skill).
- Uniform padding, radius and card height everywhere, so nothing is primary (Kosta, impeccable).
- Rounded corners on everything, faint uniform drop shadows, a hairline border plus wide soft shadow (prg.sh, impeccable).
- A coloured left-edge stripe on cards, which Kosta and impeccable call one of the most recognisable signatures.
- Cards nested in cards. A huge metric with a tiny label as hero. Numbered sections with no real sequence (impeccable).
- Gratuitous glassmorphism and floating pill nav (impeccable, taste-skill).
- Decorative blobs, grid-line backgrounds, fake dashboards made of grey bars (impeccable, taste-skill).

**Icons and imagery**
- Emoji as icons (taste-skill). Thin generic line icons that fit any product (925). An icon in a rounded tile above every heading (impeccable).
- Rough hand-coded SVG illustrations made from generic shapes (impeccable).

**Motion**
- No motion, or one fade on everything (Anthropic, Kosta, taste-skill).
- Pulsing "live" dots, blinking cursors, auto-scrolling marquees, bouncy easing on routine dialogs, hover zoom (impeccable).

**Copy**
- "Build the future of…", "world-class", "supercharge", "Not X. A Y." (impeccable, Kosta, taste-skill).
- Invented testimonials, stats and logos (taste-skill).

**Missing craft**
- No empty, loading or error states, no validation, no accessibility (Kosta, prg.sh).

### Mobile-specific tells (🛠 my synthesis by analogy; not from a single cited source)
- A "Good morning, Alex 👋" header, then a 2×2 grid of pastel stat cards, then a card list. Every app becomes the same dashboard.
- SF Symbols or Material icons in **pastel rounded-square tiles** on every row.
- A gradient FAB or gradient primary button. Gradient app-bar backgrounds.
- A bottom sheet with heavy blur on every modal. Glass tab bars over flat white content (Liquid Glass misused as decoration rather than as the system material).
- The same 16 dp radius on chips, cards, sheets, buttons *and* images.
- Lottie "success" checkmarks from free packs that clash with the rest of the UI.
- No haptics anywhere, or `.heavy` impacts on everything. Real ADA winners tune haptics per action.
- No dark mode, or dark mode that's just inverted grey with the same purple accent.

### How the real apps above avoid slop (the inverse rules)
1. **One owned idea carried everywhere**: Duolingo's characters, Flighty's airport board, Tide Guide's sky, Nothing's dots.
2. **A custom or distinctive typeface used with conviction.** Every brand above commissioned or chose a face, and none default to Inter for display. (Wise and Revolut reportedly use Inter only for *body* ⚠️.)
3. **One accent colour with a reason** (Monzo coral = warmth, Robin Neon vs. rainbow competitors, Wise green vs. fintech blue).
4. **Scale contrast**: one exaggerated element per screen (Monzo "exaggerated UI", Cash App amount, Wrapped stats).
5. **Sound and haptics designed, not defaulted** (Not Boring, Pok Pok, Duolingo toggles).
6. **Real state design**: Flighty's IRROPS states, Duolingo's widget mood tied to streak risk.

---

## 7. Real typefaces used by these apps, and free (OFL) alternatives you can ship

Every alternative listed was checked to exist in the **google/fonts** repo under `ofl/` (SIL Open Font License) on 2026-10-18, except Roboto Slab (Apache 2.0). All are on Google Fonts. "Feel" matches are my judgement 🛠, not foundry claims.

| App | Real typeface (licence) | Source | Free OFL alternatives (closest feel) |
|---|---|---|---|
| Airbnb | **Airbnb Cereal** (proprietary; Dalton Maag, 2018, 6 weights, tall x-height) | INT ✅, AIGA ✅ | **Plus Jakarta Sans**, **Figtree**, **DM Sans** |
| Uber | **Uber Move** / Uber Move Text (proprietary; MCKL ⚠️) | Uber design page 🔒, Uber 2018 brand PDF (search) | **Manrope**, **Albert Sans**, **Schibsted Grotesk** |
| Monzo | **Oldschool Grotesk** (hero) + **Monzo Sans** (custom Universal Sans cut) | Monzo blog ✅ | **Familjen Grotesk**, **Bricolage Grotesque** (hero); **Hanken Grotesk** (text) |
| Revolut | ⚠️ **Aeonik Pro** (CoType Foundry, commercial) + Inter body | 3rd-party only | **Sora**, **Outfit**, **Urbanist** |
| Robinhood | **Martina Plantijn** (serif, Klim, commercial) + **RH Phonic** (custom sans) | Porto Rocha ✅ | Serif: **Newsreader**, **Source Serif 4**, **Fraunces**. Sans with ink traps: **Rethink Sans**, **Onest** |
| Mercury | ⚠️ **Arcadia / Arcadia Display** (custom) | 3rd-party only | **Instrument Sans**, **Funnel Sans** |
| Flighty, Things 3 | SF Pro / system (both lean on Apple system type) ⚠️ | inferred | Android: **Roboto Flex**. For airport-board figures: **Chivo Mono**, **Martian Mono** |
| Duolingo | **Feather Bold** (custom, Fontsmith/Monotype with Johnson Banks; used for wordmark and headlines) + ⚠️ **DIN Next Rounded** (Monotype) for UI. Sources conflict on DIN Round vs DIN Next Rounded. | Creative Bloq ✅, Monotype (search) | Display: **Nunito** (ExtraBold/Black), **Fredoka**, **Baloo 2**. UI rounded: **Nunito**, **M PLUS Rounded 1c**, **Varela Round** |
| Headspace | Custom **Aperçu** cut by Colophon (proprietary) | INT ✅ | **Work Sans**, **Figtree**, **Albert Sans** |
| Spotify | **Spotify Mix** (custom variable with Dinamo, 2024; replaced **Circular** by Lineto/Laurenz Brunner) | INT ✅, Fonts in Use ✅ | Variable width: **Bricolage Grotesque**, **Anybody**. Circular-like geometric: **Figtree**, **Outfit** |
| Wise | **Wise Sans** (bespoke, heavy display) + ⚠️ Inter for body | Creative Review ✅ | Heavy display: **Archivo Black**, **Anton**, **Dela Gothic One**. Body: **Hanken Grotesk** |
| Cash App | **Cash Sans** (custom) | designcompass ✅ | **Space Grotesk** (but it's on the "slop" list, so avoid it as a default), **Schibsted Grotesk**, **Gabarito** |
| Nike / SNKRS | ⚠️ Nike Futura ND (condensed) / Trade Gothic + Helvetica Now (sources conflict) | 3rd-party | Condensed display: **Bebas Neue**, **Anton**, **Oswald**, **Barlow Condensed**, **League Gothic**, **Big Shoulders Display**. Body: **Archivo** |
| NYT / NYT Games | NYT Cheltenham, NYT Karnak, NYT Franklin, NYT Imperial (all custom) ⚠️ app use unconfirmed | Fonts in Use (search) | Serif display: **DM Serif Display**, **Gloock**, **Young Serif**. Slab (Karnak-like): **Zilla Slab**, **Roboto Slab** (Apache-2.0), **Alfa Slab One**. Grotesk: **Libre Franklin** |
| Nothing | **Ndot55 / Ndot57** (proprietary dot matrix), NType; ⚠️ Geist in OS 4 | Nothing Community ✅ | **Doto** (variable dot-matrix) ✅ https://fonts.google.com/specimen/Doto, **DotGothic16** |
| Teenage Engineering | Monospace throughout (⚠️ exact family unconfirmed) | 3rd-party | **JetBrains Mono**, **IBM Plex Mono**, **Space Mono**, **Martian Mono**, **Fragment Mono** |
| Gumroad | ⚠️ ABC Favorit (Dinamo, commercial) | generated style pages | **Familjen Grotesk**, **Darker Grotesque**, **Archivo** |

**Fonts that are free but NOT OFL, so check the licence before shipping:** Satoshi, General Sans and Cabinet Grotesk are Fontshare (ITF Free Font License) and are **not** in Google Fonts.

**Fonts to avoid as *defaults*, because they are AI tells:** Inter, Roboto, Open Sans, Lato, Arial (Anthropic), plus the second-order defaults Geist, Space Grotesk and Instrument Serif (impeccable, Anthropic). They're fine for a stated reason (e.g. Inter as Wise's body face). They're slop as an unexamined default.

### Suggested pairings per preset (🛠; all OFL and verified on Google Fonts)
| Preset | Display | Text / UI | Accent / data |
|---|---|---|---|
| Warm premium | Plus Jakarta Sans 700–800, or Fraunces (soft serif) | Figtree / DM Sans 400–500 | Newsreader for editorial moments |
| Neo-brutalist | Archivo Black / Anton / Familjen Grotesk 700 | Archivo / Hanken Grotesk | JetBrains Mono / Space Mono / Doto (numbers) |
| Playful | Fredoka 600–700 / Nunito 900 / Baloo 2 | Nunito 600 | Lilita One or Titan One for one-off hero words |
| Editorial | Bricolage Grotesque (wdth/opsz), Big Shoulders Display, or DM Serif Display / Gloock | Libre Franklin / Source Serif 4 | Chivo Mono / Martian Mono for tabular data |

---

## 8. Gaps and caveats
- **Brutalist native mobile apps**: few documented shipped examples. Gumroad and Figma are mainly web and brand. Nothing, Teenage Engineering, grug, Halide and Rooms are *adjacent*. Use Mobbin to pull real screens.
- **Duolingo's 3D button lip** and exact colour and type tokens: no official source found, since the public brand-guidelines site was retired. The lip is observable in the app.
- **Revolut, Mercury, Cash Sans, Nike fonts, Gumroad fonts**: only secondary or generated sources, all marked ⚠️.
- **Uber design page** returns 404/406 to scripted clients but is indexed in many locales. Check in a browser.
- **Material Design Awards** after 2021 and a specific **Webby 2025 native-app visual-design winner**: not found.
- **Locket, BeReal, Lapse, Partiful, Cron/Notion Calendar, Linear mobile, Carrot's exact type**: not researched in depth. I found no primary design write-ups (Partiful only has a student critique, https://ixd.prattsi.org/2025/02/design-critique-partiful/, which says little about visuals).
