#!/usr/bin/env python3
"""Tests for the judge prompts (evals/judges.py) and blind_critique.py's score parsing. No model calls.

  python3 evals/test_judges.py
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "evals"))
import blind_critique  # noqa: E402
import judges  # noqa: E402


class Prompts(unittest.TestCase):
    def test_access_judge_sees_four_frames_and_scores_access(self):
        p = judges.prompt("access", "A medication Today screen.", "ios")
        for s in ("A-ax5.png", "B-ax5.png", "AX5", "Access, 1-10", "ACCESS A:", "WINNER:", "A medication Today screen."):
            self.assertIn(s, p)
        self.assertIn("font scale 2.0", judges.prompt("access", "x", "android"))

    def test_phone_and_mac_keep_their_round_wording(self):
        self.assertIn("390x844", judges.prompt("phone", "x"))
        self.assertIn("1280x800", judges.prompt("mac", "x"))
        with self.assertRaises(ValueError):
            judges.prompt("tablet", "x")


class Scores(unittest.TestCase):
    def test_six_criteria_and_overall(self):
        v = "notes\nSCORES: Idea 7 · Hierarchy 6 · Craft 5 · Substance 6 · Platform 7 · Access 4.5 → overall 5.9 (caps: Access ≤ 5)\nFIX 1: x"
        s = blind_critique.parse_scores(v)
        self.assertEqual(s["access"], 4.5)
        self.assertEqual(s["overall"], 5.9)
        self.assertEqual(len(s), 7)

    def test_no_scores_line(self):
        self.assertEqual(blind_critique.parse_scores("no verdict"), {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
