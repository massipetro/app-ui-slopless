# Preset: Retro

**Feel:** a past machine made usable now. A phosphor terminal, a pixel-art game screen or an old 1-bit desktop, rebuilt with today's legibility, accessibility and touch. The constraint is the style: one hue, one grid, one frame language, kept with discipline.

**Dealt only when named.** `deal.py --preset retro` is the only way in: the open deal never offers it, because a nostalgia look nobody asked for is a costume on most products. When the user asks for "retro", "pixel", "8-bit", "terminal", "CRT", "Pip-Boy", "Game Boy" or "old Mac/Windows" looks, deal inside this preset.

**Fits:** games and companion apps, indie and dev tools, music gear and synth companions, hobby apps about retro things (collecting, emulation, vintage tech), outdoors and survival tools that want an instrument feel, and playful utilities where the user asked for it.
**Doesn't fit:** banking, insurance and health records (reads unserious), government, anxious contexts, long reading. If the user wants it there anyway, use the bitmap desktop direction (dark on light, the most legible) and warn once.

**Default dials:** `BOLDNESS 6–7 · MOTION 3–6 · DENSITY 5–6 · COLOR 2–6 · FIDELITY 7–8` (the direction decides: the terminal is one hue at C2, the sprite screen a 16-colour set at C6).

Sources and evidence: `research/retro-references.md`.

## Real anchors
- **Fallout's UI and the Pip-Boy companion app (2015).** One controlled phosphor hue on a wrist-computer frame. The art director: "Green is very important to Fallout"; in Fallout 4 the player can recolour the HUD, so the hue is a setting, not a constant. [TheGamer](https://www.thegamer.com/fallout-3-green-colour-debate/) · [9to5Google](https://9to5google.com/2015/11/05/fallout-4-pip-boy-now-available-google-play-store-android-ios/)
- **Alien: Isolation.** Analogue terminals recorded to worn VHS; its lead said lo-fi "didn't necessarily mean crappy". [Engadget](https://www.engadget.com/2014-10-07-alien-isolation-launch-interview.html)
- **cool-retro-term.** Phosphor profiles (green, amber, IBM 3287) and every CRT effect as a separate dial. [GitHub](https://github.com/Swordfish90/cool-retro-term)
- **Balatro (Apple Design Award 2025).** Limited-palette sprites scaled nearest-neighbour; its CRT, bloom and shake effects can each be turned off. [Apple Newsroom](https://www.apple.com/sn/newsroom/2025/06/apple-unveils-winners-and-finalists-of-the-2025-apple-design-awards)
- **Shovel Knight, "Breaking the NES".** Keeps the NES palette and 240 lines that make the identity, drops the sprite flicker and 4:3 that only hurt. The best documented constraint system for a retro style. [Yacht Club](https://www.yachtclubgames.com/blog/breaking-the-nes/)
- **Playdate (Panic).** 1-bit screen and the best published pixel-type spec: text sizes as cap height in pixels, 2 px strokes. [Playdate guidelines](https://help.play.date/developer/designing-for-playdate/)
- **Return of the Obra Dinn.** 1-bit Mac Plus inspiration with "legibility above all else": outlines over dither. [PlayStation Blog](https://blog.playstation.com/archive/2019/10/17/lucas-pope-on-return-of-the-obra-dinns-art-style)
- **Poolsuite.** Mac OS 9 and Nokia cues recoloured into its own pink world: transformation, not a copy. [TechCrunch](https://techcrunch.com/2020/09/10/retro-inspired-music-player-poolside-fm-brings-its-summery-fun-to-iphone)

## Type
- **Two faces, always:** a bitmap or terminal face for display, numbers and short labels, and a readable face for names and running text. Pixel faces for paragraphs are the commonest failure.
- **Integer sizes only.** A pixel face is crisp only at whole multiples of its grid: Press Start 2P and Silkscreen at 8, 16, 24 px; Pixelify Sans at 11, 22, 33; VT323 lands closest at 25 and 50. In SwiftUI pick the size per `dynamicTypeSize` step (`Font.custom(_:fixedSize:)` from a table) instead of letting it scale fractionally; in Compose snap the `sp` value. At accessibility text sizes, fall back to the readable face.
- **Floors (Playdate):** body or dialogue at least 12 px cap height (14 ideal), HUD labels 10 px, nothing under 8 px, strokes at least 2 px.
- OFL on Google Fonts: **VT323**, **Press Start 2P**, **Silkscreen** (caps only: labels and navigation), **Pixelify Sans** (has lowercase), **Jersey 15/20/25**, **Sixtyfour** (its SCAN and BLED axes fake a CRT in the type, with no shader). Readable partners: **IBM Plex Mono**, **Atkinson Hyperlegible**, **IBM Plex Sans**. **Departure Mono** is excellent in a shipped app but isn't on Google Fonts, so mocks can't load it.
- Never the Fallout face (Monofonto is a paid Typodermic licence), Chicago or Minecraft look-alikes.
- Caps budget still holds: terminal and pixel looks pull toward uppercase everything. Keep sentence case; caps-only faces (Silkscreen) go on two-word labels.

## Colour
- **Every text tier at 4.5:1.** Full phosphor passes easily (#33FF33 on black is 15.5:1); the "dim" secondary greens and ambers that feel authentic fail (#1F7A1F on black is 3.9:1, #7A5400 is 3.1:1). Make the secondary tier a lighter tint, not a darker one.
- **Polarity.** Light text on black is less legible for most readers, more so at small sizes, and blooms for people with astigmatism (NN/g, Piepenbrock et al. 2013). So the terminal keeps body text at 16–17 pt and offers a light mode that isn't a dimmed terminal: listing paper (green-bar or amber continuous-form paper). The bitmap desktop is dark on light by nature.
- **Limited palettes are a system, not a mood.** A 16-colour set or four tones, every sprite drawn only from it; colour carries state (thirsty, done, alert). Not the original handheld's four greens: judges read them as a borrowed Game Boy (round 14).
- The hue can be a user setting (green or amber), as in Fallout 4.

## Shape and depth
- One **art-pixel grid** (2 or 3 pt on iOS, so it's a whole number of device pixels at @2x and @3x). Borders, icon sizes, spacing and shadows are whole art pixels. On Android, fractional densities make 1 dp a fraction of a pixel; size art in px through `LocalDensity` where crispness matters.
- **Nearest-neighbour scaling** for every bitmap: SwiftUI `.interpolation(.none)`, Compose `filterQuality = FilterQuality.None`, CSS `image-rendering: pixelated`. Or draw the sprite as rects in a `Canvas`.
- Hard edges: stepped corners, 9-slice frames, one-art-pixel drop shadows, ordered dither instead of gradients. No blur anywhere.
- **Touch targets stay 44 pt / 48 dp** even when the sprite is 16×16 at 2× (32 pt): pad the hit area with `.contentShape` or `Modifier.minimumInteractiveComponentSize()`.
- Keep pixel frames inside the safe area; let the ground colour or pattern bleed to the edges. Never align a bitmap border to the rounded display corners.

## How much pixel art a screen carries
The round-14 judges split between a legible screen with retro as seasoning and a baseline that wore a fuller RPG costume. Resolve it by committing the *content*, not the chrome:
- **All in:** every item's state is pixel art (its sprite, its meter), the key number is in the pixel face, and every content block sits in a pixel frame on the grid. Section titles may use the pixel face at an integer size.
- **Readable:** names, body text, numbers inside sentences, the system bars and the text on controls stay in the readable face.
- **Two tests on the resting frame.** Cover the sprites, meters and frames: if what's left reads as a stock list with pixel icons, it's under-committed. Cover the readable text: if pixel type carries more than the key number, the section titles and two short labels, it's over-committed.
- **Meters show their value.** A thirst bar, battery or progress pip row must look different for different values at rest (segments lit, fill, colour step). Three urgencies drawn as the same empty bar is decoration.

## Motion
- Stepped, not tweened: sprite loops at 8–12 fps, 2–4 frame state changes, type-on text, inverse-video presses.
- **CRT effects are seasoning.** A static scanline overlay on chrome and frames only. **No glow on type**, the key number included: in round 14 a glow smeared the hero digits and lost the pair. A faint glow may sit on rules and frames. No curvature, chromatic aberration, jitter, rolling bars or flicker over content.
- **No flashing:** at most three flashes a second (WCAG 2.3.1); a 60 Hz flicker loop fails outright. Reduce Motion turns every animated effect off (lines appear whole, the cursor holds, sprites hold their idle frame), and the screen offers a setting to switch effects off, as Balatro does.

## Signature moves (pick 2–3)
1. **Readout lines:** label, dot leader, value and unit in a bitmap face at an integer size (terminal).
2. **A live cursor line** that blinks at 1 Hz and holds under Reduce Motion (terminal).
3. **Bracketed commands** that invert on press (terminal).
4. **9-slice pixel frames** like RPG dialogue boxes, all on one art-pixel grid (sprite).
5. **Sprites whose frames show state:** the plant wilts, the battery drains, the ferry docks (sprite).
6. **Sections as framed windows** with striped title bars and a close box (desktop).
7. **Bevelled buttons** that invert their bevel on press (desktop).
8. **Inverse-video selection** for the chosen row, in every direction.

## Platform notes
- iOS: opaque bars in the palette ground (Liquid Glass fights all three directions); Dynamic Type through a size table per step, then the readable fallback face. VoiceOver labels on every drawn readout and sprite: the sprite's state is its value ("Monstera, thirsty").
- Android: no ripple on pixel buttons (the one-pixel press is the indication); dynamic colour off, because the palette is the identity; `sp` snapped to the face's grid.
- Mac: keep the real title bar and traffic lights; never draw a fake title bar on the window itself. The terminal direction gains a command field with history.

## How cheap imitations go wrong
- **IP cosplay:** Pip-Boy, Vault-Tec, Vault Boy or RobCo names and art; the Fallout font; Nintendo's Game Boy logo or a Minecraft face; the rainbow apple, the Windows flag or the Happy Mac. Take the *machine* (phosphor, grid, bevel), never the brand.
- **A nostalgia costume with no product idea:** hearts, swords and gold coins on a plant app; a terminal skin over a stock list. The product's own state has to drive the sprite or the readout.
- Pixel fonts at fractional sizes or anti-aliased, and sprites scaled with smoothing: soft, smeared, the opposite of the style.
- Micro type: body text under 12 px cap height, 1 px strokes, caps-only faces for running text.
- Dim phosphor tiers under 4.5:1; long text on pure black at small sizes.
- Effects over content: scanlines, bloom or flicker on lists and paragraphs, and no way to turn them off.
- Raw ROM bitmaps pretending to be CRT text (real terminals stretched and bled their dots); noisy auto-dither and scrolled checkerboards that flash.
