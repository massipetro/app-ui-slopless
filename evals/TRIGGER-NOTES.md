# Description trigger tuning — status (2026-10-18)

`trigger-eval.json`: 20 queries (9 should-trigger, 11 near-miss), approved by the user.

Two skill-creator `run_loop` runs (Sonnet 5.5 and Opus 5.5, 5 iterations each) gave **invalid** scores:
recall stayed at 0–22% and precision at 100%, and the description never improved.
Cause: the default `--timeout 30` per query is too short. A run that hasn't reached its first tool call within 30s counts as "not triggered".
A manual `claude -p` probe of "make my app look less AI…" on Opus *did* invoke the skill as its first tool.

The Opus run cost ~300 full `claude -p` sessions (10 parallel) in ~5 minutes, which burned the usage budget. Don't repeat that.

Next time:
- Smoke-test 1–2 queries with `--timeout 120 --runs-per-query 1 --num-workers 2` on Sonnet. Ask the user before scaling up.
- skill-creator scripts need `from __future__ import annotations` on system python3 3.9.

## Update (2026-10-18, second pass)

The low recall of the run_loop runs was mostly a measurement bug, not the description:

- **Shared commands dir.** run_eval writes one `.claude/commands/<name>-skill-<id>.md` per worker into the same project. With N workers a session sees N copies and often invokes another worker's copy, which scored as "not triggered". Fix: accept any `<name>-skill-` match (all workers test the same description).
- **First tool call ends the run.** Upstream scores "not triggered" if the first tool call is not Skill/Read (e.g. Bash, ToolSearch). Fix: allow up to 3 other tool calls.
- **Running from the Claude desktop app.** The nested `claude -p` inherits the desktop session env (`CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH`, messaging socket...) and the standalone CLI must be logged in (`claude auth login`). Otherwise every run exits in ~3s and silently scores as "not triggered". Fix: strip `CLAUDE*`, `MCP_*`, `ANTHROPIC_*` from the child env.
- **Model ID.** CLI 2.1.277 logs `unrecognized_model` for `claude-sonnet-5-5`. Use `--model sonnet`.

With those fixes (scratch copy of skill-creator's run_eval.py), Sonnet, 1 run per query, 2 workers, `--timeout 120`, on 9 should-trigger + 4 near-miss queries (React landing page, LazyColumn jank, pixel-identical XML→Compose, Figma auto layout):

| Description | Should-trigger | Near-miss correctly skipped | Total |
|---|---|---|---|
| Original | 6/9 | 4/4 | 10/13 |
| New (this branch) | 7/9 | 4/4 | 11/13 |

The new description fixed "restyle the order tracking flow". Both still miss the two audit/critique queries: the screenshot or login screen doesn't exist in the eval sandbox, so Claude asks for it first and says it will load the skill once it has it. That is an artifact of the empty sandbox more than a description problem. Single runs, so ±1 query is noise.

## Update (2026-10-20): macOS

The description now names Mac screens and windows. `trigger-eval.json` gained 3 queries (2 should-trigger, 1 near-miss: a notarization/entitlements problem). They have not been run through `run_loop` yet, so the 11/13 figures above predate the macOS wording; rerun the smoke test (Sonnet, `--timeout 120`, 2 workers) before trusting recall.
