#!/usr/bin/env python3
"""Deal researched design directions for app-ui-slopless.

Asked to invent a look, a model picks the category default every time. This
script deals directions from library/directions.json instead; the model then
chooses among them against the product inventory.

  deal.py --options 3 [--content list,number] [--preset P] [--sector S] [--have photography] [--platform macos] [--seed N]
  deal.py --direction ID [--seed N] [--keep palette,type] [--platform macos]
  deal.py --list
  deal.py --check

--platform macos deals for a Mac window: each direction's `mac` block replaces
the phone composition, moves and shape, adds how it treats system chrome, and
overrides the dials; directions whose `mac` block says `skip` are not dealt.

Standard library only; works on Python 3.9.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

LIBRARY = Path(__file__).resolve().parent.parent / "library" / "directions.json"
PRESETS = ("warm-premium", "neo-brutalist", "playful", "editorial",
           "native-craft", "pro-instrument", "document-first")
# Mac-only presets: dealt only with --platform macos, where one option always comes from them.
MAC_PRESETS = ("native-craft", "pro-instrument", "document-first")
ROLES = ("ground", "surface", "ink", "ink2", "accent", "on_accent")
SHAPES = ("list", "number", "detail", "collection", "canvas", "story", "progression", "action",
          "table", "document")  # the last two only occur on a Mac
REQUIRED = ("id", "preset", "name", "anchors", "composition", "content", "device", "dials",
            "type", "palettes", "shape", "moves", "motion", "needs", "not_for", "pitfall")
MAC_REQUIRED = ("composition", "moves", "shape", "chrome", "dials")
# Phone mechanics that must not leak into a Mac block (the reason the blocks exist).
PHONE_WORDS = re.compile(r"thumb|tab bar|bottom bar|bottom sheet|sheet springs|selection haptic|notification haptic|firm haptic|\btap\b|\bswip|9:16|home screen|\d\s*dp\b|live activity", re.I)


def load() -> list[dict]:
    return json.loads(LIBRARY.read_text())["directions"]


def mac_only(d: dict) -> bool:
    return d.get("platforms") == ["macos"]


def for_platform(d: dict, platform: str | None) -> dict | None:
    """The direction as dealt on this platform, or None when it has no form there."""
    if platform != "macos":
        return None if mac_only(d) else d
    if mac_only(d):
        return d  # written for a Mac window already
    mac = d["mac"]
    if "skip" in mac:
        return None
    view = dict(d)
    view["composition"] = mac["composition"]
    view["moves"] = mac["moves"]
    view["shape"] = mac["shape"]
    view["motion"] = mac.get("motion", d["motion"])
    view["pitfall"] = mac.get("pitfall", d["pitfall"])
    view["chrome"] = mac["chrome"]
    view["dials"] = {**d["dials"], **mac["dials"]}
    view["content"] = mac.get("content", d["content"])
    view["anchors"] = d["anchors"] + mac.get("anchors", [])
    return view


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    channels = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def contrast_report(scheme: dict) -> list[tuple[str, float, float, bool]]:
    """(label, ratio, required, hard). Hard failures break --check; soft ones are warnings."""
    return [
        ("ink on ground", contrast(scheme["ink"], scheme["ground"]), 4.5, True),
        ("ink on surface", contrast(scheme["ink"], scheme["surface"]), 4.5, True),
        ("ink2 on ground", contrast(scheme["ink2"], scheme["ground"]), 4.5, True),
        ("on_accent on accent", contrast(scheme["on_accent"], scheme["accent"]), 4.5, True),
        ("accent vs ground", contrast(scheme["accent"], scheme["ground"]), 3.0, False),
    ]


def sub_rng(seed: int, direction_id: str, slot: str) -> random.Random:
    # Independent stream per slot, so redealing one slot never shifts another.
    return random.Random(f"{seed}:{direction_id}:{slot}")


def deal_options(directions: list[dict], n: int, seed: int, preset: str | None,
                 sector: str | None, have: set[str] | None, content: list[str] | None = None,
                 platform: str | None = None) -> list[dict]:
    pool = [d for d in directions
            if (preset is None or d["preset"] == preset)
            and (sector is None or sector not in d["not_for"])
            and (have is None or set(d["needs"]) <= have)
            # The first content shape is what the user came for: a direction must be able to show it.
            and (not content or content[0] in d["content"])]
    rng = random.Random(seed)
    if preset is None:
        # Spread across presets first, so the options are real alternatives.
        by_preset: dict[str, list[dict]] = {}
        for d in pool:
            by_preset.setdefault(d["preset"], []).append(d)
        presets = list(by_preset)
        rng.shuffle(presets)
        # Within each preset, prefer directions that also hold the secondary content shapes.
        fit = lambda d: len(set(content[1:]) & set(d["content"])) if content else 0
        picked = []
        if platform == "macos":
            # Mac users reward Mac-native craft, so one option always comes from a Mac preset
            # (research/macos-references.md); the others stay a spread across all presets.
            native = [p for p in presets if p in MAC_PRESETS]
            if native and not any(p in MAC_PRESETS for p in presets[:n]):
                presets.remove(native[0])
                presets.insert(n - 1 if n > 0 else 0, native[0])
        for p in presets[:n]:
            best = max(fit(d) for d in by_preset[p])
            picked.append(rng.choice([d for d in by_preset[p] if fit(d) == best]))
        rest = [d for d in pool if d not in picked]
        rng.shuffle(rest)
        return (picked + rest)[:n]
    rng.shuffle(pool)
    return pool[:n]


def print_option(d: dict) -> None:
    dials = " ".join(f"{k}{v}" for k, v in d["dials"].items())
    print(f"- {d['id']}  ({d['preset']}) {d['name']}  [{dials}]")
    print(f"    anchors: {'; '.join(d['anchors'])}")
    print(f"    composition: {d['composition']}")
    print(f"    holds: {', '.join(d['content'])}")
    print(f"    idea slot: In this app, <inventory item> becomes {d['device']}.")
    if d["needs"]:
        print(f"    needs: {', '.join(d['needs'])}")
    if d["not_for"]:
        print(f"    not for: {', '.join(d['not_for'])}")


def print_scheme(label: str, scheme: dict) -> None:
    roles = "  ".join(f"{r} {scheme[r]}" for r in ROLES)
    print(f"  {label}: {roles}")
    for name, ratio, required, hard in contrast_report(scheme):
        verdict = "ok" if ratio >= required else ("FAIL" if hard else "warn: add a stroke or tone step")
        print(f"    {name}: {ratio:.1f}:1 (needs {required}) {verdict}")


def print_sheet(d: dict, seed: int, keep: set[str]) -> None:
    type_choice = sub_rng(seed, d["id"], "type").choice(d["type"])
    palette = sub_rng(seed, d["id"], "palette").choice(d["palettes"])
    dials = " ".join(f"{k}{v}" for k, v in d["dials"].items())
    platform = " on macOS" if "chrome" in d else ""
    print(f"DIRECTION {d['id']}: {d['name']}  (preset {d['preset']}, seed {seed}){platform}")
    print(f"Dials (defaults, user may override): {dials}")
    print(f"Anchors: {'; '.join(d['anchors'])}")
    print()
    print(f"Composition: {d['composition']}")
    print(f"Holds (content shapes): {', '.join(d['content'])}")
    print(f"Idea slot: In this app, <inventory item> becomes {d['device']}.")
    print()
    if "type" in keep:
        print("Type: kept from the brand; map its faces onto display / text / data.")
    else:
        print(f"Type: display {type_choice['display']} / text {type_choice['text']} / data {type_choice['data']}")
    if "palette" in keep:
        print("Palette: kept from the brand; map its colours onto ground / surface / ink / ink2 / accent / on_accent and run the contrast check.")
    else:
        print(f"Palette: {palette['name']}. {palette['proportions']}")
        if palette.get("support"):
            print(f"  support (role colours, never body text): {', '.join(palette['support'])}")
        if palette.get("ramp"):
            print(f"  ramp: {', '.join(palette['ramp'])} (re-check ink contrast at every stop)")
        print_scheme("light", palette["light"])
        print_scheme("dark", palette["dark"])
    print()
    print(f"Shape and depth: {d['shape']}")
    if "chrome" in d:
        print(f"Window chrome: {d['chrome']}")
        print("Mac type: keep the dealt faces, set them on the Mac scale (body 13 pt, rows 22-32 pt) with one display moment at 40-96 pt; see platform-macos.md section 6.")
    print("Signature moves (pick 2-3):")
    for m in d["moves"]:
        print(f"  - {m}")
    print("  After the build, point at each chosen move in the resting frame; at least two must show there.")
    print(f"Motion: {d['motion']}")
    if d["needs"]:
        print(f"Needs: {', '.join(d['needs'])}")
    print(f"How it goes wrong: {d['pitfall']}")
    print("Caps budget: at most two small uppercase labels per screen; caps belong at display size.")
    print()
    flag = " --platform macos" if "chrome" in d else ""
    print(f"Reproduce: deal.py --direction {d['id']} --seed {seed}{flag}")


def check_mac(d: dict) -> list[str]:
    if mac_only(d):
        problems = [] if d.get("chrome") else [f"{d['id']}: a Mac-only direction needs a chrome line"]
        if "mac" in d:
            problems.append(f"{d['id']}: a Mac-only direction is written for the Mac already; drop its mac block")
        if d["preset"] not in MAC_PRESETS:
            problems.append(f"{d['id']}: Mac-only directions belong to a Mac preset {MAC_PRESETS}")
        text = " ".join([d["composition"], d["shape"], d["chrome"], d["motion"], d["pitfall"], *d["moves"]])
        leaks = sorted({m.group(0).lower() for m in PHONE_WORDS.finditer(text)})
        if leaks:
            problems.append(f"{d['id']}: phone mechanics in a Mac-only direction: {leaks}")
        return problems
    if d["preset"] in MAC_PRESETS:
        return [f"{d['id']}: a {d['preset']} direction must be Mac-only (platforms: [\"macos\"])"]
    if "mac" not in d:
        return [f"{d['id']}: missing mac block (or mark it platforms: [\"macos\"])"]
    mac = d["mac"]
    if "skip" in mac:
        return [] if mac["skip"].strip() else [f"{d['id']} / mac: skip needs a reason"]
    problems = [f"{d['id']} / mac: missing {k}" for k in MAC_REQUIRED if k not in mac]
    if problems:
        return problems
    if len(mac["moves"]) < 2:
        problems.append(f"{d['id']} / mac: needs at least two moves")
    bad_dials = [k for k in mac["dials"] if k not in d["dials"]]
    if bad_dials:
        problems.append(f"{d['id']} / mac: unknown dials {bad_dials}")
    bad = [c for c in mac.get("content", []) if c not in SHAPES]
    if bad:
        problems.append(f"{d['id']} / mac: content shapes {bad} not in {SHAPES}")
    text = " ".join([mac["composition"], mac["shape"], mac["chrome"], mac.get("motion", d["motion"]),
                     mac.get("pitfall", d["pitfall"]), *mac["moves"]])
    leaks = sorted({m.group(0).lower() for m in PHONE_WORDS.finditer(text)})
    if leaks:
        problems.append(f"{d['id']} / mac: phone mechanics in the Mac block (or the motion and pitfall it inherits): {leaks}")
    return problems


def check(directions: list[dict]) -> int:
    problems = []
    ids = set()
    for d in directions:
        missing = [k for k in REQUIRED if k not in d]
        if missing:
            problems.append(f"{d.get('id', '?')}: missing {missing}")
            continue
        if d["id"] in ids:
            problems.append(f"{d['id']}: duplicate id")
        ids.add(d["id"])
        bad = [c for c in d["content"] if c not in SHAPES]
        if bad or not d["content"]:
            problems.append(f"{d['id']}: content shapes {bad or 'missing'} not in {SHAPES}")
        if d["preset"] not in PRESETS:
            problems.append(f"{d['id']}: unknown preset {d['preset']}")
        for p in d["palettes"]:
            for mode in ("light", "dark"):
                scheme = p[mode]
                absent = [r for r in ROLES if r not in scheme]
                if absent:
                    problems.append(f"{d['id']} / {p['name']} / {mode}: missing roles {absent}")
                    continue
                for name, ratio, required, hard in contrast_report(scheme):
                    if hard and ratio < required:
                        problems.append(f"{d['id']} / {p['name']} / {mode}: {name} {ratio:.2f}:1 < {required}")
        problems += check_mac(d)
    counts = {p: sum(1 for d in directions if d["preset"] == p) for p in PRESETS}
    on_mac = sum(1 for d in directions if for_platform(d, "macos") is not None)
    for line in problems:
        print(f"FAIL {line}")
    print(f"{len(directions)} directions {counts}, {on_mac} with a Mac form; {len(problems)} problem(s)")
    return 1 if problems else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--options", type=int, help="deal N direction summaries to choose from")
    ap.add_argument("--direction", help="print the full sheet for one direction id")
    ap.add_argument("--preset", choices=PRESETS, help="deal only within this preset (the user named it)")
    ap.add_argument("--sector", help="exclude directions marked not_for this sector, e.g. finance, health, kids")
    ap.add_argument("--content", help="content shapes the screen must show at rest, primary first, comma-separated: " + ", ".join(SHAPES))
    ap.add_argument("--have", help="assets that really exist, comma-separated: photography (default: none, so photo-dependent directions are skipped)")
    ap.add_argument("--platform", choices=("ios", "android", "macos"),
                    help="macos deals each direction's Mac window form and drops those without one (default: phone)")
    ap.add_argument("--keep", default="", help="brand-fixed slots to leave undealt: palette, type")
    ap.add_argument("--seed", type=int, help="reuse a seed to reproduce a deal")
    ap.add_argument("--list", action="store_true", help="list all direction ids")
    ap.add_argument("--check", action="store_true", help="validate the library (fields and contrast)")
    args = ap.parse_args()

    directions = load()
    if args.check:
        return check(directions)
    if args.platform == "macos":
        skipped = [d["id"] for d in directions if for_platform(d, "macos") is None]
        directions = [v for v in (for_platform(d, "macos") for d in directions) if v is not None]
    else:
        # Phone (or unspecified): Mac-only directions are not dealt.
        skipped = [d["id"] for d in directions if mac_only(d)]
        directions = [d for d in directions if not mac_only(d)]
    if args.list:
        for d in directions:
            print(f"{d['id']:24} {d['preset']:14} {d['name']}")
        return 0

    seed = args.seed if args.seed is not None else random.SystemRandom().randrange(10_000, 100_000)
    if args.direction:
        match = [d for d in directions if d["id"] == args.direction]
        if not match:
            if args.direction in skipped:
                d = next(d for d in load() if d["id"] == args.direction)
                if mac_only(d):
                    print(f"{args.direction} is Mac-only; pass --platform macos", file=sys.stderr)
                else:
                    print(f"{args.direction} has no macOS form: {d['mac']['skip']}", file=sys.stderr)
            else:
                print(f"unknown direction {args.direction}; see --list", file=sys.stderr)
            return 2
        print_sheet(match[0], seed, {k.strip() for k in args.keep.split(",") if k.strip()})
        return 0
    if args.options:
        # No --have means no assets: directions that need photographs are not dealt (taste-skill's default).
        have = {h.strip() for h in (args.have or "").split(",") if h.strip()}
        content = [c.strip() for c in (args.content or "").split(",") if c.strip()]
        unknown = [c for c in content if c not in SHAPES]
        if unknown:
            print(f"unknown content shape(s) {unknown}; choose from {SHAPES}", file=sys.stderr)
            return 2
        dealt = deal_options(directions, args.options, seed, args.preset, args.sector, have, content, args.platform)
        if not dealt:
            print("no direction matches those filters", file=sys.stderr)
            return 2
        print(f"Dealt {len(dealt)} direction(s), seed {seed}. Hold each against the inventory; choose the one that can carry something only this product has.")
        for d in dealt:
            print_option(d)
        flag = " --platform macos" if args.platform == "macos" else ""
        print(f"\nThen: deal.py --direction <id> --seed {seed}{flag}")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
