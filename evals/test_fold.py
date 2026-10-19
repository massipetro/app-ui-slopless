#!/usr/bin/env python3
"""Tests for scripts/fold.py on generated mocks with known bottom edges. No model calls.

Each mock is a 390x844 screen: a scrolling list of 72 px bordered cards (title, then a
subtitle), a 100 px opaque tab bar pinned to the bottom (top edge at 744), and optionally
a 20 px fade above it. The list's top padding decides where the fold falls.

  python3 evals/test_fold.py
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
from filmstrip import find_chrome  # noqa: E402

TMP = Path(tempfile.mkdtemp(prefix="fold-test-"))
BAR_TOP = 744          # 844 - the 100 px bar
STEP = 84              # 72 px card + 12 px gap


def mock(name: str, card_top: int, fade: bool = False, bottom_pad: int = 120, scrolls: bool = True) -> Path:
    """Some card starts at card_top px; the list's top padding puts it there."""
    pad_top = card_top % STEP
    cards = "".join(f'<div class="card"><div class="t">Habit number {i}</div><div class="s">Done at 0{i % 10}:15</div></div>'
                    for i in range(14))
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
  body {{ margin: 0; width: 390px; height: 844px; position: relative; overflow: hidden; background: #f4efe6; font-family: sans-serif; }}
  #scroll {{ position: absolute; inset: 0; overflow-y: {'auto' if scrolls else 'hidden'}; padding: {pad_top}px 16px {bottom_pad}px; box-sizing: border-box; }}
  .card {{ box-sizing: border-box; height: 72px; margin-bottom: 12px; padding: 8px 12px; background: #fff; border: 2px solid #111; border-radius: 12px; }}
  .t {{ font-size: 16px; line-height: 20px; }}
  .s {{ font-size: 13px; line-height: 16px; margin-top: 10px; }}
  .fade {{ position: absolute; left: 0; right: 0; bottom: 100px; height: 20px; background: linear-gradient(to bottom, rgba(244,239,230,0), #f4efe6); }}
  .bar {{ position: absolute; left: 0; right: 0; bottom: 0; height: 100px; box-sizing: border-box; background: #ffffff; border-top: 2px solid #111; display: flex; }}
  .bar div {{ flex: 1; text-align: center; padding-top: 14px; }}
</style></head><body>
<div id="scroll">{cards}</div>
{'<div class="fade"></div>' if fade else ''}
<div class="bar"><div>Today</div><div>Stats</div><div>Me</div></div>
</body></html>"""
    p = TMP / f"{name}.html"
    p.write_text(page)
    return p


def fold(path: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPTS / "fold.py"), str(path)], capture_output=True, text=True, timeout=180)


@unittest.skipUnless(find_chrome(), "no Chromium-based browser")
class Fold(unittest.TestCase):
    def test_fold_in_a_gap_passes(self):
        r = fold(mock("gap", BAR_TOP - 72 - 6))                  # card 8 ends 6 px above the bar, card 9 is hidden
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("whole", r.stdout)

    def test_sliver_behind_a_fade_is_cut(self):
        r = fold(mock("sliver", BAR_TOP - 7, fade=True))         # 7 px of a card show, under a fade: round 8's defect
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("7 px of a 72 px row show", r.stdout)

    def test_a_peek_is_cut_too(self):
        r = fold(mock("peek", BAR_TOP - 35, fade=True))          # title shows, subtitle hidden: judges call it cut
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("35 px of a 72 px row show", r.stdout)

    def test_one_pixel_of_card_is_cut(self):
        r = fold(mock("onepx", BAR_TOP - 1))                     # round 9: the rounded top edge of the next card
        self.assertEqual(r.returncode, 1, r.stdout)

    def test_text_through_the_edge_is_cut(self):
        r = fold(mock("text", BAR_TOP - 48))                     # the edge runs through the subtitle
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("crosses the bar", r.stdout)

    def test_last_row_must_clear_the_bar(self):
        r = fold(mock("nopad", BAR_TOP - 72 - 6, bottom_pad=0))  # no bottom padding: the last card ends under the bar
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("needs at least 8 px clear", r.stdout)

    def test_a_mock_that_cannot_scroll_fails(self):
        r = fold(mock("locked", BAR_TOP - 72 - 6, scrolls=False))
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("doesn't scroll", r.stdout)


if __name__ == "__main__":
    try:
        unittest.main(verbosity=2)
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
