#!/usr/bin/env python3
"""Typecheck SwiftUI files against the iOS simulator or macOS SDK, without an Xcode project.

  typecheck.py <file.swift or folder> [...] [--platform ios|macos] [--ios <target>] [--macos <target>]

The platform is read from --platform, else from the project (Package.swift platforms, or
SDKROOT / *_DEPLOYMENT_TARGET in the .xcodeproj), else from the code (AppKit, NSViewRepresentable,
MenuBarExtra, Settings {} mean macOS), else iOS.

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


def _vkey(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in v.split("."))


def project_target(files: list[Path], platform: str) -> tuple[str, str] | None:
    """The deployment target the project declares for `platform`, searching up from the first file."""
    start = files[0].resolve().parent
    spec = {"ios": (r"\.iOS\(", "IPHONEOS_DEPLOYMENT_TARGET"), "macos": (r"\.macOS\(", "MACOSX_DEPLOYMENT_TARGET")}[platform]
    for d in [start, *start.parents]:
        pkg = d / "Package.swift"
        if pkg.exists():
            m = re.search(spec[0] + r"\s*(?:\.v(\d+)(?:_(\d+))?|\"(\d+(?:\.\d+)?)\")", pkg.read_text(errors="ignore"))
            if m:
                ver = m.group(3) or (m.group(1) + "." + (m.group(2) or "0"))
                return ver, str(pkg)
        for proj in d.glob("*.xcodeproj/project.pbxproj"):
            vers = re.findall(spec[1] + r" = ([\d.]+);", proj.read_text(errors="ignore"))
            if vers:
                return min(vers, key=_vkey), str(proj)
        if (d / ".git").exists():
            break
    return None


MAC_MARKERS = re.compile(r"^\s*import\s+AppKit\b|\bNSViewRepresentable\b|\bNSWindow\b|\bNSApp\b|\bNSColor\b|\bNSImage\b"
                         r"|\bMenuBarExtra\b|\bSettings\s*\{|\.commands\s*\{|\.inspector\(|\bNavigationSplitView\b.*\.windowStyle", re.M)
IOS_MARKERS = re.compile(r"^\s*import\s+UIKit\b|\bUIViewRepresentable\b|\bUIColor\b|\bUIImage\b|\bUIApplication\b|\.navigationBarTitleDisplayMode\b|\.sensoryFeedback\b", re.M)


def detect_platform(files: list[Path]) -> tuple[str, str]:
    """(platform, why). Project declaration first, then the code."""
    start = files[0].resolve().parent
    for d in [start, *start.parents]:
        pkg = d / "Package.swift"
        if pkg.exists():
            txt = pkg.read_text(errors="ignore")
            has_ios, has_mac = ".iOS(" in txt, ".macOS(" in txt
            if has_mac and not has_ios:
                return "macos", f"{pkg} declares only macOS"
            if has_ios and not has_mac:
                return "ios", f"{pkg} declares only iOS"
        for proj in d.glob("*.xcodeproj/project.pbxproj"):
            txt = proj.read_text(errors="ignore")
            sdk = set(re.findall(r"SDKROOT = (\w+);", txt))
            has_ios, has_mac = "IPHONEOS_DEPLOYMENT_TARGET" in txt, "MACOSX_DEPLOYMENT_TARGET" in txt
            if "macosx" in sdk and not has_ios:
                return "macos", f"{proj} targets macOS"
            if has_mac and not has_ios:
                return "macos", f"{proj} targets macOS"
            if has_ios and not has_mac:
                return "ios", f"{proj} targets iOS"
        if (d / ".git").exists():
            break
    text = "\n".join(f.read_text(errors="ignore") for f in files)
    mac, ios = bool(MAC_MARKERS.search(text)), bool(IOS_MARKERS.search(text))
    if mac and not ios:
        return "macos", "the code uses AppKit / macOS-only APIs"
    return "ios", "default (nothing says macOS)"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--platform", choices=["ios", "macos"], help="SDK to check against; default: detected (see above)")
    ap.add_argument("--ios", help="iOS deployment target; default: the project's (Package.swift / .xcodeproj), else 17.0")
    ap.add_argument("--macos", help="macOS deployment target; default: the project's (Package.swift / .xcodeproj), else 14.0")
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

    if args.platform:
        platform, why = args.platform, "--platform"
    else:
        platform, why = detect_platform(files)
    if platform == "ios" and args.macos:
        print("typecheck: note: --macos given but the platform is iOS; pass --platform macos to check against macOS")
    if platform == "macos" and args.ios:
        print("typecheck: note: --ios given but the platform is macOS; ignoring it")

    sdk_name, label = ("macosx", "macOS") if platform == "macos" else ("iphonesimulator", "iOS")
    sdk = subprocess.run(["xcrun", "--sdk", sdk_name, "--show-sdk-path"], capture_output=True, text=True)
    if sdk.returncode != 0 or not sdk.stdout.strip():
        print(f"typecheck: not run, no {label} SDK (install Xcode{'' if platform == 'macos' else chr(39) + 's iOS platform'})")
        return 3

    imports = set()
    for f in files:
        imports |= set(re.findall(r"^\s*import\s+(\w+)", f.read_text(errors="ignore"), re.M))
    known = {"SwiftUI", "Foundation", "Observation", "Combine", "CoreGraphics", "CoreText", "MapKit", "Charts",
             "PhotosUI", "AVFoundation", "AVKit", "CoreHaptics", "CoreLocation", "OSLog", "os", "StoreKit", "WidgetKit",
             "Accessibility", "UniformTypeIdentifiers", "QuartzCore", "WebKit", "EventKit", "SwiftData",
             "UserNotifications", "ImageIO", "CoreImage"}
    known |= {"AppKit", "Carbon", "ServiceManagement", "QuickLook", "QuickLookUI"} if platform == "macos" else \
             {"UIKit", "ActivityKit", "SafariServices"}
    foreign = sorted(imports - known)
    if foreign:
        print(f"typecheck: note: imports outside the SDK ({', '.join(foreign)}) will fail to resolve here")

    declared = project_target(files, platform)
    fallback = "14.0" if platform == "macos" else "17.0"
    default_target, source = declared if declared else (fallback, "skill default; no project target found")
    flag = args.macos if platform == "macos" else args.ios
    flag_name = "--macos" if platform == "macos" else "--ios"
    if flag and flag != default_target:
        print(f"typecheck: note: {flag_name} {flag} overrides the deployment target {default_target} ({source}). "
              "Only do this if the project really targets it, and say so in the report; "
              "otherwise keep the target and wrap newer APIs in `if #available`.")
    target = flag or default_target
    print(f"typecheck: platform {label} ({why}), deployment target {label} {target}"
          + ("" if target != default_target else f" ({source})"))

    arch = "arm64" if subprocess.run(["uname", "-m"], capture_output=True, text=True).stdout.strip() == "arm64" else "x86_64"
    triple = f"{arch}-apple-macos{target}" if platform == "macos" else f"{arch}-apple-ios{target}-simulator"
    # -emit-sil, not -typecheck: the SIL passes are where errors like a missing return in a getter show
    # (round 20 found one that -typecheck passed). It still emits nothing to disk.
    cmd = ["xcrun", "--sdk", sdk_name, "swiftc", "-emit-sil", "-o", "/dev/null", "-target", triple, "-sdk", sdk.stdout.strip()]
    if not any(f.name == "main.swift" for f in files):
        cmd.append("-parse-as-library")  # a lone file with @main is otherwise parsed as top-level code
    cmd += map(str, files)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    errors = [l for l in proc.stderr.splitlines() if re.search(r":\d+:\d+: error:", l)]
    for line in errors:
        print(line)
    status = "pass" if proc.returncode == 0 and not errors else "FAIL"
    print(f"typecheck {status}: {len(files)} file(s), {len(errors)} error(s), {label} {target} {'SDK' if platform == 'macos' else 'simulator SDK'}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
