# Audit mode

How to critique an existing mobile or Mac screen against the studied principles. For a Mac app also read `platform-macos.md` and use the `R-MAC-*` rules in `principles.md` in place of the touch and reach rules. Read `principles.md` first; every finding cites one of its rule IDs.

## Process
1. **Understand the screen.** Who is the primary user, what is their goal here, how often do they come, and what platform(s) is it for? If the code alone doesn't say, infer it and state the assumption.
2. **Walk the gulfs** (Norman). Can the user tell what to do (execution)? Can they tell what happened (evaluation)?
3. **Sweep by category:** signifiers & feedback → reach & targets → structure & memory → forms & errors → type/colour/hierarchy → motion → platform mechanics → accessibility → slop tells → personality.
4. **Measure, don't guess.** Compute contrast ratios from the hex values. Read target sizes off the modifiers. Count type sizes. Quote the line.
5. **Rate severity** (Nielsen's 0–4 scale):
   - **4 Catastrophe:** blocks the task or excludes users (unlabelled control for screen readers, primary CTA unreachable, data loss).
   - **3 Major:** frequent friction or likely errors (placeholder-only labels, sub-44 targets on a primary action, illegible contrast).
   - **2 Minor:** slows people down or confuses them occasionally.
   - **1 Cosmetic:** polish; fix if time allows.
   - Slop and blandness findings are usually 1–2, but say so explicitly. Blandness has a measured cost (R-COG-1, evidence table).
6. **Taste, from the screenshot.** If you have a screenshot or can render the screen, run the passes in `critique.md` and include its scores. Cover-the-logo and fullness findings are often the real reason a screen "feels meh".
7. **Then the redesign direction.** Read the existing look and identity assets, inventory the product (SKILL.md step 1), deal directions with `scripts/deal.py --options 3`, put them through the fit test including category fit, and recommend the one that carries something only this product has and keeps its identity assets. If the user already chose a preset, use it, and warn once if the fit table lists it as a poor fit.

## Report template

```markdown
# UX audit: <screen> (<platform>)

**Context assumed:** <user, goal, frequency; for macOS also the window sizes it must hold and the input it expects (pointer, keyboard, trackpad)>
**Verdict:** <2–3 sentences: the biggest problems and the overall impression>

## Findings
| # | Sev | Finding | Where | Rule | Fix |
|---|---|---|---|---|---|
| 1 | 4 | Card number field has no persistent label; placeholder vanishes on typing | `CheckoutScreen.kt:42` | R-FORM-1 | Top label "Card number", `KeyboardType.Number`, autofill `CreditCardNumber` |
| 2 | 3 | (macOS) Custom row button has no hover state and no right-click menu | `VoyageRow.swift:31` | R-MAC-3 | `.onHover` fill, `.contextMenu { }`, `.help` on the icon buttons |
| … | | | | | |

## Measurements
- Contrast: <pair> = <ratio> (needs <n>)
- Targets: <element> = <size> (needs 44 pt / 48 dp; macOS: ≥22 pt control, ≥24×24 pt icon button)
- Type sizes in use: <list> → <count>; display moment: yes/no

## What's working
<1–3 bullets: keep these>

## Redesign direction
Current look: <closest preset + identity assets>. Direction: <id> (seed <n>), dials: B<n> M<n> D<n> C<n> F<n>, and why it beats the other two dealt (product category + existing look). Keeps: <assets>. Owned idea: In this app, <inventory item> becomes <device>. Signature moves: <2–3>.
```

Order the findings by severity, then by frequency of use. Keep each finding to one line. The fix should be concrete enough to implement.

## Computing contrast quickly

Relative luminance per channel: c = v/255; c ≤ 0.04045 ? c/12.92 : ((c+0.055)/1.055)^2.4. L = 0.2126 R + 0.7152 G + 0.0722 B. Ratio = (L1+0.05)/(L2+0.05).

For text on translucent surfaces, composite the colours first (alpha-blend over what's behind), then compute. For text on gradients, check against the *worst* stop.

If a shell is available, a one-liner is faster than mental arithmetic:
`python3 -c "f=lambda h:[(c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4) for c in [int(h[i:i+2],16)/255 for i in (0,2,4)]];L=lambda h:sum(w*c for w,c in zip((.2126,.7152,.0722),f(h)));a,b=sorted([L('FFFFFF'),L('9C6BFF')]);print(round((b+.05)/(a+.05),2))"`
