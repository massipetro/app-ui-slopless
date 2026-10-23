#!/usr/bin/env python3
"""Tests for lint.py's accessibility rules on small generated files. No model calls, no toolchain.

Each rule gets a snippet it must flag and a near-miss it must not: the fix the rule asks for,
or the pattern that only looks like the defect. Criteria in brackets are WCAG 2.2.

  python3 evals/test_lint_a11y.py
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

TMP = Path(tempfile.mkdtemp(prefix="lint-a11y-"))
N = [0]


def rules(body: str, ext: str = "swift", platform: str | None = "ios") -> list[str]:
    N[0] += 1
    f = TMP / f"S{N[0]}.{ext}"
    f.write_text(("import SwiftUI\n" if ext == "swift" else "") + body)
    return [r for r, _, _ in lint.lint_file(f, platform if ext == "swift" else None)]


def view(inner: str, extra: str = "") -> str:
    return f"struct V: View {{\n  @State var on = false\n{extra}  var body: some View {{\n{inner}\n  }}\n}}\n"


class TapNoRole(unittest.TestCase):  # 4.1.2, 2.1.1
    def test_swift_tap_on_a_row(self):
        self.assertIn("tap-no-role", rules(view('    HStack { Text("Ischia") }\n      .padding()\n      .onTapGesture { on = true }')))

    def test_swift_tap_with_button_trait(self):
        r = rules(view('    HStack { Text("Ischia") }\n      .onTapGesture { on = true }\n      .accessibilityAddTraits(.isButton)'))
        self.assertNotIn("tap-no-role", r)

    def test_swift_trait_before_the_gesture(self):
        r = rules(view('    HStack { Text("Ischia") }\n      .accessibilityAddTraits(.isButton)\n      .padding()\n      .onTapGesture { on = true }'))
        self.assertNotIn("tap-no-role", r)

    def test_swift_tap_to_dismiss_the_keyboard(self):
        self.assertNotIn("tap-no-role", rules(view('    Color.clear\n      .onTapGesture { focused = false }', "  @FocusState var focused: Bool\n")))

    def test_swift_icon_tap_is_also_unlabelled(self):
        r = rules(view('    Image(systemName: "heart")\n      .onTapGesture { on.toggle() }'))
        self.assertIn("tap-no-role", r)
        self.assertIn("unlabelled-icon-button", r)

    def test_compose_detect_tap_gestures(self):
        kt = 'fun Row() { Box(Modifier.pointerInput(Unit) { detectTapGestures(onTap = { go() }) }) { Text("Ischia") } }\n'
        self.assertIn("tap-no-role", rules(kt, "kt"))

    def test_compose_clickable_with_role(self):
        kt = 'fun Row() { Box(Modifier.clickable(role = Role.Button, onClickLabel = "Open Ischia") { go() }) { Text("Ischia") } }\n'
        r = rules(kt, "kt")
        self.assertNotIn("tap-no-role", r)
        self.assertNotIn("clickable-no-role", r)

    def test_compose_clickable_without_role(self):
        self.assertIn("clickable-no-role", rules('fun Row() { Box(Modifier.clickable { go() }) { Text("Ischia") } }\n', "kt"))


class ToggleState(unittest.TestCase):  # 4.1.2
    def test_swift_button_that_flips_a_bool(self):
        r = rules(view('    Button { on.toggle() } label: {\n      Circle().fill(on ? Ink.a : Ink.b).frame(width: 44, height: 44)\n    }'))
        self.assertIn("toggle-no-state", r)

    def test_swift_toggle_with_value(self):
        r = rules(view('    Button { on.toggle() } label: { Circle() }\n      .accessibilityValue(on ? "On" : "Off")'))
        self.assertNotIn("toggle-no-state", r)

    def test_swift_label_that_says_the_state(self):
        r = rules(view('    Button { on.toggle() } label: { Label(on ? "Pause" : "Play", systemImage: on ? "pause" : "play") }'))
        self.assertNotIn("toggle-no-state", r)

    def test_swift_show_panel_is_a_plain_button(self):
        self.assertNotIn("toggle-no-state", rules(view('    Button { showInspector.toggle() } label: { Label("Inspector", systemImage: "sidebar.trailing") }')))

    def test_compose_clickable_flip(self):
        kt = 'fun Fav() { var fav by remember { mutableStateOf(false) }\n Box(Modifier.clickable(role = Role.Button) { fav = !fav }) { } }\n'
        self.assertIn("toggle-no-state", rules(kt, "kt"))

    def test_compose_toggleable(self):
        kt = 'fun Fav() { var fav by remember { mutableStateOf(false) }\n Box(Modifier.toggleable(value = fav, role = Role.Switch) { fav = it }) { } }\n'
        self.assertNotIn("toggle-no-state", rules(kt, "kt"))


class Images(unittest.TestCase):  # 1.1.1
    def test_named_image_without_label(self):
        self.assertIn("image-no-label", rules(view('    Image("ferry-hero").resizable()')))

    def test_decorative_and_labelled_images(self):
        self.assertNotIn("image-no-label", rules(view('    VStack {\n      Image(decorative: "wave")\n      Image("ferry-hero").accessibilityLabel("The Procida ferry at the pier")\n    }')))

    def test_canvas_labelled_where_it_is_used(self):
        src = 'struct Gauge: View { var body: some View { Canvas { c, s in } } }\n' + view('    Gauge().accessibilityLabel("Bulk ferment").accessibilityValue("62%")')
        self.assertNotIn("image-no-label", rules(src))

    def test_canvas_never_labelled(self):
        self.assertIn("image-no-label", rules('struct Gauge: View { var body: some View { Canvas { c, s in } } }\n' + view('    Gauge()')))

    def test_compose_canvas(self):
        self.assertIn("image-no-label", rules('fun Jar() { Canvas(Modifier.size(80.dp)) { drawRect(Color.Red) } }\n', "kt"))
        ok = 'fun Jar() { Canvas(Modifier.size(80.dp).semantics { contentDescription = "Jar, 40% full" }) { } }\n'
        self.assertNotIn("image-no-label", rules(ok, "kt"))


class HiddenControl(unittest.TestCase):  # 4.1.2
    def test_hidden_button(self):
        self.assertIn("a11y-hidden-control", rules(view('    Button("Buy for €12") { }\n      .accessibilityHidden(true)')))

    def test_hidden_decoration(self):
        self.assertNotIn("a11y-hidden-control", rules(view('    Image(systemName: "sparkle").accessibilityHidden(true)')))

    def test_compose_cleared_clickable(self):
        kt = 'fun B() { Box(Modifier.clickable(role = Role.Button) { }.clearAndSetSemantics { }) { } }\n'
        self.assertIn("a11y-hidden-control", rules(kt, "kt"))


class LabelInName(unittest.TestCase):  # 2.5.3
    def test_name_without_the_visible_words(self):
        self.assertIn("label-in-name", rules(view('    Button { } label: { Text("Buy ticket") }\n      .accessibilityLabel("Purchase")')))

    def test_name_that_starts_with_them(self):
        self.assertNotIn("label-in-name", rules(view('    Button { } label: { Text("Buy ticket") }\n      .accessibilityLabel("Buy ticket, 12 euros")')))


class ColourOnly(unittest.TestCase):  # 1.4.1
    def test_status_colour_alone(self):
        src = view('    Text(dep.time)\n      .foregroundStyle(late ? Ink.red : Ink.ink)', "  var late = false\n")
        self.assertIn("colour-only-state", rules(src))

    def test_status_with_an_icon(self):
        src = view('    HStack {\n      Text(dep.time).foregroundStyle(late ? Ink.red : Ink.ink)\n      if late { Image(systemName: "exclamationmark.triangle") }\n    }', "  var late = false\n")
        self.assertNotIn("colour-only-state", rules(src))

    def test_zebra_band_is_not_a_state(self):
        self.assertNotIn("colour-only-state", rules(view('    Text("x").background(banded ? Ink.band : .clear)', "  var banded = false\n")))

    def test_accessibility_value_alone_doesnt_help_sighted_users(self):
        src = view('    Text(dep.time)\n      .foregroundStyle(late ? Ink.red : Ink.ink)\n      .accessibilityValue(late ? "Late" : "")', "  var late = false\n")
        self.assertIn("colour-only-state", rules(src))

    def test_compose(self):
        kt = 'fun T(overdue: Boolean) { Text("Fern", color = if (overdue) Palette.error else Palette.ink) }\n'
        self.assertIn("colour-only-state", rules(kt, "kt"))


class TextScaling(unittest.TestCase):  # 1.4.4, 1.4.10
    def test_fixed_height_row_of_text(self):
        self.assertIn("fixed-text-frame", rules(view('    HStack { Text("Pozzuoli") }\n      .frame(height: 44)')))

    def test_min_height_and_scaled_metric(self):
        src = view('    VStack {\n      HStack { Text("Pozzuoli") }.frame(minHeight: 44)\n      HStack { Text("Ischia") }.frame(height: row)\n    }',
                   "  @ScaledMetric(relativeTo: .body) var row: CGFloat = 44\n")
        self.assertNotIn("fixed-text-frame", rules(src))

    def test_icon_frame_is_fine(self):
        self.assertNotIn("fixed-text-frame", rules(view('    Image(systemName: "ferry").frame(width: 44, height: 44)')))

    def test_mac_has_no_dynamic_type(self):
        self.assertNotIn("fixed-text-frame", rules(view('    HStack { Text("Pozzuoli") }.frame(height: 22)'), platform="macos"))

    def test_compose_fixed_row(self):
        self.assertIn("fixed-text-frame", rules('fun R() { Row(Modifier.height(48.dp)) { Text("Fern") } }\n', "kt"))
        self.assertNotIn("fixed-text-frame", rules('fun R() { Row(Modifier.heightIn(min = 48.dp)) { Text("Fern") } }\n', "kt"))

    def test_capped_dynamic_type(self):
        self.assertIn("dynamic-type-capped", rules(view('    Text("Ischia").dynamicTypeSize(...DynamicTypeSize.xxLarge)')))
        self.assertNotIn("dynamic-type-capped", rules(view('    Text("12:40").dynamicTypeSize(...DynamicTypeSize.accessibility3)')))
        self.assertIn("dynamic-type-capped", rules('fun A() { CompositionLocalProvider(LocalDensity provides Density(density.density, fontScale = 1f)) { } }\n', "kt"))


class Gestures(unittest.TestCase):  # 2.5.1, 2.5.7
    def test_drag_only(self):
        self.assertIn("gesture-no-alternative", rules(view('    Capsule().gesture(DragGesture().onEnded { _ in })')))

    def test_drag_with_action(self):
        src = view('    Capsule().gesture(DragGesture().onEnded { _ in })\n      .accessibilityAdjustableAction { _ in }')
        self.assertNotIn("gesture-no-alternative", rules(src))

    def test_press_state_drag_is_not_a_drag(self):
        self.assertNotIn("gesture-no-alternative", rules(view('    Capsule().gesture(DragGesture(minimumDistance: 0).onChanged { _ in })')))

    def test_compose_swipe(self):
        self.assertIn("gesture-no-alternative", rules('fun S() { Box(Modifier.pointerInput(Unit) { detectHorizontalDragGestures { _, _ -> } }) }\n', "kt"))


class Overlays(unittest.TestCase):  # 2.4.3
    def test_home_made_modal(self):
        src = view('    ZStack {\n      List { Text("a") }\n      if on {\n        Color.black.opacity(0.4).ignoresSafeArea().onTapGesture { on = false }\n        Panel()\n      }\n    }')
        self.assertIn("overlay-not-modal", rules(src))

    def test_modal_trait(self):
        src = view('    ZStack {\n      List { Text("a") }\n      if on {\n        Color.black.opacity(0.4).ignoresSafeArea()\n        Panel().accessibilityAddTraits(.isModal)\n      }\n    }')
        self.assertNotIn("overlay-not-modal", rules(src))


class Headings(unittest.TestCase):  # 1.3.1, 2.4.6
    def test_titles_without_header_trait(self):
        self.assertIn("heading-missing", rules(view('    VStack {\n      Text("Today").font(.title2)\n      Text("Tomorrow").font(.title2)\n    }')))

    def test_header_trait(self):
        src = view('    VStack {\n      Text("Today").font(.title2).accessibilityAddTraits(.isHeader)\n      Text("Tomorrow").font(.title2).accessibilityAddTraits(.isHeader)\n    }')
        self.assertNotIn("heading-missing", rules(src))


class Criteria(unittest.TestCase):
    def test_every_mapped_rule_exists(self):
        self.assertEqual(set(lint.CRITERIA) - set(lint.RULES), set())


if __name__ == "__main__":
    try:
        unittest.main(verbosity=1)
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
