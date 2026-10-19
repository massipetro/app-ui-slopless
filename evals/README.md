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

Seven rounds, October 2026. Each build was a separate `claude -p` session, run once with the skill and once without, given the same prompt plus one line asking for a 390×844 HTML mock, and the same tools. A separate judge saw only the two rendered mocks, shuffled as A and B, the brief and `references/critique.md`. Screens are HTML mocks rendered in headless Chromium, not SwiftUI or Compose renders.

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

- Round 7 (open): a direction can still be executed as the stock layout (nothing checks the built screen against the direction's signature moves), and a run can raise the iOS deployment target to make newer APIs compile instead of keeping the documented iOS 17.

### Limits

One run per config and one judge per pair, so a single score carries about half a point of noise. Judges are models, not people. The screens are HTML stand-ins for native renders. The briefs were written alongside the skill, so they may favour it.
