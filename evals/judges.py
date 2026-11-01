"""Prompts for the blind eval judges, so every round's harness uses the same words.

A harness's make_pairs.py imports this module: it copies A.png and B.png (and for the access judge
A-ax5.png and B-ax5.png) and references/critique.md into each pair's folder, and writes
prompt(kind, brief) to prompt.txt. Three independent judges per pair, so every pair has a majority.

  phone   rounds 1-20: two 390x844 phone renders, the five criteria of critique.md before round 22
  mac     rounds 10-21: two 1280x800 Mac windows
  access  round 22 on: each screen at the default text size and at the largest (iOS AX5 or Android
          font scale 2.0), scored on the six criteria including Access (critique.md pass 15, from
          the pixels). Use it for any brief that asks for accessibility, and for any phone brief from
          now on, since critique.md scores Access everywhere. Round 22 used this prompt with iOS-only
          wording ("renders of the same SwiftUI code on the iOS Simulator") and without the clause
          "is the thing to act on now still in the first screen", which was added after that round.

The tally reads the last lines: SCORE A / SCORE B / WINNER, and with the access judge ACCESS A /
ACCESS B as well.
"""
from __future__ import annotations

END = ("Then say which is better and why in under 120 words. End with exactly these three lines: "
       "'SCORE A: <overall>', 'SCORE B: <overall>', 'WINNER: A' or 'WINNER: B'. Do not guess which tool produced either.")

PHONE = ("You are a blind design judge. Two phone screens, A.png and B.png (390x844 renders at @2x of HTML mocks standing in "
         "for a native app screen), answer this brief: '{brief}' Read critique.md in this folder, then look at both images "
         "(Read tool) and score EACH with its passes, criteria and caps: Idea, Hierarchy, Craft, Substance, Platform (judge "
         "Platform as a native phone app: safe areas, touch targets, readable text sizes, platform mechanics), each 1-10, an "
         "overall, and any cap that applies. " + END)

MAC = ("You are a blind design judge. Two Mac app windows, A.png and B.png (1280x800 renders of HTML mocks standing in for a "
       "native macOS SwiftUI app), answer this brief: '{brief}' Read critique.md in this folder, then look at both images "
       "(Read tool) and score EACH with its passes, criteria and caps: Idea, Hierarchy, Craft, Substance, Platform (judge "
       "Platform as macOS: sidebar/toolbar, density, window chrome, not a stretched phone), each 1-10, an overall, and any "
       "cap that applies. " + END)

ACCESS = ("You are a blind design and accessibility judge. Two {device} screens, A and B, answer this brief: '{brief}' "
          "For each screen you get two renders of the same code: A.png at the default text size and A-ax5.png at the largest "
          "accessibility text size ({largest}); B.png and B-ax5.png the same. Read critique.md in this folder, then look at "
          "all four images (Read tool) and score EACH screen with its passes, criteria and caps: Idea, Hierarchy, Craft, "
          "Substance, Platform, each 1-10, and Access, 1-10: critique pass 15 from the pixels (at the largest size, does text "
          "that carries meaning clip, truncate or overlap; does the layout reflow; is the thing to act on now still in the "
          "first screen; does every state read without colour; are contrast and target sizes enough for an older user with "
          "low vision or a tremor). Overall is the mean of the six, then apply the caps. Then say which is better and why in "
          "under 120 words. End with exactly these five lines: 'ACCESS A: <n>', 'ACCESS B: <n>', 'SCORE A: <overall>', "
          "'SCORE B: <overall>', 'WINNER: A' or 'WINNER: B'. Do not guess which tool produced either.")

LARGEST = {"ios": ("iPhone", "AX5, body text about three times larger"),
           "android": ("Android phone", "font scale 2.0, small text about twice as large")}


def prompt(kind: str, brief: str, platform: str = "ios") -> str:
    if kind == "phone":
        return PHONE.format(brief=brief)
    if kind == "mac":
        return MAC.format(brief=brief)
    if kind == "access":
        device, largest = LARGEST[platform]
        return ACCESS.format(brief=brief, device=device, largest=largest)
    raise ValueError(f"unknown judge kind {kind!r}: phone, mac or access")
