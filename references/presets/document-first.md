# Preset: Document first (macOS only)

**Feel:** the document is the design. The app's identity is how it sets text (the face, the measure, the way markup is shown) and how completely the chrome gets out of the way when you work. Everything else is quiet and Mac-standard.

**Fits:** writing, notes, journals, screenwriting, translation and subtitling, code-adjacent text tools, reading and annotation.
**Doesn't fit:** apps whose content isn't text the user makes or reads at length; dashboards.

**Default dials:** `BOLDNESS 3–4 · MOTION 2–3 · DENSITY 3–6 · COLOR 1–3 · FIDELITY 5`

Sources and evidence: `research/macos-references.md` §5.

## Real anchors
- **iA Writer.** Built with almost no settings; Focus Mode dims everything but the current sentence; on the Mac the top bar disappears while you type; Markdown keeps your hands off the mouse. Its own faces (Mono, Duo, Quattro) are OFL. [iA](https://ia.net/topics/ia-writer-for-mac)
- **Ulysses.** Groups, a sheet list and the editor in three panes that collapse one at a time.
- **Bear.** Tags in the sidebar, markup shown and styled rather than hidden, a warm editor face.

## Type
- **The editor face is the brand.** Pick one with a real text cut and good figures: iA Writer Quattro/Duo/Mono, Literata, Newsreader, Source Serif 4 (all OFL). Set it at 15–18 pt with a 64–72-character measure and 1.4–1.6 line height. The UI around it stays SF Pro at 13 pt.
- Headings in the document are set by the editor (real sizes and weights), not by a toolbar.
- Offer zoom (⌘+ / ⌘−) and a few editor sizes; there's no Dynamic Type on the Mac.

## Colour
- Paper and ink, near-monochrome, one marker colour (the caret, the selection, links, the current-sentence highlight).
- Dark mode is a real night palette, not inverted paper: lower-contrast ink on warm or cool black.
- **Not cream and terracotta by reflex**: that's a dated "tasteful AI" tell. Derive the paper and marker from the product's world.

## Shape and layout
- No boxes in the editor: margins, measure and space do the work.
- Lists and library panes are standard (rows 28–44 pt with first lines), with 1 pt dividers between panes.
- Chrome fades while typing and returns on pointer move, so it's never hidden permanently.

## Icons
- Few. Words in the toolbar where space allows ("Export", "Share"). Markup glyphs (#, **, >) are shown dimmed in the text itself.

## Motion
- Chrome fades over ~300 ms when typing starts. Focus dimming crossfades in ~200 ms. Panes slide in 200 ms. Nothing loops. Under Reduce Motion, all of it is instant.

## Signature moves (pick 2–3)
1. **Chrome that disappears while typing** and returns on pointer move.
2. **Focus mode:** only the current sentence or paragraph at full ink.
3. **Markup shown and styled** (dimmed syntax, real headings) instead of hidden.
4. **Panes that collapse one by one** with ⌘1/⌘2/⌘3.
5. **The document's own number** (reading time, word target, timecode) as the single readout.
6. **A sheet list that shows first lines**, not just titles.

## Platform notes
- Mac-only; `deal.py` deals it only with `--platform macos` (with `--content document`).
- Use the system text stack (`NSTextView` via a small representable, or `TextEditor` for simple cases) so spelling, dictation, Writing Tools, find, undo and the services menu all work. A custom text engine that loses these isn't Mac-like, however it looks.
- Full keyboard use, VoiceOver reading the document, and the system's find bar (⌘F) are hard requirements.

## How cheap imitations go wrong
- Minimal as an excuse for missing features: no search, no export, no word count.
- A web-style rich-text toolbar floating over the editor.
- A fixed editor size with no zoom, or the editor set at the 13 pt UI size.
- A typewriter skeuomorph: paper texture, a fake carriage return sound by default.
