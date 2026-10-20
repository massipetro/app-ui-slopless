# Evals

Two kinds of eval live here:

- **Trigger evals** (`trigger-eval.json`, notes in `TRIGGER-NOTES.md`): does the description make the skill load on the right requests and stay quiet on near-misses.
- **Build evals** (`evals.json`, graded by `grade.py`): does the skill make better screens than no skill.

## Build evals

| id | name | tests |
|---|---|---|
| 1 | `playful-habit-home-cmp` | a named preset (playful), CMP craft: lips, haptics, springs, semantics |
| 2 | `neobrutalist-profile-swiftui` | redesign of `files/ProfileView.swift` in a named preset, native mechanics kept |
| 3 | `checkout-audit-warm-premium` | audit of `files/CheckoutScreen.kt` with cited principles, then a redesign |
| 4 | `ferry-home-no-preset-swiftui` | **no preset named**: inventory, dealt direction, owned idea, live countdown, lint, critique |
| 5 | `flat-budget-no-preset-cmp` | **no preset named**: the same workflow in CMP, with a sector that must not be misread as banking |
| 6 | `guesthouse-photos-no-preset-swiftui` | **no preset, no photos**: a photo-led brief (room detail and booking) where the honest answer is designed image slots and credited pictures of the place, never grey boxes or found photos passed off as the room |

Evals 4, 5 and 6 are the ones that test the workflow itself. Evals 1–3 name a preset, so they test craft inside a style.

### How to run

**Each eval is a full build session**, so a run is expensive: 6 evals × 2 configs = 12 sessions per iteration. Agree the count, model and parallelism with the owner before starting.

1. For each eval, run the prompt in a fresh session **with the skill** and in another **without it** (the baseline). Save each session's final reply as `response.md` and its files under:
   `<iteration>/eval-<id>-<name>/<with_skill|without_skill>/run-<n>/outputs/`
2. Grade both configs: `python3 evals/grade.py <iteration>`. It writes `grading.json` per run and prints pass counts. The no-preset evals reuse `scripts/lint.py`, so "no FAIL" means the same thing it means in the skill.
3. **Judge the screenshots blind.** Render each run's screen at phone size (simulator, `@Preview` screenshot test, or the HTML mock the skill falls back to). Shuffle the with/without pair into A and B, and have a judge who doesn't know which is which score both with `references/critique.md` (five criteria, caps, overall). A fresh agent with only the two images and `critique.md` works as the judge.
4. Record per eval: grader pass rate, lint FAIL count, and blind critique overall for both configs. The skill earns its place when it wins the blind critique, not just the regex checks.

`grade.py` checks presence of craft and absence of tells. It can't see taste; step 3 is where taste is measured.

## Results

Nine rounds, October 2026. Each build was a separate `claude -p` session, run once with the skill and once without, given the same prompt plus one line asking for a 390×844 HTML mock, and the same tools. A separate judge saw only the two rendered mocks, shuffled as A and B, the brief and `references/critique.md`. Screens are HTML mocks rendered in headless Chromium, not SwiftUI or Compose renders.

### Round 10: macOS, eval 7 (v1.5.0, Sonnet 5.5 at medium effort)

First macOS round: the Mac library redesign (`files/LibraryView.swift`), two runs per config, Sonnet 5.5 builds ($3 cap) and two blind Sonnet 5.5 judges ($1 cap), the pairs shuffled as A and B. The brief also asked for a 1280×800 HTML mock, rendered headless.

| Pair | With skill | Without | Judge picked the skill | Grader, with vs without |
|---|---|---|---|---|
| 1 | 6 (Craft capped at 4) | 5 (Craft and Substance capped) | yes | 19 / 19 vs 9 / 19 |
| 2 | 7.4 | 5 (Idea capped at 5 for the stock layout; Craft capped at 4 for an unreadable selected cell) | yes | 19 / 19 vs 8 / 19 |

- **2 of 2 pairs, margin +1.7.** The skill runs built a sidebar, toolbar and inspector Mac window, carried the owned idea (the shipping line's funnel livery) through it, and wrote the full report. The baselines were more native-looking in one pair (sortable column headers) but sparse (five rows) or generic.
- Both skill runs typechecked on the macOS SDK (macOS 14 default), linted with no FAIL, and wrote "fold.py not measured: a Mac window has no pinned bottom bar" instead of running the phone-sized check.
- The sample is small (n = 2, one brief, Sonnet, not the Opus used in rounds 1–9), so treat it as a smoke test of the macOS path, not as the strength of the result.
- Two caveats on the measurement. The grader's menu-commands regex and the `fold.py` check were loosened after the first grading, because both skill runs put `Commands` in a separate struct (the task only asked for one file) and `fold.py` measures a 390×844 phone mock. That moved the skill runs from 18 / 20 to 19 / 19 and did not touch the baselines. Judge 1 also saw a blank band at the bottom of both mocks from the headless screenshot size (800 px minus browser chrome), which both configs share.
- Cost: $2.82 for four builds (skill about $1.05 each, baselines about $0.37) plus $0.21 for two judges.

### Round 9: every gate in place, evals 1 and 4 (main at `d0aed63`)

This round measured the four changes since round 8: the required mascot kit, `fold.py`, the signature check and the iOS 17 default. It used two briefs, the playful habit home (CMP) and the ferry home (SwiftUI, no preset). Each ran twice per config with Opus 5.5 builds ($5 cap), judged by four blind Opus 5.5 judges ($2 cap) who saw the stills and the filmstrips.

| Eval | With skill (runs) | Mean | Without (runs) | Mean | Judge picked the skill | Grader, with vs without |
|---|---|---|---|---|---|---|
| 1 Habit home, CMP | 6.0 · 6.0 | 6.0 | 6.0 · 5.8 | 5.9 | 2 of 2 | 16 / 17 each vs 9 and 12 / 14 |
| 4 Ferry home, SwiftUI | 7.0 · 7.0 | 7.0 | 6.0 · 6.0 | 6.0 | 2 of 2 | 17 / 17 each vs 6 / 17 and 4 / 16 |

- **4 of 4 pairs, margin +0.55.** Uncapped, the habit screens averaged 7.0 and 7.2. Both were capped at Craft 4 for a row cut at the tab bar (see below). Motion: 7.25 with the skill against 6.0 without.
- **All four fixes showed up in every skill run that needed them.**
  - Mascot kit: both habit runs drew an SVG rig, used `mascot.py svg2code --into HabitHomeScreen.kt` and ran `mascot.py check`. In round 8 neither run used the kit.
  - iOS 17: both ferry runs typechecked at iOS 17.0 ("skill default; no project") and never passed `--ios`.
  - Signature check: every report points at each move in the resting frame and runs the stock-layout test.
  - `fold.py`: each run called it 3–5 times.
- **But `fold.py` passed both cut rows.** One was a 2 px sliver of the next card's rounded top edge, inside its 2 px tolerance. The other was a 38-of-72 px "peek", title intact and subtitle hidden, which its rules allowed. The judges capped both. `fold.py` is now strict, matching the judges: under a pinned bar, a row is fully visible or fully hidden. It also measures the settled frame (reduced motion, fonts loaded, one-off animations finished), the same frame the screenshots show. Rerun on this round, it flags exactly the two capped screens and passes the six others.
- **Still open: the stock layout.** In ferry run 2 the judge capped the skill's screen at Idea 5 for the stock transit layout. The run's own stock-layout test had passed it, so the self-check is lenient. The baseline it beat had the stronger idea (Idea 9) but around 18 small uppercase labels.
- Kotlin compiled in both skill runs and one of two baselines. Swift typechecked in both skill runs and one of two baselines.
- Cost: $19.98 for eight builds (skill $3.34 average, baselines $1.66) plus $1.64 for four judges.

### Round 8: motion and the mascot kit, eval 1 (branch `mascot-kit` at `5b1fe8b`)

The playful habit brief ("Duolingo-level fun"), two runs per config, Opus 5.5 builds ($5 cap) and two blind Opus 5.5 judges ($2 cap). The harness asked both configs to put any animation in the mock as CSS and to start tap-triggered motion on `#play`. It then filmed every mock with `filmstrip.py` (0–2400 ms), and the judges saw the filmstrips as well as the stills and scored motion with critique pass 14.

| Run | With skill | Without | Judge picked | Motion, with vs without | Grader, with vs without |
|---|---|---|---|---|---|
| 1 | 6.0 (Craft capped at 4: a card border cut by the nav bar) | 6.0 | skill | 7 vs 6 | 14 / 14 vs 12 / 14 |
| 2 | 7.0 | 6.0 | skill | 7 vs 8 | 14 / 14 vs 11 / 14 |

- Margin +0.5, and the skill won both pairs. Uncapped, run 1's skill screen averaged 6.8 against 6.2. Judge 1 picked it for the deeper content (partial-progress habits, a streak freeze, a countdown to midnight). Judge 2 picked the skill's "worried star" mascot tied to the time left before midnight, and called the baseline "Duolingo's home screen re-skinned".
- Motion tied (7.0 each on average). Both baselines animated as much as the skill runs (21–26 animations each), and one had the more celebratory check-off. The skill's motion was more honest: a baseline updated its counters before the check landed, which judge 1 caught in the filmstrip. That shows the strip does its job: a still would never have revealed it.
- **Neither skill run used the mascot kit.** Both read `references/mascot.md`, then drew the mascot freehand in Compose and CSS. The brief asks for the code in one file, and `svg2code` wrote a separate file. The baselines used emoji for habit icons, which judge 1 counted as a tell.
- The resting-frame fold check missed a card border cut by the nav bar again (run 1), the same defect as rounds 4–5.
- Both skill runs filmed their own motion (4–11 `filmstrip.py` calls each) and wrote the numbers on the report's Live thing line. Kotlin compiled in all four runs.
- The harness filmstrips came out in dark mode, because the machine was set to dark, and at full screen with small frames. Both were fixed after the round (below).
- Cost: $9.37 for four builds (skill $2.98 average, baselines $1.70) plus $0.78 for two judges.

### Round 7: three runs per config, with both compile gates (main at `a5207a0`)

Same setup as round 6, now with `compile_kotlin.py` in the skill as well as the Swift typecheck.

| Eval | With skill (runs) | Mean | Without (runs) | Mean | Margin | Judge picked the skill |
|---|---|---|---|---|---|---|
| 4 Ferry home, SwiftUI | 7.4 · 7.0 · 7.6 | 7.33 | 6.0 · 6.0 · 6.0 | 6.00 | +1.33 | 2 of 3 |
| 5 Flat budget, CMP | 7.2 · 7.6 · 6.6 | 7.13 | 7.0 · 7.2 · 6.0 | 6.73 | +0.40 | 3 of 3 |

- Average margin +0.87; the skill's highest means so far. By score the skill won all six pairs; in ferry run 2 the judge picked the baseline anyway, saying the skill's screen was the stock transit layout (Idea 4) while the baseline was only capped for caps labels.
- Kotlin: all three skill budget files compile, and every skill run called the gates (7–13 times). The baselines also compiled this round.
- Swift: two of three skill ferry files typecheck at iOS 17. The third used the iOS 18 `Tab` API and checked itself with `--ios 18.0`, raising the deployment target on its own. Two of three baseline ferry files have real compile errors.
- Grader: 14 / 14 on five skill runs and 13 / 14 on one; baselines 3–5. 0 lint FAILs on every skill run.
- Cost: $22.79 for 12 builds (skill $2.34 average, baselines $1.46) plus $1.95 for six judge calls.

### Round 6: three runs per config, with the fit test and compile gate (main at `5f8b172`)

Same setup as round 5, now with the content-shape deal, the fit test, the brief-at-rest rule and the Swift compile gate. Builds and judge on `claude-opus-5-5`; the judging is balanced, with the skill's screen shown as A in three pairs and B in three.

| Eval | With skill (runs) | Mean | Without (runs) | Mean | Margin | Skill picked |
|---|---|---|---|---|---|---|
| 4 Ferry home, SwiftUI | 7.4 · 7.2 · 6.0 | 6.87 | 6.0 · 5.8 · 6.0 | 5.93 | +0.93 | 2 of 3 |
| 5 Flat budget, CMP | 7.0 · 7.0 · 7.0 | 7.00 | 5.8 · 6.0 · 6.0 | 5.93 | +1.07 | 3 of 3 |

- Average margin +1.0 (round 5: +0.4); the skill won 3 of 3 pairs as A and 2 of 3 as B.
- Every skill run passed `--content`, and no misfit direction was dealt (newspaper frame and departure board for the ferry; toy box, dot matrix and persona for the budget).
- All three skill ferry files typecheck (round 5: 1 of 3). Grader 14 / 14 (ferry) and 13 / 13 (budget) on every skill run; baselines 3–5. 0 lint FAILs.
- The one loss was a 6.0 tie: the departure board passed the fit test but was built as stock cards and pills, while that baseline found its own maritime ticket idea.
- Two budget builds were cut off by a usage limit and rebuilt before judging. Cost: $22.90 for the 12 valid builds, $2.37 for the cut-off ones, $1.94 for six judge calls.

### Round 5: three runs per config on evals 4 and 5 (main at `3d23111`)

Builds and judge on `claude-opus-5-5`; each run-n pair judged separately. This round tested the two-frame bottom edge, the caps budget and the fixed report block, and averages out some single-run noise.

| Eval | With skill (runs) | Mean | Without (runs) | Mean | Margin | Skill picked |
|---|---|---|---|---|---|---|
| 4 Ferry home, SwiftUI | 7.6 · 7.0 · 5.0 | 6.53 | 6.0 · 6.0 · 6.0 | 6.00 | +0.53 | 2 of 3 |
| 5 Flat budget, CMP | 7.0 · 6.0 · 7.0 | 6.67 | 6.0 · 6.0 · 7.2 | 6.40 | +0.27 | 2 of 3 |

- Process: every skill run passed 13 / 13 grader checks (baselines 2–4), ended with the full 15-label report block, rendered a scrolled-to-the-end frame, and had 0 lint FAILs (baselines 54) with no `caps-labels` or `pinned-bottom-overlap` warnings. No skill screen was capped for a cut row.
- The two losses: ferry run 3 was dealt `nb-poster-blocks`, which the judge called "a trend, not a ferry idea" (5.0); flat-budget run 3 lost 7.0 to 7.2 because its hero pushed all but one receipt below the fold, although its idea scored higher.
- In all three ferry pairs the skill's screen was in position B, so position bias isn't ruled out there.
- Cost: $22.50 for 12 builds (skill runs $2.25 on average, baselines $1.49) plus $1.91 for 6 judge calls.

### Round 4: all six evals, Opus 5.5 builds and Opus 5.5 judge (main at `609d7b1`)

Builds and judge on `claude-opus-5-5` (judge capped at $2 a call, below every build cap). Raw `curl` was replaced, for both configs, by a download helper with a generic User-Agent that refuses URLs containing an @.

| Eval | Blind, with | Blind, without | Judge picked | Grader, with | Grader, without |
|---|---|---|---|---|---|
| 1 Habit home, CMP (playful) | 7.6 | 5.8 | skill | 13 / 13 | 10 / 13 |
| 2 Profile redesign, SwiftUI (neo-brutalist) | 6.0 | 5.4 | skill | 11 / 12 | 11 / 12 |
| 3 Checkout audit + redesign (warm premium) | 6.8 | 5.6 | skill | 10 / 11 | 11 / 11 |
| 4 Ferry home, SwiftUI (no preset) | 6.0 | 6.0 | baseline | 11 / 12 | 3 / 12 |
| 5 Flat budget, CMP (no preset) | 6.0 | 6.6 | baseline | 12 / 12 | 3 / 12 |
| 6 Guesthouse room, SwiftUI (no preset, no photos) | 7.0 | 6.2 | skill | 12 / 12 | 1 / 12 |

- The skill won 4 of 6, average margin +0.6. Idea scored 7–8 with the skill; the baseline scored 4 on three briefs, where it copied the reference (Duolingo, Airbnb) or a stock template.
- Eval 5 was lost to the bottom-edge cap: the judge called the skill's receipt design "unmistakably its own" but a row sat cut mid-line behind the pinned bar. Eval 4 was a 6.0 tie (both capped for overusing small tracked uppercase labels) that the judge gave to the baseline.
- `lint.py`: 0 FAIL with the skill, 51 without; no `pinned-bottom-overlap` warnings on the skill's screens.
- Four of six final messages carried the full report; the checkout run left out the inventory and idea, and the ferry run wrote prose instead of the template.
- No outgoing request in the 12 runs carried the user's email or name.
- Cost: $22.08 for the 12 builds ($14.44 with the skill, $7.64 without, 1.9×) plus $1.89 for the six judge calls.

### Round 3: all six evals, Opus 5.5 (main at `bee4629`)

Builds on `claude-opus-5-5`, judge on `claude-sonnet-5-5`.

| Eval | Blind, with | Blind, without | Grader, with | Grader, without |
|---|---|---|---|---|
| 1 Habit home, CMP (playful) | 6.0 | 6.0 | 12 / 13 | 10 / 13 |
| 2 Profile redesign, SwiftUI (neo-brutalist) | 7.4 | 6.0 | 11 / 12 | 10 / 12 |
| 3 Checkout audit + redesign (warm premium) | 7.6 | 5.0 | 10 / 11 | 10 / 11 |
| 4 Ferry home, SwiftUI (no preset) | 7.6 | 6.0 | 10 / 12 | 3 / 12 |
| 5 Flat budget, CMP (no preset) | 6.0 | 5.0 | 8 / 12 | 5 / 12 |
| 6 Guesthouse room, SwiftUI (no preset, no photos) | 7.0 | 5.0 | 8 / 12 | 1 / 12 |

- The judge picked the skill's screen in all six pairs; eval 1 was a tie on score (6.0 each, both capped for a row cut at the bottom edge) and the judge preferred the skill's screen for its idea.
- Average blind margin +1.4. Idea was the steadiest gap: 8–9 with the skill, 3–7 without.
- `lint.py` across the six outputs: 1 FAIL with the skill, 65 without.
- Cost: $20.59 for the 12 builds ($13.88 with the skill, $6.71 without, so 2.1×) plus $0.84 for the six judge calls.

### Rounds 1–2: evals 4 and 5 only

| Round | Builds | Ferry, with vs without | Flat budget, with vs without |
|---|---|---|---|
| 2 | Opus 5.5 (judge Sonnet 5.5) | 8.0 vs 7.4 | 7.0 vs 6.6 |
| 1 | Sonnet 5 (judge Sonnet 5) | 8 vs 6 | 7 vs 6 |

Round 1 used a CLI whose `sonnet` alias still pointed at Sonnet 5; later rounds pass the model id explicitly and stop any session that reports a different model.

Across the seven rounds the skill won 28 of 34 blind pairs. Round 4's Opus judge applied the caps more strictly than round 3's Sonnet judge. The margin shrinks as the baseline model gets stronger: about 1.5 points on Sonnet 5, about 0.5 on Opus 5.5 for the same two briefs.

### What the rounds changed in the skill

- Round 1: neither run showed its inventory or critique, so both must now appear in the reply.
- Round 2: the inventory is the brief's first line and gates `deal.py`; a bottom-edge pass joined the critique.
- Round 3: the final message repeats the full report (some hosts show only the last message); the bottom-edge rule covers both structure (`safeAreaInset` / `Scaffold` bottom bar, `pinned-bottom-overlap` lint) and the resting frame; requests to outside services must never carry the user's identity (one run put the user's email in a User-Agent).

- Round 4: the resting frame still showed rows cut behind the pinned bar even when the list was inset correctly, and the neo-brutalist and editorial directions overused small uppercase labels. The skill now renders every scrolling screen twice (at rest and scrolled to the end, `mock.html#end` for the HTML mock) and runs a row-by-row fold check; a caps budget (at most two small uppercase labels per screen) runs through the core rules, presets, library and deal sheet, with a `caps-labels` lint warning. Round 5 confirmed all three in practice (see above).

- Round 5: a dealt direction could miss the product (poster blocks for a ferry timetable), and a big hero could push the brief's content below the fold. Each direction now declares the content shapes it can hold, `deal.py --content` only deals directions that can show the screen's primary shape, and every option goes through a fit test (content at rest, owned idea, costume test) before it can be chosen. A "brief at rest" rule keeps every must-have visible in the resting frame (three rows for a list, hero under about 45% of the height), with a matching critique cap. Round 6 measured these together with the compile gate: +1.0.

- Compilation (checked afterwards, no model calls): typechecking every Swift output from rounds 3–5 against the iOS simulator SDK, 4 of the skill's 10 files failed and 0 of 9 baselines. All four were ferry screens; three created a `@MainActor` model in a default argument, which the skill's own code baseline had encouraged, and one hit a compiler failure on a `keyframeAnimator` with a conditional inside its builder. Step 5 now typechecks before handing over (`scripts/typecheck.py`), the SwiftUI baseline has rules for both causes, `lint.py` warns on the default-argument pattern, and `grade.py` adds "Swift typechecks" to the Swift evals. Kotlin is now compiled too (`scripts/compile_kotlin.py`: a throwaway Kotlin 2.2.21 + Compose Multiplatform 1.9.0 / Material 3 1.4 project, JVM and Android targets). Compiling every Kotlin output from rounds 3–6, 6 of the skill's 13 files failed and 5 of the baselines' 12. The skill's failures were a missing `animateFloat` import on an infinite transition (3), `rememberSaveable` imported from the wrong package (1), and a `BackHandler` API that isn't in Compose Multiplatform 1.9.0 (2). `lint.py` now fails the first two kinds before any compile, the Compose baseline has a rule for them, and `grade.py` adds "Kotlin compiles" to evals 1, 3 and 5. Building the harness also showed the skill's own rule 9 (state-based `TextField`) needs Material 3 1.4, which the `compose.material3` accessor in CMP 1.9.0 doesn't give you; the rule now says so.

- Round 6 (open): a direction that fits on paper can still be built generically (stock cards and pills); the fit test checks the plan, not the execution. Kotlin compiles in evals now (see the compilation note).

- Round 7: a direction could still be executed as the stock layout (ferry run 2), and a run raised the iOS deployment target to make an iOS 18 API compile (ferry run 3, `Tab` checked with `--ios 18.0`). Step 5 now has a signature check on the resting frame: point at each signature move (at least two must show) and run a stock-layout test against the category default, with a matching critique cap (Idea ≤ 5) and a report field. `typecheck.py` reads the deployment target from the project (iOS 17 when none is set) and prints a note when `--ios` overrides it; the skill and SwiftUI rule 17 put newer APIs behind `#available` and never raise the target to pass. `grade.py` pins its typecheck to iOS 17 and checks the signature line. After round 7 the render step also records motion: `scripts/filmstrip.py` pauses an HTML mock's animations at set times and tiles the frames into one image with measured durations (or tiles frames from a Compose test clock or a simulator recording), critique pass 14 reads it, and a cap applies when the dial promises motion that the strip doesn't show. Round 8 measured the motion part (above).

- Round 8: the skill runs read the mascot kit and then drew freehand anyway, partly because the brief asks for a single file. The kit is now the required path whenever the screen has a character. `mascot.py svg2code --into <screen file>` adds the generated code to a single-file brief's file, with imports merged, in a marked block that a rerun replaces. The HTML mock embeds the same SVG. The report's Pictures line names the rig and the command. `grade.py` checks for a rig `.svg` with pivots and generated code whenever the reply mentions a mascot. `filmstrip.py` now crops to the area that moves (`--crop auto`, the default: the union of the animated elements' boxes over their run, preferring the triggered motion over loops) and renders in light mode whatever the machine uses (`--scheme`). New headless Chrome's window frame no longer cuts the last row of frames. Not yet measured: no eval calls since.

- After round 8: the fold check is measured, not eyeballed. A thin sliver of card above the tab bar cost the skill a Craft cap in rounds 4, 5 and 8, and every time the run's own look at the screenshot missed it (round 8 even had a fade over it). `scripts/fold.py` loads the mock at 390×844, finds the pinned bar (a buy bar stacked on a tab bar counts as one) and the scroller, and classes every row at the bar's edge as whole, peek (at least 40% and 24 px show, no line of text crosses) or cut. A sliver is cut whether or not a fade covers it. It also checks that the last row clears the bar by 8 px and that the mock scrolls at all. Step 5 treats it as a gate, critique pass 13 uses its result, the report's Bottom edge line carries it, and `grade.py` adds it to every eval with a mock and a pinned bar. Rerun on every earlier mock with a pinned bar, it flags 9 of 11 skill mocks from rounds 3–4, 2 of 18 from round 5 on (round 7 budget run 3, and round 8 run 1, the one the judge capped), and 11 of 17 baselines. I checked the flags against the screenshots: each is a sliver, a line of text through the bar, or a mock that can't scroll. `evals/test_fold.py` pins the rules on six generated mocks. Not yet measured in an eval round.

- Round 9: the strict fold rule above. `fold.py` no longer accepts a peek or a sliver of 2 px or less, and it measures the settled frame. The skill text, critique pass 13 and the report's Bottom edge line follow it. Rerun with the strict rule on every earlier mock with a pinned bar, it flags 9 of 11 skill mocks from rounds 3–4, 2 of 16 from round 5 on, and 11 of 17 baselines. Not yet measured in an eval round.

### Limits

One run per config and one judge per pair, so a single score carries about half a point of noise. Judges are models, not people. The screens are HTML stand-ins for native renders. The briefs were written alongside the skill, so they may favour it.

## Fold check tests

`python3 evals/test_fold.py` runs `scripts/fold.py` on seven generated mocks with known bottom edges. No model calls. A fold in a gap passes. A 7 px sliver of card behind a fade fails, and so do 1 px of a card's top edge, a 35 px peek with its title intact, and a line of text through the bar's edge. A list with no bottom padding fails the end frame, and a mock that can't scroll fails too. Skipped without a Chromium browser.

## Mascot kit tests

`python3 evals/test_deal.py` checks `scripts/deal.py`'s platform handling. No model calls. The library passes `--check`, which now also rejects a Mac block missing a field or carrying phone mechanics (thumb zone, tab bar, bottom sheet, tap, swipe, 9:16, dp, iOS haptics), including the motion and pitfall it inherits. Over 40 seeds and four content shapes, `--platform macos` never deals a direction whose Mac block says skip; every Mac sheet carries the Mac composition, the window chrome line and the Mac dials and no phone words; and every phone sheet is unchanged.

`python3 evals/test_mascot.py` checks `scripts/mascot.py` on a hand-written mascot (`fixtures/pip.svg`, a rig in the pl-toy-box palette, written the way Illustrator exports) and its motion spec (`fixtures/pip.motion.json`: an idle loop with breathing and a blink, and a celebration with a hop, a mouth morph and sparks drawing on). No model calls. It checks that the path parser handles relative commands, S/T curves and compact arc flags; that the SwiftUI output typechecks (`typecheck.py`) and renders on macOS with the eyes open at rest and covered on the blink; that the Compose output compiles (`compile_kotlin.py`); that the Lottie has `v fr ip op w h layers`, is parented and anchored at the pivots, and doesn't leave its canvas; that a morph between shapes with different vertex counts and an unknown part are refused; and that the preview runs through `filmstrip.py`, which measures the reaction at 900 ms and the idle state as looping, and that its frames visibly change and land back on rest, in both clock and `--frames` mode. Steps whose toolchain is missing are skipped, not failed: Xcode, JDK 17 + Gradle, a Chromium browser, and network for lottie-web.
