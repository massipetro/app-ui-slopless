# Preset: Playful / toy-like

**Feel:** chunky, tactile, alive. Buttons you want to press, a character who reacts, a core action that feels like a small win every time. Fun is the feature, but it's *designed* fun, with rhythm and restraint, not confetti everywhere.

**Fits:** habits, learning, fitness, wellbeing, kids and family, games, social, personal finance for beginners, onboarding-heavy consumer apps.
**Doesn't fit:** dense pro tools, serious bad-news surfaces. Keep the shell playful but calm those specific screens (R-EMO-6).

**Default dials:** `BOLDNESS 8 · MOTION 8 · DENSITY 3 · COLOR 8 · FIDELITY 7`

## Real anchors
- **Duolingo (ADA 2023).** Shapes built from a *few* rounded primitives with the fewest details needed, plus "rhythm" (deliberate variety of sizes). Bright, saturated colour framed by white space. A cast of characters animated in **Rive state machines** (20+ visemes, idle variations so loops don't repeat). The streak milestone turns Duo into a phoenix. The widget's Duo panics as midnight nears, *tied to real state*. Sound and haptics have separate toggles. [Shape language](https://blog.duolingo.com/shape-language-duolingos-art-style/) · [Streak animation](https://blog.duolingo.com/streak-milestone-design-animation/) · [Widget](https://blog.duolingo.com/widget-feature/) · [Rive + Lily](https://rive.app/blog/duolingo-s-ai-powered-video-call-brings-lily-to-life)
  - The 3D button "lip" (a darker bottom edge that disappears on press) is visible in the shipped app. There is no official write-up.
- **(Not Boring) Habits (ADA 2022).** The checkbox is an *explosive 3D event*: press and hold longer than expected, with a hold-progress cue, 6–7 layered effects, and custom sound and haptics. Standard controls stay stock. The journey is framed as 66 levels. [Behind the Design](https://developer.apple.com/news/?id=9ab1g4r3)
- **Headspace.** Signature orange, warm illustration, an orange smiley with a *range* of moods, breath-driven animation, and "simplicity at the surface" (a Today tab). [Behind the Design](https://developer.apple.com/news/?id=fkfnhq8u)
- **Pok Pok Playroom (ADA 2021).** Hand-drawn art with a rule that everything may "jitter a little", sounds recorded from real objects, and consistent mappings (blue = C). [Behind the Design](https://developer.apple.com/news/?id=5bcex7xf)
- **Bears Gratitude (ADA 2024).** The art came first and the app was built around it. Flip-card prompts, no sign-in wall. [Behind the Design](https://developer.apple.com/news/?id=i74v3f4r)
- **CARROT Weather (ADA 2021).** A persona with a user-selectable personality level (Professional → Overkill) over serious data.
- **Gentler Streak (ADA 2024).** The abstract mascot Yorhart, and encouraging rather than pushy copy. Proof that playful ≠ guilt-tripping. [Behind the Design](https://developer.apple.com/news/?id=3m0ht22s)

## Type
- **Rounded, heavy display face** plus a friendly, legible text face.
- OFL options: display **Fredoka 600–700**, **Nunito 900**, or **Baloo 2**; text **Nunito 600** (rounded UI); one-off hero words in **Lilita One** / **Titan One**.
- The key number (streak, XP, level) is huge (48–72 pt), heavy, and animates when it changes.
- Copy voice is short, warm, specific and a little cheeky, set by the persona's "this, not that" pairs.

## Colour
- **Vibrant and saturated, not pastel-only.** A primary hero colour, 3–4 supporting hues with *roles* (success green, streak orange, XP gold, info blue), on a white or very light base so the art doesn't fight the UI.
- Each pressable colour has a **darker "lip" partner** (same hue, ~20% darker in OKLCH L) for the 3D edge.
- Dark mode: deep tinted navy or plum surfaces (not grey), with the hues slightly lifted.
- Success, error and streak states are never colour-only. Pair them with an icon, a word, and the character's reaction.

## Shape and depth: a world of chunky toys
- **3 primitives** (rounded rect, circle, rounded triangle), corners always rounded (radius 14–20 on controls, full on chips), and **rhythm**: one big, two medium, many small.
- **Everything sits on a base.** The screen should look like a set of physical toy pieces, not flat UI with a few raised buttons.
  - **Pressables** (buttons, habit rows, answer tiles, tabs) sit on a **4–5 dp lip** in a darker shade of their own hue. On press, the face drops onto it and the lip disappears.
  - **Static panels** (the hero card, the week tray, stat blocks) get a **quieter 2–3 dp base** and never move. They still read as objects, but the difference in height and the lack of motion keep "what's pressable" clear.
- **Lips must be visible.** A lip needs ≥3:1 contrast against the surface below it. On white cards, use a 2 dp tinted border (e.g. `#E5E5E5` light grey-blue, or the hue at low L) **plus** a darker bottom edge in the same tint (`#D0D0D0`-ish or the hue's lip colour). A white card on a white lip is invisible, and invisible means flat.
- Cards are colour fields or white with a tinted border plus a lip. No soft grey shadows.
- A warm off-white or tinted base (`#FFF7E8` cream, `#F0F7FF` sky) gives white cards something to sit on. Pure white on pure white kills the toy feel.
- Illustration and character: **one system, one artist's hand**. Never mix packs.

## Icons: chunky, custom, alive
Stock rounded Material/SF icons look generic here. The style needs its own glyphs:
- **The check (or core verb) is the hero glyph.** Draw it: a thick (3–4 dp at 24 dp), rounded-cap tick, slightly asymmetric for hand-made charm, in white on the habit's hue or in the hue's dark lip colour. Animate it **drawing on** (path trim 0 → 1 in ~220 ms with an overshoot scale 0.6 → 1.15 → 1), with 6–8 sparkles bursting from the token.
- **Habit/category icons:** each habit owns a **vivid hue + a custom glyph** (water drop, book, shoe, moon) inside a lipped tile. Glyphs are chunky, filled, two-tone (a highlight on the face), and drawn in code as one family. Never emoji.
- **Streak flame:** a two-tone, layered flame (outer orange, inner yellow) with a subtle flicker loop (scale-y 1 → 1.06, 1.2 s, eased), stopped under Reduce Motion.
- **Tab icons:** filled when selected, with a little hop (translateY −3 dp spring) on selection.
- **Mascot:** built from the same primitives as the UI, with a few poses (happy, nervous, cheering) driven by app state. Blink every 3–6 s at random, and breathe (scale 1 → 1.03, 2.4 s).

## Motion: the screen is alive (default `MOTION 8`)
At this preset's default dial, the motion budget's 7–10 row is the brief, not an upper limit:
- **Entrance:** cards pop in staggered (scale 0.9 → 1 + fade, 40 ms apart, spring damping 0.6) on first load.
- **Every pressable squishes:** the face drops onto the lip and scales to ~0.96 in ≤80 ms, then springs back with a little overshoot on release.
- **Check-off:** token squish → fills with colour → check draws on → sparkles → row settles into its "done" pressed state, with a success haptic and an optional pop sound. Under 600 ms total, so it never slows down someone checking off five habits.
- **Numbers roll:** the streak counter rolls like an odometer, and the "3 of 5" chip bounces when it changes.
- **Ambient:** the mascot blinks and breathes, the flame flickers, and the hero art can bob gently. Small amplitude, slow cycles.
- **Milestones** (perfect day, 7/30/100-day streak) get a full moment: the mascot cheers, confetti in the brand hues, a big number slam. ≤2.5 s, skippable, once per event.
- **Reduce Motion:** keep the colour change, the check (shown fully drawn), haptic and sound; drop the bounce, ambient loops and particles.

## Motion details
- Springs: bouncy (damping 0.5–0.65) on presses, the core verb and celebrations; settled (0.8) on navigation. Bouncy dialogs and sheets are the cheap version.
- **Character state machine** (Rive/Lottie, or code-drawn with a few poses): inputs like `idle`, `celebrate`, `atRisk`, `sad`, with ≥3 idle variants. Its mood reflects *real app state*.
- Hold-to-complete (Not Boring) is an option for high-stakes verbs. For a quick daily check-off, a single tap with a rich animation is usually better. If you use hold, keep it ≤500 ms and provide a tap alternative for accessibility.
- Sound: a few slightly different variants of each click so repeats don't grate, with a toggle in settings. Haptics: light on press, success on completion. Never heavy on everything.

## Signature moves (pick 2–3)
1. **Lip buttons and lip check-offs** that compress on press.
2. **Celebration core verb:** hold-to-complete with a progress ring and a layered success.
3. **Mascot tied to state:** happy when on track, nervous near the deadline, cheering at milestones (with a small, consistent set of poses).
4. **Streak/progress as the hero:** a big flame or number at the top with a week row of chunky day dots below.
5. **Path or level map** instead of a plain list, if the product has real progression.
6. **Rhythmic layout:** one big hero card, a pair of medium tiles, then small chips. Never a uniform grid.
7. **Jitter/boil:** a subtle 2–3 frame wobble on illustrated elements (8–12 fps) for hand-made life.
8. **Personality dial:** let the user pick how cheeky the copy is (CARROT).

## Platform notes
- Rive has iOS, Android and (via community or wrappers) KMP runtimes. Lottie works everywhere. In CMP, wrap the native views or use a Compose Lottie port.
- Keep native navigation (tab bar or navigation bar with labels, system back). The fun lives *in* the screens.
- Haptics: iOS `.sensoryFeedback`; Android `HapticFeedbackConstants.CONFIRM` / `REJECT`.

## How cheap imitations go wrong
- **Too polite:** white rows with hairline borders, stock icons, one bouncy moment. That's a normal app with a mascot sticker. The toy feel needs bases under everything, custom glyphs and constant small motion.
- Emoji or stock 3D blobs as the "mascot", with no personality, expressions or states.
- Bounce on dialogs, sheets and navigation transitions (presses and celebrations are where bounce belongs).
- Confetti on trivial taps. It dilutes the reward.
- Pastel-only, same-radius everything: that reads as a kids' template. Duolingo is *vibrant* with strong contrast.
- Lottie files from different artists.
- Sounds without an off switch, or one sample replayed 50 times.
- Guilt-trip copy pretending to be cute ("Duo is sad 😢 you failed").
