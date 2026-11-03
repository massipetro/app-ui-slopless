#!/usr/bin/env python3
"""Render every iOS or Android build of an eval round natively, at the default and largest text size, for the blind judges.

  python3 evals/render_builds.py <iteration-dir> [--eval eval-13-*]

Kotlin builds go through render_compose.py on its own emulator, at font scale 1.0 and 2.0, with the
clock from the @Preview's name; the rest of this describes Swift.

For each <eval>/<config>/run-<n>/outputs it renders the run's Swift with scripts/render_swiftui.py
--platform ios, the same script for every config, and writes native.png and native-ax5.png. The status
bar shows the build's own clock:
  - the --clock HH:MM the build passed to its own renders, found in its response.md;
  - else the time in its #Preview's name ("Today, 09:20"), which render_swiftui.py reads itself;
  - else the wall clock, which render.txt then says.
When the Swift doesn't render, it falls back to the mock (screenshot.png, and fold.py --text-scale ax5
for mock-ax5.png). Each run's render.txt records which frames were used, the clock and its source, and the
bottom-edge lines render_swiftui.py printed. make_pairs.py reads native.png / native-ax5.png, or the
mock frames when those are missing.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def build_clock(outputs: Path) -> str | None:
    resp = outputs / "response.md"
    m = re.search(r"--clock\s+([01]?\d|2[0-3]):([0-5]\d)\b", resp.read_text(errors="ignore")) if resp.exists() else None
    return f"{m.group(1)}:{m.group(2)}" if m else None


def render(swift: list[Path], out: Path, size: str, clock: str | None) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(SCRIPTS / "render_swiftui.py"), *map(str, swift), "--platform", "ios",
           "--dynamic-type", size, "--out", str(out)] + (["--clock", clock] if clock else [])
    return subprocess.run(cmd, capture_output=True, text=True, timeout=900)


def render_kotlin(o: Path, fonts: str | None) -> list[str]:
    """Render one Kotlin build at both sizes, falling back to the mock as the Swift path does."""
    kt = sorted(o.glob("*.kt"))
    rc = Path(__file__).resolve().parent / "render_compose.py"
    a = subprocess.run([sys.executable, str(rc), *map(str, kt), "--out", str(o / "native.png")] + (["--fonts", fonts] if fonts else []),
                       capture_output=True, text=True, timeout=1200) if kt else None
    b = subprocess.run([sys.executable, str(rc), *map(str, kt), "--skip-build", "--font-scale", "2.0", "--out", str(o / "native-ax5.png")],
                       capture_output=True, text=True, timeout=300) if a and a.returncode == 0 else a
    if a and a.returncode == 0 and b.returncode == 0:
        lines = ["native (Android emulator, font scale 1.0 and 2.0)"]
        lines += [f"default {l[8:]}" for l in a.stdout.splitlines() if "status bar" in l or " text" in l or "CUT" in l]
        lines += [f"large {l[8:]}" for l in b.stdout.splitlines() if " text" in l or "CUT" in l]
        return lines
    if (o / "mock.html").exists():
        subprocess.run([sys.executable, str(SCRIPTS / "fold.py"), str(o / "mock.html"), "--text-scale", "android2",
                        "--shot", str(o / "mock-ax5.png")], capture_output=True, text=True, timeout=300)
    why = (a.stdout + a.stderr).strip().splitlines()[-3:] if a else ["no Kotlin"]
    return [f"mock (native render failed: {' / '.join(why)})"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("iteration")
    ap.add_argument("--eval", default="eval-*", help="glob for the eval folders to render")
    ap.add_argument("--fonts", help="Kotlin: a folder of font files for the R.font names a build doesn't ship")
    args = ap.parse_args()
    runs = sorted(Path(args.iteration).glob(f"{args.eval}/*/run-*/outputs"))
    if not runs:
        print("render_builds: no run outputs found")
        return 2
    for o in runs:
        if list(o.glob("*.kt")) and not list(o.glob("*.swift")):
            lines = render_kotlin(o, args.fonts)
            (o.parent / "render.txt").write_text("\n".join(lines) + "\n")
            print(f"{o.relative_to(args.iteration)}: " + " | ".join(lines))
            continue
        swift = sorted(o.glob("*.swift"))
        clock = build_clock(o)
        lines = []
        if swift:
            a = render(swift, o / "native.png", "large", clock)
            b = render(swift, o / "native-ax5.png", "ax5", clock) if a.returncode == 0 else a
            ok = a.returncode == 0 and b.returncode == 0
        else:
            ok = False
        if ok:
            status = re.search(r"status bar ([^,;]+(?: \(from the preview's name\))?)", a.stdout)
            source = "the build's --clock" if clock else ("the preview's name" if status and "preview" in status.group(1) else "none: wall clock")
            shown = status.group(1).replace(" (from the preview's name)", "") if status else "unknown"
            lines.append(f"native; clock {shown} (source: {source})")
            lines += [f"default {l[8:]}" for l in a.stdout.splitlines() if "bottom edge" in l or " CUT " in l]
            lines += [f"ax5 {l[8:]}" for l in b.stdout.splitlines() if "bottom edge" in l or " CUT " in l]
        else:
            if (o / "mock.html").exists():
                subprocess.run([sys.executable, str(SCRIPTS / "fold.py"), str(o / "mock.html"), "--text-scale", "ax5",
                                "--shot", str(o / "mock-ax5.png")], capture_output=True, text=True, timeout=300)
            why = "no Swift" if not swift else (a.stdout + a.stderr).strip().splitlines()[-1:] or ["?"]
            lines.append(f"mock (native render failed: {why if isinstance(why, str) else why[0]})")
        (o.parent / "render.txt").write_text("\n".join(lines) + "\n")
        print(f"{o.relative_to(args.iteration)}: " + " | ".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
