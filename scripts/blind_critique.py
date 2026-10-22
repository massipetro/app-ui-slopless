#!/usr/bin/env python3
"""A blind judge for the screens you just built: it sees the pixels, never your intent.

  blind_critique.py screen.png [more.png ...] --brief "<the brief in one or two sentences>"
                    [--platform ios|android|macos] [--model M] [--dry-run]

Your own critique knows what you meant to build, so it reads intent into the pixels. In our
blind evals the builds' own critiques passed what the judges then capped: a stock transit
layout (round 9), a heading orphaned above the bar (round 14), a counter that disagreed with
its list (round 17), live numbers implying three different times of day (round 18).

This copies only the screenshots, the brief and references/critique.md into an empty folder
and asks a fresh headless `claude` session, with nothing else in its context, to score them
and name the three problems a blind judge would mark down first. Fix those, then write your
own critique round.

Exit 0: judged (the verdict is printed and saved as blind-critique.json next to the first
screenshot). Exit 3: no `claude` CLI here; the hand-off for a fresh subagent is printed
instead (give it exactly those files and that prompt, and nothing else). Exit 1: the judge
ran but returned no verdict.

Standard library only; works on Python 3.9. Set CLAUDE_BIN to use a specific CLI.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CRITIQUE = Path(__file__).resolve().parent.parent / "references" / "critique.md"

PLATFORM = {
    "ios": "an iPhone screen (judge Platform as iOS: safe areas, 44 pt targets, text that scales, native back and sheets)",
    "android": "an Android screen (judge Platform as Android: insets, 48 dp targets, text in sp, system back)",
    "macos": "a Mac window (judge Platform as macOS: sidebar and toolbar, density, window chrome, pointer and keyboard paths, not a stretched phone)",
}

PROMPT = """You are a blind design judge. The image file(s) {files} in this folder are renders of {what}. They answer this brief: '{brief}'
Read critique.md in this folder, then look at every image (Read tool). You know nothing about how they were made; judge only what is visible.
Score the screen with critique.md's passes, criteria and caps: Idea, Hierarchy, Craft, Substance, Platform, each 0-10, an overall, and every cap that applies.
Look hard for what a strict judge would mark down: no single answer at a glance (and on a screen kept open all day, nothing readable from across a room); live numbers that disagree with each other or with the clock shown; anything cut, clipped or orphaned at an edge or under a bar; the category's stock layout in new colours; small uppercase labels; low contrast; a must-have from the brief that isn't visible at rest.
Then give the three most important problems, most damaging first, each as: where on the screen, what is wrong, and the fix.
End with exactly these lines:
SCORES: Idea n · Hierarchy n · Craft n · Substance n · Platform n → overall n (caps: <which, or none>)
FIX 1: <...>
FIX 2: <...>
FIX 3: <...>"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("images", nargs="+", help="the rendered screens (PNG or JPEG): the resting frame first")
    ap.add_argument("--brief", required=True, help="the user's brief in one or two sentences, no design notes")
    ap.add_argument("--platform", choices=sorted(PLATFORM), default="ios")
    ap.add_argument("--model", help="model for the judge (default: the CLI's default)")
    ap.add_argument("--dry-run", action="store_true", help="print the hand-off without running a judge")
    args = ap.parse_args()

    images = [Path(i) for i in args.images]
    missing = [str(i) for i in images if not i.is_file()]
    if missing:
        print(f"blind_critique: not found: {', '.join(missing)}")
        return 2

    # Only the pixels, the brief and the rubric go in: no code, no report, no direction sheet.
    folder = Path(tempfile.mkdtemp(prefix="blind-critique-"))
    names = []
    for n, img in enumerate(images, 1):
        name = f"screen-{n}{img.suffix.lower()}"
        shutil.copy(img, folder / name)
        names.append(name)
    shutil.copy(CRITIQUE, folder / "critique.md")
    (folder / "brief.txt").write_text(args.brief)
    prompt = PROMPT.format(files=", ".join(names), what=PLATFORM[args.platform], brief=args.brief.replace("'", "’"))

    cli = os.environ.get("CLAUDE_BIN") or shutil.which("claude")
    if args.dry_run or not cli:
        why = "dry run" if args.dry_run else "no `claude` CLI on this machine"
        print(f"blind_critique: {why}. Hand this to a fresh subagent with no other context.")
        print(f"Files (and nothing else): {folder}")
        print(f"Prompt:\n{prompt}")
        return 0 if args.dry_run else 3

    cmd = [cli, "-p", prompt, "--allowedTools", "Read", "--output-format", "json"]
    if args.model:
        cmd += ["--model", args.model]
    try:
        proc = subprocess.run(cmd, cwd=folder, capture_output=True, text=True, timeout=600)
        result = json.loads(proc.stdout or "{}")
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        print(f"blind_critique: the judge didn't answer ({type(e).__name__}); critique by eye and say so")
        return 1
    finally:
        shutil.rmtree(folder, ignore_errors=True)
    verdict = (result.get("result") or "").strip()
    if "SCORES:" not in verdict:
        print(f"blind_critique: no verdict returned ({proc.stderr.strip()[:200] or 'empty answer'}); critique by eye and say so")
        return 1
    cost = result.get("total_cost_usd")
    (images[0].parent / "blind-critique.json").write_text(json.dumps(
        {"images": [str(i) for i in images], "brief": args.brief, "verdict": verdict, "cost_usd": cost}, indent=2))
    print(verdict)
    print(f"\nblind_critique: judged {len(images)} screen(s){f', ${cost:.2f}' if cost else ''}; saved blind-critique.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
