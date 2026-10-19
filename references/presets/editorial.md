# Preset: Editorial / expressive type

**Feel:** a magazine you can touch. Type *is* the image: huge, confident, cropped and set with intent. Strong contrast, a strict grid with one deliberate rule-breaker, and content treated like a story.

**Fits:** media, news, music, culture, fashion and retail drops, sports stats, personal year-in-review, portfolios, reading apps, data-heavy apps with a point of view.
**Doesn't fit:** form-heavy enterprise flows, tiny utility apps with no content to set.

**Default dials:** `BOLDNESS 8 · MOTION 5 · DENSITY 5 · COLOR 4 · FIDELITY 6`

## Real anchors
- **Spotify Mix + Wrapped.** A variable typeface with a width axis from condensed (tall screens) to extended (wide moments), designed to animate. Wrapped 2022 used interlocking shapes on a 16×16 grid as both background and data container. The lesson from Wrapped 2021's criticism: squashed type and imagery that doesn't integrate look cheap. [Spotify Mix](https://www.itsnicethat.com/articles/spotify-dinamo-new-typeface-spotify-mix-project-230524) · [Wrapped 2022](https://www.itsnicethat.com/features/spotify-wrapped-campaign-identity-2022-graphic-design-301122)
- **NYT Games (ADA 2024).** One editorial frame with per-game colour and glyph identities, game cards showing progress state, and a serif heritage. [ADA 2024](https://developer.apple.com/design/awards/2024/)
- **Nike SNKRS.** Drops presented as stories: full-bleed photography, a monochrome UI where the product supplies the colour, huge condensed uppercase headlines. [Instrument](https://www.instrument.com/work/snkrs)
- **Wise (2023 rebrand).** Green instead of fintech blue, and Wise Sans used very heavy and very large. [Creative Review](https://www.creativereview.co.uk/wise-rebrand-ragged-edge/)
- **Cash App (2025).** The amount screen with giant numerals is the archetypal exaggerated number. Fluorescent green, custom Cash Sans. [designcompass](https://designcompass.org/en/2025/12/03/cash-apps-new-design-language-and-ai-moneybot/)
- **Any Distance (ADA 2023).** Workouts as shareable poster cards, with photos in an *oval mask* that became a brand trait. [Behind the Design](https://developer.apple.com/news/?id=uiiopcl8)
- **Robinhood (2024).** Serif headlines for authority, against a characterful sans and one neon accent.

## Type
- **Contrast is the whole game:** one huge size, one small size, very little in between. Usually 3–4 sizes per screen.
- OFL options: display **Bricolage Grotesque** (width + optical-size axes), **Big Shoulders Display** (condensed), **Anton** / **Bebas Neue** (condensed caps), or a serif display (**DM Serif Display**, **Gloock**, **Young Serif**). Text: **Libre Franklin**, or **Source Serif 4** for reading. Data: **Chivo Mono** / **Martian Mono**.
- Hero headlines at **48–96 pt**, line height **0.9–1.0**, tracking −2% to −4% on heavy grotesques. Break lines deliberately (2–4 lines), and let them crop at the edge when it's the hero.
- **Use a real condensed cut or the width axis to fit. Never `scaleX`.**
- Serif for *structure* (headlines, pull numbers), not as one decorative italic word.
- Body text set like reading: 17–19 pt, 1.4–1.5 line height, 45–75 characters per line (cap the width on tablets).

## Colour
- **Near-monochrome type and UI + one strong colour** (or the content's own colour: photography, album art, the product).
- High contrast: true black on paper white (`#0D0D0D` on `#FAF8F3`), or the inverse for night.
- **Per-section identity inside one frame** (NYT Games): each section or category gets one colour and glyph, while the type stays shared.
- Colour blocks are full-bleed fields, not little badges.

## Shape and layout
- **A strict grid** (4-column on phone, 8 on tablet) with **one rule-breaker per screen**: a headline that bleeds off the edge, an image breaking the column, a giant numeral overlapping a photo.
- Thin rules (1 dp) and generous margins in place of cards. Content separated by typography and space, not boxes.
- Images: full-bleed, or in a *distinctive mask* (oval, arch, tall crop) used consistently.
- Radius: 0 for editorial blocks. Small radii only on controls.

## Icons
- Few icons. Prefer **words** where space allows ("Share", "Save"), set in the UI face. That's an editorial move in itself.
- Where icons are needed, use fine, consistent line glyphs (1.5 dp) in ink, or typographic glyphs (arrows →, ↗, numerals in circles).
- Section identity glyphs (NYT Games style) are custom, simple, bold shapes, one per section, used large.
- The core verb's state change is typographic: a word that swaps with a crossfade or slide ("Save" → "Saved"), or a counter that ticks.

## Motion
- **Typographic motion:** headlines that animate width or weight on transition (variable fonts), staggered line reveals, numbers that count up once.
- Page-like transitions: horizontal paging for stories, and a vertical scroll with sticky section headers that change as you pass them.
- Calm otherwise. Stagger 30–50 ms per line, ease out, no bounce.
- Reduce Motion: show the final state; no width animation, no counting.

## Signature moves (pick 2–3)
1. **Type as image:** a 64–96 pt hero headline cropped at the edge, with tight leading.
2. **The one number:** 72–120 pt tabular numerals, with the unit beside it in the text face, lowercase ("42 min"), not a tracked caps label.
3. **Story cards:** 9:16 full-bleed, one stat or idea per card, tap to advance, shareable (Wrapped, Any Distance).
4. **Serif + grotesk contrast:** serif headline, grotesk UI.
5. **Grid with one breaker** per screen.
6. **Section colour + glyph identity** inside one editorial frame.
7. **Monochrome chrome, content supplies colour** (SNKRS).
8. **Article-shaped results:** lede, image carousel, sections, rather than a card list (Arc Search).
9. **Animated variable width/weight** on scroll or transition.

## Platform notes
- iOS: big titles fit well with `.navigationBarTitleDisplayMode(.large)` restyled, or a custom header. Keep the back button visible. Liquid Glass over full-bleed photography works.
- Android: M3 Expressive's larger type scale points the same way. Use a `LargeTopAppBar` with a custom display font as the native-feeling base.
- **Dynamic Type is the hard part:** huge type must still reflow. Use `ViewThatFits` / `minimumScaleFactor` sparingly on hero headlines, and let body text scale fully. At AX sizes, stack the layout instead of shrinking it.

## How cheap imitations go wrong
- An italic serif "accent word" in a headline as decoration.
- An oversized headline with nothing behind it. Big type needs a real idea or real content.
- Crushed tracking on body text, or collisions on display text.
- Squashed or distorted type to fit (`scaleX`), Wrapped 2021's sin.
- Too many sizes per screen, which kills the contrast.
- A tiny letter-spaced uppercase "eyebrow" above every heading, and fake numbered sections (01/02/03) with no real sequence. Editorial caps belong to the condensed hero headline; the caps budget (at most two small uppercase labels per screen) holds here too.
- Magazine layouts that break at large text sizes.
