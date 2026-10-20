# Preset: Pro instrument (macOS only)

**Feel:** a tool that disappears into the work. Dense, fast, keyboard-first, with the content in the middle, controls at the edges and every readout exact. Its personality is precision: the way a value scrubs, how the command palette answers, a live number in the menu bar.

**Fits:** creative and media tools, developer tools, data, trading and monitoring, admin consoles, launchers and automation, anything used daily by experts for hours.
**Doesn't fit:** kids, casual consumer apps, first-time or once-a-month users (they need the novice path first).

**Default dials:** `BOLDNESS 4 · MOTION 3 · DENSITY 8–9 · COLOR 2–3 · FIDELITY 4–6`

Sources and evidence: `research/macos-references.md` §3–4.

## Real anchors
- **Raycast.** Fast, simple, delightful. A big search field, an action bar for the selection, a Compact Mode, a keycap icon that says "keyboard". [Raycast blog](https://www.raycast.com/blog/a-fresh-look-and-feel)
- **Linear (desktop app).** ⌘K on everything, dense lists, shortcuts shown in place. Borrow the app, not the marketing site.
- **Logic Pro, Final Cut Pro, Pixelmator Pro.** Content in the centre, tools and a tabbed inspector at the edges, neutral grey chrome, tabular readouts (by observation).
- **iStat Menus, Fantastical.** A live value in the menu bar, and a full mini window one click away.

## Why it works (the literature)
- Hotkeys make experts much faster but are learned slowly, and showing the mapping at the moment of the click measurably speeds learning (Grossman et al., CHI 2007). So show the shortcut **on the row and in the palette**, not only in the menu.
- People don't switch to expert methods on their own. The interface has to prompt the switch, keep the dip small and allow a high ceiling (Scarr et al. 2011; Cockburn et al. 2014).
- The menu bar sits on the screen edge, so it's the cheapest target on a Mac (Tognazzini's "mile-high menu bar"). That makes a menu bar extra the cheapest possible glance.
- Experts handle density that would overwhelm novices. Let the user adjust it (compact and comfortable).

## Type
- **SF Pro** at 11–13 pt for UI. **SF Mono**, JetBrains Mono or IBM Plex Mono for values, IDs, timecodes and shortcuts. One display readout per window at 28–40 pt.
- Tabular figures everywhere a number updates. Units in the text face, smaller, after the value.

## Colour
- **Neutral chrome** (graphite or studio grey, light and dark) so the content's colour is judged correctly.
- Colour in the chrome means **state**: record or live red, selection blue, warning amber, ok green, each with a word or shape too.
- One key colour for the brand: the palette's highlight, the active tool.
- **Not the "Linear style"**: no dark gradient backgrounds, no glowing accents, no purple light leaks. It became the 2025–26 SaaS default and reads as slop.

## Shape and layout
- Radius 4–6. 1 pt dividers between panels. `controlSize(.small)` for inspector controls, with a typed value field next to every slider.
- Panels resize, collapse and remember their arrangement. On a 13-inch screen the content still gets ≥60% of the width.
- Lists at 22–26 pt rows, with a compact/comfortable toggle.

## Icons
- SF Symbols at the small size for tools, each with a tooltip (`.help`) that names it and its shortcut.
- The keycap is the signature glyph: drawn as an 18 pt rounded rect with a 1 pt stroke, wherever a shortcut is shown.

## Motion
- Functional only. Meters and playheads move in real time; the palette opens in ≤100 ms; panels collapse in 150 ms. Selection never animates.

## Signature moves (pick 2–3)
1. **⌘K command palette** that finds items and verbs, with the shortcut on every result.
2. **Keycap hints** beside rows and in an action bar for the selection.
3. **Scrub-to-set values:** drag over a label to scrub, click to type, arrow keys to nudge, ⌘Z to undo.
4. **Inspector tabs** that remember their state per selection type.
5. **The live value in the menu bar** (≤6 characters, so the notch doesn't hide it), with a popover for the next few items.
6. **State colour only** in the chrome.

## Platform notes
- Mac-only; `deal.py` deals it only with `--platform macos`.
- The palette is an accelerator, never the only way in: every command also lives in the menu bar. Don't take the standard shortcuts (⌘N, ⌘W, ⌘,, ⌘Z…) for other meanings.
- Keyboard-only use must be complete, and VoiceOver must read values with their units.

## How cheap imitations go wrong
- The Linear-style landing-page look applied to an app: dark gradients, glow, purple.
- Dark mode for its own sake on an app whose content is light (documents, spreadsheets).
- 10 pt grey-on-grey labels below contrast. Density is no excuse for 3:1 text.
- Panels that can't be hidden on a laptop, and a palette that hides features the menus don't show.
- A menu bar extra that is wide, coloured or polls constantly.
