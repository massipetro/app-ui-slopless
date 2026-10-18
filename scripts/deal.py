#!/usr/bin/env python3
"""Deal researched design directions for app-ui-slopless.

Asked to invent a look, a model picks the category default every time. This
script deals directions from library/directions.json instead; the model then
chooses among them against the product inventory.

  deal.py --options 3 [--preset P] [--sector S] [--have photography] [--seed N]
  deal.py --direction ID [--seed N] [--keep palette,type]
  deal.py --list
  deal.py --check

Standard library only; works on Python 3.9.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

LIBRARY = Path(__file__).resolve().parent.parent / "library" / "directions.json"
PRESETS = ("warm-premium", "neo-brutalist", "playful", "editorial")
ROLES = ("ground", "surface", "ink", "ink2", "accent", "on_accent")
REQUIRED = ("id", "preset", "name", "anchors", "composition", "device", "dials",
            "type", "palettes", "shape", "moves", "motion", "needs", "not_for", "pitfall")


def load() -> list[dict]:
    return json.loads(LIBRARY.read_text())["directions"]


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
                 sector: str | None, have: set[str] | None) -> list[dict]:
    pool = [d for d in directions
            if (preset is None or d["preset"] == preset)
            and (sector is None or sector not in d["not_for"])
            and (have is None or set(d["needs"]) <= have)]
    rng = random.Random(seed)
    if preset is None:
        # Spread across presets first, so the options are real alternatives.
        by_preset: dict[str, list[dict]] = {}
        for d in pool:
            by_preset.setdefault(d["preset"], []).append(d)
        presets = list(by_preset)
        rng.shuffle(presets)
        picked = [rng.choice(by_preset[p]) for p in presets[:n]]
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
    print(f"DIRECTION {d['id']}: {d['name']}  (preset {d['preset']}, seed {seed})")
    print(f"Dials (defaults, user may override): {dials}")
    print(f"Anchors: {'; '.join(d['anchors'])}")
    print()
    print(f"Composition: {d['composition']}")
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
    print("Signature moves (pick 2-3):")
    for m in d["moves"]:
        print(f"  - {m}")
    print(f"Motion: {d['motion']}")
    if d["needs"]:
        print(f"Needs: {', '.join(d['needs'])}")
    print(f"How it goes wrong: {d['pitfall']}")
    print()
    print(f"Reproduce: deal.py --direction {d['id']} --seed {seed}")


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
    counts = {p: sum(1 for d in directions if d["preset"] == p) for p in PRESETS}
    for line in problems:
        print(f"FAIL {line}")
    print(f"{len(directions)} directions {counts}; {len(problems)} problem(s)")
    return 1 if problems else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--options", type=int, help="deal N direction summaries to choose from")
    ap.add_argument("--direction", help="print the full sheet for one direction id")
    ap.add_argument("--preset", choices=PRESETS, help="deal only within this preset (the user named it)")
    ap.add_argument("--sector", help="exclude directions marked not_for this sector, e.g. finance, health, kids")
    ap.add_argument("--have", help="assets that really exist, comma-separated: photography (default: none, so photo-dependent directions are skipped)")
    ap.add_argument("--keep", default="", help="brand-fixed slots to leave undealt: palette, type")
    ap.add_argument("--seed", type=int, help="reuse a seed to reproduce a deal")
    ap.add_argument("--list", action="store_true", help="list all direction ids")
    ap.add_argument("--check", action="store_true", help="validate the library (fields and contrast)")
    args = ap.parse_args()

    directions = load()
    if args.check:
        return check(directions)
    if args.list:
        for d in directions:
            print(f"{d['id']:24} {d['preset']:14} {d['name']}")
        return 0

    seed = args.seed if args.seed is not None else random.SystemRandom().randrange(10_000, 100_000)
    if args.direction:
        match = [d for d in directions if d["id"] == args.direction]
        if not match:
            print(f"unknown direction {args.direction}; see --list", file=sys.stderr)
            return 2
        print_sheet(match[0], seed, {k.strip() for k in args.keep.split(",") if k.strip()})
        return 0
    if args.options:
        # No --have means no assets: directions that need photographs are not dealt (taste-skill's default).
        have = {h.strip() for h in (args.have or "").split(",") if h.strip()}
        dealt = deal_options(directions, args.options, seed, args.preset, args.sector, have)
        if not dealt:
            print("no direction matches those filters", file=sys.stderr)
            return 2
        print(f"Dealt {len(dealt)} direction(s), seed {seed}. Hold each against the inventory; choose the one that can carry something only this product has.")
        for d in dealt:
            print_option(d)
        print(f"\nThen: deal.py --direction <id> --seed {seed}")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
