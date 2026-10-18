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
1. Writes a short **design brief**: owned idea, persona, type, colour, icons, motion, signature moves.
2. Builds tokens first, then components, then the screen, following a **code baseline** (stable identity, state that survives, transforms not layout).
3. **Renders the result and looks at it**, fixing clipped, stretched or off-centre elements.
4. Reports accessibility trade-offs as warnings (it doesn't silently block bold choices).

## Grounded in

Norman, Nielsen, Shneiderman, Fitts, Hick–Hyman, Cowan, Hoober, Clark, Budiu/NN/g, Cooper, Wroblewski, Bringhurst, Lupton, Albers, Tufte, Chang & Ungar, Willenskomer, Saffer, Walter, Kurosu & Kashimura, Tractinsky, Lindgaard, Tuch, Hassenzahl, Apple HIG, Material 3, and WCAG 2.2. See [`research/literature.md`](research/literature.md); every claim is tagged by how well it's verified.

The visual references are **real shipped apps** (Apple Design Award winners, design-team case studies), not AI concept shots. See [`research/real-ui-references.md`](research/real-ui-references.md).

## Install

Claude Code (personal):
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
research/                   the source material behind the rules
evals/                      test prompts, input files, grade.py
```

## Evals

Three prompts (playful CMP home screen, neo-brutalist SwiftUI redesign, Compose checkout audit + warm-premium redesign), each run with and without the skill. `evals/grade.py` runs objective checks for craft and slop tells; humans judge the visuals.

| Round | Model | With skill | Without |
|---|---|---|---|
| 3 | Sonnet 5.5 (medium) | 100% | 76% |
| 2 | Sonnet 5.5 (medium) | 100% | 75% |
| 1 | Opus 5.5 | 100% | 92% |

## Licence

MIT. See [LICENSE](LICENSE).
