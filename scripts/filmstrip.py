#!/usr/bin/env python3
"""Turn motion into one still image a model can read: a filmstrip of frames.

  filmstrip.py mock.html [--hash play] [--times 0,60,120,180,240,320,480,800]
                         [--crop auto|full|x,y,w,h] [--scheme light|dark|system]
                         [--size 390x844] [--out filmstrip.png]
  filmstrip.py frame-01.png frame-02.png ... [--out filmstrip.png]

HTML mock: every frame is the mock with all CSS animations and transitions paused at
time t (the Web Animations API), so frames are exact, not sampled. Open the mock with
`--hash play` to start the motion under test on load (the mock's own `#play` handler).
Only CSS / Web Animations can be stepped; motion driven by requestAnimationFrame or
timers shows as "0 animations". The strip's header and stdout give the measured facts:
how many animations, the longest finite one in ms, and how many loop forever.
By default the frames are cropped to the area that moves (`--crop auto`: the union of the
animated elements' boxes over their run, preferring the triggered motion over loops), and
rendered in light mode (`--scheme`), whatever the machine's own setting.

PNG frames (from a Compose test with a paused clock, or a simulator recording split
with ffmpeg): tiles them in order, labelled with the file names.

Needs a Chromium-based browser to take the screenshot (Chrome, Chromium, Edge, Brave,
or Playwright's Chromium; or set CHROME=/path). Without one it writes the strip as HTML,
prints how to screenshot it, and exits 3: say "motion not recorded" in the report.

Standard library only; works on Python 3.9.
"""
from __future__ import annotations

import argparse
import glob
import html
import json
import os
import re
import shutil
import struct
import subprocess
import sys
from pathlib import Path

FREEZE = """<script>/* filmstrip.py: pause every animation at ?t=<ms> */(function () {
  var m = location.search.match(/[?&]t=(\\d+)/); if (!m) return;
  var t = +m[1];
  function freeze() {
    var anims = document.getAnimations(), longest = 0, loops = 0;
    anims.forEach(function (a) {
      var tm = a.effect && a.effect.getComputedTiming();
      if (tm) { if (tm.endTime === Infinity) loops++; else longest = Math.max(longest, tm.endTime); }
      a.pause(); a.currentTime = t;
    });
    var out = { n: anims.length, longest: Math.round(longest), loops: loops };
    if (/[?&]measure=1/.test(location.search)) {   // where does it move? union of boxes over the run
      var boxes = { finite: null, all: null };
      var grow = function (k, r) {
        if (r.width < 1 || r.height < 1) return;
        var b = boxes[k];
        boxes[k] = b ? [Math.min(b[0], r.left), Math.min(b[1], r.top), Math.max(b[2], r.right), Math.max(b[3], r.bottom)]
                     : [r.left, r.top, r.right, r.bottom];
      };
      anims.forEach(function (a) {
        var el = a.effect && a.effect.target; if (!el || !el.getBoundingClientRect) return;
        var tm = a.effect.getComputedTiming(), loop = tm.endTime === Infinity;
        var span = loop ? (tm.duration || 1000) : tm.endTime;
        [0, .25, .5, .75, 1].forEach(function (f) {
          a.currentTime = Math.max(0, span * f - (f === 1 ? 1 : 0));
          var r = el.getBoundingClientRect();
          grow('all', r); if (!loop) grow('finite', r);
        });
        a.currentTime = t;
      });
      out.box = boxes.finite || boxes.all;
    }
    document.documentElement.setAttribute('data-filmstrip', JSON.stringify(out));
  }
  addEventListener('load', function () { freeze(); requestAnimationFrame(function () { requestAnimationFrame(freeze); }); });
})();</script>"""

SHEET = """<!doctype html><meta charset="utf-8"><style>
  html, body {{ margin: 0; background: #e9e7e2; font: 13px/1.3 -apple-system, system-ui, sans-serif; color: #1b1a17; }}
  #head {{ padding: 10px {gap}px 0; font-weight: 600; }}
  #grid {{ display: grid; grid-template-columns: repeat({cols}, {cw}px); gap: {gap}px; padding: {gap}px; }}
  .cell {{ display: flex; flex-direction: column; gap: 4px; }}
  .clip {{ width: {cw}px; height: {ch}px; overflow: hidden; position: relative; background: #fff; outline: 1px solid #0003; }}
  .clip iframe {{ position: absolute; border: 0; transform-origin: 0 0; }}
  .clip img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
  .cap {{ font-variant-numeric: tabular-nums; }}
</style>
<div id="head">{head}</div>
<div id="grid">{cells}</div>
"""


def find_chrome() -> str | None:
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    home = str(Path.home())
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        *sorted(glob.glob(home + "/Library/Caches/ms-playwright/chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium"), reverse=True),
        *sorted(glob.glob(home + "/Library/Caches/ms-playwright/chromium-*/chrome-mac*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"), reverse=True),
        *sorted(glob.glob(home + "/.cache/ms-playwright/chromium-*/chrome-linux*/chrome"), reverse=True),
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    for name in ("google-chrome", "chromium", "chromium-browser", "microsoft-edge"):
        if shutil.which(name):
            return shutil.which(name)
    return None


def png_size(p: Path) -> tuple[int, int]:
    with open(p, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"filmstrip: {p} is not a PNG")
    return struct.unpack(">II", head[16:24])


def write_frames(mock: Path) -> Path:
    src = mock.read_text(errors="ignore")
    frames = mock.with_name(mock.stem + ".filmstrip-frames.html")
    frames.write_text(src.replace("</body>", FREEZE + "</body>") if "</body>" in src else src + FREEZE)
    return frames


def auto_crop(box, vw: int, vh: int, pad: int = 16, min_h: int = 140) -> tuple[int, int, int, int]:
    """The moving area, padded, full width (so the frame keeps its context), at least min_h tall."""
    if not box:
        return 0, 0, vw, vh
    top, bottom = max(0, int(box[1]) - pad), min(vh, int(box[3] + 0.999) + pad)
    if bottom - top < min_h:
        mid = (top + bottom) // 2
        top, bottom = max(0, mid - min_h // 2), min(vh, max(0, mid - min_h // 2) + min_h)
    return 0, top, vw, bottom - top


def html_strip(mock: Path, frames: Path, crop: tuple[int, int, int, int], args) -> tuple[Path, list[Path], int, int]:
    vw, vh = (int(v) for v in args.size.lower().split("x"))
    x, y, w, h = crop
    times = [int(t) for t in args.times.split(",")]
    scale = args.scale or min(1.0, 360 / w)
    cw, ch = round(w * scale), round(h * scale)
    hash_ = ("#" + args.hash) if args.hash else ""
    cells = "".join(
        f'<div class="cell"><div class="clip"><iframe src="{html.escape(frames.name)}?t={t}{hash_}" width="{vw}" height="{vh}" '
        f'style="left:{-x * scale}px;top:{-y * scale}px;transform:scale({scale})"></iframe></div>'
        f'<div class="cap">t = {t} ms</div></div>' for t in times)
    cols = max(1, min(len(times), 2400 // (cw + 12)))
    if cw > 200 and len(times) > 4:      # wide frames: two rows, so each frame stays readable when downscaled
        cols = min(cols, -(-len(times) // 2))
    rows = -(-len(times) // cols)
    sheet = mock.with_name(mock.stem + ".filmstrip.html")
    sheet.write_text(SHEET.format(gap=12, cols=cols, cw=cw, ch=ch, cells=cells,
                                  head=f"{html.escape(mock.name)}{html.escape(hash_)} · {len(times)} frames · "
                                       f"crop y {y}–{y + h} of {vh}"))
    return sheet, [frames, sheet], cols * (cw + 12) + 12, rows * (ch + 30) + 12 + 40


def measure(base: list[str], frames: Path, hash_: str, size: str) -> tuple[str, list | None]:
    """Read the animation facts and the moving area from one frame document (deterministic; no iframes)."""
    vw, vh = size.lower().split("x")
    dom = subprocess.run(base + [f"--window-size={vw},{vh}", "--dump-dom", frames.resolve().as_uri() + "?t=0&measure=1" + hash_],
                         capture_output=True, text=True, timeout=120)
    m = re.search(r'data-filmstrip="([^"]*)"', dom.stdout)
    if not m:
        return "filmstrip: no measurement (the frame script didn't run; is JavaScript blocked?)", None
    d = json.loads(html.unescape(m.group(1)))
    return f"filmstrip: {d['n']} animations · longest finite {d['longest']} ms · {d['loops']} looping", d.get("box")


def png_strip(pngs: list[Path], args) -> tuple[Path, list[Path], int, int]:
    w0, h0 = png_size(pngs[0])
    cw = args.cell or 260
    ch = round(cw * h0 / w0)
    out_dir = Path(args.out).resolve().parent
    cells = "".join(
        f'<div class="cell"><div class="clip"><img src="{html.escape(os.path.relpath(p.resolve(), out_dir))}"></div>'
        f'<div class="cap">{html.escape(p.name)}</div></div>' for p in pngs)
    cols = max(1, min(len(pngs), 2400 // (cw + 12)))
    rows = -(-len(pngs) // cols)
    sheet = out_dir / (Path(args.out).stem + ".filmstrip.html")
    sheet.write_text(SHEET.format(gap=12, cols=cols, cw=cw, ch=ch, cells=cells, head=f"filmstrip: {len(pngs)} frames"))
    return sheet, [sheet], cols * (cw + 12) + 12, rows * (ch + 30) + 12 + 40


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="one mock .html, or PNG frames in order")
    ap.add_argument("--hash", default="play", help="hash the mock opens with to start the motion (default play; '' for none)")
    ap.add_argument("--times", default="0,60,120,180,240,320,480,800", help="frame times in ms (HTML mock)")
    ap.add_argument("--crop", default="auto", help="auto (default: the area that moves), full, or x,y,w,h in CSS px")
    ap.add_argument("--scheme", default="light", choices=["light", "dark", "system"],
                    help="prefers-color-scheme for the frames (default light, whatever the machine uses)")
    ap.add_argument("--size", default="390x844", help="phone viewport in CSS px (HTML mock)")
    ap.add_argument("--scale", type=float, help="frame scale (default: frames about 360 px wide, never enlarged)")
    ap.add_argument("--cell", type=int, help="cell width in px for PNG frames (default 260)")
    ap.add_argument("--out", default="filmstrip.png")
    ap.add_argument("--keep", action="store_true", help="keep the intermediate HTML files")
    args = ap.parse_args()

    paths = [Path(p) for p in args.inputs]
    for p in paths:
        if not p.exists():
            print(f"filmstrip: {p} not found")
            return 2
    is_mock = len(paths) == 1 and paths[0].suffix.lower() in (".html", ".htm")
    if not is_mock and not all(p.suffix.lower() == ".png" for p in paths):
        print("filmstrip: give one .html mock or a list of .png frames")
        return 2
    chrome = find_chrome()
    base = [chrome or "chrome", "--headless=new", "--hide-scrollbars", "--no-first-run", "--disable-gpu",
            "--allow-file-access-from-files", "--virtual-time-budget=6000"]
    if args.scheme != "system":
        base.append(f"--blink-settings=preferredColorScheme={1 if args.scheme == 'light' else 0}")
    summary = f"filmstrip: {len(paths)} frames"
    if is_mock:
        if args.out == "filmstrip.png":
            args.out = str(paths[0].with_name(paths[0].stem + "-filmstrip.png"))
        vw, vh = (int(v) for v in args.size.lower().split("x"))
        frames = write_frames(paths[0])
        hash_ = ("#" + args.hash) if args.hash else ""
        box = None
        if chrome:
            summary, box = measure(base, frames, hash_, args.size)
        if args.crop == "auto":
            crop = auto_crop(box, vw, vh)
        elif args.crop == "full":
            crop = (0, 0, vw, vh)
        else:
            crop = tuple(int(v) for v in args.crop.split(","))
        sheet, temps, width, height = html_strip(paths[0], frames, crop, args)
    else:
        sheet, temps, width, height = png_strip(paths, args)

    if not chrome:
        print(f"filmstrip: not rendered, no Chromium-based browser found (set CHROME=/path). Sheet written to {sheet};")
        print(f"  screenshot it at {width}x{height} with JavaScript on and without --force-prefers-reduced-motion.")
        return 3
    url = sheet.resolve().as_uri()
    # New headless Chrome keeps ~90 px of the window for its own frame, so ask for more; the extra is page background.
    shot = subprocess.run(base + [f"--window-size={width},{height + 120}", "--force-device-scale-factor=2",
                                  f"--screenshot={Path(args.out).resolve()}", url], capture_output=True, text=True, timeout=120)
    if shot.returncode != 0 or not Path(args.out).exists():
        print(f"filmstrip: screenshot failed ({chrome}): {(shot.stderr or '').strip()[-300:]}")
        return 1
    if not args.keep:
        for t in temps:
            t.unlink(missing_ok=True)
    print(summary)
    if is_mock:
        print(f"filmstrip: crop {','.join(map(str, crop))} ({args.crop}), {args.scheme} scheme")
    if is_mock and summary.startswith("filmstrip: 0 animations"):
        print("filmstrip: note: nothing to step. Either the mock has no CSS / Web Animations motion, or it runs on "
              "requestAnimationFrame / timers, or the motion needs a trigger (pass --hash, or start it on '#play').")
    print(f"filmstrip: wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
