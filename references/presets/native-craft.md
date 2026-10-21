# Preset: Native craft (macOS only)

**Feel:** a Mac-assed Mac app. It behaves exactly like a Mac app (menus, shortcuts, focus, drag and drop, right-click, a real Settings window) and is unmistakably *this* app because its identity is concentrated in a few places that are built with care. The craft is in what's left out.

**Fits:** almost every Mac app, and especially utilities, productivity, readers, file and developer tools, and any app used for hours next to other apps.
**Doesn't fit:** kids' apps and games (they want Playful), a brand whose whole value is spectacle.

**Default dials:** `BOLDNESS 3–5 · MOTION 3–4 · DENSITY 5–8 · COLOR 3–5 · FIDELITY 2–6` (the direction decides: *native chrome, owned content* sits at F3, *owned chrome* at F6).

Sources and evidence: `research/macos-references.md` §1–2.

## Real anchors
- **Panic: Nova and Transmit.** Stock Mac controls, a Settings window modelled on System Settings that applies changes immediately, a sidebar that behaves like Finder, and one lavish brand moment (Nova's animated welcome). [MacStories](https://www.macstories.net/reviews/nova-review-panics-code-editor-demonstrates-why-mac-like-design-matters/)
- **NetNewsWire.** Brent Simmons' own example of a "Mac-assed Mac app": three panes, standard everything, fast. [Daring Fireball](https://daringfireball.net/linked/2020/03/20/mac-assed-mac-apps)
- **Things 3 for Mac.** Custom chrome with Mac manners: bold type, white space, coloured glyphs, a toolbar that isn't at the top, no translucency under the content. [MacStories](https://www.macstories.net/reviews/things-3-beauty-and-delight-in-a-task-manager/) · [Simmons 2026](https://inessential.com/2026/09/22/that-about-wraps-it-up-for.html)
- **Ivory for Mac.** System fonts throughout, with the brand carried by mascot art, sound and accent themes; up to six user-arranged columns. [MacStories](https://www.macstories.net/reviews/ivory-for-mac-review-tapbots-superb-mastodon-client-comes-to-apple-desktops-and-laptops/)

## Two honest kinds of native
- **Native chrome, owned content:** the system's chrome, controls and materials, with the identity drawn **into the content column**: a custom column, glyph or mini-visual in every row that only this product has, and one display moment heading the column. Restraint in the chrome, not in the content. Brand only in the inspector, Settings or first run is invisible in the resting window, and blind judges cap it as a stock layout (round 11). Not dealt for collection or hobby briefs (`deal.py --content …collection`, `--sector hobby`): even with the idea in every row it lost all three it was dealt in rounds 11 and 11b to directions that make the collecting itself the layout (a year grid that shows the gaps).
- **Owned chrome:** the app draws its own window (an opaque sidebar, its own toolbar), but every Mac *behaviour* stays. Simmons' 2026 argument is that stock UI is no longer the safe choice under Liquid Glass; Things is the proof that custom can be Mac-like.

Either way, the tell of a fake is the same: Mac *looks* without Mac *behaviour*.

## Type
- System faces are legitimate here: **SF Pro** at the Mac scale (body 13 pt, headline 13 bold, title 15–22 pt), with **SF Mono** or `.monospacedDigit()` for numbers. One display moment per window (a list title at 22–28 pt bold, or **New York** for an editorial heading).
- A custom face only if the brand owns one. Use it for titles, never for the 13 pt UI text.
- Counts, times and sizes in tabular figures.

## Colour
- The **user's accent colour drives standard controls**. The brand colour takes the one owned control, the area or section identity, and perhaps the selection. Say which in the brief.
- Light and dark are equal. Check text over materials at the user's Liquid Glass setting, from clear to opaque (macOS 27 added a slider), and with Reduce Transparency on.
- Colour in splashes with a role (Things' area colours, coloured sidebar icons, which macOS 27 restored), never a tinted wash over the whole window.

## Shape and layout
- System radii and controls. Edge-to-edge sidebar. Rows at 24–28 pt. Dividers and tone steps instead of cards.
- Density is a feature: a Mac list shows 15–30 rows.
- Toolbars: either the standard NSToolbar with `Label`s, or (owned chrome) a compact bar at the foot of the list with coloured, spaced icons. Either way, every toolbar item also lives in a menu with a shortcut.

## Icons
- SF Symbols for utility chrome, at the system size, in the sidebar's colours.
- **One custom glyph family** for the core verb and the areas or categories, drawn in code (`Path`/`Canvas`, or the mascot kit for anything figurative).
- **No icon on every menu item** (the Tahoe mistake; Apple now says to use them sparingly). Icons only where a metaphor is clear: Share, Delete, a category glyph.

## Motion
- The system's own, plus one crisp animation on the core verb (≤250 ms) and one on first run.
- Rows that reorder slide; selection never animates.

## Signature moves (pick 2–3)
1. **A custom-drawn column in every row** carrying the owned idea; the chrome stays stock.
2. **A designed first run and empty state** that carry the owned idea, then convention (Panic's welcome).
3. **A full menu bar** with shortcuts for daily actions, and a real Settings window (⌘,) of native controls that apply immediately.
4. **Area colour and glyph** carried from the sidebar into the list and the item (Things).
5. **Owned bottom toolbar** under the list, coloured and spaced, mirrored in the menus.
6. **User-arranged columns**, saved per window (Ivory, NetNewsWire).

## Platform notes
- This preset is Mac-only; `deal.py` deals it only with `--platform macos`. On iPhone the closest equivalent is Warm premium at a low `FIDELITY`.
- Keep the traffic lights, a draggable title area, focus rings (or an equally visible drawn one), VoiceOver labels and full keyboard access. With owned chrome these are where it most often breaks.

## How cheap imitations go wrong
- Correct and forgettable: a stock table with the idea only in the inspector. Cover the inspector: if the content column alone could be Finder, it's a costume. Also: empty striped rows filling the window under a short list.
- Custom chrome that drops Mac behaviour: no right-click, no menu commands, a title bar you can't drag, no keyboard focus.
- An iPad layout scaled up: 44 pt rows, 20 pt radii, a bottom tab bar.
- An icon on every menu item, and translucent panels stacked on translucent panels.
