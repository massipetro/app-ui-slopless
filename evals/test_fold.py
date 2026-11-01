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


def mock(name: str, card_top: int, fade: bool = False, bottom_pad: int = 120, scrolls: bool = True, grow: bool = False) -> Path:
    """Some card starts at card_top px; the list's top padding puts it there."""
    pad_top = card_top % STEP
    cards = "".join(f'<div class="card"><div class="t">Habit number {i}</div><div class="s">Done at 0{i % 10}:15</div></div>'
                    for i in range(14))
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
  body {{ margin: 0; width: 390px; height: 844px; position: relative; overflow: hidden; background: #f4efe6; font-family: sans-serif; }}
  #scroll {{ position: absolute; inset: 0; overflow-y: {'auto' if scrolls else 'hidden'}; padding: {pad_top}px 16px {bottom_pad}px; box-sizing: border-box; }}
  .card {{ box-sizing: border-box; {'min-height' if grow else 'height'}: 72px; margin-bottom: 12px; padding: 8px 12px; background: #fff; border: 2px solid #111; border-radius: 12px; }}
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


def sections_mock(name: str, heading_bottom: int, plain: bool = False) -> Path:
    """Two sections, each a 24 px heading over 72 px cards. The second heading ends at heading_bottom;
    its first card starts 8 px lower. plain: the 'heading' is styled like the rows, so it isn't one."""
    head = '<div class="t">Habit 9</div>' if plain else '<h2>Evening</h2>'
    card = '<div class="card"><div class="t">Habit {i}</div><div class="s">Done at 08:15</div></div>'
    first = "".join(card.format(i=i) for i in range(4))
    pad_top = heading_bottom - 24 - (32 + 4 * STEP)
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
  body {{ margin: 0; width: 390px; height: 844px; position: relative; overflow: hidden; background: #f4efe6; font-family: sans-serif; }}
  #scroll {{ position: absolute; inset: 0; overflow-y: auto; padding: {pad_top}px 16px 120px; box-sizing: border-box; }}
  h2, section > .t {{ font-size: {16 if plain else 20}px; line-height: 24px; height: 24px; margin: 0 0 8px; font-weight: {400 if plain else 700}; }}
  section {{ margin-bottom: 0; }}
  section:first-child {{ padding-top: 0; }}
  .card {{ box-sizing: border-box; height: 72px; margin-bottom: 12px; padding: 8px 12px; background: #fff; border: 2px solid #111; border-radius: 12px; }}
  .t {{ font-size: 16px; line-height: 20px; }}
  .s {{ font-size: 13px; line-height: 16px; margin-top: 10px; }}
  .bar {{ position: absolute; left: 0; right: 0; bottom: 0; height: 100px; box-sizing: border-box; background: #fff; border-top: 2px solid #111; display: flex; }}
  .bar div {{ flex: 1; text-align: center; padding-top: 14px; }}
</style></head><body>
<div id="scroll"><section style="height: {32 + 4 * STEP}px"><h2>Morning</h2>{first}</section><section>{head}{"".join(card.format(i=i) for i in range(4, 8))}</section></div>
<div class="bar"><div>Today</div><div>Stats</div><div>Me</div></div>
</body></html>"""
    p = TMP / f"{name}.html"
    p.write_text(page)
    return p


def fold(path: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPTS / "fold.py"), str(path), *extra], capture_output=True, text=True, timeout=180)


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


    def test_an_orphaned_heading_is_cut(self):
        r = fold(sections_mock("orphan", BAR_TOP - 4))           # round 14: the heading shows, its rows are all under the bar
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("orphaned", r.stdout)

    def test_a_heading_with_its_first_row_passes(self):
        r = fold(sections_mock("headed", BAR_TOP - 72 - 8 - 12))  # heading and its first card both show above the bar
        self.assertNotIn("orphaned", r.stdout)

    def test_a_plain_first_row_is_not_a_heading(self):
        r = fold(sections_mock("plain", BAR_TOP - 4, plain=True))  # styled like the rows: whole-or-hidden still holds
        self.assertNotIn("orphaned", r.stdout)

    def test_large_text_moves_the_fold(self):
        # Rows that grow with their text (min-height, as a native row does): in a gap at 100%, but at
        # 200% each card is 102 px and the sixth one runs through the bar's top edge.
        m = mock("grow", BAR_TOP - 72 - 6, grow=True)
        self.assertEqual(fold(m).returncode, 0)
        shot = TMP / "grow-2x.png"
        r = fold(m, "--text-scale", "2", "--shot", str(shot))
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("measured at large text (2)", r.stdout)
        self.assertTrue(shot.exists() and shot.stat().st_size > 1000)

    def test_ax5_runs_and_an_unknown_scale_is_refused(self):
        m = mock("ax5", BAR_TOP - 72 - 6, grow=True)
        r = fold(m, "--text-scale", "ax5", "--json")
        self.assertIn("measured at large text (ax5)", r.stdout)
        self.assertEqual(fold(m, "--text-scale", "nonsense").returncode, 2)


if __name__ == "__main__":
    try:
        unittest.main(verbosity=2)
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
