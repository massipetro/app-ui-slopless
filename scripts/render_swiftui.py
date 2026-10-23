#!/usr/bin/env python3
"""Render a SwiftUI screen natively, from its #Preview, to a PNG: no Xcode project.

  render_swiftui.py <file.swift or folder> [...] --out screen.png [--size 1280x800] [--scale 2]
                    [--appearance light|dark] [--preview <index or name>] [--locale en_US] [--macos 14.0]
                    [--platform macos|ios] [--dynamic-type large|ax1..ax5|xSmall..xxxLarge] [--device "iPhone 17 Pro"] [--ios 17.0]

macOS (the default): a real window, as below. iOS (--platform ios): the preview is built into a small
app for the iOS Simulator, launched on an iPhone simulator (booted if none is, and left running) and
screenshotted, status bar and all. --dynamic-type sets the text size the screen sees (ax5 is the largest
accessibility size, about 3x body text), so a layout that clips, truncates or overlaps at large text
shows in the image. macOS has no Dynamic Type: Apple documents that the dynamicTypeSize environment
value "does not affect the text size" there, and a render with it is identical (measured on macOS 26),
so --dynamic-type is refused for a Mac render; render an in-app zoom by passing the zoom factor in your
own preview instead.

The HTML mock is a hand-written copy of the screen; this renders the code itself. It takes the
body of a #Preview (the first, or --preview), compiles every file together with a small host
against the macOS SDK, shows the view in a window whose content is --size points, lets it settle
for a moment, and captures the window: title bar, toolbar, sidebar materials and all. Truncation,
real fonts and real controls show as they are, which the mock can hide. The window opens behind
your other windows for about two seconds and never takes focus, so its traffic lights are grey.
Without a window server (no GUI session) it draws the content offscreen instead, and translucent
materials come out flat.

The #Preview must build the view with its sample data (that's what previews are for). Fonts that
ship next to the code (.ttf/.otf/.ttc in its folders, a Fonts folder included, or --fonts) are
registered first, as the app's bundle would; any name passed to Font.custom that still isn't
available is named, because the render then shows the system font in its place. Files
are copied first: #Preview blocks and @main are removed from the copies, never from yours.

Without a #Preview it falls back to the app's WindowGroup content, then to a root view named
like its file with no arguments, and says which it used.

Exit 0: rendered. Exit 1: it didn't compile or didn't render (the first errors are printed;
this compiles fully, so it also catches errors `-typecheck` misses, like a missing return).
Exit 2: nothing to render. Exit 3: no Xcode toolchain here (say "not rendered natively").
Exit 3 on iOS also means no iOS Simulator runtime or iPhone device here.

Standard library only; works on Python 3.9.
"""
from __future__ import annotations

import argparse
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HOST = """import SwiftUI
import AppKit
import CoreText

@main
struct RenderHost {
    @MainActor static func main() {
        let a = CommandLine.arguments
        let size = NSSize(width: Double(a[2])!, height: Double(a[3])!)
        let app = NSApplication.shared
        app.setActivationPolicy(.accessory)
        // The fonts that ship next to the code, registered for this process the way the app's bundle would.
        let env = ProcessInfo.processInfo.environment
        for path in (env["RENDER_FONTS"] ?? "").split(separator: "\\n") {
            CTFontManagerRegisterFontsForURL(URL(fileURLWithPath: String(path)) as CFURL, .process, nil)
        }
        for name in (env["RENDER_FONT_NAMES"] ?? "").split(separator: "\\n").map(String.init)
        where NSFont(name: name, size: 12) == nil && NSFontManager.shared.availableMembers(ofFontFamily: name) == nil {
            print("render: font '\\(name)' not available, the system font is shown in its place")
        }
        // A real window behind the others, so the window server draws materials, the title bar and the
        // toolbar as the app would show them. It never takes focus, so the traffic lights are inactive.
        let window = NSWindow(contentRect: NSRect(origin: NSPoint(x: 40, y: 40), size: size),
                              styleMask: [.titled, .closable, .miniaturizable, .resizable],
                              backing: .buffered, defer: false)
        window.appearance = NSAppearance(named: a[4] == "dark" ? .darkAqua : .aqua)
        let host = NSHostingView(rootView: __previewBody().frame(width: size.width, height: size.height))
        window.contentView = host
        window.orderBack(nil)
        RunLoop.main.run(until: Date().addingTimeInterval(1.5))   // onAppear, tasks and one-off animations settle
        var rep: NSBitmapImageRep?
        var how = "window"
        if let cg = CGWindowListCreateImage(.null, .optionIncludingWindow, CGWindowID(window.windowNumber),
                                            [.boundsIgnoreFraming, .bestResolution]), cg.width > 1 {
            rep = NSBitmapImageRep(cgImage: cg)
        } else if let r = host.bitmapImageRepForCachingDisplay(in: host.bounds) {
            // No window server to capture from: draw the content offscreen (materials come out flat).
            host.cacheDisplay(in: host.bounds, to: r)
            rep = r
            how = "offscreen, materials flat"
        }
        guard let png = rep?.representation(using: NSBitmapImageRep.FileType.png, properties: [:]) else { print("render: no image"); exit(1) }
        do { try png.write(to: URL(fileURLWithPath: a[1])) } catch { print("render: \\(error)"); exit(1) }
        print("render: \\(rep!.pixelsWide)x\\(rep!.pixelsHigh) px (\\(how))")
        exit(0)
    }
}
"""


HOST_IOS = """import SwiftUI
import CoreText

@main
struct RenderHostApp: App {
    init() {
        for url in Bundle.main.urls(forResourcesWithExtension: nil, subdirectory: "Fonts") ?? [] {
            CTFontManagerRegisterFontsForURL(url as CFURL, .process, nil)
        }
    }
    var body: some Scene {
        WindowGroup {
            let a = ProcessInfo.processInfo.arguments
            let size = Self.size(a.first(where: { $0.hasPrefix("--dt=") }).map { String($0.dropFirst(5)) } ?? "large")
            __previewBody()
                .environment(\\.dynamicTypeSize, size)
                .preferredColorScheme(a.contains("--dark") ? .dark : .light)
        }
    }
    static func size(_ s: String) -> DynamicTypeSize {
        switch s {
        case "xSmall": return .xSmall
        case "small": return .small
        case "medium": return .medium
        case "xLarge": return .xLarge
        case "xxLarge": return .xxLarge
        case "xxxLarge": return .xxxLarge
        case "ax1": return .accessibility1
        case "ax2": return .accessibility2
        case "ax3": return .accessibility3
        case "ax4": return .accessibility4
        case "ax5": return .accessibility5
        default: return .large
        }
    }
}
"""

PLIST = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>CFBundleIdentifier</key><string>{bundle}</string>
<key>CFBundleExecutable</key><string>Render</string>
<key>CFBundleName</key><string>Render</string>
<key>CFBundlePackageType</key><string>APPL</string>
<key>CFBundleShortVersionString</key><string>1.0</string>
<key>CFBundleVersion</key><string>1</string>
<key>MinimumOSVersion</key><string>{ios}</string>
<key>UIDeviceFamily</key><array><integer>1</integer><integer>2</integer></array>
<key>UILaunchScreen</key><dict/>
<key>UIApplicationSceneManifest</key><dict><key>UIApplicationSupportsMultipleScenes</key><true/></dict>
{fonts}</dict></plist>
"""

SIZES = ("xSmall", "small", "medium", "large", "xLarge", "xxLarge", "xxxLarge", "ax1", "ax2", "ax3", "ax4", "ax5")


def previews(src: str) -> list[tuple[int, int, str, str]]:
    """(start, end, name, body) for every #Preview block, matching braces."""
    out = []
    for m in re.finditer(r"#Preview\s*(\(([^)]*)\))?\s*\{", src):
        i, depth = m.end(), 1
        while depth and i < len(src):
            depth += (src[i] == "{") - (src[i] == "}")
            i += 1
        name = re.search(r'"([^"]*)"', m.group(2) or "")
        out.append((m.start(), i, name.group(1) if name else "", src[m.end():i - 1]))
    return out


def font_files(files: list[Path], extra: list[str]) -> list[Path]:
    """Font files next to the code (in its folders, a Fonts folder included) and in any --fonts folder."""
    skip = {".build", "DerivedData", "node_modules", ".git", "Pods"}
    roots = {f.parent for f in files} | {Path(d) for d in extra}
    found = []
    for root in roots:
        found += [f for f in root.rglob("*") if f.suffix.lower() in (".ttf", ".otf", ".ttc") and not skip & set(f.parts)]
    return sorted(set(found))[:80]


def font_names(files: list[Path]) -> list[str]:
    """The names passed to Font.custom / NSFont(name:): string literals, and constants that hold one."""
    src = "\n".join(f.read_text(errors="ignore") for f in files)
    names = set(re.findall(r'(?:\.custom|NSFont)\(\s*(?:name:\s*)?"([^"]+)"', src))
    for ident in set(re.findall(r'(?:\.custom|NSFont)\(\s*(?:name:\s*)?([A-Za-z_][\w.]*)\s*[,)]', src)):
        m = re.search(rf'\b(?:let|var)\s+{re.escape(ident.split(".")[-1])}\s*(?::\s*String)?\s*=\s*"([^"]+)"', src)
        if m:
            names.add(m.group(1))
    return sorted(names)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--out", required=True, help="PNG to write")
    ap.add_argument("--size", default="1280x800", help="window content size in points")
    ap.add_argument("--scale", type=int, default=2, help="backing scale (2 = Retina)")
    ap.add_argument("--appearance", choices=["light", "dark"], default="light")
    ap.add_argument("--preview", default="0", help="which #Preview: an index (default 0) or its name")
    ap.add_argument("--locale", default="en_US", help="process locale, so number and date formats are stable")
    ap.add_argument("--macos", default="14.0", help="deployment target")
    ap.add_argument("--fonts", action="append", default=[], help="another folder of .ttf/.otf files to register (repeatable)")
    ap.add_argument("--platform", choices=["macos", "ios"], default="macos", help="macos: a real window (default); ios: the iOS Simulator")
    ap.add_argument("--dynamic-type", default="large", help="iOS only: " + ", ".join(SIZES) + " (ax5 = the largest)")
    ap.add_argument("--device", default="", help="iOS only: simulator name or UDID (default: a booted iPhone, else the newest iPhone)")
    ap.add_argument("--ios", default="17.0", help="iOS deployment target")
    args = ap.parse_args()
    if args.dynamic_type not in SIZES:
        print(f"render: --dynamic-type is one of {', '.join(SIZES)}")
        return 2
    if args.platform == "macos" and args.dynamic_type != "large":
        print("render: macOS has no Dynamic Type (the environment value doesn't change text size there), so a Mac render "
              "can't show it. Render the iOS screen with --platform ios, or your in-app zoom from a #Preview that applies it.")
        return 2

    files = []
    for p in map(Path, args.paths):
        files += sorted(p.rglob("*.swift")) if p.is_dir() else [p]
    if not files:
        print("render: no .swift files")
        return 2
    if not shutil.which("xcrun"):
        print("render: not rendered natively, no Xcode toolchain here")
        return 3
    sdk_name = "iphonesimulator" if args.platform == "ios" else "macosx"
    sdk = subprocess.run(["xcrun", "--sdk", sdk_name, "--show-sdk-path"], capture_output=True, text=True).stdout.strip()
    if not sdk:
        print(f"render: not rendered natively, no {sdk_name} SDK here")
        return 3

    found = [(f, *pv) for f in files for pv in previews(f.read_text(errors="ignore"))]
    if not found:
        # No #Preview: try the app's WindowGroup content, then a root view named like its file.
        for f in files:
            src = f.read_text(errors="ignore")
            for m in re.finditer(r"WindowGroup\s*(\([^)]*\))?\s*\{", src):
                i, depth = m.end(), 1
                while depth and i < len(src):
                    depth += (src[i] == "{") - (src[i] == "}")
                    i += 1
                found.append((f, 0, 0, "the app's WindowGroup", src[m.end():i - 1]))
            if re.search(rf"struct\s+{re.escape(f.stem)}\s*:\s*View\b", src):
                found.append((f, 0, 0, f"{f.stem}()", f" {f.stem}() "))
    if not found:
        print("render: no #Preview in these files; add one that builds the screen with its sample data")
        return 2
    pick = next((x for x in found if x[3] == args.preview), None)
    if pick is None:
        if not args.preview.isdigit() or int(args.preview) >= len(found):
            print(f"render: no #Preview {args.preview!r}; have {[x[3] or i for i, x in enumerate(found)]}")
            return 2
        pick = found[int(args.preview)]
    # Without a #Preview, try each fallback until one compiles.
    candidates = [pick] + [x for x in found if x is not pick and x[1] == x[2] == 0 and pick[1] == pick[2] == 0]
    for pick in candidates:
        code = render(files, pick, found, args)
        if code != 1 or pick is candidates[-1]:
            return code
    return 1


def render(files: list[Path], pick: tuple, found: list, args: argparse.Namespace) -> int:
    if args.platform == "ios":
        return render_ios(files, pick, found, args)
    sdk = subprocess.run(["xcrun", "--sdk", "macosx", "--show-sdk-path"], capture_output=True, text=True).stdout.strip()

    work = Path(tempfile.mkdtemp(prefix="render-swiftui-"))
    try:
        sources = []
        for n, f in enumerate(files):
            src = f.read_text(errors="ignore")
            for start, end, _, _ in reversed(previews(src)):
                src = src[:start] + src[end:]
            src = re.sub(r"(?m)^(\s*)@main\b", r"\1", src)
            if f == pick[0]:   # the preview may use this file's private types, so it lives in the same file
                src += "\n\n@MainActor @ViewBuilder func __previewBody() -> some View {" + pick[4] + "}\n"
            dst = work / f"{n:02d}-{f.name}"
            dst.write_text(src)
            sources.append(str(dst))
        (work / "zz-host.swift").write_text(HOST)
        binary = work / "render"
        arch = "arm64" if platform.machine() == "arm64" else "x86_64"
        build = subprocess.run(["xcrun", "--sdk", "macosx", "swiftc", "-Onone", "-parse-as-library",
                                "-target", f"{arch}-apple-macos{args.macos}", "-sdk", sdk,
                                *sources, str(work / "zz-host.swift"), "-o", str(binary),
                                # AVKit and friends load lazily; link them so a player view resolves at run time
                                "-framework", "AVKit", "-framework", "AVFoundation"],
                               capture_output=True, text=True, timeout=600)
        if build.returncode != 0:
            errors = [l for l in build.stderr.splitlines() if "error:" in l][:5]
            print("render: didn't compile\n  " + "\n  ".join(errors or build.stderr.splitlines()[-5:]))
            return 1
        w, h = (int(v) for v in args.size.lower().split("x"))
        lang = args.locale.split("_")[0]
        fonts = font_files(files, args.fonts)
        run = subprocess.run([str(binary), str(Path(args.out).resolve()), str(w), str(h), args.appearance,
                              "-AppleLocale", args.locale, "-AppleLanguages", f"({lang})"],
                             capture_output=True, text=True, timeout=120,
                             env={"PATH": "/usr/bin:/bin", "LANG": f"{args.locale}.UTF-8",
                                  "CG_CONTEXT_SHOW_BACKTRACE": "0",
                                  "RENDER_FONTS": "\n".join(map(str, fonts)),
                                  "RENDER_FONT_NAMES": "\n".join(font_names(files))})
        if run.returncode != 0 or not Path(args.out).exists():
            print("render: didn't render\n  " + (run.stdout + run.stderr).strip()[-400:])
            return 1
        if args.scale != 2:
            subprocess.run(["sips", "-z", str(h * args.scale), str(w * args.scale), args.out], capture_output=True)
        for line in run.stdout.splitlines():
            if "not available" in line:
                print(line)
        label = pick[3] if pick[1] == pick[2] == 0 else f"#Preview {pick[3] or found.index(pick)!r}"
        print(f"render: {Path(args.out).name} from {label} in {pick[0].name}, {w}x{h} pt, {args.appearance}, {args.locale}"
              + (f", {len(fonts)} font file(s) registered" if fonts else ""))
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


def sources_for(files: list[Path], pick: tuple, work: Path) -> list[str]:
    """Copies with #Preview blocks and @main removed; the picked preview's body becomes __previewBody()."""
    sources = []
    for n, f in enumerate(files):
        src = f.read_text(errors="ignore")
        for start, end, _, _ in reversed(previews(src)):
            src = src[:start] + src[end:]
        src = re.sub(r"(?m)^(\s*)@main\b", r"\1", src)
        if f == pick[0]:
            src += "\n\n@MainActor @ViewBuilder func __previewBody() -> some View {" + pick[4] + "}\n"
        dst = work / f"{n:02d}-{f.name}"
        dst.write_text(src)
        sources.append(str(dst))
    return sources


def simulator(want: str) -> tuple[str, str] | None:
    """(udid, name) of the iPhone to render on: the one named, a booted iPhone, else the newest one."""
    import json
    out = subprocess.run(["xcrun", "simctl", "list", "devices", "available", "-j"], capture_output=True, text=True).stdout
    try:
        runtimes = json.loads(out)["devices"]
    except (ValueError, KeyError):
        return None
    phones = []
    for rt, devs in runtimes.items():
        if "iOS" not in rt:
            continue
        ver = tuple(int(x) for x in re.findall(r"\d+", rt.split("iOS")[-1])[:2])
        phones += [(ver, d) for d in devs if "iPhone" in d["name"]]
    if want:
        hit = [d for _, d in phones if want in (d["udid"], d["name"])]
        return (hit[0]["udid"], hit[0]["name"]) if hit else None
    booted = [d for _, d in phones if d["state"] == "Booted"]
    if booted:
        return booted[0]["udid"], booted[0]["name"]
    phones.sort(key=lambda p: (p[0], "Pro" in p[1]["name"] and "Max" not in p[1]["name"]), reverse=True)
    return (phones[0][1]["udid"], phones[0][1]["name"]) if phones else None


def render_ios(files: list[Path], pick: tuple, found: list, args: argparse.Namespace) -> int:
    import fcntl
    import os
    import time
    sdk = subprocess.run(["xcrun", "--sdk", "iphonesimulator", "--show-sdk-path"], capture_output=True, text=True).stdout.strip()
    dev = simulator(args.device)
    if not dev:
        print("render: not rendered natively, no iPhone simulator here (Xcode > Settings > Components adds one)")
        return 3
    udid, name = dev
    work = Path(tempfile.mkdtemp(prefix="render-swiftui-ios-"))
    bundle = f"dev.slopless.render.p{os.getpid()}"
    try:
        sources = sources_for(files, pick, work)
        (work / "zz-host.swift").write_text(HOST_IOS)
        app = work / "Render.app"
        (app / "Fonts").mkdir(parents=True)
        fonts = font_files(files, args.fonts)
        for f in fonts:
            shutil.copy(f, app / "Fonts" / f.name)
        listed = "".join(f"<string>Fonts/{f.name}</string>" for f in fonts)
        (app / "Info.plist").write_text(PLIST.format(bundle=bundle, ios=args.ios,
                                                      fonts=f"<key>UIAppFonts</key><array>{listed}</array>\n" if fonts else ""))
        arch = "arm64" if platform.machine() == "arm64" else "x86_64"
        build = subprocess.run(["xcrun", "--sdk", "iphonesimulator", "swiftc", "-Onone", "-parse-as-library",
                                "-target", f"{arch}-apple-ios{args.ios}-simulator", "-sdk", sdk,
                                *sources, str(work / "zz-host.swift"), "-o", str(app / "Render")],
                               capture_output=True, text=True, timeout=600)
        if build.returncode != 0:
            errors = [l for l in build.stderr.splitlines() if "error:" in l][:5]
            print("render: didn't compile for the iOS Simulator\n  " + "\n  ".join(errors or build.stderr.splitlines()[-5:]))
            return 1
        lock_path = Path.home() / ".cache" / "app-ui-slopless" / "simulator.lock"
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with open(lock_path, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)   # one render at a time owns the simulator's screen
            subprocess.run(["xcrun", "simctl", "boot", udid], capture_output=True, text=True)
            subprocess.run(["xcrun", "simctl", "bootstatus", udid, "-b"], capture_output=True, text=True, timeout=300)
            inst = subprocess.run(["xcrun", "simctl", "install", udid, str(app)], capture_output=True, text=True, timeout=120)
            if inst.returncode != 0:
                print("render: didn't install on the simulator\n  " + inst.stderr.strip()[-300:])
                return 1
            lang = args.locale.split("_")[0]
            launch = ["xcrun", "simctl", "launch", "--terminate-running-process", udid, bundle,
                      "-AppleLocale", args.locale, "-AppleLanguages", f"({lang})", f"--dt={args.dynamic_type}"]
            if args.appearance == "dark":
                launch.append("--dark")
            run = subprocess.run(launch, capture_output=True, text=True, timeout=120)
            if run.returncode != 0:
                print("render: didn't launch\n  " + run.stderr.strip()[-300:])
                return 1
            time.sleep(2.5)   # onAppear, tasks and one-off animations settle
            shot = subprocess.run(["xcrun", "simctl", "io", udid, "screenshot", "--type=png", str(Path(args.out).resolve())],
                                  capture_output=True, text=True, timeout=60)
            subprocess.run(["xcrun", "simctl", "terminate", udid, bundle], capture_output=True)
            subprocess.run(["xcrun", "simctl", "uninstall", udid, bundle], capture_output=True)
        if shot.returncode != 0 or not Path(args.out).exists():
            print("render: no screenshot\n  " + shot.stderr.strip()[-300:])
            return 1
        label = pick[3] if pick[1] == pick[2] == 0 else f"#Preview {pick[3] or found.index(pick)!r}"
        print(f"render: {Path(args.out).name} from {label} in {pick[0].name}, iOS Simulator ({name}), Dynamic Type "
              f"{args.dynamic_type}, {args.appearance}, {args.locale}" + (f", {len(fonts)} font file(s) bundled" if fonts else "")
              + "; the simulator is left booted")
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
