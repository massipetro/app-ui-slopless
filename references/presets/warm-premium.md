# Preset: Warm premium

**Feel:** confident, generous, expensive without being cold. Real imagery or one hero object carries the screen, while the UI chrome stays quiet and sure of itself. Think of a great hotel lobby: nothing shouts, but everything was chosen.

**Fits:** travel, hospitality, mobility, fintech, marketplaces, food, real estate, premium consumer.
**Doesn't fit:** kids, games, anything that needs to feel scrappy or irreverent.

**Default dials:** `BOLDNESS 5 · MOTION 5 · DENSITY 4 · COLOR 3 · FIDELITY 4`

## Real anchors (study these, don't copy them)
- **Airbnb (2025 "dimensional" release).** In-house 3D icons used *only* for categories and navigation, a horizontally scrolling illustrated category bar, rounder and softer edges, subtle motion, and the custom Cereal face with a tall x-height. [It's Nice That](https://www.itsnicethat.com/articles/airbnb-app-redesign-140525) · [Airbnb newsroom](https://news.airbnb.com/product-releases/airbnb-2025-summer-release/)
- **Uber.** Near-monochrome black and white, with colour almost absent. The map is the hero and the chrome stays quiet. Uber Move comes in Display and Text cuts. [Base Web](https://baseweb.design/)
- **Monzo (2024–25 refresh).** One hot-coral signature over navy and soft white. Warm photography with sunny flares and dramatic shadows. Oldschool Grotesk as hero, with UI elements deliberately "exaggerated". [Monzo blog](https://monzo.com/blog/weve-had-a-little-makeover)
- **Robinhood (2024, Porto Rocha).** A serif headline (Martina Plantijn) against a characterful sans, one electric "Robin Neon" accent on black and white, and single-object still-life photography. [Case study](https://www.portorocha.com/robinhood)
- **Flighty (ADA 2023).** The airport-board rule: one line per flight, key information always visible, Live Activities, and a progress ring in the Dynamic Island. They sketch 20 concepts per feature. [Apple: Behind the Design](https://developer.apple.com/news/?id=970ncww4)
- **Things 3.** Calm, typographic, white, and premium through *interaction*: the draggable Magic Plus button.
- **Tide Guide (ADA 2026).** An aqua palette that shifts to match the sky through the day, with full-screen hour-by-hour charts.

## Type
- **One family with personality for display** (tall x-height, open apertures) at 2–3 weights, plus a quiet text cut. Don't mix three families.
- OFL options: display **Plus Jakarta Sans 700–800** or **Fraunces** (soft serif, for an editorial-luxury tilt); text **Figtree** / **DM Sans** 400–500; an editorial accent in **Newsreader**. Or keep SF Pro / Roboto Flex for text and add only the display face.
- **The exaggerated number:** price, time, amount or distance at 40–64 pt, display weight, tabular figures. Its label is small and sits beside or below it.
- Body text stays **full ink**. Thin grey "elegant" body text is the classic fake-premium move.

## Colour
- **Neutral base + ONE owned accent** on ≤10% of pixels: the primary CTA, the selected state, one data highlight. Give the accent a reason (Monzo: coral = warmth; Robinhood: neon vs competitors' rainbows).
- Neutrals are *warm or cool on purpose*, not default grey. Light example: surface `#FFFCF8`, ink `#1C1A17`, secondary ink `#5C564E`. Dark: surface `#14120F`, ink `#F5F1EA`.
- Photography supplies the rest of the colour. No decorative gradients.
- Dark mode is first-class. Tune the accent separately, since it is often slightly lighter and less saturated on dark.

## Shape and depth
- Radii are soft but *varied by role*: images 16–20, cards 20–24, buttons 14 or full pill, chips full. Not one 16 everywhere.
- **Depth through light:** a single directional, low-blur, slightly *tinted* shadow (warm brown or brand-tinted), or none at all, using separation by surface tone instead. Never a 5%-black blur on every card.
- Photography: edge to edge, or large with a radius. Put text *below* images. Overlay text only on a real scrim (a gradient from the bottom, ≥4.5:1 checked).

## Icons
- **Utility chrome:** the system family (SF Symbols / Material Symbols Rounded) at a consistent weight, tinted in ink, not the accent.
- **Categories and hero moments:** a custom, *dimensional* set in the Airbnb spirit: soft 3D or two-tone illustrated glyphs at 28–32 dp, made as one family (same light direction, same palette), used only for categories and navigation.
- **The core verb** (book, pay, save) gets a designed state change: a heart that fills with a soft spring, a "confirmed" stamp, a ticket that tears. It should be calm and precise, not bouncy.

## Motion
- Calm, physical and continuous. Use **springs with low bounce** (damping 0.85–0.9) for spatial moves, and fades for colour.
- **Shared-element continuity** from card to detail (iOS `.navigationTransition(.zoom)`, Compose `sharedElement`). This is *the* premium motion.
- Animated numerals when a value changes (`.contentTransition(.numericText)` / `AnimatedContent`).
- Haptics: light and rare. Selection ticks on pickers and a success notification on booking or payment.

## Signature moves (pick 2–3)
1. **Hero object per screen:** one photo, map or object edge to edge, with the UI floating on top in neutral ink.
2. **Illustrated category rail:** a horizontally scrolling row of custom icons at 28–32 dp over 11–12 sp labels. The selected one gets a 2 dp underline and full opacity, the rest sit at 60–70%.
3. **Exaggerated key number:** 48–64 pt tabular figures (price per night, amount, ETA), with everything else small.
4. **Airport-board rows** for dense status: one row per entity, fixed columns, status as colour *and* word, layout stable when data changes.
5. **Sticky summary + one CTA:** a bottom bar with the total on the left and a single bold accent CTA on the right, always in the thumb zone (the Airbnb reserve bar pattern).
6. **Owned accent as a signature:** one colour used only for "go" and selection, so users learn it.
7. **Interaction as luxury:** one bespoke gesture with a visible fallback (Things' draggable plus button).
8. **Time-aware palette:** subtle surface tint shifts by time of day or context (Tide Guide).

## Platform notes
- iOS 26: Liquid Glass bars over photography look right here, so let the system glass float.
- Android: dynamic colour can work for secondary surfaces if the accent stays fixed. Usually you keep the brand scheme.

## How cheap imitations go wrong
- Stock photos of laughing people, or AI-generated imagery. The style lives on *specific, art-directed* images.
- Gold or purple gradients to signal "luxury". Real examples use flat colour plus photography.
- Three or more accent colours.
- 3D icons on *everything*, including utility actions, or mismatched 3D packs.
- Glass cards stacked on photos everywhere. One glass layer is intentional; five is a template.
- Monotonous rhythm: every card the same height and every gap the same. Premium layouts vary scale: one big hero, then dense supporting rows.
- Cream background + terracotta accent as an unexamined default. That's the newer "tasteful AI" tell.
