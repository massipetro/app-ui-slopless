# Mascot kit: draw it, ship it, animate it

How to design a mascot or hero glyph that this skill can draw well, then ship it as native code and animate it as Lottie with `scripts/mascot.py`. Read this when the brief has a mascot, a character, empty-state art with a face, or a hero glyph that should move (the streak flame, the core verb's check).

## Contents
1. What works and what doesn't
2. Design it from the direction
3. The rig: groups, pivots, rest poses
4. The four tests
5. Ship it natively (`svg2code`)
6. Animate it (`lottie`)
7. Look at the motion (`preview`, filmstrip, pass 14)
8. Limits

## 1. What works and what doesn't

**Works:** flat, geometric characters built from a handful of primitives, like Duolingo's Duo, Headspace's smiley, Gentler Streak's Yorhart, or a toy-like blob with big eyes. A model draws these well because each part is a circle, an ellipse, a rounded rect or a short cubic curve with numbers you can reason about. They read at 24 px, take 2–3 flat colours, and animate by moving whole parts (squash, hop, blink, wave).

**Doesn't work:** painterly, textured, shaded or detailed characters: fur, hair strands, gradients for volume, hands with fingers, realistic faces, anything that needs an illustrator's hand. A model's attempt looks lumpy and uncanny, and it's the "stock 3D blob" slop tell. If the brief needs that, say so, and design the slot (size, pose list, states it reacts to) for a commissioned artist instead of drawing it.

**Rive can't be generated.** Duolingo animates in Rive state machines, but `.riv` is a binary editor format with no text form to write. This kit makes Lottie (JSON), which every platform plays. Say so if the user asks for Rive. A Lottie with named states and markers is the honest substitute; a designer can rebuild it in Rive later from the same SVG.

**Gradients aren't supported yet.** A gradient fill is drawn as its first stop colour, with a note. Flat colour is the style anyway.

## 2. Design it from the direction

The mascot belongs to the dealt direction, not to "cute":
- **Shape language.** Take the primitives from the direction sheet's `shape` line and the preset file. Playful: rounded rect, circle, rounded triangle, round caps, no sharp corners. Neo-brutalist: squares and hard rectangles, 2.5–3 dp ink outline, square caps, a hard offset shadow drawn as a second, offset copy of the silhouette in ink. Editorial: one heavy geometric mark (a letterform, a dot) rather than a character. Use the same corner and stroke rules as the custom icons, so the mascot looks like one family with them.
- **Palette: 2–3 colours from the deal sheet.** Usually the accent (body), the ink (eyes, mouth, outline) and the surface or ground (belly, eye whites). `mascot.py check` counts them; a fourth has to earn its place (a cheek, a lip shade from the preset's lip rule). Never a new hue invented for the mascot.
- **Proportions for small sizes.** A big head-body (one mass), eyes about a fifth of the body's width each, set wide, and one feature that makes the silhouette unique: Pip's sprout, a crest, ears, a beak, a tail. Limbs are short ovals that sit at the sides.
- **The product's inventory.** The character comes from the product's own objects (step 1): a seed for a habit garden, a ticket stub for a ferry, a coin for a budget jar. It isn't a generic animal.
- **Build in SVG by hand.** Write the SVG directly: primitives first, then cubic paths only where a curve needs character (a body that's an egg rather than a circle, a leaf, a smile). Keep coordinates on whole or half units in a 100–150 unit box, so you can edit by reasoning about the numbers.
- **Leave headroom.** The viewBox is the motion box, not the art box: a hop of 18 units needs 18+ units above the head, and a squash to 112% needs ~6% at the sides. Lottie players clip at the canvas, and `mascot.py lottie` reports any part that leaves it. A negative viewBox origin (`viewBox="-12 -24 144 144"`) adds room without moving the art.

## 3. The rig: groups, pivots, rest poses

Each part that moves is a `<g>` with an `id` and a pivot in viewBox units:

```xml
<g id="body" data-pivot="60,112">            <!-- squash from the feet -->
  <g id="arm-left" data-pivot="26,76"> … </g> <!-- shoulder -->
  <path id="body-shape" … />
  <g id="eyes" data-pivot="60,58"> … </g>
  <g id="lids" data-pivot="60,46" data-rest="scale:100,0"> … </g>  <!-- hidden until a blink -->
  <g id="mouth" data-pivot="60,76"><path id="mouth-smile" … /></g>
</g>
<defs><path id="mouth-open" … /></defs>       <!-- a morph target, same vertex count -->
```

- **The usual parts:** `body`, `eyes`, `lids`, `mouth`, limbs (`arm-left`, `arm-right`, `foot-…`), and one signature part (`leaf`, `tail`, `flame`). Add `spark` or `confetti` for a reaction's effects. Fewer parts are better: each one is a layer to keep in sync.
- **Pivots are where the part hinges:** the body at its feet (squash and hop read as weight), an arm at its shoulder, the lids at the top edge of the eyes (a blink closes downward), a leaf at its stem, the mouth at its centre.
- **Nesting is parenting.** A group inside another moves with it, so the face rides the body's squash. Draw order is z-order, the same as in SVG, including shapes after a nested group (the kit splits them into extra layers to keep the order).
- **Rest poses:** `data-rest="scale:100,0"` (lids), `data-rest="opacity:0"` (sparks), also `rotation:` and `position:dx,dy`. The native code and the Lottie both start from it.
- **Opacity and trim apply to a part's own shapes, not to the parts nested in it.** This matches Lottie and After Effects. Fade a whole character by fading each part, or the view that holds it.
- **Lids beat scaling the eyes.** A body-coloured lid that scales in from the top reads as a blink at 24 px and keeps the pupils in place. Squashing the eyes to a line looks like a squint.
- **Morph targets** live in `<defs>` with an id, and must have the same number of vertices, in the same order, as the shape they replace. Draw the open mouth by moving the smile's points, not by drawing a new shape.

## 4. The four tests

Run `python3 <skill>/scripts/mascot.py check mascot.svg --bg <ground>` and look at the PNG. It shows the rest pose at 160 px, squinted, at 48 and 24 px, as a silhouette at 48 and 24, and on the ink colour.
1. **Silhouette at 24 px.** Filled black, does it still name the character and not "a blob"? The signature part (sprout, ears, crest) should stick out of the outline. If it doesn't, make the part bigger or move it to the edge of the outline.
2. **Squint.** Grey and blurred, the face (two eyes and a mouth) is still the strongest contrast in the shape. If the eyes vanish, they're too small or too close in value to the body.
3. **Expression at small size.** At 24 px, can you tell happy from worried? One clear mouth shape and the eye whites carry it. Brows and pupils alone don't.
4. **On ink.** On the dark ground it doesn't disappear. Dark mode needs at least one light part (belly, eye whites) or an outline.

Write the results in the report: "silhouette 24: reads (sprout); squint: face holds; 24 px happy/worried: distinct".

## 5. Ship it natively (`svg2code`)

```bash
python3 <skill>/scripts/mascot.py svg2code pip.svg --swift -o PipMascot.swift
python3 <skill>/scripts/mascot.py svg2code pip.svg --compose --package app.ui.mascot -o PipMascot.kt
# the brief names one file for the code: add it to that file instead
python3 <skill>/scripts/mascot.py svg2code pip.svg --compose --into HabitHomeScreen.kt
```

`--into` merges the imports into the screen file, drops the package line, and puts the code in a marked block at the end; rerunning after an SVG edit replaces that block. This is how a single-file brief still gets the kit's drawing: never hand-copy or redraw the shapes. In the HTML mock, paste the same SVG inline and animate its groups with CSS, with `transform-origin` at each `data-pivot`, so the mock shows exactly what ships.

No runtime library is needed. It handles path commands (M L H V C S Q T A Z, relative too; arcs become cubics), rect with rx/ry, circle, ellipse, line, polyline, polygon, nested transforms, fill, stroke, width, caps, joins, fill-rule and opacities. Styles can come from attributes, `style=""` or simple `<style>` rules (`.class`, `#id`, tag), as Illustrator exports them.

- **SwiftUI:** `PipMascot(pose:)` draws the rig. Each drawn part is a `Shape` (strokes come out outlined, so they scale), each rig group is a nested layer with its pivot as the anchor, and `PipPose` (offset, scale, rotation, opacity, trim) animates through a `GeometryEffect`:
  ```swift
  @State private var pose: [PipRig: PipPose] = [:]
  PipMascot(pose: pose).frame(width: 120, height: 120).accessibilityHidden(true)
  // celebrate
  withAnimation(.spring(duration: 0.35, bounce: 0.55)) { pose[.body] = PipPose(scale: CGSize(width: 1.1, height: 0.9)) }
  ```
- **Compose:** `PipVector` is a static `ImageVector` at rest (icons, widgets, placeholders). `rememberPipPainter(pose)` is the animatable one; drive the pose from `animateFloatAsState` or an `Animatable` and draw it with `Image(painter, contentDescription = null)`.
- **Gate it like any other code:** `typecheck.py` and `compile_kotlin.py` (`lint.py` warns `no-reduce-motion` on the generated painter, because the caller decides about Reduce Motion: honour it there). Under Reduce Motion, keep the pose changes that carry meaning (the happy face, the closed eyes) as instant changes, and drop hops, breathing and loops.
- **Native or Lottie?** Native code suits a few poses driven by app state, with springs that interrupt nicely (press, check-off, mood). Lottie suits authored sequences (a celebration with sparks drawing on, a morph). The same SVG makes both, so they match.

## 6. Animate it (`lottie`)

```bash
python3 <skill>/scripts/mascot.py lottie pip.svg pip.motion.json -o pip.json
```

The motion spec is a list of named states. Each animates rig parts with keyframes; `ease` on a key shapes the move from that key to the next, as in CSS:

```json
{ "fr": 60,
  "states": [
    { "name": "idle", "loop": true, "ms": 2400, "tracks": {
        "body": { "scale": [ {"t": 0, "v": [100, 100], "ease": "inOut"}, {"t": 1200, "v": [98, 103], "ease": "inOut"}, {"t": 2400, "v": [100, 100]} ] },
        "lids": { "scale": [ {"t": 0, "v": [100, 0], "ease": "hold"}, {"t": 1500, "v": [100, 0], "ease": "in"},
                             {"t": 1560, "v": [100, 100], "ease": "out"}, {"t": 1660, "v": [100, 0], "ease": "hold"}, {"t": 2400, "v": [100, 0]} ] } } },
    { "name": "celebrate", "ms": 900, "tracks": {
        "mouth": { "path": [ {"t": 0, "v": "mouth-smile", "ease": "out"}, {"t": 160, "v": "mouth-open", "ease": "hold"}, {"t": 780, "v": "mouth-smile"} ] },
        "spark": { "trim": [ {"t": 220, "v": [0, 0], "ease": "out"}, {"t": 420, "v": [0, 100]} ] } } }
  ] }
```

- **Properties:** `position` (offset `[dx, dy]` from rest, viewBox units), `scale` (`[sx, sy]` percent), `rotation` (degrees clockwise), `opacity` (0–100), `trim` (`[start, end]` percent of each path: draw-on), `path` (a morph target's id).
- **Eases:** `linear`, `in`, `out`, `inOut` (the default), `back` (small overshoot), `hold` (step), or `[x1, y1, x2, y2]`.
- **States:** one idle loop (breathe 2–3 s, blink every 3–6 s, a gentle sway) and one reaction per moment that matters (`pop`, `celebrate`, `worried`). They're laid end to end with a marker each. Play one by marker name: lottie-web `goToAndPlay('celebrate')`, lottie-ios `play(fromMarker:toMarker:)`, lottie-android `setMinAndMaxFrame("celebrate")` (lottie-compose: a marker clip spec). For CMP, use a multiplatform Lottie player such as Compottie, or wrap the native views. Check the API names against the player version in the project.
- **Refusals, not surprises:** an unknown part or property, keys less than a frame apart, a key past the state's end, or a morph between shapes with different vertex counts all stop the build with the reason. A loop that doesn't end where it started gets a note. So does any part that leaves the canvas, with the time range in ms.
- **Timing by preset.** Playful: squash 80–100 ms, the hop's peak at ~300 ms, `back` on the landing, a celebration of 600–900 ms (2.5 s at most for a milestone). Neo-brutalist: 100–200 ms, `linear` or `hold` (stepped, stamped), no overshoot, no breathing. The motion budget's `MOTION` row decides whether there's an idle loop at all.

## 7. Look at the motion (`preview`, filmstrip, pass 14)

```bash
python3 <skill>/scripts/mascot.py preview pip.json --bg <ground>
python3 <skill>/scripts/filmstrip.py pip.preview.html --crop 0,0,240,240 --times 0,80,160,240,320,480,640,880
python3 <skill>/scripts/filmstrip.py pip.preview.html --hash state=idle --crop 0,0,240,240 --times 0,600,1200,1500,1530,1560,1620,1800
```

The preview plays the Lottie with lottie-web 5.12.2 from cdnjs (it needs network). lottie-web runs on `requestAnimationFrame`, which `document.getAnimations()` can't see, so the page drives it from a Web Animation clock: filmstrip pauses the clock at each t and measures it ("1 animations · longest finite 900 ms" for a reaction, "1 looping" for idle). `#play` plays the first non-looping state, and `#state=<name>` plays any state. `--frames` drops the clock and steps with `?t=<ms>` and `goToAndStop` directly, if a browser misbehaves with the clock.

Read both strips with `references/critique.md` pass 14: the reaction visibly changes and lands back on rest, nothing clips against the canvas, the squash reads before the hop, overshoot is small, the blink is 2–3 frames closed, not a slow fade. Put the numbers on the report's "Live thing" line, and the four tests' results next to them.

## 8. Limits

- Flat geometry only (section 1). Gradients become their first stop colour. Masks, clip paths, filters, `<use>`, images and text are skipped with a note: outline text and expand symbols before converting.
- Path morph is Lottie only, and only between shapes with the same vertex count. In native code, swap the shape (`opacity`) or animate the parts around it.
- No Rive (`.riv` is binary). No bone deformation or mesh warps: parts move rigidly about their pivots, which is the flat style's grammar anyway.
- Group opacity on a non-rig `<g>` is folded into its children, so overlapping children inside it look slightly different from a browser.
- The generated code is a snapshot of the SVG. Edit the SVG and regenerate it; don't hand-edit the Swift or Kotlin.
