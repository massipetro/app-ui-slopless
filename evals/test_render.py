#!/usr/bin/env python3
"""Tests for render_swiftui.py's bottom-edge check on the iOS render, on synthetic probes. No simulator.

The probe is what the render host writes: the screen, the system tab bars, the main scroll views with their
bottom content inset, and every accessibility element with its frame (points, window coordinates).

  python3 evals/test_render.py
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import render_swiftui as r  # noqa: E402

SCREEN = [0, 0, 402, 874]


def probe(elements, tab_bars=(), inset=34):
    return {"screen": SCREEN, "safeBottom": 34, "tabBars": list(tab_bars),
            "scrolls": [[0, 0, 402, 874, inset]], "elements": [{"label": l, "frame": f} for l, f in elements]}


class BottomEdge(unittest.TestCase):
    def test_row_across_a_safe_area_inset_bar_is_cut(self):
        # A .safeAreaInset bar 143 pt tall: the fold is at 874 - 143 = 731; round 23's 6 pt sliver.
        out = r.bottom_edge(probe([("Lisinopril 10 mg", [16, 600, 370, 70]), ("Metformin 500 mg", [16, 725, 370, 76])], inset=143))
        self.assertIn("starts at 731", out[0])
        self.assertTrue(any("CUT" in l and "Metformin" in l and "6 of 76" in l for l in out), out)
        self.assertFalse(any("Lisinopril" in l for l in out))

    def test_tab_bar_top_is_the_fold(self):
        out = r.bottom_edge(probe([("Row", [16, 780, 370, 40])], tab_bars=[[20, 800, 362, 60]], inset=83))
        self.assertIn("the tab bar starts at 791", out[0])  # the tab bar (800) sits below the inset fold (791): the higher wins
        self.assertTrue(any("CUT" in l for l in out), out)

    def test_rows_in_a_gap_pass(self):
        out = r.bottom_edge(probe([("Row", [16, 640, 370, 70]), ("Under", [16, 760, 370, 70])], inset=143))
        self.assertTrue(out[-1].startswith("render: bottom edge pass"), out)

    def test_no_pinned_bar(self):
        out = r.bottom_edge(probe([("Row", [16, 820, 370, 70])], inset=34))
        self.assertIn("nothing pinned", out[0])

    def test_no_elements_is_not_a_pass(self):
        self.assertIn("not measured", r.bottom_edge({"screen": SCREEN, "elements": []})[0])
        self.assertIn("not measured", r.bottom_edge(None)[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
