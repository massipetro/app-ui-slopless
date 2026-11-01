#!/usr/bin/env python3
"""Tests for scripts/acr.py: the report line is parsed per criterion, and lint evidence overrides a claim.
No model calls, no toolchain.

  python3 evals/test_acr.py
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import acr  # noqa: E402

TMP = Path(tempfile.mkdtemp(prefix="acr-test-"))
LINE = ("Accessibility: WCAG 2.2 AA from code, lint and renders, not tested with assistive technology. "
        "Supports: 1.1.1 (every glyph labelled, the gull hidden), 4.1.2 (custom toggles expose isSelected); "
        "Partially supports: 1.4.4 (the countdown is capped at AX2 (it fills its region), everything else scales to AX5); "
        "Does not support: none; Not applicable: 1.2.2 (no media), 3.3.1 (no input)")


class ParseLine(unittest.TestCase):
    def test_terms_and_reasons(self):
        c = acr.parse_line("intro\n" + LINE + "\n")
        self.assertEqual(c["1.1.1"][0], "Supports")
        self.assertEqual(c["4.1.2"], ("Supports", "custom toggles expose isSelected"))
        self.assertEqual(c["1.4.4"][0], "Partially Supports")
        self.assertIn("(it fills its region)", c["1.4.4"][1])
        self.assertEqual(c["1.2.2"][0], "Not Applicable")
        self.assertNotIn("2.4.3", c)

    def test_no_line(self):
        self.assertEqual(acr.parse_line("no report here"), {})


class Build(unittest.TestCase):
    def setUp(self):
        self.code = TMP / "V.swift"
        self.code.write_text('import SwiftUI\nstruct V: View { var body: some View {\n'
                             '  HStack { Text("Ischia") }\n    .onTapGesture { }\n } }\n')

    def test_a_lint_fail_downgrades_a_supports_claim(self):
        md = acr.build([self.code], LINE, "Ferry home", "ios")
        row = next(l for l in md.splitlines() if l.startswith("| 4.1.2 "))
        self.assertIn("Partially Supports", row)
        self.assertIn("`tap-no-role` V.swift:4", row)

    def test_unanswered_criteria_are_to_evaluate_and_sets_are_not_applicable(self):
        md = acr.build([self.code], LINE, "Ferry home", "ios")
        self.assertIn("| 2.4.3 Focus Order (Level A) | To evaluate |", md)
        self.assertIn("| 2.4.5 Multiple Ways (Level AA) | Not Applicable | WCAG2ICT", md)
        self.assertIn("Not tested with VoiceOver", md)
        self.assertEqual(sum(1 for l in md.splitlines() if l.startswith("| ") and "(Level " in l), 55)


if __name__ == "__main__":
    try:
        unittest.main(verbosity=2)
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
