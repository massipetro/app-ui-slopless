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
| 7 | `library-sidebar-macos-swiftui` | **macOS redesign** of `files/LibraryView.swift` (an iPhone layout in a window): sidebar, menu commands, minimum window size, Mac density, an owned idea |
| 8 | `subtitle-window-macos-swiftui` | **macOS new build**, a pro tool: table, video and editor in one window, keyboard-first, reading speed |
| 9 | `retro-terminal-trail-swiftui` | a named **retro** style (phosphor terminal) on a phone: legibility, no Fallout marks, CRT effects off under Reduce Motion |
| 10 | `retro-pixel-plants-compose` | a named **retro** style (16-bit pixel art) on a phone: pixel grid, nearest-neighbour art, meters that show their value |
| 11 | `retro-film-log-macos-swiftui` | **retro on a Mac**, the look left to the designer: real window chrome kept, no Apple or Microsoft marks |
| 12 | `bake-day-macos-swiftui` | **a fresh macOS brief**, neither a collection nor a pro tool: a home baker's bake-day window kept open on the counter all day |
| 13 | `medication-today-a11y-swiftui` | **accessibility**: a medication Today screen for older users on VoiceOver, Voice Control and the largest text sizes, for a buyer who needs an ACR (VPAT, WCAG 2.2 AA) |

Evals 4, 5 and 6 are the ones that test the workflow itself. Evals 1–3 name a preset, so they test craft inside a style. Evals 7, 8 and 12 test the Mac deal (`--platform macos`); 9–11 the retro preset, which is dealt only when named. Eval 13 tests accessibility: its grader checks names, roles, states, large-text layout, announcements and the report's Accessibility line. Its pairs are judged on native iOS renders at the default size and at AX5, with a judge prompt that scores Access as well as the five criteria.

### How to run

**Each eval is a full build session**, so a run is expensive: n runs × evals × configs sessions per round (round 18: 3 × 1 × 3 = 9). Agree the count, model and parallelism with the owner before starting.

1. For each eval, run the prompt in a fresh session **with the skill** and in another **without it** (the baseline). Save each session's final reply as `response.md` and its files under:
   `<iteration>/eval-<id>-<name>/<with_skill|without_skill>/run-<n>/outputs/`
2. Grade both configs: `python3 evals/grade.py <iteration>`. It writes `grading.json` per run and prints pass counts. The no-preset evals reuse `scripts/lint.py`, so "no FAIL" means the same thing it means in the skill.
3. **Judge the screenshots blind.** Render each run's screen at phone size (simulator, `@Preview` screenshot test, or the HTML mock the skill falls back to). Shuffle the with/without pair into A and B, and have a judge who doesn't know which is which score both with `references/critique.md` (six criteria from round 22 on, five before; caps; overall). A fresh agent with only the two images and `critique.md` works as the judge. For iOS briefs, `python3 evals/render_builds.py <iteration>` renders every run's own Swift on the iOS Simulator at the default size and at AX5, with each build's clock (its `--clock`, else the time in its `#Preview`'s name), and records the native bottom-edge result in each run's `render.txt`. The judge prompts live in `evals/judges.py` (`phone`, `mac`, and `access`, which shows each screen at the default and the largest text size and scores Access as a sixth criterion); a round's `make_pairs.py` imports it, so every round asks the same question.
4. Record per eval: grader pass rate, lint FAIL count, and blind critique overall for both configs. The skill earns its place when it wins the blind critique, not just the regex checks.

`grade.py` checks presence of craft and absence of tells. It can't see taste; step 3 is where taste is measured.

## Results

Twenty-four rounds, October 2026, newest first: rounds 1–9 and 20 on the phone, 10–13 and 18–21 on the Mac, 14–17 on the retro preset, 22–24 on accessibility. Each build was a separate `claude -p` session with the skill, without it, and from round 11 with the previous release (v1.5.0) as well, given the same prompt plus one line asking for an HTML mock (390×844 on the phone, 1280×800 on the Mac) and the same tools. Blind judges saw only the two rendered mocks, shuffled as A and B, the brief and `references/critique.md`: one judge per pair up to round 11, two from round 12, three from round 15, so every pair has a majority winner. Screens are HTML mocks rendered in headless Chromium, not SwiftUI or Compose renders. The harnesses live outside the repo, in `app-ui-slopless-workspace/iteration-<n>`.

### Round 24: native bottom edge and the build's clock, eval 13, three judges (HEAD vs round 23's HEAD)

HEAD is `247aa27` (worktree `skill-head24`). Since round 23:
- every iOS render checks its own bottom edge, by reading the accessibility elements that cross the tab bar or a pinned bar;
- the render takes the clock from the `#Preview`'s name when `--clock` isn't passed;
- the eval 13 grader adds the native bottom edge.

The comparison is round 23's HEAD `a2668bb` (`skill-head23`). The setup is round 23's, except that the harness rendered with `evals/render_builds.py`, so each build appears with its own clock. Five of the six builds named their preview with a time and got it; round 23's HEAD run 1 didn't and shows the wall clock. No build passed `--clock`.

| Run | HEAD direction | Round 23 HEAD direction | HEAD vs round 23 HEAD | Access | Votes |
|---|---|---|---|---|---|
| 1 | wp-departure-board | wp-departure-board | **7.27** vs 5.57 | **8.0** vs 4.3 | 3–0 |
| 2 | wp-departure-board | ed-newspaper-frame | **7.23** vs 6.00 | 7.7 vs **8.0** | 3–0 |
| 3 | ed-newspaper-frame | wp-departure-board | 7.04 vs **7.18** | **8.0** vs 7.0 | 1–2 |

- **2 of 3 pairs, 7 of 9 votes, mean 7.18 vs 6.25; Access 7.89 vs 6.44.** This is HEAD's highest mean on eval 13 so far. It is still n = 3 on one brief.
- **Nothing cut at the bottom edge on the HEAD side.**
  - The native check found nothing pinned over the list in any HEAD build, so no row could be cut.
  - It flagged rows cut by the floating tab bar in two of round 23's HEAD builds, at both sizes: a 3 pt sliver in run 1 and 17 pt in run 2.
  - Every judge in pairs 1 and 2 named those cut rows. They were the craft cap that decided both pairs.
  - The grader's new native check failed exactly those two builds.
  - HEAD run 3's mock failed `fold.py` (text crossing the mock's bar) while its native render had no pinned bar; the judges saw the native render.
- **The clock shows up in a judgement for the first time.** In pair 1, all three judges said HEAD's times agree with the status bar, while the other screen's lateness contradicted its 15:37 wall clock.
- **Pair 3 went to round 23's HEAD on hierarchy.** All three judges gave HEAD the better AX5 behaviour (Access 8 vs 7): both buttons in the first screen, the action reordered first. Two of them preferred the other screen's single strong focus over HEAD's headings, which carried as much weight as the overdue dose, and its small "Show" link.
- **Lint:** no FAIL on either side.
- Grader: HEAD 29–30 of 30–31, round 23's HEAD 29–30 of 30–31.
- Cost: $29.91 for 6 builds (HEAD $14.57, round 23's HEAD $15.34). Builds took 19.0 minutes against 21.0. Judges: $2.39 for 9.
- **Not measured:** Android, the Mac, and any assistive technology. The Access score is a judgement on pixels.

### Round 23: round 22's follow-ups, eval 13, three judges (HEAD vs round 22's HEAD)

HEAD is `a2668bb` (worktree `skill-head23`). Since round 22 it has:
- the brief at rest held at AX5;
- `render_swiftui.py --clock`;
- Access as a sixth scored criterion in the critique and the in-build blind judge.

The comparison is round 22's HEAD `eb4197d` (`skill-head`), so this round measures only those changes. The setup is round 22's, except the judges:
- Eval 13, three runs per config, Opus 5.5 builds ($8 cap).
- The harness rendered every build natively on the iOS Simulator at the default size and at AX5; all six rendered.
- Three blind Opus 5.5 judges per pair, with `evals/judges.py`'s `access` prompt. It adds the question of whether the thing to act on now is still in the first screen.
- The judges got the six-criterion `critique.md`.

| Run | HEAD direction | Round 22 HEAD direction | HEAD vs round 22 HEAD | Access, HEAD vs round 22 HEAD | Votes |
|---|---|---|---|---|---|
| 1 | wp-departure-board | wp-departure-board | **5.67** vs 5.37 | **5.3** vs 4.0 | 3–0 |
| 2 | wp-departure-board | wp-departure-board | **6.43** vs 6.33 | **8.0** vs 5.0 | 1–2 |
| 3 | wp-exaggerated-number | wp-departure-board | **6.73** vs 5.73 | **8.0** vs 4.7 | 3–0 |

- **2 of 3 pairs, 7 of 9 votes, mean 6.28 vs 5.81; Access 7.11 vs 4.56.** This is n = 3 on one brief. The overall gap of 0.47 is within the noise seen at that size. The Access gap is not: every one of the nine judges scored HEAD's Access higher.
- **The AX5 rule took.** In all three pairs, the judges named the same difference.
  - HEAD at AX5 kept the overdue dose and its Take and Skip buttons in the first screen.
  - Round 22's HEAD let its header and summary push every action below the fold there, the same failure that lost round 22's run 1.
  - Two HEAD reports say in words that the action stays in the first screen at AX5.
- **Pair 2 went the other way on a cut row.** All three judges preferred HEAD's AX5 frame (Access 8 vs 5), but two of them picked round 22's HEAD overall.
  - At the default size, HEAD's screen showed a row sliver above its pinned bar, which triggered the craft cap.
  - `fold.py` passed the mock, because the cut was the native iOS 26 floating tab bar, which the HTML mock doesn't draw.
  - A fold check on the native render would catch it; the skill has none.
- **`--clock` wasn't used.** No build passed it, and the harness renders at the wall clock for both configs. The judges again saw a status-bar time that disagrees with the sample data. One called it "likely an artefact of how they were rendered" and scored it the same for both. So this round doesn't measure the clock fix.
- **Lint:** the new rules found nothing on either side. `lint.py` found one `fixed-font-size` FAIL in HEAD run 1 and one in each of round 22's runs 1 and 3. HEAD run 1 also has no heading traits.
- Grader: HEAD 28–30 of 29–30, round 22's HEAD 28–29 of 29–30. Both configs ask for the same process now, so the grader no longer separates them.
- Cost: $27.76 for 6 builds (HEAD $13.92, round 22's HEAD $13.84). Builds took 19.3 minutes against 18.2. Judges: $2.44 for 9.
- **Not measured:** Android, the Mac, any assistive technology, and the `--clock` fix. The Access score is a judgement on pixels.
- **After this round** (not yet measured):
  - **Every iOS render checks its own bottom edge.** `render_swiftui.py --platform ios` switches app accessibility on for the render (and back after), reads the screen's accessibility elements, and prints each one that runs across the top of whatever is pinned over the content: the system tab bar or a `.safeAreaInset` bar. Builds fix every `CUT`, as with `fold.py`, and the report's Bottom edge line carries the result.
    - Rerun on this round's six builds at the default size, it flags a cut row in all three HEAD builds and in one of round 22's HEAD. That includes the 6-of-76 pt sliver that lost pair 2; `fold.py` had passed it on the mock.
    - It sees text and controls, not bare card edges.
  - **The render takes the build's clock.** Without `--clock` it uses a time in the `#Preview`'s name ("Today, 10:40"), which five of these six builds had. It also prints a note when it falls back to the wall clock.
  - **The harness's render step is in the repo.** `evals/render_builds.py` renders each run with its own clock and records the clock's source.
  - **The eval 13 grader adds the native bottom edge** at the default size and at AX5.

### Round 22: accessibility, eval 13, native iOS renders at default and AX5, three judges (HEAD vs v1.7.0)

HEAD is `eb4197d` on the `accessibility` branch, pinned in a worktree (`skill-head`). It adds:
- 18 accessibility lint rules, each mapped to a WCAG 2.2 criterion;
- the Accessibility mode;
- critique pass 15 (Access);
- the iOS Simulator render at AX5 (`render_swiftui.py --platform ios --dynamic-type ax5`) and `fold.py --text-scale`;
- the report's Accessibility line, in VPAT terms;
- `acr.py`.

Eval 13 is new and untuned: a medication Today screen for older users on VoiceOver, Voice Control and the largest text sizes, for a buyer who needs an ACR. Three runs per config, Opus 5.5 builds ($8 cap) against v1.7.0 (the `skill-v1.7.0` worktree at the tag).

Judging changed for this brief:
- Both configs were asked for a `#Preview`, so the harness could render each build's own Swift on the iOS Simulator (iPhone 17 Pro, iOS 26.2) at the default size and at AX5. All six rendered natively.
- Each blind Opus 5.5 judge saw four images: A, A at AX5, B, B at AX5.
- The judges scored a sixth criterion, Access (critique pass 15, from the pixels), and the overall is the mean of the six.
- Three judges per pair.

| Run | HEAD direction | v1.7.0 direction | HEAD vs v1.7.0 | Access, HEAD vs v1.7.0 | Votes |
|---|---|---|---|---|---|
| 1 | ed-newspaper-frame | wp-departure-board | 5.57 vs **5.67** | 5.7 vs **6.7** | 1–2 |
| 2 | wp-departure-board | wp-departure-board | **7.27** vs 5.83 | **8.0** vs 6.3 | 3–0 |
| 3 | ed-newspaper-frame | wp-exaggerated-number | **6.67** vs 5.23 | **7.7** vs 4.7 | 3–0 |

- **2 of 3 pairs, 7 of 9 votes, mean 6.50 vs 5.58; Access 7.11 vs 5.89.** This is one brief at n = 3. The run-2 and run-3 margins are large, but run 1 went the other way, so treat it as a first measure, not a settled lead.
- **The judges decided on the AX5 frame.** In the two HEAD wins, the screen at AX5 still led with the late dose and its two big buttons, reflowed with nothing clipped, and showed every state in words or shape. The v1.7.0 screens pushed the overdue dose and its actions below the fold at AX5, or ran text under the floating tab bar.
- **Run 1 lost on the same thing, reversed.** HEAD's ed-newspaper-frame screen at AX5 was "all summary": headers and counts, with the late dose, its actions and the refill below the fold. All three judges gave v1.7.0 the better Access score, while two of them gave HEAD the stronger idea.
  - **Next fix:** apply the brief-at-rest rule to the large-text frame too. The must-have action, here the dose due now, stays in the first screen at AX5.
- **Both configs built accessibly in code.** The brief asks for accessibility in so many words, and Opus without the skill responded.
  - `lint.py --a11y` found nothing in any HEAD build and two `image-no-label` WARNs in one v1.7.0 build.
  - The grader's product checks were 45 of 46 for HEAD against 45 of 48 for v1.7.0. HEAD's miss was a `fold.py` end-frame failure in run 3. v1.7.0's misses: no taken or skipped state exposed in two runs, and no status announcement in one.
  - **The lead shows in the renders and the report, not in the code checks.**
- **The reports state conformance.**
  - Every HEAD build wrote the Accessibility line and ran `acr.py`, which drafted 55 criteria with none left "To evaluate".
  - Every HEAD build said it wasn't tested with assistive technology.
  - None of the v1.7.0 builds made a per-criterion claim.
  - **The drafts lean optimistic.** Run 3 claimed 2.4.11 Focus Not Obscured "Supports, from code", while the judges saw rows under the floating tab bar and `fold.py` failed its end frame. Run 1 marked the same criterion "Partially Supports" for that reason. A "Supports" should need a render behind it, and `acr.py` could take the `fold.py` result as evidence for 2.4.11.
- **Harness artifacts hit both configs.**
  - The simulator's status bar shows the wall clock, so every judge saw a time that contradicted the app's sample `now` (Substance ≤ 5 for "times that disagree with the clock").
  - iOS 26's floating glass tab bar covers the bottom rows in both configs' native renders. The HTML mocks never showed this.
  - A `--clock` option that sets the simulator's status bar (`simctl status_bar override --time`) would remove the first artifact.
- Grader: HEAD 28–29 of 29–30, v1.7.0 24–27 of 30. The process items only HEAD is asked to pass (blind judge, Accessibility line, the not-tested statement, the large-text render) account for most of the gap.
- Cost: $25.54 for 6 builds (HEAD $15.10, v1.7.0 $10.44, +45%). HEAD builds took 20.2 minutes against 14.3. Judges: $2.47 for 9. The native renders and the large-text render add the time.
- **Not measured:** Android and the Mac. This round is iPhone only, and no build or judge used VoiceOver, TalkBack or Voice Control. The Access score is a judgement on pixels.
- **After this round** (not yet measured):
  - **The brief at rest now holds at the largest text size.** At AX5 the thing to act on now, and its control, stays in the first screen. Summaries and finished groups move below it at accessibility sizes. The rule is in SKILL.md, critique pass 15 (with a Substance ≤ 5 cap), `accessibility.md` §3.3 and the blind judge's prompt.
  - **`render_swiftui.py --clock HH:MM`** sets the simulator's status bar to the preview's `now` for the screenshot, then clears the override. Builds are told to pass it, so a render no longer contradicts its own sample data.
  - **Access is its own criterion.** `critique.md` now scores six criteria: Platform keeps passes 8 and 11, and Access scores pass 15. The pass 15 caps moved from Platform to Access. `blind_critique.py` scores Access from the pixels, says it couldn't check names and order, and saves the scores in `blind-critique.json`. The report's Critique line carries Access too. Overalls from here on are means of six, so they don't compare directly with earlier rounds' five.
  - **The eval judge prompts are in the repo:** `evals/judges.py`, with round 22's access prompt (made platform-neutral, plus the first-screen clause) next to the phone and Mac prompts used until round 21.

### Round 21: the blind judge sees the real Mac window, eval 12, three judges (HEAD vs v1.7.0)

HEAD is `4662de6`. Mac builds now render the real SwiftUI window from its `#Preview` with `scripts/render_swiftui.py`, and hand that render, not the HTML mock, to the blind judge. Eval 12 (sourdough bake day), three runs per config, Opus 5.5 builds ($8 cap), three blind Opus 5.5 judges per pair. The eval judges still compare the HTML mocks, since v1.7.0 only makes mocks.

| Run | HEAD direction | v1.7.0 direction | Blind judge's first score | HEAD vs v1.7.0 | Votes |
|---|---|---|---|---|---|
| 1 | nc-owned-chrome | nc-owned-chrome | 6 | 6.6 vs **7.0** | 0–3 |
| 2 | nc-owned-chrome | nc-owned-chrome | 5 | **7.3** vs 6.7 | 3–0 |
| 3 | wp-exaggerated-number | nc-owned-chrome | 6 | **7.3** vs 7.2 | 2–1 |

- **2 of 3 pairs, 5 of 9 votes, mean 7.07 vs 6.98.** Round 20 on this brief was 3 of 9 and 6.64 vs 7.13. Over both rounds, HEAD has 8 of 18 votes against v1.7.0 on the Mac. The swing is in the right direction but within the noise measured at n = 3.
- **All three HEAD builds rendered the real window**, at several sizes and in light and dark. The reports don't say which image each build gave the blind judge.
- **Run 1 lost as "the polished category default".** v1.7.0 had more sourdough in it: a rise jar, a named starter with a peak window, and a two-day schedule. Run 2 won 3–0 with the whole bake as 12 timed steps and a levain build. Run 3 won 2–1 with a jar-rise gauge that says bulk is done at +50%, not when the clock says so.
- **Renderer gap:** custom fonts aren't registered in the native render, so it shows the system font. Two builds noted it, and one worked around it with a scratch copy.
- Grader: HEAD 19–20 of 20, v1.7.0 17–19. Product checks: HEAD 24 of 24, v1.7.0 23 of 24.
- Cost: $20.63 for 6 builds (HEAD $11.86, v1.7.0 $8.77, +35%). HEAD builds took 14.6 minutes against 10.7. Judges: $1.73 for 9.

### Round 20: a blind judge inside the build, evals 4 and 12, three judges (HEAD vs v1.7.0)

HEAD is `bc944b6`. Before its own critique, the skill now hands its screenshots to a fresh judge that never sees the code or the intent (`scripts/blind_critique.py`), and takes its fixes first. v1.7.0 (a worktree at the tag) is the same skill without that step. Evals 4 (ferry home, iPhone) and 12 (sourdough bake day, Mac), three runs per config, Opus 5.5 builds ($8 cap), three blind Opus 5.5 judges per pair.

| Eval | Run | HEAD direction | v1.7.0 direction | Blind judge on HEAD's first frame | HEAD vs v1.7.0 | Votes |
|---|---|---|---|---|---|---|
| 4 | 1 | wp-departure-board | wp-exaggerated-number | 6 ("the standard transit layout") | **7.2** vs 6.3 | 3–0 |
| 4 | 2 | wp-departure-board | wp-departure-board | 6 | **7.2** vs 6.7 | 3–0 |
| 4 | 3 | wp-exaggerated-number | wp-departure-board | 7 (Idea capped at 5, stock layout) | **7.7** vs 7.1 | 3–0 |
| 12 | 1 | nc-owned-chrome | wp-exaggerated-number | 5.8 | 6.5 vs **7.1** | 0–3 |
| 12 | 2 | nb-dot-matrix | nc-owned-chrome | 5.6 | 6.1 vs **7.5** | 0–3 |
| 12 | 3 | nc-owned-chrome | wp-exaggerated-number | 6 | **7.3** vs 6.9 | 3–0 |

- **Phone: 3 of 3 pairs, 9 of 9 votes, mean 7.36 vs 6.71.** The blind judge told two of three builds they had the standard transit layout. Their final screens made the last boat back the structure of the screen (a timeline ending at the last boat, a hatched dead zone, its own amber line), and every eval judge named exactly that.
- **Mac: 1 of 3 pairs, 3 of 9 votes, mean 6.64 vs 7.13.** HEAD's losses lacked Mac structure: primary actions in a sidebar footer with no toolbar (run 1), and a dot-matrix timer that doesn't read from across a kitchen, in a grid of cards with no sidebar (run 2). The blind judge saw an HTML mock, which can't show a real toolbar or sidebar. The next step is to give it the native render from `render_swiftui.py`.
- **Overall: 4 of 6 pairs, 12 of 18 votes, mean 7.00 vs 6.92.**
- **The reports are more honest.** Every HEAD build ran the blind judge and reported its score. Taken before the fixes, it sat 0.2–1.4 below the build's own final critique. One run wrote that its own 7.6 "was written after seeing my own code, so the blind 7 is the more reliable number."
- **Confound:** `typecheck.py` switched to a stricter SIL compile at 15:12 while four HEAD builds were still running. It only makes the compile gate stricter; all six HEAD builds passed it.
- Grader: HEAD 17–19, v1.7.0 17–19. Product checks: HEAD 46 of 46, v1.7.0 46 of 47.
- Cost: $38.20 for 12 builds (HEAD $21.43, v1.7.0 $16.77, +28%), and HEAD builds took 14.9 minutes against 10.7. Judges: $3.53 for 18.

### Round 19: the fresh Mac brief after its fixes, eval 12, three judges (HEAD vs v1.5.0 vs none)

HEAD is `1f632fa`. It carries round 18's fixes: one moment in time (every live value derived from one `now`), one dominant readout for ambient screens, and two Mac-native options in a Mac deal. The setup is the same as round 18: three runs per config, Opus 5.5 builds ($8 cap), v1.5.0 from `d2593d9`, and three blind Opus 5.5 judges per pair.

| Run | HEAD direction | v1.5.0 direction | vs v1.5.0 | vs none |
|---|---|---|---|---|
| 1 | nc-owned-chrome | wp-departure-board | 6.7 vs **7.2** (0–3) | **7.1** vs 6.0 (3–0) |
| 2 | nc-owned-chrome | ed-newspaper-frame | **7.6** vs 7.2 (2–1) | **7.4** vs 6.5 (3–0) |
| 3 | wp-exaggerated-number | pl-persona | 6.7 vs **6.8** (1–2) | **7.3** vs 6.0 (3–0) |

- **Against no skill: 3 of 3 pairs, 9 of 9 votes, mean 7.27 vs 6.16.** Round 18 was 4 of 9. Most judges named HEAD's one dominant readout, or its numbers agreeing with one clock. One caught the baseline with a conflicting dough figure.
- **Against v1.5.0: 1 of 3 pairs, 3 of 9 votes, mean 7.00 vs 7.07.** Still a tie. v1.5.0 won run 1 with a bigger single number and run 3 with a talking starter. On this brief, nothing since v1.5.0 shows a measurable gain.
- **Read the swing with the noise.** HEAD's own mean barely moved (about 7.0 in round 18, 7.0–7.3 here). The no-skill mean fell from 6.91 to 6.16 between two rounds of the same brief, so part of the 9-of-9 is run-to-run variance. A real Mac gain over v1.5.0 needs more runs or more briefs to show.
- **The deal change took.** Two of three HEAD runs chose `nc-owned-chrome` (Mac-only). None chose the playful persona that lost round 18; run 3 chose `wp-exaggerated-number`.
- Grader: HEAD 18–19 of 19, v1.5.0 16–17, no skill 6–7. Product checks: HEAD 23 of 24 (run 1 tripped the 44 pt / phone-frame check), v1.5.0 24 of 24, no skill 19 of 24.
- Cost: $22.89 for 9 builds (HEAD $8.99, v1.5.0 $10.23, none $3.67) and $3.77 for 18 judges.

### Round 18: a fresh Mac brief, eval 12, three judges (HEAD vs v1.5.0 vs none)

HEAD is `ed41eff` (1.7.0). Eval 12 is new and untuned: a sourdough bake-day window kept open on the kitchen counter all day, neither a collection nor a pro tool. Three runs per config, Opus 5.5 builds at medium effort ($8 cap), v1.5.0 from the `d2593d9` worktree, mocks at 1280×800, three blind Opus 5.5 judges per pair.

| Run | HEAD direction | v1.5.0 direction | vs v1.5.0 | vs none |
|---|---|---|---|---|
| 1 | wp-departure-board | wp-departure-board | **7.3** vs 7.2 (2–1) | 7.1 vs **7.3** (1–2) |
| 2 | nc-owned-chrome | wp-exaggerated-number | **6.9** vs 6.5 (3–0) | **7.2** vs 6.0 (3–0) |
| 3 | pl-persona | ed-newspaper-frame | 6.7 vs **7.2** (0–3) | 6.7 vs **7.4** (0–3) |

- **Against v1.5.0: 2 of 3 pairs, 5 of 9 votes, mean 7.00 vs 6.96.** A tie.
- **Against no skill: 1 of 3 pairs, 4 of 9 votes, mean 7.02 vs 6.91.** Opus without the skill built a calm, glanceable window: one huge elapsed timer readable across a kitchen, a warm palette, every number consistent.
- **So the Mac lead from evals 7 and 8 doesn't carry over to an untuned brief yet.** Those briefs were tuned against three times; this one wasn't.
- **One moment in time.** Run 1 lost to no skill because its progress bar, fold countdown and time since feeding implied different times of day ("fatal for a screen bakers trust all day"). Round 17 had a counter that disagreed with its list. The skill has no check that live numbers agree.
- **One focal point for an ambient window.** The winners answered the counter glance with one dominant timer; HEAD's run 3 split attention between two timers and a talking starter, with the accent spread everywhere.
- **Phone-first directions on a Mac.** `pl-persona`'s Mac form became "a stock grid of rounded cards" and lost both pairs 0–3; `nc-owned-chrome` (Mac-only) swept both 3–0.
- Grader: HEAD 18–19 of 19, v1.5.0 16–17, no skill 6–7. Product checks: HEAD 24 of 24, v1.5.0 23, no skill 20 (all three no-skill runs lack menu shortcuts). The grader can't see what lost.
- Cost: $22.81 for 9 builds (HEAD $10.87, v1.5.0 $8.36, none $3.58) and $3.49 for 18 judges.

### Round 17: pixel names and game states, eval 10, three judges (HEAD vs none)

HEAD is `6510d3a`. The pixel sprite direction now sets item names and named game states (parched, thirsty, quenched) in Pixelify Sans, lowercase, at an integer 22 px or more; body text and secondary lines stay in the readable face. Eval 10 only, two runs per config, Opus 5.5 builds ($8 cap), mocks at @2x, three blind Opus 5.5 judges per pair.

| Eval | Run | HEAD direction | HEAD vs none | Votes |
|---|---|---|---|---|
| 10 | 1 | rt-pixel-sprite | **6.5** vs 6.0 | 3–0 |
| 10 | 2 | rt-pixel-sprite | **7.2** vs 5.9 | 3–0 |

- **2 of 2 pairs, 6 of 6 judge votes, mean 6.9 vs 6.0.** On this brief: round 14 had 2 of 4 votes, round 15 4 of 6, round 16 4 of 6.
- **What the judges named:** plants as named party members (ruffles, fronda, monty) with lit HP bars and named states, one focal count, and a talking plant in a dialogue box that "no competitor ships", with pixel type kept to names, states and display.
- **The baselines lost on the platform:** 32–40 dp tap targets, walls of uppercase pixel labels, a menu "taken almost straight from Final Fantasy", iOS chrome on an Android brief.
- **Still to watch:** run 1 showed a "1/5" counter against 4 thirsty plants and listed a peace lily twice. A judge caught it; the run's own critique didn't.
- Product checks: HEAD 22 of 22, no skill 15 of 21 (both miss Reduce Motion and fail to compile). Grader: HEAD 22/22 twice, no skill 8/21 and 7/22.
- Cost: $10.29 for 4 builds (HEAD $6.67) and $1.26 for 6 judges.

### Round 16: the pixel direction as an RPG, eval 10, three judges (HEAD vs none)

HEAD is `3200e8e`. The pixel sprite direction is now an RPG party screen: HP-style meters lit in the state colour, a dialogue box for the message that matters now, and a quest line with a counter, with at least two of them required. Eval 10 only, two runs per config, Opus 5.5 builds ($8 cap), mocks at @2x, three blind Opus 5.5 judges per pair.

| Eval | Run | HEAD direction | HEAD vs none | Votes |
|---|---|---|---|---|
| 10 | 1 | rt-pixel-sprite | **6.9** vs 5.7 | 3–0 |
| 10 | 2 | rt-pixel-sprite | 6.67 vs **6.73** | 1–2 |

- **1 of 2 pairs, 4 of 6 judge votes, mean 6.8 vs 6.2.** Round 15 on this brief was also 4 of 6 votes, but at 6.3 vs 6.1.
- **The moves landed.** Both skill runs built lit HP meters (red and orange at low thirst), a talking plant in a dialogue box and a "Morning round 2/5" quest counter. In run 1 all three judges named the dialogue box and the round counter as the idea that belongs to the product.
- **Run 2 lost by 0.07 on legibility against commitment.** Two judges preferred a baseline set entirely in pixel type, body text included, with named states (PARCHED, THIRSTY, DRY, QUENCHED) and the whole day at rest. The third capped that baseline for its caps labels, its pixel body text and an iOS status bar on an Android brief. The preset keeps names and body text in a readable face on purpose (`research/retro-references.md`: bitmap type at small sizes, caps-only faces), so this is a trade-off to decide, not a defect.
- **Worth taking from the baseline:** named game states next to the lit segments.
- Product checks: HEAD 18 of 18, no skill 14 of 19 (both miss Reduce Motion and fail to compile). Grader: HEAD 20/20, no skill 6/20 and 8/21.
- Cost: $9.74 for 4 builds (HEAD $6.16) and $1.20 for 6 judges.

### Round 15: the retro preset after its fixes, evals 9, 10 and 11, three judges (HEAD vs none)

HEAD is `dbc1b95`. It carries round 14's fixes: no glow on type, `fold.py` catching an orphaned heading, meters that show their value, the four-green palette replaced, and a pixel budget. This round also added a Mac brief: eval 11, a film-photography log asking for "a retro old-computer look, your pick". Two runs per config, Opus 5.5 builds ($8 cap), phone mocks at @2x and the Mac window at 1280×800. Judging moves to **three** blind Opus 5.5 judges per pair, so every pair has a majority winner; Mac pairs get the Mac judge prompt.

| Eval | Run | HEAD direction | HEAD vs none | Votes |
|---|---|---|---|---|
| 9 | 1 | rt-phosphor-terminal | **7.3** vs 6.0 | 3–0 |
| 9 | 2 | rt-phosphor-terminal | **7.0** vs 6.0 | 3–0 |
| 10 | 1 | rt-pixel-sprite | **6.5** vs 5.9 | 3–0 |
| 10 | 2 | rt-pixel-sprite | 6.1 vs **6.3** | 1–2 |
| 11 | 1 | rt-bitmap-desktop (Mac) | **7.2** vs 5.6 | 3–0 |
| 11 | 2 | rt-bitmap-desktop (Mac) | **6.9** vs 6.5 | 2–1 |

- **5 of 6 pairs, 15 of 18 judge votes, mean 6.9 vs 6.1.** Round 14 had 4 of 8 votes and 6.5 vs 6.2.
- **Product checks: HEAD 52 of 52, no skill 31 of 53.** Neither Mac baseline typechecks; both phone pixel baselines miss Reduce Motion.
- **The terminal is fixed: 6 of 6 votes.** Neither run glowed its type or orphaned a heading. The judges named the terminal "as structure, not paint" and one focal number (minutes of light left) as the reasons.
- **Correction (round 20):** one HEAD build here (eval 11, run 1) has a missing return in a `switch` getter that `-typecheck` passed. `typecheck.py` now compiles through SIL and fails it, so HEAD's product checks were 51 of 52, and its Swift typechecked in 5 of 6 skill builds, not 6.
- **The Mac works: 5 of 6 votes.** Both skill runs dealt `--preset retro --platform macos` and chose the bitmap desktop: a dithered contact sheet, a lab-pipeline stepper, keyboard-labelled actions inside a real Mac window. Both baselines reskinned the whole window as System 6 ("a 1984 Finder clone"), which is exactly what the preset forbids.
- **The pixel screen is still the weak spot: 4 of 6 votes.** HEAD was the cleaner phone screen in both runs. But in run 2 the thirst bars differed in length with every segment unlit grey, so "the meter barely reads". Across both rounds the judges gave the baselines the better RPG mechanics: HP-style thirst bars, a plant that talks in a dialogue box.
- **Next for pixel:** require meters as lit segments in the state colour (an RPG health bar), and name RPG mechanics (an HP bar, a dialogue box, a quest line) as signature moves.
- Cost: $27.45 for 12 builds (HEAD $17.61) and $3.65 for 18 judges.

### Round 14: the retro preset, evals 9 and 10 (HEAD vs none)

First measure of the retro preset (`da857b4`): three named-only directions (phosphor terminal, pixel sprite, bitmap desktop) from `research/retro-references.md`. Two phone briefs name the style: a backpacker's trail status as "an old green phosphor terminal, Fallout Pip-Boy style" (eval 9, SwiftUI) and a plant-watering home as "16-bit pixel art, like an old RPG" (eval 10, Compose). Two runs per config, Opus 5.5 builds at medium effort ($8 cap), mocks at 390×844 shot at @2x with `evals/shot.mjs`, and two blind Opus 5.5 judges per pair. There is no v1.5.0 config, since it has no retro preset.

| Eval | Run | HEAD direction | HEAD vs none | Votes |
|---|---|---|---|---|
| 9 | 1 | rt-phosphor-terminal | **7.4** vs 6.0 | 2–0 |
| 9 | 2 | rt-phosphor-terminal | 6.0 vs **6.7** | 0–2 |
| 10 | 1 | rt-pixel-sprite | 6.3 vs 6.0 | 1–1 |
| 10 | 2 | rt-pixel-sprite | 6.3 vs 6.0 | 1–1 |

- **4 of 8 judge votes, mean 6.5 vs 6.2:** one pair won, one lost, two split.
- **Product checks: HEAD 36 of 36, no skill 24 of 35.** These leave out the process items only a skill run can pass. No skill missed Reduce Motion on both plant screens, a terminal face on both trail screens, the fold on three screens and one Kotlin compile. All four skill builds dealt `--preset retro` with the Deal line and picked the matching direction; none used a Fallout name, face or mark.
- **The terminal won clearly when clean.** In run 1 both judges said the idea shapes the layout (a shell prompt for the trail day, dot-leader readouts, a sunset-versus-arrival line), while the baseline was "a generic card dashboard painted green" with caps labels and dim secondary text.
- **It lost to its own defects.** In run 2 both judges gave HEAD the better idea and picked the baseline: the hero digits were smeared by a glow (the preset allowed "one soft glow on the key number"), and the refill-log heading peeked above the pinned button. `fold.py` passed it, because it checks rows, not section headings.
- **The pixel screen split twice.** One judge rewarded HEAD's legibility and one-glance count; the other rewarded the baseline's fuller RPG costume (a quest banner, health bars). In run 2, HEAD's meters showed three different urgencies as the same empty bar, and its four-green palette read as a borrowed Game Boy.
- **To fix next:** no glow on type; `fold.py` should catch a heading cut by a pinned bar; a meter must vary with its value; move the four-green palette off the handheld's original hues; and decide how much pixel art a screen should carry.
- Cost: $17.16 for 8 builds (HEAD $10.31) and $1.68 for 8 judges.

### Round 13: Opus builds, evals 7 and 8 (HEAD vs v1.5.0 vs none)

Same as round 12 except the builder. It used the same two prompts, three runs per config, v1.5.0 from the `d2593d9` worktree, 1280×800 mocks shot with `evals/shot.mjs`, and two blind Opus 5.5 judges per pair ($2 cap each). The builds ran on Opus 5.5 at medium effort, with the cap raised from $3 to $8 so skill builds wouldn't be cut off. Every Mac round before this one built on Sonnet, while the phone rounds built on Opus. HEAD is `d462d54`: round 12's skill plus the Deal line in the report. Each score is the mean of the two judges.

| Eval | Run | HEAD direction | vs v1.5.0 | vs none |
|---|---|---|---|---|
| 7 | 1 | ed-newspaper-frame (Mac form) | **7.3** vs 6.6 | **7.2** vs 5.9 |
| 7 | 2 | ed-newspaper-frame (Mac form) | **7.5** vs 7.1 | **7.2** vs 6.5 |
| 7 | 3 | ed-newspaper-frame (Mac form) | 7.2 vs 7.3 (judges split) | **7.4** vs 6.3 |
| 8 | 1 | pi-instrument-panel | **7.9** vs 6.5 | **7.8** vs 6.3 |
| 8 | 2 | nc-quiet-native | **7.5** vs 7.0 | **7.6** vs 6.0 |
| 8 | 3 | df-library | **7.4** vs 7.0 | **7.6** vs 5.8 |

- **Against v1.5.0: 5 of 6 pairs and 1 split, 11 of 12 judge votes, mean 7.5 vs 6.9.** By eval: eval 7 7.3 vs 7.0, eval 8 7.6 vs 6.8.
- **Against no skill: 6 of 6 pairs, 12 of 12 judge votes, mean 7.5 vs 6.1.** By eval: eval 7 7.3 vs 6.2, eval 8 7.7 vs 6.0.
- **The lead holds on Opus but narrows.** Round 12 had the same harness with Sonnet builds, and HEAD led v1.5.0 by 0.8 and no skill by 1.7. Here the leads are 0.55 and 1.3. Opus lifts both baselines more than it lifts HEAD: no skill went from 5.6 to 6.1, v1.5.0 from 6.4 to 6.9, HEAD from 7.1–7.3 to 7.5. The phone rounds on Opus showed the same pattern (round 9: +0.55 over no skill).
- **Eval 7 is now close against v1.5.0.** All six skill runs built ed-newspaper-frame, as in round 12, and HEAD's margin fell from 1.0 to 0.3. The split pair is run 3. One judge preferred v1.5.0's collector detail (gaps in each run, provenance, price paid, sailings transcribed from the timetable) over HEAD's "in force today" idea, which in its words "doesn't really serve collectors of old timetables". The other preferred HEAD's density and its live idea. HEAD's eval-7 wins come from Mac density and the coverage strips.
- **Eval 8 is where HEAD pulls ahead.** HEAD dealt three different directions and won with all three: pi-instrument-panel by 1.4, nc-quiet-native by 0.5 and df-library by 0.4. Every v1.5.0 run built nb-spec-sheet. Quiet native won its pair against v1.5.0 again (it lost only on collection briefs).
- **The Deal line works.** All six HEAD runs recorded it, for example `deal.py --options 3 --content collection,detail --sector hobby --platform macos --seed 57916`. Every eval-7 run passed `--sector hobby` and a collection-led `--content`, so quiet native couldn't be dealt there.
- Grader, without the new "Deal command recorded" item (only HEAD can pass it): HEAD scored 16–19 of 19 on eval 7 and 20–21 of 21 on eval 8; v1.5.0 17–19 of 19 and 18–20 of 21; no skill 8 of 19 and 8–9 of 21. All 18 Swift files typecheck on macOS 14.0. The two judges agreed on 11 of 12 pairs, and HEAD sat in position A in 7 of 12.
- Cost: $51.36 for 18 builds (HEAD $21.58, v1.5.0 $20.42, none $9.36), 3.2× round 12's Sonnet builds, and $4.28 for 24 Opus judges. The most expensive build was $4.43, well under the $8 cap.

### Round 12: quiet native out of collection briefs, Opus judges, evals 7 and 8 (HEAD vs v1.5.0 vs none)

This round ran HEAD at `de50768`: v1.6.0, with nc-quiet-native no longer dealt for collection or hobby briefs (`not_for_content: [collection]`, `not_for: hobby`). As the eval 7 notes below explain, it doesn't measure that change on its own. Round 11's judges rejected the stronger-move alternative: after `42f7fa3` put the idea in every row, quiet native still lost as "a competent table with a decorative timeline strip". Builds were the same as round 11: the same two prompts, Sonnet 5.5 at medium effort ($3 cap), v1.5.0 from the `d2593d9` worktree, and 1280×800 mocks shot with `evals/shot.mjs`. This round used three runs per config on both evals. The judges changed to two independent blind Opus 5.5 judges per pair ($2 cap each), 12 pairs with A and B shuffled. Each score below is the mean of the two judges.

| Eval | Run | HEAD direction | vs v1.5.0 | vs none |
|---|---|---|---|---|
| 7 | 1 | ed-newspaper-frame (Mac form) | **7.1** vs 6.2 | **7.2** vs 4.7 |
| 7 | 2 | ed-newspaper-frame (Mac form) | **7.5** vs 6.0 | **7.6** vs 5.9 |
| 7 | 3 | ed-newspaper-frame (Mac form) | **6.6** vs 6.0 | **6.7** vs 4.7 |
| 8 | 1 | pi-instrument-panel | **7.2** vs 6.7 | **7.5** vs 6.6 |
| 8 | 2 | pi-instrument-panel | **7.1** vs 6.0 | **7.0** vs 6.0 |
| 8 | 3 | nc-quiet-native | **7.4** vs 7.2 | **7.7** vs 5.8 |

- **Against v1.5.0: 6 of 6 pairs, 12 of 12 judge votes, mean 7.1 vs 6.4.** By eval: eval 7 7.1 vs 6.1, eval 8 7.2 vs 6.6.
- **Against no skill: 6 of 6 pairs, 12 of 12 judge votes, mean 7.3 vs 5.6.** By eval: eval 7 7.2 vs 5.1, eval 8 7.4 vs 6.1.
- Grader: HEAD scored 18–19 of 19 on eval 7 and 20 of 21 on eval 8; v1.5.0 scored 18–19 of 19 and 18–19 of 21; no skill scored 9 of 19 and 7–9 of 21. The two judges agreed on the winner of every pair, and HEAD sat in position A in 5 of the 12.
- **Swift typechecks: 18 of 18.** Each run's Swift file passed `typecheck.py --platform macos` against the macOS 14.0 deployment target (Xcode 26.2, macOS SDK 26.2): HEAD 3 of 3 on each eval, v1.5.0 3 of 3, no skill 3 of 3. Compilation doesn't separate the configs on these briefs; the grader's own typecheck item agrees on every run.
- **Eval 7: the fix changed none of the three first deals.** Every HEAD run and every v1.5.0 run built ed-newspaper-frame, so the eval-7 margin is that direction's Mac form against v1.5.0's phone form. The judges marked v1.5.0 down for a magazine masthead in the content area, tall rows (about 8 visible), an empty inspector and Platform 6. HEAD kept Mac density (15–18 rows, sortable columns) and drew the collecting into the content: a season grid ("17 of 38 seasons held") and a year strip with gaps for wanted editions.
  - What `--content` the runs passed wasn't recorded. Replayed with collection-primary shapes (`collection,list` or `collection,table`, which fit what the runs report) at the runs' seeds (48103, 49219, 31744), the pre-fix `deal.py` deals the same three options: ed-newspaper-frame, nb-sticker-sheet and nc-columns. The primary-shape rule and nc-columns' ranking already keep quiet native out of those deals; `not_for_content` doesn't have to.
  - The fix mattered once. Run 2 also dealt inside native-craft to compare (`--preset native-craft`, seed 7) and kept editorial. That deal now gives nc-columns; before the fix, nc-quiet-native came first.
  - So this round is evidence for the Mac form of ed-newspaper-frame, not for the fix. The fix still matters wherever a deal reaches quiet native for a collection brief: a deal inside native-craft, a wide deal, or `detail,collection`. `test_deal.py` now tests those cases.
- **Eval 8.** Quiet native was still dealt for the table brief, as intended. It won narrowly against v1.5.0's ed-newspaper-frame, 7.4 vs 7.2, and both judges picked it, but on Mac fit rather than idea. Both judges gave the richer idea to v1.5.0: per-row speed bars, a speed-coloured waveform and concrete advice ("Cut 3 characters, or hold the out-point 0.17 s"). HEAD won on a 16-row list, search, in/out nudge buttons and a visible ⌘↩ shortcut. pi-instrument-panel won its two pairs against v1.5.0 by 0.5 and 1.1, and its two against no skill by 0.9 and 1.0.
- **Not comparable to round 11's numbers.** The judge model and the number of judges changed. Under round 11's single Sonnet judge, v1.5.0's ed-newspaper-frame ranged from 6.0 (11b) to 8.0. Under Opus here it got 6.0–6.2. The scale may differ between judge models, so compare win counts and margins within a round, not score levels across rounds.
- Setup: every config ran with `--setting-sources project,local`, so the account's user-level skills and plugins stayed out of all three; the user's global CLAUDE.md still loaded for all of them. Models are pinned by id (`claude-sonnet-5-5`, `claude-opus-5-5`) on Claude Code 2.1.304. A first batch on 2.1.277 didn't know Sonnet 5.5: it priced it about 2.3× too high and capped it at 200k context, which would have tightened the $3 cap. That batch was stopped and isn't counted.
- Cost: $16.26 for 18 builds (HEAD $7.59, v1.5.0 $6.06, none $2.61) and $4.39 for 24 Opus judges.
- **After this round: the report records the deal.** `deal.py` now ends every deal with a `Deal:` line, the command with its flags and seed that deals the same options again. The report's Direction line carries it, and each redeal's, because round 12's eval-7 deals could only be replayed by guessing their `--content`. `grade.py` checks for it ("Deal command recorded"), so grader totals rise by one from round 13 on: 20 on eval 7, 22 on eval 8. Round 12's grades above are from the grader before this check.

### Round 11: the Mac deal and the Mac presets, evals 7 and 8 (v1.6.0 vs v1.5.0 vs none)

This round measured `deal.py --platform macos` (each direction's Mac window form) and the three Mac-only presets. It used two briefs: the library redesign (eval 7) and a new build, a subtitle translator's main window (eval 8: `table` + `document` + `canvas`). Builds ran on Sonnet 5.5 at medium effort ($3 cap) in three configs: v1.6.0, v1.5.0 (a worktree at `d2593d9`) and no skill. Each build wrote a 1280×800 mock, rendered through the DevTools protocol at an exact 1280×800 viewport, which fixes round 10's blank band. One blind Sonnet 5.5 judge per pair ($1 cap) saw two screenshots, with A and B shuffled.

| Eval | Run | v1.6.0 direction | vs v1.5.0 | vs none |
|---|---|---|---|---|
| 7 | 1 | nc-quiet-native | 5.8 vs **7.6** | **6.8** vs 5.4 |
| 7 | 2 | wp-departure-board (Mac form) | 6.2 vs **7.6** | **7.8** vs 6.6 |
| 7 | 3 | nc-quiet-native | 5.8 vs **8.0** | **7.0** vs 6.4 |
| 8 | 1 | pi-instrument-panel | **7.8** vs 6.0 | **7.6** vs 6.0 |
| 8 | 2 | pi-instrument-panel | 7.2 vs 7.2 (judge picked v1.5.0) | **7.8** vs 7.2 |

- **Against no skill: 5 of 5, mean 7.4 vs 6.3.** Grader: v1.6.0 18–20 of 19/21 on every run, baselines 7–9.
- **Against v1.5.0: 1 of 5, mean 6.6 vs 7.3.** On the Mac-native pro-tool brief (eval 8), pi-instrument-panel won one pair and tied the other. On eval 7 every v1.5.0 run dealt ed-newspaper-frame and built the idea into the content: per-operator year strips that show the gaps in a collection. Two v1.6.0 runs dealt nc-quiet-native and built exactly its pitfall, a stock Finder-style table with the idea only in the inspector, so the judge capped Idea at 5 for a stock layout.
- **Fix (`42f7fa3`).** nc-quiet-native became "Native chrome, owned content": the owned idea is drawn into every row of the content column, and a cover-the-inspector test sits in its pitfall. `deal.py` now deals for macOS on its own when the project or code says macOS, after one eval-8 run dealt without the flag and had to redeal.
- **Round 11b: eval 7 rerun with the fix, 3 runs.** Run 1 dealt nc-quiet-native again and rose to 6.8, still behind v1.5.0's 7.8 ("a competent table with a decorative timeline strip"); against no skill it scored 8.0 vs 6.0. Run 2 dealt ed-newspaper-frame in its Mac form: 8.0 vs v1.5.0's 6.0 and 7.8 vs no skill's 5.6. Run 3 hit the account's session limit mid-build, so its two pairs aren't counted.
- **Read.** The Mac deal and the pro-instrument directions hold up. Quiet native is still the weakest Mac option under judges who reward visible identity, even after the fix. Next: stop dealing it for collection and hobby briefs, or give it a stronger required move. Also re-measure with Opus judges and n ≥ 3 per eval: this round is one judge per pair on Sonnet.
- Cost: $13.38 for the 15 builds, $2.27 for the 3 fix builds, and $1.62 for 16 judges.

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

`python3 evals/test_deal.py` checks `scripts/deal.py`'s platform handling. No model calls. The library passes `--check`, which now also rejects a Mac block missing a field or carrying phone mechanics (thumb zone, tab bar, bottom sheet, tap, swipe, 9:16, dp, iOS haptics), including the motion and pitfall it inherits. Over 40 seeds and four content shapes, `--platform macos` never deals a direction whose Mac block says skip and always deals at least one Mac-only preset option when one can show the content, while a phone deal never deals a Mac-only direction; every Mac sheet carries the Mac composition, the window chrome line and the Mac dials and no phone words; and every phone sheet is unchanged.

`python3 evals/test_mascot.py` checks `scripts/mascot.py` on a hand-written mascot (`fixtures/pip.svg`, a rig in the pl-toy-box palette, written the way Illustrator exports) and its motion spec (`fixtures/pip.motion.json`: an idle loop with breathing and a blink, and a celebration with a hop, a mouth morph and sparks drawing on). No model calls. It checks that the path parser handles relative commands, S/T curves and compact arc flags; that the SwiftUI output typechecks (`typecheck.py`) and renders on macOS with the eyes open at rest and covered on the blink; that the Compose output compiles (`compile_kotlin.py`); that the Lottie has `v fr ip op w h layers`, is parented and anchored at the pivots, and doesn't leave its canvas; that a morph between shapes with different vertex counts and an unknown part are refused; and that the preview runs through `filmstrip.py`, which measures the reaction at 900 ms and the idle state as looping, and that its frames visibly change and land back on rest, in both clock and `--frames` mode. Steps whose toolchain is missing are skipped, not failed: Xcode, JDK 17 + Gradle, a Chromium browser, and network for lottie-web.
