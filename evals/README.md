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

Five rounds, October 2026. Each build was a separate `claude -p` session, run once with the skill and once without, given the same prompt plus one line asking for a 390×844 HTML mock, and the same tools. A separate judge saw only the two rendered mocks, shuffled as A and B, the brief and `references/critique.md`. Screens are HTML mocks rendered in headless Chromium, not SwiftUI or Compose renders.

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

Across the five rounds the skill won 18 of 22 blind pairs. Round 4's Opus judge applied the caps more strictly than round 3's Sonnet judge. The margin shrinks as the baseline model gets stronger: about 1.5 points on Sonnet 5, about 0.5 on Opus 5.5 for the same two briefs.

### What the rounds changed in the skill

- Round 1: neither run showed its inventory or critique, so both must now appear in the reply.
- Round 2: the inventory is the brief's first line and gates `deal.py`; a bottom-edge pass joined the critique.
- Round 3: the final message repeats the full report (some hosts show only the last message); the bottom-edge rule covers both structure (`safeAreaInset` / `Scaffold` bottom bar, `pinned-bottom-overlap` lint) and the resting frame; requests to outside services must never carry the user's identity (one run put the user's email in a User-Agent).

- Round 4: the resting frame still showed rows cut behind the pinned bar even when the list was inset correctly, and the neo-brutalist and editorial directions overused small uppercase labels. The skill now renders every scrolling screen twice (at rest and scrolled to the end, `mock.html#end` for the HTML mock) and runs a row-by-row fold check; a caps budget (at most two small uppercase labels per screen) runs through the core rules, presets, library and deal sheet, with a `caps-labels` lint warning. Round 5 confirmed all three in practice (see above).

- Round 5: a dealt direction could miss the product (poster blocks for a ferry timetable), and a big hero could push the brief's content below the fold. Each direction now declares the content shapes it can hold, `deal.py --content` only deals directions that can show the screen's primary shape, and every option goes through a fit test (content at rest, owned idea, costume test) before it can be chosen. A "brief at rest" rule keeps every must-have visible in the resting frame (three rows for a list, hero under about 45% of the height), with a matching critique cap. Not yet re-run.

### Limits

One run per config and one judge per pair, so a single score carries about half a point of noise. Judges are models, not people. The screens are HTML stand-ins for native renders. The briefs were written alongside the skill, so they may favour it.
