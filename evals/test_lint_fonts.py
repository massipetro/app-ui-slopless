#!/usr/bin/env python3
"""Tests for lint.py's unshipped-font rule on generated files. No model calls, no toolchain.

A custom face named in code must ship as a font file somewhere in the project, or the system
font quietly takes its place (round 21: four of six Mac builds). Each case writes a small
project into a temp folder and lints it.

  python3 evals/test_lint_fonts.py
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import lint  # noqa: E402

TMP = Path(tempfile.mkdtemp(prefix="lint-fonts-"))


def project(name: str, files: dict[str, str]) -> Path:
    d = TMP / name
    for rel, body in files.items():
        f = d / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(body)
    return d


def flagged(path: Path) -> list[str]:
    return [detail for rule, _, detail in lint.lint_file(path) if rule == "unshipped-font"]


SWIFT = 'import SwiftUI\nenum Face { static let display = "Bricolage Grotesque" }\nstruct V: View { var body: some View {\n' \
        '  Text("Hi").font(.custom(Face.display, size: 28, relativeTo: .title))\n  Text("Yo").font(.custom("Figtree-Bold", size: 17, relativeTo: .body)) } }\n'


class UnshippedFont(unittest.TestCase):
    def test_names_without_files_are_flagged(self):
        d = project("bare", {"V.swift": SWIFT})
        self.assertEqual(sorted(flagged(d / "V.swift")), ["'Bricolage Grotesque'", "'Figtree-Bold'"])

    def test_shipped_files_match_by_family_and_style(self):
        d = project("shipped", {"Sources/V.swift": SWIFT, "Sources/Fonts/BricolageGrotesque[opsz,wght].ttf": "",
                                "Sources/Fonts/Figtree-Bold.ttf": "", "Package.swift": "// swift-tools-version:5.9"})
        self.assertEqual(flagged(d / "Sources/V.swift"), [])

    def test_fonts_found_from_the_project_root(self):
        d = project("root", {"App/Screens/V.swift": SWIFT, "App/Resources/BricolageGrotesque-Regular.otf": "",
                             "App/Resources/Figtree-Bold.ttf": "", "App.xcodeproj/project.pbxproj": ""})
        self.assertEqual(flagged(d / "App/Screens/V.swift"), [])

    def test_system_faces_need_no_file(self):
        d = project("system", {"V.swift": 'import SwiftUI\nlet a = Font.custom("New York", size: 20, relativeTo: .title)\n'
                                           'let b = NSFont(name: "Menlo-Regular", size: 12)\nlet c = Font.custom("Geneva", size: 13)\n'})
        self.assertEqual(flagged(d / "V.swift"), [])

    def test_compose_resources(self):
        kt = 'val Display = FontFamily(Font(Res.font.press_start_2p))\nval Body = FontFamily(Font(R.font.atkinson_hyperlegible_regular))\n'
        bare = project("compose-bare", {"Home.kt": kt})
        self.assertEqual(sorted(flagged(bare / "Home.kt")), ["'atkinson_hyperlegible_regular'", "'press_start_2p'"])
        shipped = project("compose-shipped", {"app/src/main/kotlin/Home.kt": kt, "settings.gradle.kts": "",
                                              "app/src/commonMain/composeResources/font/press_start_2p.ttf": "",
                                              "app/src/main/res/font/atkinson_hyperlegible_regular.ttf": ""})
        self.assertEqual(flagged(shipped / "app/src/main/kotlin/Home.kt"), [])

    def test_google_downloadable_fonts_are_not_flagged(self):
        d = project("google", {"T.kt": 'val f = FontFamily(Font(googleFont = GoogleFont("Pixelify Sans"), fontProvider = provider))\n'})
        self.assertEqual(flagged(d / "T.kt"), [])


if __name__ == "__main__":
    try:
        unittest.main(verbosity=2)
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
