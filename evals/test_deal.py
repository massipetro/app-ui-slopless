#!/usr/bin/env python3
"""Checks scripts/deal.py's platform handling. No model calls, stdlib only.

- the library passes --check (fields, contrast, Mac blocks, no phone wording in them);
- a macOS deal never deals a direction whose Mac block says skip, over many seeds;
- a macOS sheet carries the Mac composition, the window chrome line and the Mac dials,
  and none of the phone mechanics;
- the phone deal and sheet are unchanged by the Mac blocks, and never deal a Mac-only direction;
- every macOS deal includes at least one Mac-native preset option when one can show the content.
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

    code, out = run("--check")
    if code != 0:
        failures.append(f"--check failed:\n{out}")

    for seed in range(40):
        for content in ("list", "story", "detail,collection", "number"):
            code, out = run("--options", "3", "--content", content, "--platform", "macos", "--seed", str(seed))
            dealt = {line.split()[1] for line in out.splitlines() if line.startswith("- ")}
            if dealt & skipped:
                failures.append(f"seed {seed} content {content}: dealt {dealt & skipped} on macOS")
            if content.split(",")[0] in native_shapes and not dealt & mac_only:
                failures.append(f"seed {seed} content {content}: no Mac-native option in {sorted(dealt)}")
            code, out = run("--options", "3", "--content", content, "--seed", str(seed))
            dealt = {line.split()[1] for line in out.splitlines() if line.startswith("- ")}
            if dealt & mac_only:
                failures.append(f"seed {seed} content {content}: phone deal dealt Mac-only {dealt & mac_only}")

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
