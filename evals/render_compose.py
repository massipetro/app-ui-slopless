#!/usr/bin/env python3
"""Render a Compose @Preview natively on an Android emulator, for the blind judges.

  python3 evals/render_compose.py <files.kt> --font-scale 2.0 --clock 09:20 --out large.png

Builds the Kotlin into a throwaway debug app (compose-render-app/) and opens the file's @Preview with
ui-tooling's PreviewActivity, on the system's own font scale, with the status bar set to the preview's
time (--clock, else a time in the @Preview's name, else the wall clock). It only ever talks to its own
emulator, on its own port (emulator-5600): started read-only and headless, so the AVD doesn't change,
and never one that's already running on this machine, which may be someone else's. --stop shuts it down.

It prints the first and last line of the visible text, from the accessibility tree (uiautomator), and
any element that runs past the bottom of the window ("CUT"). Exit 0: rendered. Exit 1: the code doesn't
build or has no @Preview. Exit 3: no emulator or SDK here.

Standard library only.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent / "compose-render-app"
WORK = Path.home() / ".cache" / "app-ui-slopless" / "compose-render"
PACKAGE = "dev.slopless.render"
SDK = Path(os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT") or Path.home() / "Library/Android/sdk")
ADB = str(SDK / "platform-tools" / "adb")
DEFAULT_AVD = "Medium_Phone_API_36.1"
PORT = "5600"
SERIAL = f"emulator-{PORT}"


def adb(*args: str, timeout: int = 60) -> str:
    return subprocess.run([ADB, "-s", SERIAL, *args], capture_output=True, text=True, timeout=timeout).stdout.strip()


def booted() -> bool:
    return adb("shell", "getprop", "sys.boot_completed") == "1"


def ensure_emulator(avd: str) -> bool:
    """Start this script's emulator when it isn't up. True when this call started it."""
    if booted():
        return False
    subprocess.Popen([str(SDK / "emulator" / "emulator"), "-avd", avd, "-port", PORT, "-read-only", "-gpu", "swiftshader_indirect", "-no-window", "-no-audio",
                      "-no-boot-anim", "-no-snapshot"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.time() + 300
    while time.time() < deadline:
        if booted():
            adb("shell", "settings", "put", "global", "hide_error_dialogs", "1")
            for key in ("window_animation_scale", "transition_animation_scale", "animator_duration_scale"):
                adb("shell", "settings", "put", "global", key, "0")
            time.sleep(30)  # a cold boot's System UI is slow to settle; this keeps its dialogs out of the shot
            return True
        time.sleep(3)
    raise TimeoutError("emulator did not boot in 5 minutes")


def find_preview(source: str) -> tuple[str, str | None] | None:
    """The first @Preview function's name, and a time in its name= if it has one."""
    for m in re.finditer(r"@Preview\b(\([^)]*\))?(?:\s*@[\w.]+(?:\([^)]*\))?)*\s*(?:(?:private|internal|public)\s+)?fun\s+(\w+)\s*\(\s*\)",
                         source):
        named = re.search(r"name\s*=\s*\"[^\"]*?\b([01]?\d|2[0-3]):([0-5]\d)\b", m.group(1) or "")
        return m.group(2), f"{named.group(1)}:{named.group(2)}" if named else None
    return None


def prepare(files: list[Path], fonts: Path | None) -> str | None:
    """Copy the code, its res/ folder and the fonts it names into the app. A missing font stops the render
    rather than falling back, so no build is judged in a typeface it didn't choose. Returns what's missing."""
    shutil.rmtree(WORK, ignore_errors=True)
    shutil.copytree(TEMPLATE, WORK)
    (WORK / "local.properties").write_text(f"sdk.dir={SDK}\n")
    src = WORK / "app" / "src" / "main" / "kotlin" / "generated"
    shutil.rmtree(src, ignore_errors=True)
    src.mkdir(parents=True)
    for f in files:
        shutil.copy(f, src / f.name)
    res = WORK / "app" / "src" / "main" / "res"
    built = files[0].parent / "res"
    if built.is_dir():
        shutil.copytree(built, res, dirs_exist_ok=True)
    source = "\n".join(f.read_text(errors="ignore") for f in files)
    names = sorted(set(re.findall(r"\bR\.font\.(\w+)", source)))
    (res / "font").mkdir(exist_ok=True)
    missing = []
    for n in names:
        if list((res / "font").glob(f"{n}.*")):
            continue
        given = next(iter(fonts.glob(f"{n}.*")), None) if fonts else None
        if given:
            shutil.copy(given, res / "font" / given.name)
        else:
            missing.append(n)
    return ", ".join(missing) or None


def bottom_cut(height: int) -> list[str]:
    """Visible text that runs past the bottom of the screen, and the first and last text on it."""
    adb("shell", "uiautomator", "dump", "/sdcard/ui.xml")
    xml = adb("shell", "cat", "/sdcard/ui.xml")
    lines: list[str] = []
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return ["bottom edge not measured"]
    texts: list[tuple[int, int, str]] = []
    for n in root.iter("node"):
        t = n.get("text") or n.get("content-desc") or ""
        m = re.findall(r"\d+", n.get("bounds", ""))
        if t and len(m) == 4:
            texts.append((int(m[1]), int(m[3]), t.replace("\n", " ")[:60]))
    if not texts:
        return ["bottom edge not measured"]
    texts.sort()
    lines.append(f"first text: {texts[0][2]}")
    lines.append(f"last text on screen: {texts[-1][2]}")
    lines += [f"CUT {t} (ends at {b} of {height})" for top, b, t in texts if b >= height and top < height]
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--font-scale", default="1.0")
    ap.add_argument("--clock", help="the status bar's time, HH:MM")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--stop", action="store_true", help="shut this script's emulator down and exit")
    ap.add_argument("--avd", default=DEFAULT_AVD)
    ap.add_argument("--fonts", type=Path, help="a folder of font files for the R.font names the build doesn't ship")
    ap.add_argument("--skip-build", action="store_true", help="reuse the app already installed from the same files")
    args = ap.parse_args()

    if args.stop:
        adb("emu", "kill")
        return 0
    if not args.files or not args.out:
        ap.error("files and --out are required")
    if not Path(ADB).exists() or not (SDK / "emulator" / "emulator").exists():
        print(f"render: no Android SDK with an emulator at {SDK}")
        return 3
    source = "\n".join(f.read_text(errors="ignore") for f in args.files)
    found = find_preview(source)
    if not found:
        print("render: no @Preview function with no parameters in these files")
        return 1
    name, named_clock = found
    clock = args.clock or named_clock
    holder = next(f for f in args.files if re.search(rf"\bfun\s+{name}\s*\(", f.read_text(errors="ignore")))
    pkg = re.search(r"^\s*package\s+([\w.]+)", holder.read_text(errors="ignore"), re.M)
    klass = f"{holder.stem[0].upper()}{holder.stem[1:]}Kt"
    target = f"{pkg.group(1)}.{klass}.{name}" if pkg else f"{klass}.{name}"

    env = {**os.environ, "ANDROID_HOME": str(SDK)}
    if not args.skip_build:
        missing = prepare(args.files, args.fonts)
        if missing:
            print(f"render: fonts not shipped and not in --fonts: {missing}")
            return 1
        r_import = re.search(r"^\s*import\s+([\w.]+)\.R\s*$", source, re.M)
        ns = [f"-Pslopless.namespace={r_import.group(1)}"] if r_import else []
        gradle = subprocess.run(["gradle", "--no-daemon", "-q", *ns, ":app:assembleDebug"], cwd=WORK, env=env,
                                capture_output=True, text=True, timeout=900)
        if gradle.returncode != 0:
            errors = [l for l in (gradle.stdout + gradle.stderr).splitlines() if l.startswith("e: ")]
            print("render: the code doesn't build\n" + "\n".join((errors or (gradle.stderr.splitlines()[-5:]))[:8]))
            return 1
    try:
        started = ensure_emulator(args.avd)
    except (TimeoutError, OSError) as e:
        print(f"render: {e}")
        return 3
    if started:
        print(f"render: started {args.avd} read-only")
    if not args.skip_build:
        adb("uninstall", PACKAGE)
        out = adb("install", "-t", str(WORK / "app/build/outputs/apk/debug/app-debug.apk"), timeout=180)
        if "Success" not in out:
            print(f"render: install failed: {out[:300]}")
            return 1

    was_scale = adb("shell", "settings", "get", "system", "font_scale")
    try:
        adb("shell", "settings", "put", "system", "font_scale", args.font_scale)
        adb("shell", "settings", "put", "global", "sysui_demo_allowed", "1")
        demo = ["shell", "am", "broadcast", "-a", "com.android.systemui.demo", "-e", "command"]
        adb(*demo, "enter")
        time.sleep(2)  # the commands below are dropped while demo mode is still starting
        if clock:
            hh, mm = clock.split(":")
            adb(*demo, "clock", "-e", "hhmm", f"{int(hh):02d}{mm}")
        adb(*demo, "battery", "-e", "level", "80", "-e", "plugged", "false")
        adb(*demo, "network", "-e", "wifi", "show", "-e", "level", "4")
        adb(*demo, "network", "-e", "mobile", "show", "-e", "datatype", "none", "-e", "level", "4")
        adb(*demo, "notifications", "-e", "visible", "false")
        adb("shell", "am", "force-stop", PACKAGE)
        started_at = adb("shell", "am", "start", "-W", "-n", f"{PACKAGE}/androidx.compose.ui.tooling.PreviewActivity",
                         "--es", "composable", target)
        if "Error" in started_at:
            print(f"render: {started_at[:300]}")
            return 1
        time.sleep(4)
        crash = adb("logcat", "-d", "-b", "crash", "-t", "20")
        if PACKAGE in crash:
            print("render: the preview crashed\n" + "\n".join(crash.splitlines()[-8:]))
            adb("logcat", "-b", "crash", "-c")
            return 1
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("wb") as fh:
            subprocess.run([ADB, "-s", SERIAL, "exec-out", "screencap", "-p"], stdout=fh, timeout=60)
        size = re.search(r"(\d+)x(\d+)", adb("shell", "wm", "size"))
        lines = bottom_cut(int(size.group(2)) if size else 2400)
        if any("isn't responding" in l for l in lines):
            print("render: a system dialog covered the screen")
            return 1
    finally:
        adb("shell", "settings", "put", "system", "font_scale", was_scale if was_scale not in ("", "null") else "1.0")
        adb("shell", "am", "broadcast", "-a", "com.android.systemui.demo", "-e", "command", "exit")
        adb("shell", "am", "force-stop", PACKAGE)
    print(f"render: {args.out} at font scale {args.font_scale}, status bar {clock or 'wall clock'}"
          + (" (from the preview's name)" if clock and not args.clock and named_clock else ""))
    for line in lines:
        print(f"render: {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
