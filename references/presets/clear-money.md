# Preset: Clear money

**Feel:** sober, exact numbers; the fun lives in the containers people name. Every figure is tabular, formatted by the locale and never clipped, and the first screen is safe to look at on a bad day. The personality goes into the pots, vaults, jars and cards: their shape, their colour, their fill, the one gesture that moves money between them. Think of a well-made wallet with coloured envelopes in it. The leather is quiet, and the envelopes are yours.

**Dealt for finance.** `deal.py --sector finance` brings this preset into the deal, and one of the options always comes from it. It is also dealt by name (`--preset clear-money`). It never joins a deal for another sector, because its devices (pots, a ledger, a wallet) only belong where money is the content.

**Fits:** current accounts and neobanks, savings and pots, multi-currency wallets, budgeting across accounts, joint accounts and shared pots, teen and student banking (the pot shelf), pensions at a glance. A flat's grocery kitty or a bill splitter is not banking: deal it without `--sector finance`.
**Doesn't fit:** trading and brokerage screens that invite trades (use calm dials, and on a Mac *pro instrument*; never celebrate a trade), B2B treasury and accounting tools (pro instrument), insurance claims (warm premium, calm dials), crypto speculation.

**Default dials:** `BOLDNESS 5–6 · MOTION 3–6 · DENSITY 4–6 · COLOR 3–6 · FIDELITY 5–7` (the direction decides: the passbook is calm at M3 C3, the pot shelf lively at M6 C6).

Sources and evidence: `research/money-references.md`.

## Real anchors
- **Up (Saver Pools, Pull-to-Save).** Savers began as donut rings and became containers whose contents move with the phone, each with the user's emoji. Pull-to-Save flicks the spare cents into a Saver with one gesture. The team was openly cautious about gamifying banking. [Up blog](https://up.com.au/blog/the-evolutionary-design-of-up/)
- **Monzo Pots.** The user names each pot and gives it a picture. One hot-coral card is the only loud thing in the brand. [Monzo](https://monzo.com/blog/2019/08/09/how-were-doing-savings-accounts-differently) · [Creative Review](https://www.creativereview.co.uk/monzo-branding-ragged-edge/)
- **Revolut 10 (2023).** All your money on one home screen across accounts, currencies and pockets, with themes and backgrounds as personal fun. Flip the phone to blur balances, on by default. [Fintech News](https://fintechnews.sg/78771/digital-banking-news-singapore/revolut-launches-its-biggest-update-yet-for-over-35-million-users/) · [Revolut help](https://help.revolut.com/en-AU/help/profile-and-plan/security-and-personal-data/why-is-my-balance-blurry)
- **Wise.** Green instead of fintech blue, the bespoke Wise Sans set heavy and big, and jars beside the currency balances. [Creative Review](https://www.creativereview.co.uk/wise-rebrand-ragged-edge/) · [Wise help](https://wise.com/help/articles/645Ve1Ah1Psi0srHGfKYmm/your-wise-account-has-a-new-look)
- **Apple Card.** Each spending category owns a colour, and the card blends the colours of what you spent on: data as colour, always labelled. [creditcards.com](https://creditcards.com/card-advice/apple-card-colors)
- **bunq.** Up to 25 accounts, each with its own picture. [DutchReview](https://dutchreview.com/expat/best-bunq-features/)
- **Copilot Money (ADA finalist 2024).** Calm through native craft: "It's all native; we just tweak it a lot." [Apple Developer](https://developer-rno.apple.com/articles/copilot-money)

## The money rules (from the literature, every direction)
1. **Money lives in named containers.** People keep separate mental accounts (Thaler 1999); partitions slow spending because opening one feels like a transgression (Cheema & Soman 2008); labelled accounts raised saving by about 30% in Malawi. So show pots as *things*, each with its label printed on it in the user's words. Never "Savings 2".
2. **One goal leads.** A single savings goal beat several in Soman & Zhao (2011). Allow many pots, but make one clearly bigger on the home screen and let the user choose which.
3. **Say what's left.** Near a goal, show the amount to go ("£40 to go"), not only a percentage (goal gradient, Kivetz et al. 2006). Progress is never faked or rounded up.
4. **The first screen is safe to look at.** People avoid checking when they expect bad news (the ostrich effect). Lead with the figure that helps ("£214 left until Friday"). Say bad news in plain words with one next step, never as an alarm-red screen. Balances hide with one gesture (Revolut's flip, N26's discreet mode), stay out of notifications and the app switcher, and VoiceOver reads them as "balance hidden".
5. **Delight only for saving, paying off and reaching a goal.** The FCA found that confetti, badges and leaderboards raise trading frequency and risk, most among young and less financially literate users. No celebration on spending, trading, borrowing or crypto; no streaks for logging in.
6. **Asymmetric friction.** Protective settings (a gambling block, a locked pot, spending limits) are one step to turn on and deliberately slower to turn off (Monzo). Moving money *into* savings is one gesture; taking it out is a confirmed step.
7. **Payday and the first of the month are moments.** Temporal landmarks motivate a fresh start (Dai, Milkman & Riis 2014): a new page, a spending bar that starts empty, a quiet "new month" state.
8. **Familiar patterns, expressive skin.** Banking relies on familiar patterns (Google's M3 Expressive research). Keep the tab bar, the transfer flow and the transaction row, and put the personality *inside* them.

## Type
- **Tabular figures are the first requirement.** Check the face really has them: DM Sans, Albert Sans, Libre Franklin and Fraunces on Google Fonts have neither `tnum` nor equal-width digits, so balances jitter as they roll (`research/money-references.md` §D). Turn `tnum` on explicitly: `.monospacedDigit()` in SwiftUI, `fontFeatureSettings = "tnum"` in Compose, `font-variant-numeric: tabular-nums` in CSS.
- **The display number** (spendable, total, the lead pot) at 44–64 pt, display weight. Minor units (pence, cents) may drop to about 60% size at display sizes only, raised to the cap line, and are read as one amount by VoiceOver. At body size the amount is one run of text.
- **Format with the locale's currency formatter** (`FormatStyle.Currency`, `NumberFormat.getCurrencyInstance`, `Intl.NumberFormat`), never string concatenation. Size the display number for its widest real value (7 digits in German format) with a shrink floor. Never truncate an amount.
- **Direction is a sign and a word,** colour optional: "+£40.00 from Sam", "−£12.50 Tesco". Use a true minus (U+2212) or the formatter's sign.
- OFL options verified for figures: **Gabarito**, **Funnel Display / Funnel Sans**, **Schibsted Grotesk** (slashed zero), **Mona Sans / Hubot Sans**, **Bricolage Grotesque**, **Reddit Sans / Reddit Mono**, **Young Serif**, **Newsreader**, **Atkinson Hyperlegible Next**. They're what the deal draws from, not a new default list.

## Colour
- **Account colours are a labelled data set,** separate from the brand accent. The library's six (tomato, ochre, green, teal, blue, pink) are mid-luminance, so each clears 3:1 against both light and dark grounds as a non-text indicator. The user assigns them. They always sit next to the account's name, and they are never text colours on a light ground.
- **The brand accent is for the primary action and selection only,** so a pot never looks like a button.
- **No red and green for in and out.** The meaning flips by market (red is up in China), and colour-only meaning fails WCAG 1.4.1. Use ink for amounts, a sign and a word for direction, and an alert colour only with its word ("Overdrawn by £12").
- Dark mode is first-class, because many money apps are opened at night. Tune the accent separately for dark.

## Shape and depth
- **Containers are objects, rows are not.** Pots, cards and passbooks get shape (rims, fills, ratios, radius by role). Transactions are plain rows on the ground with hairline separators, never cards.
- Radii by role: containers 20–28, cards 18 at the payment-card ratio, buttons full pill, rows none.
- Depth: one soft contact shadow under containers or between stacked cards, and nothing else.

## Icons
- Utility chrome: the system family (SF Symbols, Material Symbols Rounded) at one weight, in ink.
- Merchants: real logos when the data has them; otherwise the category glyph on the category colour, never grey initials in circles.
- **The core verb** (move money into a pot, pay, save) gets the designed moment: the fill rising, a stamp pressing, a card settling. Precise, low bounce, and only for that verb.

## Motion
- Calm and physical: low-bounce springs (damping 0.8–0.9) for containers and cards; numbers roll ~250 ms (`.contentTransition(.numericText)`, `AnimatedContent`).
- Money moving is *shown* moving: the source shrinks as the destination grows, in one animation.
- Haptics: a selection tick while dragging an amount, and a success haptic only when a goal is reached or a payment lands.
- Reduce Motion: fills and segments cross-fade to their new size; tilt effects lie flat.

## Signature moves (pick 2–3; the direction sheet's come first)
1. **Fill as progress:** a pot's fill height is its real progress, its surface tilting with the phone.
2. **One leading goal:** the user's chosen pot at twice the size of the rest.
3. **One bar for all the money:** a full-width bar segmented by account, labelled by a legend-list in the same order.
4. **The stack is the list:** accounts as cards whose top strips are rows.
5. **Stamped deposits:** saving lands as a dated stamp on a ruled passbook page.
6. **Payday turns the page:** the month resets visibly, with the balance carried forward.
7. **Hide with a gesture:** flip, long-press or a toolbar toggle blurs every balance, and the state is visible.
8. **Pull-to-save:** a gesture that sends spare change to the leading pot, with a button fallback.

## Platform notes
- iOS: `.privacySensitive()` on every amount, so balances redact in widgets on a locked device; cover the app switcher snapshot yourself (an overlay when `scenePhase` leaves `.active`). `.monospacedDigit()` on rolling numbers. A Lock Screen widget shows "left until payday", never the total.
- Android: `FLAG_SECURE` on screens with full card numbers. Amounts in `fontFeatureSettings = "tnum"`. Keep dynamic colour off for account colours, since they're data.
- Mac: sidebar of accounts, transactions as a Table with sortable columns, Cmd-shortcuts for move money and hide balances.

## How cheap imitations go wrong
- The glassy purple or blue gradient credit card with a fake chip and "•••• 4291" as the hero of an app where the card isn't the point.
- "Total balance" with an eye icon, four round quick actions (Send, Request, Top up, More), then "Recent transactions": the vendor-template bank app.
- A line chart with a gradient area fill and no axis, and a "+12.4%" badge as decoration. A spending donut with a pastel legend.
- Green "+" and red "−" as the only signal. Grey initials in circles for every merchant.
- Pots as identical white cards in a 2×2 grid. Pot fills that are decoration, not data.
- Confetti on a transfer, streaks for opening the app, badges for spending.
- "Good morning, Alex 👋" above the balance.
- Fun bolted on with a mascot that cracks jokes about overdrafts. Personality goes in the containers, not in jokes about money worries.
