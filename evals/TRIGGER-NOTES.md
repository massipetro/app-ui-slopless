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
