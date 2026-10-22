#!/usr/bin/env python3
"""Checks scripts/deal.py's platform handling. No model calls, stdlib only.

- the library passes --check (fields, contrast, Mac blocks, no phone wording in them);
- a macOS deal never deals a direction whose Mac block says skip, over many seeds;
- a macOS sheet carries the Mac composition, the window chrome line and the Mac dials,
  and none of the phone mechanics;
- the phone deal and sheet are unchanged by the Mac blocks, and never deal a Mac-only direction;
- every macOS deal includes two Mac-native preset options when two can show the content (one when only one can);
- a direction is never dealt when a requested shape is in its not_for_content, including deals
  inside its preset and wide deals that would otherwise include it, and --sector hobby drops the
  directions marked not_for hobby (nc-quiet-native for collection and hobby briefs, after round 11);
- named-only presets (retro) are dealt only with --preset, never in the open deal;
- the Deal line deal.py prints replays the same options in the same order.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEAL = ROOT / "scripts" / "deal.py"
sys.path.insert(0, str(DEAL.parent))
import deal  # noqa: E402


def run(*args: str) -> tuple[int, str]:
    p = subprocess.run([sys.executable, str(DEAL), *args], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def main() -> int:
    failures: list[str] = []
    directions = deal.load()
    skipped = {d["id"] for d in directions if deal.for_platform(d, "macos") is None}
    mac_only = {d["id"] for d in directions if deal.mac_only(d)}
    native_shapes = {c for d in directions if deal.mac_only(d) for c in d["content"]}
    preset = {d["id"]: d["preset"] for d in directions}

    def native_presets(content: str) -> set[str]:
        """Mac presets with a direction that can show the primary shape and isn't ruled out by any requested shape."""
        shapes = content.split(",")
        return {d["preset"] for d in directions if deal.mac_only(d) and shapes[0] in d["content"]
                and not set(shapes) & set(d.get("not_for_content", []))}


    code, out = run("--check")
    if code != 0:
        failures.append(f"--check failed:\n{out}")

    for seed in range(40):
        for content in ("list", "story", "detail,collection", "number"):
            code, out = run("--options", "3", "--content", content, "--platform", "macos", "--seed", str(seed))
            dealt = {line.split()[1] for line in out.splitlines() if line.startswith("- ")}
            if dealt & skipped:
                failures.append(f"seed {seed} content {content}: dealt {dealt & skipped} on macOS")
            need = min(2, len(native_presets(content)))
            if len({preset[i] for i in dealt & mac_only}) < need:
                failures.append(f"seed {seed} content {content}: fewer than {need} Mac-native options in {sorted(dealt)}")
            code, out = run("--options", "3", "--content", content, "--seed", str(seed))
            dealt = {line.split()[1] for line in out.splitlines() if line.startswith("- ")}
            if dealt & mac_only:
                failures.append(f"seed {seed} content {content}: phone deal dealt Mac-only {dealt & mac_only}")

    # Round 11: quiet native lost every collection brief it was dealt, so it is never dealt for one.
    avoided = {d["id"]: set(d.get("not_for_content", [])) for d in directions if d.get("not_for_content")}
    hobby = {d["id"] for d in directions if "hobby" in d["not_for"]}
    if "nc-quiet-native" not in hobby or "collection" not in avoided.get("nc-quiet-native", set()):
        failures.append("nc-quiet-native should be not_for hobby and not_for_content collection")
    # Most collection deals drop quiet native before not_for_content is reached (it no longer holds
    # collection, and nc-columns outranks it on the secondary shape), so the cases include deals that
    # reach it: inside native-craft (a redeal there was in round 12) and a wide deal.
    cases = [(["--options", "3", "--content", c], True)
             for c in ("collection", "table,collection", "list,collection", "detail,collection")]
    cases += [(["--options", "3", "--preset", "native-craft", "--content", "list,collection"], False),
              (["--options", "8", "--content", "table,collection"], False)]
    for seed in range(40):
        for args, native in cases:
            code, out = run(*args, "--platform", "macos", "--seed", str(seed))
            dealt = {line.split()[1] for line in out.splitlines() if line.startswith("- ")}
            content = set(args[args.index("--content") + 1].split(","))
            bad = {i for i in dealt & set(avoided) if avoided[i] & content}
            if bad:
                failures.append(f"seed {seed} {' '.join(args)}: dealt {bad} for a shape it is not for")
            if native and not dealt & mac_only:
                failures.append(f"seed {seed} {' '.join(args)}: no Mac-native option in {sorted(dealt)}")
    # The same deals without collection must reach quiet native, or the cases above test nothing.
    reached = set()
    for seed in range(40):
        code, out = run("--options", "3", "--preset", "native-craft", "--content", "list,table", "--platform", "macos", "--seed", str(seed))
        reached |= {line.split()[1] for line in out.splitlines() if line.startswith("- ")}
    if "nc-quiet-native" not in reached:
        failures.append("the native-craft deal never reaches nc-quiet-native, so the not_for_content cases are vacuous")
    for seed in range(40):
        code, out = run("--options", "3", "--content", "table", "--sector", "hobby", "--platform", "macos", "--seed", str(seed))
        dealt = {line.split()[1] for line in out.splitlines() if line.startswith("- ")}
        if dealt & hobby:
            failures.append(f"seed {seed} sector hobby: dealt {dealt & hobby}")

    # Named-only presets (retro) join a deal only when asked for, on the phone and the Mac.
    named = {d["id"] for d in directions if d["preset"] in deal.NAMED_ONLY}
    if not named:
        failures.append("no named-only directions in the library")
    for seed in range(40):
        for content in ("list", "number", "action", "detail,collection"):
            for platform in ([], ["--platform", "macos"]):
                code, out = run("--options", "3", "--content", content, *platform, "--seed", str(seed))
                dealt = {line.split()[1] for line in out.splitlines() if line.startswith("- ")}
                if dealt & named:
                    failures.append(f"seed {seed} content {content} {platform}: open deal dealt named-only {dealt & named}")
        for platform in ([], ["--platform", "macos"]):
            code, out = run("--options", "3", "--preset", "retro", *platform, "--seed", str(seed))
            dealt = {line.split()[1] for line in out.splitlines() if line.startswith("- ")}
            if not dealt or dealt - named:
                failures.append(f"seed {seed} --preset retro {platform}: dealt {sorted(dealt)}")

    # The Deal line replays the deal: same options, same order.
    for args in (["--options", "3", "--content", "collection,list", "--platform", "macos"],
                 ["--options", "3", "--preset", "native-craft", "--content", "list,table", "--sector", "hobby", "--platform", "macos"],
                 ["--options", "4", "--content", "list,number", "--have", "photography"]):
        code, out = run(*args)
        line = next((l for l in out.splitlines() if l.startswith("Deal: deal.py ")), "")
        again = run(*line.split("  (")[0].split()[2:])[1] if line else ""
        dealt = [l.split()[1] for l in out.splitlines() if l.startswith("- ")]
        if not line or dealt != [l.split()[1] for l in again.splitlines() if l.startswith("- ")]:
            failures.append(f"{' '.join(args)}: the Deal line {line!r} doesn't replay {dealt}")

    for d in directions:
        if d["id"] in mac_only:
            code, out = run("--direction", d["id"], "--seed", "1", "--platform", "macos")
            if code != 0 or "Window chrome: " + d["chrome"] not in out or deal.PHONE_WORDS.search(out):
                failures.append(f"{d['id']}: Mac-only sheet missing its chrome line or mentions phone mechanics")
            code, out = run("--direction", d["id"], "--seed", "1")
            if code == 0:
                failures.append(f"{d['id']}: Mac-only sheet printed without --platform macos")
            continue
        if d["id"] in skipped:
            code, out = run("--direction", d["id"], "--platform", "macos")
            if code == 0 or "no macOS form" not in out:
                failures.append(f"{d['id']}: sheet printed on macOS though its Mac block says skip")
            continue
        code, out = run("--direction", d["id"], "--seed", "1", "--platform", "macos")
        mac = d["mac"]
        dials = " ".join(f"{k}{v}" for k, v in {**d["dials"], **mac["dials"]}.items())
        for want in (mac["composition"], "Window chrome: " + mac["chrome"], dials, "--platform macos"):
            if want not in out:
                failures.append(f"{d['id']}: macOS sheet lacks {want[:50]!r}")
        leak = deal.PHONE_WORDS.search(out)
        if leak:
            failures.append(f"{d['id']}: macOS sheet mentions {leak.group(0)!r}")

        code, out = run("--direction", d["id"], "--seed", "1")
        if d["composition"] not in out or "Window chrome" in out or "--platform" in out:
            failures.append(f"{d['id']}: phone sheet changed by the Mac block")

    for f in failures:
        print(f"FAIL {f}")
    print("OK" if not failures else f"{len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
