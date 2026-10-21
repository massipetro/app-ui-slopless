# Retro references: phosphor terminal, pixel sprite, bitmap desktop

Research behind `references/presets/retro.md` and the three `rt-` directions in `library/directions.json`, gathered October 2026.

Scope: three candidate directions: **Phosphor terminal**, **Pixel sprite** and a possible third (**Bitmap desktop**: System 6/7, Win95, 1-bit). Every claim carries a URL. Items marked **[unverified]** come from secondary or forum sources I could not confirm. Items marked **[computed]** are my own calculations.

---

## A. Shipped anchors and what each identity rests on

### Phosphor terminal

| Anchor | What the identity rests on | Sources |
|---|---|---|
| **Fallout Pip-Boy companion app** (iOS/Android, 2015) | Green-on-black wrist-computer frame. It shows stats, inventory, map, radio and holotape minigames. It has a demo mode and a "hardware mode" that resizes the display to fit the physical Pip-Boy harness. | https://9to5google.com/2015/11/05/fallout-4-pip-boy-now-available-google-play-store-android-ios/ · https://electronic.partners/news/bethesda-releases-the-pip-boy-fallout-4-companion-app-for-android/ |
| **Fallout series UI** | One controlled hue. Art director Istvan Pely says "Green is very important to Fallout" and ties it to phosphor-green computer screens, and the team went through "endless shades of green". In Fallout 4 the player can recolour the HUD and Pip-Boy (amber is a popular choice). So the hue is a token, not a constant. | https://www.thegamer.com/fallout-3-green-colour-debate/ · https://steamcommunity.com/app/377160/discussions/0/496881136903982447 **[forum]** |
| **Fallout Shelter** (mobile) | A contrast case. Its identity is the 1950s Vault-Tec advertising illustration style and Vault Boy, not the terminal look. Even help files and notifications use that style. | https://www.trustedreviews.com/fallout-shelter-review |
| **Alien: Isolation** (Creative Assembly) | "Lo-fi" analogue chrome. The UI was recorded to worn VHS and degraded with magnets. Terminals are green monochrome. The creative lead said lo-fi "didn't necessarily mean crappy". | https://www.pcgamer.com/uk/the-making-of-horror-masterpiece-alien-isolation-it-was-a-giddy-exhausting-intense-time/ · https://www.engadget.com/2014-10-07-alien-isolation-launch-interview.html |
| **Cathode** (Secret Geometry, Mac/iOS) | A full CRT simulation: colour, lighting, screen shape, bitmap fonts, and jitter when the window moves. It is now discontinued: no updates since about 2017, and it runs under Rosetta only. Good as reference, not as a live anchor. | https://www.pcworld.com/article/494330/turn_your_new_mac_into_an_old_terminal_with_cathode.html · https://rosettacheck.com/apps/yw9ne4kn · https://alternativeto.net/software/cathode/about |
| **cool-retro-term** (Linux/macOS, GPL, about 26k GitHub stars) | Built on Qt/QML. It ships profiles named Amber, Green, Apple ][, IBM DOS, IBM 3287 and others. Its effects are curvature, bloom, scanlines, chromatic aberration, flicker, static noise, burn-in and jitter. | https://github.com/Swordfish90/cool-retro-term · https://en.ubunlog.com/cool-retro-term-a-terminal-emulator-for-the-most-nostalgic/ · https://dev.to/remojansen/i-have-open-sourced-a-webgl-front-end-for-your-terminal-that-emulates-a-crt-monitor-2icd |
| **DEC VT100/VT220 (the source)** | 8×10 ROM glyphs drawn in a 10×10 cell. Each lit dot is stretched one pixel horizontally, phosphor bleed opens the counters, and scanlines are visible. Raw ROM bitmaps therefore look wrong without that stretching. | https://www.masswerk.at/nowgobang/2019/dec-crt-typography |

### Pixel sprite

| Anchor | What the identity rests on | Sources |
|---|---|---|
| **Playdate** (Panic) | A 1-bit 400×240 reflective Sharp Memory LCD at about 173 ppi with no backlight. Text sizes are given as cap height in pixels (see B). Dithering is cleaned up by hand. A 2× display scale is available. The crank has a d-pad fallback. | https://help.play.date/developer/designing-for-playdate/ |
| **Balatro** (Apple Design Award 2025, Delight and Fun) | Limited-palette sprites scaled with nearest neighbour, a CRT shader layer and juicy score feedback. The CRT, bloom and screen-shake effects each have their own setting and can be turned to 0. | https://www.apple.com/sn/newsroom/2025/06/apple-unveils-winners-and-finalists-of-the-2025-apple-design-awards · https://steamcommunity.com/app/2379780/discussions/0/4201364375109001844 **[forum]** · https://foro3d.com/2026/mayo/el-arte-del-crt-digital-balatro-y-la-magia-de-love.html **[secondary]** |
| **Shovel Knight** (Yacht Club) | "Breaking the NES" deliberately: it keeps the 54-colour NES palette plus only four extra colours, keeps 240 vertical lines, widens to 400×240 and drops the sprite flicker. This is the best documented example of a constraint system for a style. | https://www.yachtclubgames.com/blog/breaking-the-nes/ |
| **Stardew Valley** | Pixel art with separate **UI scale** and **zoom** settings. Mobile ships a larger UI scale than PC allows. Players ask for integer scaling on HiDPI screens. | https://stardewvalleywiki.com/User:Dem1se · https://forums.stardewvalley.net/threads/integer-scaling-on-high-dpi-displays-zoom-pixelization.4683/latest **[forum]** |
| **Poolsuite FM** (iOS) | Transformation, not copying. The iOS app borrows Nokia 3310 cues ("outdated fonts, pixel-y shading and grainy imagery") but in bright pink with a jewel-toned theme picker. | https://techcrunch.com/2020/09/10/retro-inspired-music-player-poolside-fm-brings-its-summery-fun-to-iphone |
| **Habitica** (habit tracker) | Retro RPG pixel avatars and items. The 2015 redesign "embraces material design", which suggests pixel art in the content and platform chrome around it. **[my inference]** | https://apps.apple.com/app/id994882113 · https://www.androidpolice.com/2015/12/14/habitrpg-developer-releases-beta-version-of-habitica-a-complete-redesign-of-the-app-that-turns-your-chores-and-to-dos-into-quests-for-gold/ |
| **Teenage Engineering OP-1** | Not really pixel retro. A 320×160 OLED where "colour is the natural link between on-screen objects and encoders". It is useful as a model for colour-coded controls, less so for this preset. | https://www.soundonsound.com/reviews/teenage-engineering-op1 · https://en.wikipedia.org/wiki/Teenage_Engineering_OP-1 |
| Pixel weather apps | Only small apps exist, e.g. "Pixel Weather" ("cute… pixel style"). I found **no** App Store editorial or ADA recognition for a pixel-styled utility. (Not Boring) Weather is 3D game-styled, not pixel. | https://apps.apple.com/app/id1278650505 · https://apps.apple.com/app/id1531063436 |

**Palettes with sources:** PICO-8 has 16 colours (#000000, #1D2B53, #7E2553, #008751, #AB5236, #5F574F, #C2C3C7, #FFF1E8, #FF004D, #FFA300, #FFEC27, #00E436, #29ADFF, #83769C, #FF77A8, #FFCCAA) per https://lospec.com/palette-list/pico-8. The popular "DMG" set #0F380F/#306230/#8BAC0F/#9BBC0F is a stylisation (https://colordesigner.io/color/0f380f). The real DMG measured greens differ (https://bulbapedia.bulbagarden.net/wiki/palette), and the bgb emulator default is #081820/#346856/#88C070/#E0F8D0 (https://lospec.com/palette-list/nintendo-gameboy-bgb). The NES has 54 usable colours (https://www.yachtclubgames.com/blog/breaking-the-nes/).

### Bitmap desktop (third candidate)

| Anchor | Identity | Sources |
|---|---|---|
| **Return of the Obra Dinn** | Inspired by 1-bit Mac Plus games (512×342). Pope chose to "prioritise legibility above all else", using outlines and sparing dither. Large dithered pixels were "too uncomfortable for long periods of play". | https://blog.playstation.com/archive/2019/10/17/lucas-pope-on-return-of-the-obra-dinns-art-style |
| **Poolsuite (web/Mac)** | The designer: "The main inspiration was Mac OS 9", with nods to early Windows and Xerox. | https://thenextweb.com/news/retro-os-mac-windows-music-poolside · https://en.wikipedia.org/wiki/Poolsuite |
| **system.css / 98.css** | MIT-licensed design systems that rebuild System 6 (from Apple's own guidelines) and Windows 98 chrome: title bars, bevels, group boxes. | https://github.com/sakofchit/system.css · https://github.com/jdan/98.css |
| **Playdate** | Also a 1-bit anchor (see above). | https://help.play.date/developer/designing-for-playdate/ |

---

## B. Typography

The **pixel grid** column is my own measurement from each TTF's outline coordinates **[computed]**: the most common coordinate step divided into unitsPerEm gives the px-per-em at which one font pixel equals one device pixel. Use integer multiples of that size.

| Font | On Google Fonts | Licence | Origin | Pixel-exact sizes | Notes |
|---|---|---|---|---|---|
| **VT323** | Yes | OFL | Peter Hull, from DEC VT320 glyphs, with beam smear simulated in rounded outlines | Never exactly crisp by design. Rows are about 80 units, so 12.5 px/em and a 7-row cap height; 25 or 50 px land closest **[computed, unverified]** | Best terminal body face on Google Fonts. Coverage is limited to the VT320 set. https://github.com/google/fonts/tree/main/ofl/vt323 |
| **Press Start 2P** | Yes | OFL | CodeMan38, from Namco arcade (Return of Ishtar 1986) | "8px, 16px and other multiples of 8" (confirmed: 125/1000 units) | Wide glyphs and a cap height equal to the em. Display only. https://github.com/google/fonts/tree/main/ofl/pressstart2p |
| **Silkscreen** | Yes (Regular and Bold) | OFL | Jason Kottke, 1999 | 8 pt and multiples, anti-aliasing off (confirmed 8 px/em) | All caps by design, so labels and navigation only. https://fedoraproject.org/wiki/Fonts/Silkscreen · https://github.com/google/fonts/tree/main/ofl/silkscreen |
| **Pixelify Sans** | Yes (variable wght 400–700) | OFL | Stefie Justprince | About 11 px/em, so 11/22/33 **[computed]** | Has lowercase. Usable for short UI text. https://github.com/google/fonts/tree/main/ofl/pixelifysans |
| **Jersey 10/15/20/25** | Yes | OFL | Sarah Cadigan-Fried, a knitting-chart family. The number is the cap height in pixels | Jersey 10 ≈ 18.67 px/em (awkward). Jersey 15 = 27, Jersey 20 = 34, Jersey 25 = 41 px/em **[computed]** | Sporty display. https://github.com/google/fonts/tree/main/ofl/jersey10 |
| **Micro 5 / Tiny5** | Yes | OFL | Cadigan-Fried / Stefan Schmidt | Micro 5 = 11 px/em, 5 px caps **[computed]** | Tiny5 has BLED/JITT/ROND axes. Micro type is decoration only. https://github.com/google/fonts/tree/main/ofl/micro5 · https://github.com/google/fonts/tree/main/ofl/tiny5 |
| **Sixtyfour / Workbench** | Yes | OFL | Jens Kutílek, C64 and Amiga | n/a (variable) | **Scanline (SCAN) and Bleed (BLED) axes** fake CRT in the type itself, with no shader. Limited glyphs. https://github.com/google/fonts/tree/main/ofl/sixtyfour |
| **DotGothic16** | Yes | OFL | Fontworks | not measured | Pixel Japanese. https://github.com/google/fonts/tree/main/ofl/dotgothic16 |
| **IBM Plex Mono / Share Tech Mono** | Yes | OFL | IBM / — | vector | The **legible fallback** for terminal body text at Dynamic Type sizes. https://github.com/google/fonts/tree/main/ofl/ibmplexmono |
| **Departure Mono** | **No** | OFL | Helena Zhang | "set the font size to increments of 11px" | Excellent modern pixel mono for shipped apps. It can't be used in our Google-Fonts-only mocks. https://github.com/rektdeckard/departure-mono |
| **Monocraft** | No | OFL 1.1 font, GPL code | Fan font in the Minecraft style | — | Not affiliated with Mojang. Its IP is debated in packaging threads. https://github.com/IdreesInc/Monocraft · https://issues.guix.gnu.org/57637 |
| **3270** | No | GitHub shows "Other". Debian lists BSD-3 or OFL **[check upstream]** | Ricardo Bánffy, from x3270 | — | IBM 3270 terminal look. https://github.com/rbanffy/3270font · https://metadata.ftp-master.debian.org/changelogs/main/3/3270font/stable_copyright |
| **Monofonto** (Fallout lineage) | No | Commercial Typodermic licence. App embedding is sold separately | Typodermic, 1999. The early version appeared in Fallout | — | Don't use it for "Fallout-ness". https://typodermicfonts.com/monofonto/ · https://www.myfonts.com/fonts/typodermic/monofonto/ |
| **Print Char 21** (Apple II) | No | **[licence unverified]** | Kreative Korp | — | https://kreativekorp.com/software/fonts/apple2/ |

**Minimum readable sizes (Playdate's guidance, which is the best published pixel-type spec):** sizes are cap height in pixels. Dialogue text needs at least 12 px and ideally 14 px. HUD text can go down to 10 px. Nothing should be below 8 px. Strokes should be at least 2 px thick, since thinner ones look "wispy". Text-heavy games should aim for about 13 px caps with 2 px strokes. Important or slow screens should use more than 16 px (https://help.play.date/developer/designing-for-playdate/ · https://help.play.date/developer/user-experience-checklist/). Playdate's pixels are about 173 ppi, so those values map roughly to a 1–2 pt font pixel on a phone **[my inference]**.

---

## C. Legibility and accessibility evidence

**Polarity.** For people with normal vision, light text on dark (negative polarity) is generally *less* legible.

- NN/g: "in users with normal vision, light mode leads to better performance most of the time", and "the smaller the font, the better it is for users to see the text in light mode" (citing Piepenbrock et al. 2013 in *Ergonomics* and in *Human Factors*) (https://www.nngroup.com/articles/dark-mode/). The Human Factors paper reports that the positive-polarity advantage "linearly increased with decreasing character size" (https://metatoc.com/papers/26930-positive-display-polarity-is-particularly-advantageous-for-small-character-sizes-implications-for-display-design).
- Dobres et al. (2016): positive-polarity glance-legibility thresholds were 38.6% lower (https://pmc.ncbi.nlm.nih.gov/articles/PMC5213401).
- Bauer & Cavonius (1980), "Improving the legibility of visual display units through contrast reversal", in Grandjean & Vigliani (eds.): widely cited as finding dark-on-light 26% more accurate. **[unverified: I found no primary text, and one secondary page characterises it differently]** (https://git.pleroma.social/pleroma/pleroma/-/merge_requests/3045/pipelines · https://laurenscharff.com/research/agecontrast.html).
- Exceptions: people with cloudy ocular media (e.g. cataracts) read faster in dark mode (Legge 1985, via NN/g above).

**Halation and astigmatism.** Light text on black blooms ("halation"), which is worse for people with astigmatism because the iris dilates in dark surroundings (https://modus.trimble.com/foundations/dark-mode). This is design-system guidance, not a controlled study. A CRT glow effect adds artificial halation on top of the optical kind **[my inference]**.

**Phosphor colours.** P1 green peaks at about 525 nm and P3 amber at about 602 nm. Common hex renderings are #33FF33 (P1), and #FFB000 or #FFB700 (P3). Wavelength-to-RGB methods disagree: P1 also renders as #4AFF00 or #00FA37 (https://publish.obsidian.md/xybre/permalink/e397c38e-aa6f-45eb-831f-f02a3836abc4).

**Contrast ratios [computed with the WCAG relative-luminance formula]:**

| Pair | Ratio | Passes |
|---|---|---|
| #33FF33 on #000000 | 15.5 | AAA |
| #33FF33 on #101810 | 13.4 | AAA |
| #FFB000 on #000000 | 11.5 | AAA |
| "dim" green #1F7A1F on black | 3.9 | **fails 4.5** |
| #0F5F0F on black | 2.7 | fails |
| dim amber #7A5400 on black | 3.1 | fails |
| DMG #0F380F on #9BBC0F | 6.0 | AA |
| DMG #306230 on #9BBC0F | 3.3 | large text only |
| Win95 black on #C0C0C0 | 11.5 | AAA |
| disabled #808080 on #C0C0C0 | 2.2 | fails, acceptable only for disabled controls |

Full-intensity phosphors pass easily. The dim secondary tiers that make the look feel "authentic" are what fail. Apple applies WCAG AA: 4.5:1 for text up to 17 pt, and 3:1 for 18 pt or bold (https://developer.apple.com/design/human-interface-guidelines/accessibility).

**Bitmap fonts at small sizes.** These need integer scaling and no anti-aliasing. Fractional scaling or linear filtering blurs glyphs (https://itch.io/post/2327468 **[forum]** · https://gitlab.gnome.org/GNOME/mutter/-/issues/1135 · https://fedoraproject.org/wiki/Fonts/Silkscreen).

**All caps.** Many pixel fonts are caps-only. Lowercase running text is read about 5–10% faster (https://microsoft.com/en-us/research/uploads/prod/2021/06/Larson-2005-the-science-of-word-recognition.pdf). Tinker found uppercase slowed reading over long passages (https://lists.w3.org/Archives/Public/w3c-wai-ig/2017AprJun/0138.html).

**Scanlines, flicker and glow.** Practitioners report that CRT shaders make dialogue and menu text unreadable, that "any amount of added bloom kills things on the bright end", and that strong scanlines cause eye strain. The usual fix is to switch the effect off on text-heavy screens (https://forums.libretro.com/t/objective-image-quality-when-using-shaders/28903?page=2 **[practitioner forum, no formal study found]**). Pope found large dithered pixels uncomfortable on a big screen (https://blog.playstation.com/archive/2019/10/17/lucas-pope-on-return-of-the-obra-dinns-art-style). Playdate warns that scrolled 2×2 dither checkerboards *flash* (https://help.play.date/developer/designing-for-playdate/).

**Flashing and motion rules.**
- WCAG 2.3.1 (Level A): no more than three flashes in any one second, or stay under the general and red flash thresholds. A general flash is a pair of opposing luminance changes of at least 10%, where the darker state is below 0.80 relative luminance. The area allowance is 25% of a 10° field, about 341×256 px (https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html). A 60 Hz CRT flicker loop that swings luminance by 10% or more fails this outright **[my inference]**.
- Apple asks apps to respond to Reduce Motion by "reducing automatic and repetitive animations". It also offers a system "Dim Flashing Lights" setting (https://developer.apple.com/design/human-interface-guidelines/accessibility).
- On the web, `prefers-reduced-motion: reduce` maps to the iOS/macOS Reduce Motion setting and Android's "Remove animations" (https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion).

**Font scaling.**
- Apple asks for text to be enlargeable to at least 200%. iOS body text defaults to 17 pt, with an 11 pt minimum (https://developer.apple.com/design/human-interface-guidelines/accessibility).
- In SwiftUI, `Font.custom(_:size:relativeTo:)` scales with Dynamic Type, while `custom(_:fixedSize:)` does not (https://developer.apple.com/documentation/swiftui/font/custom(_:size:relativeto:)). UIKit's equivalent is `UIFontMetrics` (https://developer.apple.com/documentation/uikit/uifontmetrics).
- Android 14 scales fonts up to 200% on a **non-linear** curve (https://developer.android.com/about/versions/14/features). A pixel font in `sp` will therefore land on non-integer multiples.
- Rule: snap pixel fonts to the nearest integer multiple of their grid for each Dynamic Type or fontScale step (`fixedSize`, chosen from `dynamicTypeSize`), and fall back to a vector mono (IBM Plex Mono) at accessibility sizes. **[my design recommendation]**

---

## D. Implementation craft

- **Nearest-neighbour scaling.**
  - SwiftUI: `Image(...).resizable().interpolation(.none)`. `.none` means "SwiftUI doesn't interpolate image data" (https://developer.apple.com/documentation/swiftui/image/interpolation/none).
  - Compose: `FilterQuality.None` is "Fastest possible filtering… Typically this implies nearest-neighbour filtering". Pass it to `Image(bitmap, filterQuality = FilterQuality.None)` or `DrawScope.drawImage` (https://developer.android.com/reference/kotlin/androidx/compose/ui/graphics/FilterQuality).
  - CSS for mocks: `image-rendering: pixelated` uses nearest neighbour to the nearest integer multiple, then smooths the remainder. `crisp-edges` is pure nearest neighbour (https://developer.mozilla.org/en-US/docs/Web/CSS/image-rendering).
- **Integer grid.** Pick one "art pixel" unit, for example 2 pt or 3 pt, and lay everything out on it: borders, icon sizes and spacing. On iOS (@2x/@3x) an integer number of points is always an integer number of pixels. On Android, fractional densities such as 2.625× make 1 dp a non-integer number of pixels. Either size the art in px through `LocalDensity`, or accept slight softness **[my inference]**. Shovel Knight shows the trade-off: a 400×240 virtual canvas at 4.5× on 1080p (https://www.yachtclubgames.com/blog/breaking-the-nes/).
- **Touch targets.** The art can be small but the hit area cannot. Apple's minimum is 44×44 pt on iOS (https://developer.apple.com/design/human-interface-guidelines/accessibility). Android's is 48×48 dp, and Material components pad to it only when they are clickable (https://developer.android.com/guide/topics/ui/accessibility/apps · https://developer.android.com/develop/ui/compose/accessibility/api-defaults). A 16×16 sprite icon at 2× (32 pt) needs `.contentShape` or padding up to 44 pt.
- **Safe areas.** No source specific to pixel UIs was found. Keep pixel frames inside the safe area, let the background colour or pattern bleed to the edges, and never align a bitmap border to the rounded display corners **[my recommendation]**. Playdate can run art to the edge only because it has a 3 mm black bezel (https://help.play.date/developer/designing-for-playdate/).
- **Cheap CRT.**
  - Prefer type-level effects such as Sixtyfour/Workbench's SCAN and BLED axes (https://github.com/google/fonts/tree/main/ofl/sixtyfour).
  - A static scanline overlay at low opacity can go on *chrome and hero areas only*. Use a single soft text-shadow for glow.
  - Skip curvature, chromatic aberration, jitter and flicker on content.
  - Gate every animated effect on Reduce Motion, and offer a setting to turn effects off, as Balatro does (https://steamcommunity.com/app/2379780/discussions/0/4201364375109001844 **[forum]**).
  - Drop effects entirely on reading-heavy screens (https://forums.libretro.com/t/objective-image-quality-when-using-shaders/28903?page=2).
- **Constraint systems beat purity.** Shovel Knight keeps the parts of the NES look that create the identity (the palette, 240 lines) and breaks the parts that only hurt (flicker, 4:3) (https://www.yachtclubgames.com/blog/breaking-the-nes/). Obra Dinn kept 1-bit but added outlines for legibility (https://blog.playstation.com/archive/2019/10/17/lucas-pope-on-return-of-the-obra-dinns-art-style).

---

## E. How these styles go wrong

1. **Pixel fonts at non-integer sizes or with anti-aliasing**: soft and smeared glyphs. Examples are Press Start 2P at 13 px or Silkscreen at 10 px (https://fedoraproject.org/wiki/Fonts/Silkscreen · https://github.com/google/fonts/tree/main/ofl/pressstart2p).
2. **Unreadable micro type**: body text at 5–8 px caps, or 1 px strokes. This breaks Playdate's floors of 8, 10 and 12–14 px and its 2 px stroke rule (https://help.play.date/developer/designing-for-playdate/).
3. **Everything uppercase** because the chosen font has no lowercase (https://microsoft.com/en-us/research/uploads/prod/2021/06/Larson-2005-the-science-of-word-recognition.pdf).
4. **Dim phosphor tiers below 4.5:1** for secondary text: #1F7A1F gives 3.9:1 and #7A5400 gives 3.1:1 **[computed]**.
5. **Long-form text on pure black at small sizes.** Negative polarity is worst for small text (https://www.nngroup.com/articles/dark-mode/). Halation affects people with astigmatism (https://modus.trimble.com/foundations/dark-mode).
6. **Effects over content**: scanlines, bloom, flicker or curvature on text and lists, and no off switch (https://forums.libretro.com/t/objective-image-quality-when-using-shaders/28903?page=2). Flicker loops can breach WCAG 2.3.1 (https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html).
7. **IP cosplay.** Vault Boy and Pip-Boy are Bethesda trademarks. Bethesda filed a Pip-Boy mark and fought Interplay over Vault Boy art (https://trademarks.justia.com/owners/bethesda-softworks-llc-2605529 · https://www.engadget.com/2010-12-23-fallout-over-bethesda-v-interplay-remains-unsettled.html). Monofonto needs a paid app licence (https://www.myfonts.com/fonts/typodermic/monofonto/). Minecraft-alike fonts carry IP doubt (https://issues.guix.gnu.org/57637). The same caution applies to Apple's Chicago, the rainbow logo and the Windows flag in the desktop direction **[my inference]**.
8. **Nostalgia costume with no product idea.** The anchors that work turn their reference into something else. Poolsuite moved Nokia 3310 cues into pink (https://techcrunch.com/2020/09/10/retro-inspired-music-player-poolside-fm-brings-its-summery-fun-to-iphone). Fallout made green an in-world fiction and a user setting (https://www.thegamer.com/fallout-3-green-colour-debate/). Alien: Isolation's lo-fi "didn't necessarily mean crappy" (https://www.engadget.com/2014-10-07-alien-isolation-launch-interview.html).
9. **Uncorrected raw ROM bitmaps** pretending to be CRT text. Real terminals stretched dots and bled (https://www.masswerk.at/nowgobang/2019/dec-crt-typography).
10. **Noisy auto-dither** and scrolled checkerboards that flash (https://help.play.date/developer/designing-for-playdate/).

---

## Recommendation on the third direction

**Include "Bitmap desktop" (System 6/7, Win95/98 bevels, 1-bit), with these constraints:**

- **Different axis.** Its identity rests on *chrome* (title bars, bevels, window frames, menus, dither fills) rather than *glow* (terminal) or *sprites and palette* (pixel). So it does not collapse into the other two.
- **Positive polarity.** Black on white or black on #C0C0C0 (11.5:1 **[computed]**) avoids the dark-mode legibility penalty that the terminal direction carries (https://www.nngroup.com/articles/dark-mode/).
- **Native mapping.** Windows, lists, buttons and menus map one-to-one onto native SwiftUI and Compose controls, and MIT-licensed reference systems exist (https://github.com/sakofchit/system.css · https://github.com/jdan/98.css). Shipped anchors exist too: Obra Dinn (https://blog.playstation.com/archive/2019/10/17/lucas-pope-on-return-of-the-obra-dinns-art-style), Poolsuite web/Mac (https://thenextweb.com/news/retro-os-mac-windows-music-poolside) and Playdate.
- **Risks.** It invites trade-dress copying of Apple and Microsoft marks. Google Fonts has no Chicago, Geneva or MS Sans Serif equivalent, so mocks must use Silkscreen or Pixelify Sans for titles and a vector sans for body text.

Considered and not recommended for now: a "segment LCD / instrument" look (Teenage Engineering, Nothing's dot matrix, Doto on Google Fonts). It is a credible future direction, but the anchors here are thinner (https://www.soundonsound.com/reviews/teenage-engineering-op1 · https://www.droid-life.com/2025/06/02/nothing-killed-glyph-interface-but-probably-for-something-cooler/).
