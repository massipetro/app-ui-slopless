# Preset: Neo-brutalist

**Feel:** honest, loud, graphic, a bit punk. Controls look like *objects*: outlined, flat-filled, casting hard shadows like paper cut-outs. Nothing is soft or blurred, and nothing pretends.

**Fits:** creator tools, indie products, music, culture, events, dev tools, Gen-Z social, portfolios, side projects with attitude.
**Doesn't fit:** finance and banking (reads untrustworthy), anxious health contexts (reads aggressive), government. If the user wants it there anyway, soften it: `BOLDNESS` ≤5, a single accent, and warn.

**Default dials:** `BOLDNESS 9 · MOTION 4 · DENSITY 5 · COLOR 7 · FIDELITY 8`

## Real anchors
Honest note: fully neo-brutalist *native mobile* apps are rare among well-documented products. Use the true examples for the visual system and the adjacent "raw/industrial" apps for how it behaves on a phone.
- **Gumroad (2021 relaunch), true neo-brutalist.** Thick black outlines, flat pastel and hot-pink fills, hard unblurred offset shadows, oversized type. Polarising, and instantly recognisable. [madegooddesigns](https://madegooddesigns.com/neobrutalism-web-design/)
- **Figma brand (2019).** Sharp dark outlines around flat shapes, clashing orange and yellow, high-contrast colour blocks.
- **Nothing OS, industrial.** Ndot dot-matrix type on a monochrome base, dot-built widgets that act as controls. Lesson: users rebelled when the dot font was removed, *and* Nothing admitted using it for running text "went too hard". Dot type is for numbers and hero labels only. [Nothing community](https://nothing.community/d/104-ndot57-the-nothing-typeface)
- **Teenage Engineering, industrial.** Monospace everywhere for terse labels, black, white and grey chrome where the product supplies the colour, and full-screen modes with no persistent chrome. [teenage.engineering](https://teenage.engineering/)
- **grug (ADA 2026 Delight & Fun), raw.** A scribbled, hand-drawn UI including a custom status bar. Raw wins when it's *fully committed*. [ADA](https://developer.apple.com/design/awards/)
- **Halide Mark II (ADA 2022), tool-honest.** Controls that look and behave like physical camera dials, reachable one-handed.
- Implementation kit: [neobrutalism.dev](https://neobrutalism.dev/) (web, but its border and shadow conventions translate directly).

## Type
- An **oversized grotesque or condensed display face** plus **monospace for metadata** (timestamps, counts, tags), set in natural case at a readable size, never as tracked uppercase labels.
- OFL options: display **Archivo Black**, **Anton**, or **Familjen Grotesk 700**; text **Archivo** / **Hanken Grotesk**; mono **JetBrains Mono**, **Space Mono**, or **IBM Plex Mono**; dot-matrix numbers **Doto**.
- Headlines are BIG (34–56 pt), tight (line height 0.95–1.05), and can go uppercase at display size for one or two words. Small labels stay sentence case (caps budget: at most two small uppercase labels per screen). Body stays sentence case at 16–17 pt in the text face, never monospace for paragraphs.

## Colour
- **Off-white or white base, pure black ink, 2–3 flat saturated accents from different hue families.** Example: base `#FFFDF5`, ink `#000000`, pink `#FF90E8`, yellow `#FFC900`, green `#23A094`, blue `#3B5BFF`.
- **Assign colour by role or section** (e.g. each tab or category owns one accent). Random colour per card is the fake version.
- No gradients and no transparency. Text on accents is **black** (white on `#FFC900` fails contrast).
- Dark mode: invert the *base*, not the system. Use a near-black surface `#111`, off-white strokes and shadows, and keep the accents (dark text on them still). Or ship light-only and say so: brutalism often reads best that way. That's a legitimate convention break; note it.

## Shape and depth
- **Stroke:** 2–3 dp solid ink on every interactive surface and card. Use 2 dp rules between list rows instead of soft cards.
- **Hard offset shadow:** 4–6 dp x and y, **zero blur**, in ink or an accent colour.
- **Radius 0–4 dp** (8 maximum for large containers). Big radii are the #1 way the style gets diluted.
- **Press = squash into the shadow:** translate the element +offset x/y and set the shadow to 0. That's the signature microinteraction, so make it fast (≤80 ms) and crisp.
- Visible structure: lists look like tables, sections get thick rules, the grid is visible.

## Icons
- Thick-stroke (2.5–3 dp at 24 dp), square-capped, geometric glyphs. Or chunky pixel / dot-matrix glyphs for an industrial take. Draw them in code as one family.
- Icons sit in **bordered square tiles** in a flat accent, never pastel rounded tiles.
- The core verb's icon gets a mechanical state change: a stamp, a hard flip, a stepped (2–3 frame) fill. No smooth morphing.

## Motion
- **Snappy, mechanical, low-bounce.** Short durations (100–200 ms), linear-ish or stepped for "printed" effects. No floaty springs.
- Allowed: a hard slide-in, a stamp (scale 1.15 → 1 with no bounce), a jitter or shake for errors, and stepped number counters.
- Haptics: a firm `rigid` / `CONFIRM` on press feels right. Keep them crisp.

## Signature moves (pick 2–3)
1. **The squash button:** a stroked, flat-filled button with a hard shadow that sinks on press.
2. **Sticker cards:** bordered cards in different accents, slightly rotated (±1–2°) on *one* hero element only.
3. **Table-honest lists:** rows separated by 2 dp rules, monospace metadata right-aligned, no cards.
4. **Marquee label:** one scrolling ticker band for status or announcements (it must pause; WCAG 2.2.2), used once.
5. **Giant uppercase section header** that crops at the screen edge.
6. **Dot-matrix numerals** (Doto) for the key number: a counter, clock or score.
7. **Full-screen task modes:** one task per screen with a huge bordered close button, no persistent chrome (Teenage Engineering).
8. **Custom tab bar** as a bordered strip with a solid-filled selected tab and labels always visible. Note it as a convention break; keep 44/48 targets and the selected-state semantics.

## Platform notes
- iOS 26 Liquid Glass fights the style. Use opaque solid bars (`.toolbarBackgroundVisibility(.visible…)` + a solid colour) and note it.
- Android: no ripples. The squash is the indication. Disable dynamic colour, because the palette *is* the brand.
- Native mechanics stay: system back and edge-swipe, sheets (restyle them with a stroke and a hard shadow at the top edge), text scaling. Thick strokes must not clip at 200% text.

## How cheap imitations go wrong
- Monospace uppercase labels on every value, tag and heading. It reads as costume, and blind judges cap it; keep caps for the one giant header.
- **"Soft brutalism":** rounded-xl + *blurred* shadow + black border. Blur is the giveaway.
- A brutalist skin on a generic layout (centred hero, three bordered feature cards).
- Random clashing colour with no system.
- White text on yellow or pink; saturated-on-saturated text.
- Monospace or dot-matrix for body copy.
- Being brutal in the wrong place: an error state that shouts at an anxious user. Keep the *voice* kind even when the visuals are loud.
