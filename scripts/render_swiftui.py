#!/usr/bin/env python3
"""Render a macOS SwiftUI screen natively, from its #Preview, to a PNG: no Xcode project.

  render_swiftui.py <file.swift or folder> [...] --out screen.png [--size 1280x800] [--scale 2]
                    [--appearance light|dark] [--preview <index or name>] [--locale en_US] [--macos 14.0]

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
iOS screens aren't rendered yet: use the HTML mock and say so.

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
    args = ap.parse_args()

    files = []
    for p in map(Path, args.paths):
        files += sorted(p.rglob("*.swift")) if p.is_dir() else [p]
    if not files:
        print("render: no .swift files")
        return 2
    if not shutil.which("xcrun"):
        print("render: not rendered natively, no Xcode toolchain here")
        return 3
    sdk = subprocess.run(["xcrun", "--sdk", "macosx", "--show-sdk-path"], capture_output=True, text=True).stdout.strip()
    if not sdk:
        print("render: not rendered natively, no macOS SDK here")
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


if __name__ == "__main__":
    sys.exit(main())
