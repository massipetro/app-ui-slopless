# app-ui-slopless

An Agent Skill for building **bold, non-generic mobile UI** for iOS (SwiftUI) and Android (Jetpack Compose / Compose Multiplatform), grounded in studied UX principles rather than vibes.

Two failure modes, equally avoided:
- **Slop:** the default AI look. Grey cards with soft shadows, purple gradients, Inter everywhere, emoji icons.
- **Pretty but broken:** bold styling on a flow that's hard to use.

Studied bones, unmistakable skin.

## What it does

| Mode | Example request |
|---|---|
| **Build** | "Build the home screen of my habit app, playful style" |
| **Redesign** | "My profile screen is boring, redesign it neo-brutalist" |
| **Audit** | "UX audit of this checkout screen, then redesign it" |
| **Spec** | "Give me a design system / tokens for this app" |

You pick the style: **one of four presets, then tune five dials.**

| Preset | Feel | Real-world anchors |
|---|---|---|
| Warm premium | photo-led, confident type, one owned accent | Airbnb, Uber, Monzo, Flighty |
| Neo-brutalist | thick strokes, hard offset shadows, flat clashing colour | Gumroad, Figma, Nothing, Teenage Engineering |
| Playful / toy | chunky lipped pieces, custom glyphs, a mascot, springy motion | Duolingo, (Not Boring) Habits, Headspace |
| Editorial | huge display type, magazine grids, stark contrast | Spotify Mix/Wrapped, NYT Games, Nike SNKRS |

Dials (1–10): `BOLDNESS`, `MOTION`, `DENSITY`, `COLOR`, `FIDELITY` (how bespoke the components look; platform mechanics stay native).

Every run:
1. Lists what only this product has, names the screen's content shapes, then **deals three researched directions** that can show them (`scripts/deal.py`, 20 directions anchored in shipped apps) instead of reaching for the category default, and drops any that fail a fit test (content at rest, owned idea, costume test) before picking one.
2. Writes a short **design brief** around an owned idea that must pass a competitor test: owned idea, live interaction, persona, type, colour, icons, motion, signature moves.
3. Builds tokens first, then components, then the screen, following a **code baseline** (stable identity, state that survives, transforms not layout).
4. **Compiles and lints the code** (`scripts/typecheck.py` for Swift, Gradle for Kotlin where a project exists; `scripts/lint.py`), then **renders the result and looks at it** twice over: a craft pass (clipped, stretched, off-centre) and a scored taste pass (one-second glance, squint, cover the logo, fullness), at most two fix rounds.
5. Reports accessibility trade-offs as warnings (it doesn't silently block bold choices).

## Grounded in

Norman, Nielsen, Shneiderman, Fitts, Hick–Hyman, Cowan, Hoober, Clark, Budiu/NN/g, Cooper, Wroblewski, Bringhurst, Lupton, Albers, Tufte, Chang & Ungar, Willenskomer, Saffer, Walter, Kurosu & Kashimura, Tractinsky, Lindgaard, Tuch, Hassenzahl, Apple HIG, Material 3, and WCAG 2.2. See [`research/literature.md`](research/literature.md); every claim is tagged by how well it's verified.

The visual references are **real shipped apps** (Apple Design Award winners, design-team case studies), not AI concept shots. See [`research/real-ui-references.md`](research/real-ui-references.md).

## Install

Claude Code plugin (updates with `/plugin update`). Run these inside Claude Code:
```
/plugin marketplace add massipetro/app-ui-slopless
/plugin install app-ui-slopless@app-ui-slopless
```

Claude Code (personal, as a plain skill):
```bash
git clone https://github.com/massipetro/app-ui-slopless ~/.claude/skills/app-ui-slopless
```

Or any agent that supports the Agent Skills format: copy the folder into its skills directory.

**Companion skills** for deeper code correctness (optional): [twostraws/swiftui-agent-skill](https://github.com/twostraws/swiftui-agent-skill) for SwiftUI, and [aldefy/compose-skill](https://github.com/aldefy/compose-skill) for Compose/CMP. See [`research/code-baseline.md`](research/code-baseline.md).

## Layout

```
SKILL.md                    workflow, core rules, motion budget, slop tells, checklist
references/
  principles.md             rule IDs (R-TOUCH-2 …) with sources, for audits
  audit.md                  audit process + report template
  platform-swiftui.md       SwiftUI patterns + code baseline
  platform-compose.md       Compose / CMP patterns + code baseline
  presets/*.md              one file per style
  critique.md               the scored taste pass on screenshots
library/directions.json     20 dealt directions (5 per preset), with palettes checked for contrast
scripts/deal.py             deals directions; --check validates the library (Python 3.9+, stdlib only)
scripts/lint.py             FAIL/WARN gate for slop tells, craft defects and code-baseline patterns in .swift / .kt
scripts/typecheck.py        typechecks SwiftUI files against the iOS simulator SDK, no Xcode project needed
research/                   the source material behind the rules
evals/                      test prompts, input files, grade.py
```

## Evals

Six build briefs, each run with and without the skill and judged blind from screenshots with `references/critique.md`, plus `evals/grade.py` for objective craft and slop checks (it reuses `scripts/lint.py`). Full method, per-eval scores and limits: [`evals/README.md`](evals/README.md).

| Round | Builds | Briefs | Blind wins for the skill | Average margin |
|---|---|---|---|---|
| 5 | Opus 5.5, Opus judge | ferry, flat budget × 3 runs | 4 of 6 | +0.4 |
| 4 | Opus 5.5, Opus judge | all six | 4 of 6 | +0.6 |
| 3 | Opus 5.5, Sonnet judge | all six | 6 of 6 (one tie on score) | +1.4 |
| 2 | Opus 5.5 | ferry, flat budget | 2 of 2 | +0.5 |
| 1 | Sonnet 5 | ferry, flat budget | 2 of 2 | +1.5 |

Rounds 1–3 were judged by Sonnet; rounds 4–5 by Opus 5.5, which applied the caps more strictly. In round 5, with three runs per config, every skill run followed the full process (13 / 13 grader checks, the complete report block, 0 lint FAILs) and the blind margin averaged +0.4. In round 4 the skill's outputs had 0 lint FAILs across six screens against 51 without it, and the skill runs cost about 1.9× as much. Both losses trace to defects the skill already names (a row cut behind the pinned bar, too many small caps labels). One run per config and one model judge per pair: treat each score as ±0.5.

## Licence

MIT. See [LICENSE](LICENSE).
