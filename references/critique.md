# Critique: judging the render

The craft pass in step 5 finds what's broken. This file finds out whether the screen is *good*. Use it on the screenshots, never on the code. You wrote the code, so you'll read your intentions into it; the picture only shows what's there.

Look at each screenshot at phone size (not zoomed), light and dark if both were rendered, and one large-text render if you have it. Make each pass on its own; don't blend them.

## Contents
1. The passes
2. The score and its caps
3. Writing the critique
4. What to fix first
5. When to stop

## 1. The passes

1. **One second.** Glance at the screen and look away. What did you see? There should be exactly one answer: the number, the object, the headline, the mascot. If the answer is "an app" or "some cards", the screen has no focal point.
2. **Squint.** Blur your attention until text turns into grey bars. The screen should reduce to two or three masses with clearly different sizes. Many similar medium masses (the 2×2 stat-card grid) means nothing leads.
3. **Cover the logo.** Hide the app's name. Could this screen belong to the nearest competitor you named in the brief, or to a different category entirely? If swapping the name would give an equally valid screen, the owned idea isn't visible here. Find where it should show and make it show.
4. **Idea reach.** When you built more than one screen or state: does the idea reach the empty state, errors, settings, sheets and the paywall, or does the app turn stock after the home screen? A distinctive first screen followed by default screens is the commonest failure.
5. **Sameness.** Write one word for each block on the screen (hero, board, rail, list, grid, cards, sheet, chart, number). The same word three times on one screen, or every screen opening with the same block, is the template showing. Also check: is every corner radius the same? Is every gap the same?
6. **Type.** Is the jump from body text to the display moment decisive (three times or more)? More than six sizes visible? Count the tiny letter-spaced uppercase labels: more than one or two (an eyebrow above every heading, a caps label on every value) is a tell even inside a direction that uses caps, and the linter can't see it. A big headline with one orphan word on its last line? Is the key number the biggest thing on the screen, and does it fit at its widest real value?
7. **Colour.** Name the proportions: what holds most of the surface, what supports, where the accent is. An accent in ten places means nothing; on the one action and one detail it means "here". Does the accent mean the same thing on every screen? Does dark mode hold up, or is it inverted grey?
8. **Thumb.** Picture the phone in one hand. Is the primary action in the bottom third? Is there one obvious primary action? Do the targets look at least 44 pt / 48 dp, with destructive actions away from frequent ones?
9. **Fullness and substance.** Is the content at real density (long names, wide numbers, enough rows to scroll)? Could the screen be mistaken for a wireframe: grey shapes, grey text, one small column? Is any region empty by accident (a hole) rather than by decision? Would the user leave knowing what they came to find out?
10. **Signature.** Could someone pick out the two or three signature moves from this still? Is the live thing visible, or at least hinted at (its current state, its affordance)?
11. **Platform.** Does it still behave like the platform where it must: a visible back affordance, safe areas and system bars respected, the native sheet and keyboard? At large text, does the layout reflow or does it clip?
12. **Slop tells.** Any tell from the SKILL.md list that you can't defend in one sentence?

## 2. The score and its caps

Score five criteria from 0 to 10. Be a hard judge: **7 is a good shipped app; 9 is Apple Design Award level.** Most first renders land at 5–6.

| Criterion | Passes | 9–10 looks like |
|---|---|---|
| **Idea** | 3, 4, 10 | Unmistakably this product; the idea is on every surface and the live thing is there |
| **Hierarchy** | 1, 2, 6, 7 | One answer at a glance, two or three masses, decisive type jumps, an accent that means "here" |
| **Craft** | the craft pass, 5 | Nothing clipped, stretched, off-centre or uneven; rhythm varies on purpose |
| **Substance** | 9 | Real content at real density; every state designed; nothing reads as a wireframe |
| **Platform & access** | 8, 11, contrast | Thumb-zone primary, 44/48 targets, native mechanics intact, text scales, contrast holds in both modes |

**Overall** = the mean, then apply the caps:
- Any visible craft defect (clipping, overlap, content under a bar, an invisible signifier): Craft ≤ 4 and overall ≤ 6.
- Cover-the-logo fails: Idea ≤ 4.
- Any slop tell without a stated reason: overall ≤ 6.
- The screen reads as a wireframe: Substance ≤ 3.
- The only primary action is out of thumb reach, or primary targets are under 44/48: Platform ≤ 5.

The aim is overall ≥ 8 with no criterion below 6.

## 3. Writing the critique

Write it in your reply, in this format, before fixing anything. Each round goes in the reply, so the user can see what you looked at and why you changed it:

```
Critique round <n>: <screens and modes looked at>
One second: <what you saw>
Squint: <the masses, largest first>
Cover the logo: <competitor> → <could / couldn't be theirs, and why>
Idea reach: <which screens and states carry the idea, which turn stock>
Sameness: <one word per block>
Type: <sizes in use, the display moment, any orphan or fit problem>
Colour: <proportions; where the accent is>
Thumb: <primary action position, target sizes>
Fullness: <density, holes, wireframe risk>
Signature: <which moves are visible; the live thing>
Platform: <back, insets, large text>
Tells: <any, with reason or "none">
Scores: Idea n · Hierarchy n · Craft n · Substance n · Platform n → overall n (caps: <which applied>)
Top three fixes: 1. … 2. … 3. …
```

## 4. What to fix first

1. **Broken things.** Any craft defect, because one clipped number makes a bold design look broken (Tuch et al. 2012).
2. **The idea.** If the cover-the-logo test failed, no amount of polish will save the screen. Go back to the inventory and the direction sheet.
3. **Hierarchy.** Make the main thing bigger and everything else smaller before adjusting anything else.
4. **Substance.** Fill the content and the states.
5. **Polish.** Rhythm, colour proportions, motion details.

Fix the top three, render again, and critique the new screenshots, not your memory of the old ones.

## 5. When to stop

After **two rounds**, or as soon as the overall is ≥ 8 with no criterion below 6. More rounds cost the user time and tokens for diminishing returns. Report the final scores honestly, with what still falls short and what you'd do next. A 6 reported as a 6 is more useful than a 6 reported as an 8.
