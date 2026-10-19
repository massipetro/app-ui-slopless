#!/usr/bin/env python3
"""Tests for scripts/mascot.py on the hand-written fixture (evals/fixtures/pip.svg + pip.motion.json).

  python3 evals/test_mascot.py            # everything this machine can run
  python3 evals/test_mascot.py -k lottie  # one group

No model calls. Steps that need a toolchain skip (not fail) when it's missing: the Swift typecheck
and macOS render need Xcode, the Kotlin compile needs JDK 17 + Gradle (first run downloads
dependencies), the preview needs a Chromium-based browser and network for lottie-web on cdnjs.

Standard library only; works on Python 3.9.
"""
from __future__ import annotations

import json
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
FIX = ROOT / "evals" / "fixtures"
SVG, MOTION = FIX / "pip.svg", FIX / "pip.motion.json"
sys.path.insert(0, str(SCRIPTS))
import mascot  # noqa: E402
from filmstrip import find_chrome  # noqa: E402

TMP = Path(tempfile.mkdtemp(prefix="mascot-test-"))


def run(*args, timeout=600):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, timeout=timeout)


def read_png(path: Path) -> tuple[int, int, int, bytes]:
    """(width, height, channels, raw pixels) for an 8-bit, non-interlaced RGB/RGBA PNG."""
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", f"{path} is not a PNG"
    pos, idat, w = 8, b"", 0
    while pos < len(data):
        n, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + n]
        if kind == b"IHDR":
            w, h, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", body)
            assert depth == 8 and ctype in (2, 6) and not interlace, "unsupported PNG flavour"
            ch = 4 if ctype == 6 else 3
        elif kind == b"IDAT":
            idat += body
        pos += 12 + n
    raw, stride, out, prev = zlib.decompress(idat), w * ch, bytearray(), bytearray(w * ch)
    for y in range(h):
        f, line = raw[y * (stride + 1)], bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        for x in range(stride):
            a = line[x - ch] if x >= ch else 0
            b, c = prev[x], prev[x - ch] if x >= ch else 0
            if f == 1:
                line[x] = (line[x] + a) & 255
            elif f == 2:
                line[x] = (line[x] + b) & 255
            elif f == 3:
                line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        out += line
        prev = line
    return w, h, ch, bytes(out)


def changed_fraction(a: Path, b: Path) -> float:
    wa, ha, ca, pa = read_png(a)
    wb, hb, cb, pb = read_png(b)
    assert (wa, ha) == (wb, hb), f"frames differ in size: {a.name} is {wa}x{ha}, {b.name} is {wb}x{hb}"
    diff = sum(1 for i in range(0, len(pa), ca) if max(abs(pa[i + k] - pb[i * cb // ca + k]) for k in range(3)) > 24)
    return diff / (wa * ha)


class Into(unittest.TestCase):
    """Single-file briefs: svg2code --into adds the mascot to the screen file, once, and it still compiles."""

    def test_into_compose_file_is_idempotent_and_compiles(self):
        screen = TMP / "into" / "HabitHomeScreen.kt"
        screen.parent.mkdir(parents=True, exist_ok=True)
        screen.write_text("package app.habits\n\nimport androidx.compose.foundation.Image\n"
                          "import androidx.compose.runtime.Composable\n\n"
                          "@Composable\nfun HabitHome() {\n    Image(painter = rememberPipPainter(), contentDescription = null)\n}\n")
        for _ in range(2):
            r = run(SCRIPTS / "mascot.py", "svg2code", SVG, "--compose", "--into", screen)
            self.assertEqual(r.returncode, 0, r.stderr)
        text = screen.read_text()
        self.assertEqual(text.count("---- mascot.py svg2code: Pip"), 1, "rerun must replace the block, not add another")
        self.assertEqual(text.count("package "), 1)
        self.assertEqual(len(re.findall(r"^import androidx.compose.runtime.Composable$", text, re.M)), 1)
        c = run(SCRIPTS / "compile_kotlin.py", screen)
        if c.returncode == 3:
            self.skipTest("no Kotlin toolchain")
        self.assertEqual(c.returncode, 0, c.stdout[-800:])


class Parser(unittest.TestCase):
    def test_path_commands(self):
        subs = mascot.parse_path("m10 10 h10 v10 l-10 0 z M30,30 q10-10 20,0 t20,0 M0 50 a10 10 0 011 1 c1 1 2 2 3 3 s4 4 5 5")
        self.assertEqual(len(subs), 3)
        self.assertTrue(subs[0].closed)
        self.assertEqual(subs[0].segs[1], ("L", (20.0, 20.0)))
        self.assertEqual(subs[1].segs[-1][-1], (70.0, 30.0))
        self.assertEqual(subs[2].segs[-1][-1], (9.0, 59.0))

    def test_arc_endpoints(self):
        segs = mascot.arc_to_cubics((0, 0), 10, 10, 0, False, True, (20, 0))
        self.assertEqual(len(segs), 2)
        self.assertEqual(segs[-1][-1], (20, 0))
        mid = segs[0][-1]
        self.assertAlmostEqual(mid[0], 10, places=6)
        self.assertAlmostEqual(abs(mid[1]), 10, places=6)

    def test_fixture_rig(self):
        rig = mascot.load_svg(SVG)
        self.assertEqual([n.id for n in rig.nodes()],
                         ["spark", "body", "leaf", "arm-left", "arm-right", "eyes", "lids", "mouth"])
        self.assertEqual(rig.node("eyes").pivot, (72.0, 82.0))  # viewBox min (-12, -24) folded in
        self.assertEqual(rig.node("lids").rest, {"scale": [100.0, 0.0]})
        self.assertEqual(rig.colors(), ["#1B2433", "#58CC02", "#FFFFFF"])
        self.assertIn("mouth-open", rig.defs)


class SvgToCode(unittest.TestCase):
    def test_swift_typechecks(self):
        out = TMP / "PipMascot.swift"
        r = run(SCRIPTS / "mascot.py", "svg2code", SVG, "--swift", "-o", out)
        self.assertEqual(r.returncode, 0, r.stderr)
        tc = run(SCRIPTS / "typecheck.py", out)
        if tc.returncode == 3:
            self.skipTest(tc.stdout.strip())
        self.assertEqual(tc.returncode, 0, tc.stdout)

    def test_compose_compiles(self):
        out = TMP / "PipMascot.kt"
        r = run(SCRIPTS / "mascot.py", "svg2code", SVG, "--compose", "--package", "app.mascot", "-o", out)
        self.assertEqual(r.returncode, 0, r.stderr)
        kc = run(SCRIPTS / "compile_kotlin.py", out, timeout=1800)
        if kc.returncode == 3:
            self.skipTest(kc.stdout.strip()[-300:])
        self.assertEqual(kc.returncode, 0, kc.stdout[-3000:])

    def test_swiftui_renders_on_macos(self):
        """Typechecking can't see a wrong picture; render rest and blink with ImageRenderer and compare."""
        if not shutil.which("xcrun"):
            self.skipTest("no Xcode toolchain")
        src = TMP / "render"
        src.mkdir(exist_ok=True)
        run(SCRIPTS / "mascot.py", "svg2code", SVG, "--swift", "-o", src / "PipMascot.swift")
        (src / "main.swift").write_text("""import SwiftUI
import ImageIO
import UniformTypeIdentifiers
MainActor.assumeIsolated {
    for (name, pose) in [("rest", [PipRig: PipPose]()), ("blink", [.lids: PipPose()])] {
        let r = ImageRenderer(content: PipMascot(pose: pose).frame(width: 120, height: 120).background(Color.white))
        r.scale = 1
        let url = URL(fileURLWithPath: CommandLine.arguments[1] + "/" + name + ".png")
        let dest = CGImageDestinationCreateWithURL(url as CFURL, UTType.png.identifier as CFString, 1, nil)!
        CGImageDestinationAddImage(dest, r.cgImage!, nil)
        CGImageDestinationFinalize(dest)
    }
}
""")
        b = subprocess.run(["xcrun", "swiftc", "-o", str(src / "render"), str(src / "PipMascot.swift"), str(src / "main.swift")],
                           capture_output=True, text=True, timeout=600)
        if b.returncode != 0:
            self.skipTest("macOS build failed (SDK too old for ImageRenderer?): " + b.stderr[-300:])
        subprocess.run([str(src / "render"), str(src)], check=True, timeout=120)
        # The eyes are open at rest and covered on the blink: a visible change around the eyes.
        self.assertGreater(changed_fraction(src / "rest.png", src / "blink.png"), 0.02)
        w, h, ch, px = read_png(src / "rest.png")
        eye = ((h * 82 // 144) * w + (w * 51 // 144)) * ch  # left eye's white, left of the pupil: (51, 82)
        self.assertGreater(min(px[eye:eye + 3]), 200, "the left eye should be white at rest")


class Lottie(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = TMP / "pip.json"
        cls.r = run(SCRIPTS / "mascot.py", "lottie", SVG, MOTION, "-o", cls.out)

    def test_top_level_keys(self):
        self.assertEqual(self.r.returncode, 0, self.r.stderr)
        d = json.loads(self.out.read_text())
        for k in ("v", "fr", "ip", "op", "w", "h", "layers"):
            self.assertIn(k, d)
        self.assertEqual(mascot.validate_lottie(d), [])
        self.assertEqual([m["cm"] for m in d["markers"]], ["idle", "celebrate"])

    def test_rig_is_parented_and_anchored(self):
        d = json.loads(self.out.read_text())
        by_name = {l["nm"]: l for l in d["layers"]}
        body, eyes = by_name["body"], by_name["eyes"]
        self.assertEqual(eyes["parent"], body["ind"])
        self.assertEqual(eyes["ks"]["a"]["k"], [72.0, 82.0, 0])
        self.assertEqual(by_name["lids"]["ks"]["s"]["k"][0]["s"], [100.0, 0.0, 100])
        # Layers are top-first: the mouth (drawn last in the SVG) is above the body shape.
        names = [l["nm"] for l in d["layers"]]
        self.assertLess(names.index("mouth"), names.index("body+1"))

    def test_no_canvas_overflow(self):
        self.assertNotIn("leaves the", self.r.stderr)

    def test_morph_needs_same_vertex_count(self):
        bad = TMP / "bad.svg"
        bad.write_text(SVG.read_text().replace(
            'd="M47,69 L73,69 C73,80 67,86 60,86 C53,86 47,80 47,69 Z"', 'd="M47,69 L73,69 L60,86 L55,80 Z"'))
        r = run(SCRIPTS / "mascot.py", "lottie", bad, MOTION, "-o", TMP / "bad.json")
        self.assertEqual(r.returncode, 1)
        self.assertIn("can't morph", r.stderr)

    def test_unknown_layer_refused(self):
        spec = json.loads(MOTION.read_text())
        spec["states"][0]["tracks"]["tail"] = {"rotation": [{"t": 0, "v": 0}]}
        p = TMP / "bad-motion.json"
        p.write_text(json.dumps(spec))
        r = run(SCRIPTS / "mascot.py", "lottie", SVG, p, "-o", TMP / "bad.json")
        self.assertEqual(r.returncode, 1)
        self.assertIn("no rig group #tail", r.stderr)


class Preview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chrome = find_chrome()
        cls.json = TMP / "pip-preview.json"
        run(SCRIPTS / "mascot.py", "lottie", SVG, MOTION, "-o", cls.json)

    def setUp(self):
        if not self.chrome:
            self.skipTest("no Chromium-based browser")

    def shot(self, page: Path, query: str, out: Path) -> Path:
        subprocess.run([self.chrome, "--headless=new", "--hide-scrollbars", "--no-first-run", "--disable-gpu",
                        "--virtual-time-budget=6000", "--window-size=240,240", "--force-device-scale-factor=1",
                        f"--screenshot={out}",
                        page.resolve().as_uri() + query], capture_output=True, text=True, timeout=120)
        self.assertTrue(out.exists(), f"no screenshot for {query}")
        return out

    def test_filmstrip_measures_the_clock(self):
        page = TMP / "pip.preview.html"
        r = run(SCRIPTS / "mascot.py", "preview", self.json, "-o", page)
        self.assertEqual(r.returncode, 0, r.stderr)
        strip = TMP / "strip.png"
        f = run(SCRIPTS / "filmstrip.py", page, "--crop", "0,0,240,240", "--times", "0,120,240,480,880", "--out", strip)
        self.assertEqual(f.returncode, 0, f.stdout)
        self.assertIn("1 animations · longest finite 900 ms", f.stdout)
        self.assertTrue(strip.exists())
        idle = run(SCRIPTS / "filmstrip.py", page, "--hash", "state=idle", "--crop", "0,0,240,240", "--out", TMP / "idle.png")
        self.assertIn("1 looping", idle.stdout)

    def test_frames_visibly_change(self):
        for mode in ("clock", "frames"):
            page = TMP / f"pip.{mode}.html"
            args = ["--frames"] if mode == "frames" else []
            run(SCRIPTS / "mascot.py", "preview", self.json, "-o", page, *args)
            a = self.shot(page, "?t=0#play", TMP / f"{mode}-0.png")
            b = self.shot(page, "?t=240#play", TMP / f"{mode}-240.png")
            c = self.shot(page, "?t=900#play", TMP / f"{mode}-900.png")
            moved = changed_fraction(a, b)
            if moved == 0 and changed_fraction(a, c) == 0 and min(read_png(a)[3]) == max(read_png(a)[3]):
                self.skipTest("blank frames: lottie-web didn't load (no network?)")
            self.assertGreater(moved, 0.03, f"{mode}: the jump frame should differ from rest")
            self.assertLess(changed_fraction(a, c), 0.01, f"{mode}: the reaction should land back on rest")


if __name__ == "__main__":
    try:
        unittest.main(verbosity=2)
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
