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
