#!/usr/bin/env python3
"""Typecheck SwiftUI files against the iOS simulator SDK, without an Xcode project.

  typecheck.py <file.swift or folder> [...] [--ios <target>]

All files are checked together as one module, so types shared between files resolve.
Exit 0: no errors. Exit 1: errors (printed as file:line: message). Exit 3: no Xcode
toolchain here (say "not compiled" in the report; don't claim a pass).

This catches what a reader can't: actor-isolation errors, wrong API shapes, missing
availability checks for the deployment target, and expressions the type checker gives
up on. It does not link, run, or check package dependencies; files that import third-party
modules can't be typechecked this way.

Standard library only; works on Python 3.9.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


def project_target(files: list[Path]) -> tuple[str, str] | None:
    """The iOS deployment target the project declares, searching up from the first file."""
    start = files[0].resolve().parent
    for d in [start, *start.parents]:
        pkg = d / "Package.swift"
        if pkg.exists():
            m = re.search(r"\.iOS\(\s*(?:\.v(\d+)(?:_(\d+))?|\"(\d+(?:\.\d+)?)\")", pkg.read_text(errors="ignore"))
            if m:
                ver = m.group(3) or (m.group(1) + "." + (m.group(2) or "0"))
                return ver, str(pkg)
        for proj in d.glob("*.xcodeproj/project.pbxproj"):
            vers = re.findall(r"IPHONEOS_DEPLOYMENT_TARGET = ([\d.]+);", proj.read_text(errors="ignore"))
            if vers:
                return min(vers, key=lambda v: tuple(int(x) for x in v.split("."))), str(proj)
        if (d / ".git").exists():
            break
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--ios", help="deployment target; default: the project's (Package.swift / .xcodeproj), else 17.0")
    args = ap.parse_args()

    files = []
    for p in map(Path, args.paths):
        if p.is_dir():
            files += sorted(f for f in p.rglob("*.swift") if ".build" not in f.parts and "Tests" not in f.parts)
        elif p.suffix == ".swift":
            files.append(p)
    if not files:
        print("typecheck: no .swift files given")
        return 2

    if not shutil.which("xcrun"):
        print("typecheck: not run, no Xcode toolchain (xcrun) on this machine")
        return 3
    sdk = subprocess.run(["xcrun", "--sdk", "iphonesimulator", "--show-sdk-path"], capture_output=True, text=True)
    if sdk.returncode != 0 or not sdk.stdout.strip():
        print("typecheck: not run, no iOS simulator SDK (install Xcode's iOS platform)")
        return 3

    imports = set()
    for f in files:
        imports |= set(re.findall(r"^\s*import\s+(\w+)", f.read_text(errors="ignore"), re.M))
    foreign = sorted(imports - {"SwiftUI", "Foundation", "UIKit", "Observation", "Combine", "CoreGraphics",
                                "CoreText", "MapKit", "Charts", "PhotosUI", "AVFoundation", "AVKit", "CoreHaptics",
                                "CoreLocation", "OSLog", "os", "StoreKit", "WidgetKit", "ActivityKit", "Accessibility",
                                "UniformTypeIdentifiers", "QuartzCore", "SafariServices", "WebKit", "EventKit"})
    if foreign:
        print(f"typecheck: note: imports outside the SDK ({', '.join(foreign)}) will fail to resolve here")

    declared = project_target(files)
    default_ios, source = declared if declared else ("17.0", "skill default; no project target found")
    if args.ios and args.ios != default_ios:
        print(f"typecheck: note: --ios {args.ios} overrides the deployment target {default_ios} ({source}). "
              "Only do this if the project really targets it, and say so in the report; "
              "otherwise keep the target and wrap newer APIs in `if #available`.")
    args.ios = args.ios or default_ios
    print(f"typecheck: deployment target iOS {args.ios}" + ("" if args.ios != default_ios else f" ({source})"))

    arch = "arm64" if subprocess.run(["uname", "-m"], capture_output=True, text=True).stdout.strip() == "arm64" else "x86_64"
    cmd = ["xcrun", "--sdk", "iphonesimulator", "swiftc", "-typecheck",
           "-target", f"{arch}-apple-ios{args.ios}-simulator", "-sdk", sdk.stdout.strip(), *map(str, files)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    errors = [l for l in proc.stderr.splitlines() if re.search(r":\d+:\d+: error:", l)]
    for line in errors:
        print(line)
    status = "pass" if proc.returncode == 0 and not errors else "FAIL"
    print(f"typecheck {status}: {len(files)} file(s), {len(errors)} error(s), iOS {args.ios} simulator SDK")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
