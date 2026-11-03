# Money references: clear numbers, playful containers

Research behind `references/presets/clear-money.md` and the four `cm-` directions in `library/directions.json`, gathered November 2026.

Scope: consumer money apps that show **several accounts at once** (a current account plus savings pots, vaults, jars, spaces or currencies) and want to feel **clear but fun**, in the Revolut, Monzo and Up family. Trading and brokerage are covered only for what not to do. Every claim carries a URL. Items marked **[unverified]** come from secondary sources I could not confirm against the original; **[computed]** marks my own measurements; **[inference]** marks my reading of a source, not its claim.

---

## A. Shipped anchors and what each identity rests on

| Anchor | What the identity rests on | Sources |
|---|---|---|
| **Up** (Australia, Ferocia) | Savers began as donut progress rings. They are now **Saver Pools**: volumetric containers whose contents respond to the phone's movement, each with its own emoji. **Pull-to-Save** flicks the spare cents of an unround balance into a Saver with one gesture, and reportedly saved over $1M in 18 months. The team "was cautious about gamifying banking". Viewing needs no passcode, but moving money out does: privacy and security are separate decisions. | https://up.com.au/blog/the-evolutionary-design-of-up/ · https://up.com.au/blog/up-1-14-0-release-notes/ · https://up.com.au/blog/up-version-1-4-3-release-notes/ |
| **Monzo** | One hot-coral card, kept through the 2022 Ragged Edge refresh. Oldschool Grotesk for display, Monzo Sans for the product. **Pots** are named by the user and carry an image, and locked pots feel unburdening rather than restricting. | https://monzo.com/blog/weve-had-a-little-makeover · https://www.creativereview.co.uk/monzo-branding-ragged-edge/ · https://monzo.com/blog/2019/08/09/how-were-doing-savings-accounts-differently · https://uxdesign.cc/what-monzo-can-teach-us-about-designing-for-money-habits-72e6cc30654d |
| **Revolut 10** (October 2023) | "All your money in one place" on the home screen, switching between accounts, currencies and pockets, with themes, custom backgrounds and widgets. Revolut also blurs balances when you flip or shake the phone, and that setting is on by default. | https://fintechnews.sg/78771/digital-banking-news-singapore/revolut-launches-its-biggest-update-yet-for-over-35-million-users/ · https://help.revolut.com/en-AU/help/profile-and-plan/security-and-personal-data/why-is-my-balance-blurry |
| **Wise** | Green instead of fintech blue (2023 Ragged Edge rebrand) and the bespoke Wise Sans set heavy and large. Currencies, **Jars** and groups sit together on Home, and a jar can hold more than one currency. The team tried "stash, pot, locker" before settling on "jars". | https://www.creativereview.co.uk/wise-rebrand-ragged-edge/ · https://wise.com/help/articles/645Ve1Ah1Psi0srHGfKYmm/your-wise-account-has-a-new-look · https://wise.com/gb/blog/save-with-jars-feature-launch |
| **Apple Card** (in Wallet) | Each spending category owns a colour. The digital card's surface blends the colours of what you spent on, and weekly and monthly summaries are colour-coded by category. Spending is shown as colour, with labels. | https://creditcards.com/card-advice/apple-card-colors · https://www.imore.com/how-apple-card-helps-you-live-healthier-financial-life |
| **Apple Wallet** | Cards stacked with their top strips showing. One is pulled out to the front, and the rest drop away. | (platform convention; observed) |
| **bunq** | Up to 25 sub-accounts, each with its own IBAN and a user-uploaded picture, sorted into folders. The 2020 V3 redesign gave each page one main button. | https://dutchreview.com/expat/best-bunq-features/ · https://techcrunch.com/2020/05/29/bunq-adds-donations-to-charities-and-tests-redesign/amp/ |
| **N26** | Discreet mode hides the balance, every transaction amount and the value of Spaces, on iOS, Android and web. | https://n26.com/en-de/blog/discreet-mode |
| **Copilot Money** (Apple Design Award finalist 2024) | Fully native with heavily tweaked UIKit ("It's all native; we just tweak it a lot"), and Swift Charts for cash flow. Its calm look comes from craft, not decoration. | https://developer-rno.apple.com/articles/copilot-money · https://techcrunch.com/2024/05/28/apples-design-awards-nominees-highlight-indies-and-startups-largely-ignore-ai-except-for-arc |
| **Cash App** | The home screen is the amount keypad (the archetypal exaggerated number). A late-2025 design language added fluorescent green and Cash Sans. | https://blog.adobe.com/en/publish/2018/05/03/uxperts-weigh-designs-love-may-edition · https://designcompass.org/en/2025/12/03/cash-apps-new-design-language-and-ai-moneybot/ |
| **Nubank** | Purple since launch, with a 2021 refresh that kept the purple and softened the shapes. NuDS standardises tokens, themes and modes across about 80% of server-driven screens. A useful contrast: purple was Nubank's owned idea in 2013, and it is everybody's default now. | https://blog.nubank.com.br/brand-refresh-como-renovamos-a-identidade-visual-do-nubank/ · https://www.figma.com/customers/nubank-design-system-accessible-experiences-with-figma/ · https://www.fastcompany.com/91631436/purple-is-everywhere-in-fintech-nu-bank-redesign (headline only; the page refused fetching) |

**Sameness, named by the industry.** UXDA's "clone wars" piece names the stock bank app: "balance on top, quick actions below, menu at the bottom", vendor templates, and only the logo and brand colour changing between apps. 11:FS calls it "fintech blanding". Both are agency opinion, not studies. https://www.theuxda.com/blog/digital-banking-clone-wars-stand-out-copy-paste-world · https://11fs.com/article/the-risk-of-fintech-blanding

---

## B. Behavioural literature: why containers, and how to show them

| Finding | Source | What it means for the screen |
|---|---|---|
| **Mental accounting.** People keep money in separate mental accounts by purpose and source, and treat a pound differently depending on which account it is in. | Thaler, R. H. (1999). Mental accounting matters. *Journal of Behavioral Decision Making* 12(3), 183–206. | The pot is the user's own mental model, so show money as named containers rather than one undifferentiated total plus a list. |
| **Partitions slow consumption.** Splitting a resource into smaller units reduces how much is used, because opening a partition carries a "transgression cost" (guilt). The effect is smaller when people aren't trying to regulate themselves. | Cheema, A. & Soman, D. (2008). The effect of partitions on controlling consumption. *JMR* 45(6), 665–675. https://journals.sagepub.com/doi/pdf/10.1509/jmkr.45.6.665 | A pot should look *closed*: a visible boundary, and a deliberate gesture to take money out. |
| **Labelled accounts raise saving.** In Malawi, multiple labelled accounts or lockboxes raised savings in the treatment accounts by about 30%. In Ghana, a labelled susu account with the goal printed in the passbook produced more total deposits (preliminary). | Aggarwal, Brailovskaya & Robinson, J-PAL: https://povertyactionlab.org/media/file-research-paper/saving-multiple-financial-needs-evidence-malawi · IPA Ghana: https://www.povertyactionlab.org/fr/evaluation/savings-account-labeling-and-financial-literacy-training-ghana | The label belongs on the container itself, always visible, in the user's words. Never "Savings 2". |
| **Fewer goals save more.** One savings goal produced more saving intention and actual saving than several, because multiple goals invite trade-off thinking that delays action. The gap shrinks when the goals are integrated. Samples came from rural India, Canada and Hong Kong. | Soman, D. & Zhao, M. (2011). The fewer the better: number of goals and savings behavior. *JMR* 48(6), 944–957. https://cenfri.org/research-paper/the-fewer-the-better-number-of-goals-and-savings-behaviour/ · https://blogs.worldbank.org/en/impactevaluations/marketing-saving-fewer-goals-can-lead-to-higher-savings | Many pots are fine, but **one leads**. The home makes one goal clearly bigger; the others are compact. |
| **Goal gradient.** Effort speeds up as a goal gets close, and an illusion of progress also speeds it up. | Kivetz, Urminsky & Zheng (2006). *JMR* 43(1), 39–58. https://business.columbia.edu/faculty/research/goal-gradient-hypothesis-resurrected-purchase-acceleration-illusionary-goal | Near the end, say what's **left** ("£40 to go"), not just a percentage. Never fake the progress: this is money. |
| **Fresh start effect.** Temporal landmarks (a new week, month or year, a birthday) raise aspirational behaviour. They mark separate "mental accounting periods". | Dai, Milkman & Riis (2014). *Management Science* 60(10), 2563–2582. https://faculty.wharton.upenn.edu/wp-content/uploads/2014/06/Dai_Fresh_Start_2014_Mgmt_Sci.pdf | Payday and the first of the month are moments: a new page, a reset bar, a quiet "new month" state. |
| **The ostrich effect.** Investors check their portfolios less after market falls, and logins drop 9.5% after declines (1.1M investors). A counter-study finds "meerkat" checking after both rises and falls. | Karlsson, Loewenstein & Seppi (2009): https://www.cmu.edu/tepper/faculty-and-research/assets/docs/ppaper-61264983153898-ostrich-effect-1.pdf · Sicherman et al. 2015: https://www.cmu.edu/news/stories/archives/2015/december/ostrich-effect.html · Gherzi et al. 2014: https://openaccess.city.ac.uk/id/eprint/3875/1/The%20meerkat%20effect.pdf | People avoid opening the app when they expect bad news, so the first screen must be safe to look at. Lead with the figure that helps ("£214 left until Friday"), say bad news in words with a next step, and never use an alarm-red full screen. |
| **Money anxiety at the app's front door.** 77% of UK consumers say they feel anxious opening a banking app to check a balance (GFT). Nearly one in three Americans avoid checking balances because of anxiety (U.S. Bank). | Secondary reports **[unverified against the surveys]**: https://openbankingexpo.com/news/uk-consumers-want-more-digital-money-management-tools-from-their-bank-amid-cost-of-living-crisis · https://wtam.iheart.com/content/2026-06-11-americans-avoid-bank-balances-due-to-anxiety/ | Same as above, and privacy (blur or discreet mode) is a comfort feature, not only a security one. |
| **Trust is judged visually, and fast.** Visual appeal, perceived usability and trustworthiness all rest largely on visual appeal, judged from 50 ms exposures. Balance and contrast are tied to trust **[secondary for the attribute detail]**. | Lindgaard et al. (2011). *ACM TOCHI* 18(1). https://api.crossref.org/works/10.1145%2F1959022.1959023 · https://www.humanfactors.com/newsletters/an_exploration_of_relations_between_visual_appeal.html | Clear money is beautiful money. Balanced layouts and strong contrast are trust signals, so fun must never cost clarity. |
| **Expressive works through familiar patterns.** In Google's M3 Expressive research (46 studies, 18k participants), expressive design was preferred and faster to scan, but banking "relies on familiar patterns". Replacing standard patterns or removing labels hurt. | `research/literature.md` §5 (Google M3 Expressive) | Keep the tab bar, the transfer flow and the transaction row. Put the personality *in* them: the containers, the colour, the numerals, the one gesture. |
| **Surface delight belongs on low-frequency moments.** | NN/g, Fessenden 2017; `research/literature.md` §5 | Celebrate a goal reached or a debt cleared, not every card payment. |

---

## C. Regulation and harm: where fun is not allowed

- **FCA, "Gaming trading" (2022).** Over 3,000 app users across four trading apps. Falling confetti after a trade, celebratory messages, badges and leaderboards were flagged as likely drivers of more frequent trading. https://www.fca.org.uk/publications/research-articles/gaming-trading-how-trading-apps-could-be-engaging-consumers-worse
- **FCA research note, "Digital engagement practices: a trading apps experiment" (2024).** Over 9,000 consumers. The practices changed both how often people traded and how much risk they took, with larger effects for people with lower financial literacy, women, and 18–34s. https://www.fca.org.uk/publications/research-notes/research-note-digital-engagement-practices-trading-apps-experiment
- **Monzo's vulnerable-customer work.** The gambling block is "a very simple on/off choice to activate" but "deliberately a much more difficult process to turn it off". There is a cooling-off period, and the 2017 concept post proposes next-day checks on late-night purchases and "blister-pack" friction on risky actions that never slows normal use. https://monzo.com/blog/2018/06/19/gambling-block-self-exclusion · https://monzo.com/blog/2017/01/27/designing-product-mental-health-mind/ · https://gamcare.org.uk/news-and-blog/news/monzo-block-9-million-in-gambling-transactions-in-2024-alone

**Rule for the preset [inference from the above]:** delight attaches only to *saving, paying off and reaching a goal*. Never attach it to trading, spending, borrowing, crypto or anything with a "buy" button. Friction is asymmetric: protective settings are easy to turn on and slow to turn off.

---

## D. Numbers and type

**Tabular figures are not a given.** I checked each candidate's Google Fonts build: does it have a `tnum` GSUB feature, and are its default digits already one width? **[computed with fontTools, 2026-11-03]**

| Face | tnum | Default digits equal-width | Verdict for money |
|---|---|---|---|
| Gabarito, Onest, Public Sans, Red Hat Text (slashed zero), Plus Jakarta Sans, Manrope, Golos Text, Schibsted Grotesk, Mona Sans, Hubot Sans, Reddit Sans, Bricolage Grotesque, Instrument Sans, Figtree, Archivo, Young Serif, Libre Caslon Text, Radio Canada Big, Atkinson Hyperlegible Next | yes | no | Use: turn `tnum` on (`.monospacedDigit()` in SwiftUI, `fontFeatureSettings = "tnum"` in Compose, `font-variant-numeric: tabular-nums` in CSS) |
| Funnel Display, Funnel Sans, Familjen Grotesk, Newsreader, Source Serif 4, Reddit Mono | yes | yes | Use: tabular even without the feature |
| Hanken Grotesk, Nunito, M PLUS Rounded 1c, Source Sans 3, Rethink Sans, Recursive, the monos | no | yes | Fine: already tabular by default |
| **DM Sans, Albert Sans, Libre Franklin, Fraunces, Fredoka, Wix Madefor, Urbanist, Be Vietnam Pro, Lexend, Inclusive Sans** | **no** | **no** | **Not tabular. Columns and rolling numbers will jitter.** Display use only. (DM Sans, Albert Sans and Libre Franklin are dealt as "tabular figures" elsewhere in the library, which is a defect to fix.) |

Other number rules, with sources:
- **Red and green do not mean the same thing everywhere.** Chinese markets show gains in red and losses in green. Japan and Korea are reported inconsistently. https://www.benzinga.com/general/education/21/10/23258001/did-you-know-you-dont-want-to-be-in-the-green-if-youre-trading-in-china-japan-or-taiwan · https://data.europa.eu/apps/data-visualisation-guide/colour-connotations. So direction is carried by a **sign and a word or arrow**, and colour, if used at all, is a per-locale token. This is also WCAG 1.4.1.
- **Format with the locale's currency formatter**, never string concatenation: symbol position, the decimal separator and digit grouping differ (`1.234,56 €` vs `€1,234.56`). Use a true minus (U+2212) or the formatter's sign.
- **Amounts never truncate.** Size the display number for its widest real value (a 7-digit balance in German format), shrink-to-fit with a floor, and never use an ellipsis. `references/principles.md` already bans clipped numbers; money makes it a correctness bug.
- **Screen readers:** the visible "£1,234.56" with small pence must read as one amount ("one thousand two hundred thirty-four pounds and fifty-six pence"), so combine the parts in one accessibility element. A hidden balance reads as "balance hidden", not as dots.

---

## E. Colour

- **Account colours are data, so they are a set, not a vibe.** Six mid-luminance hues (relative luminance 0.13–0.30) clear 3:1 against both a near-white ground and a near-black ground, so one swatch works in light and dark as a non-text indicator **[computed]**. The set used in the library is tomato `#E5533D`, ochre `#B7791F`, green `#2B8A3E`, teal `#0B7285`, blue `#1C7ED6` and pink `#D6336C`. Each passes 3:1 on `#FFFFFF`, `#F3F4F1`, `#101216` and `#050506`. They are never text colours on light grounds, and each always sits beside its account name.
- **The brand accent is separate from the account colours,** and it is used only for the primary action and selection. Otherwise a pot that happens to be the brand colour reads as a button.
- **Purple-to-indigo and "trust blue" are the category default** (Nubank's purple was owned in 2013; by 2026 it is the template; Wise left blue on purpose). Cream and terracotta is the generic "tasteful AI" default (SKILL.md slop tells).

---

## F. The fintech slop look (as of 2026-11)

Compiled from the UXDA clone-wars list, Dribbble-style fintech shots and the skill's own baseline runs **[inference]**:
1. A glassy purple or blue gradient credit card as the hero, with a fake chip, a "VISA" mark and "•••• 4291", in an app where the card isn't the point.
2. "Total balance" with an eye icon, then four round quick actions (Send, Request, Top up, More), then "Recent transactions".
3. A line chart with a gradient area fill, no axis and no values: "+12.4% this month" as decoration.
4. A spending donut with a legend of pastel dots.
5. Green for "+" and red for "−" as the only signal.
6. Grey circles with initials for every merchant.
7. "Good morning, Alex 👋", plus confetti on a transfer.
8. Every account as an identical white rounded card in a 2×2 grid.

---

## G. What the four directions take from this

| Direction | Evidence it rests on | Anchors |
|---|---|---|
| `cm-pot-shelf` (Pots on a shelf) | mental accounting, partitions, labels, one goal leads, goal gradient | Up Saver Pools, Monzo Pots, Wise Jars |
| `cm-one-bar` (All your money in one bar) | trust from balance and contrast, colour as labelled data, fresh start | Apple Card category colours, Revolut 10 "all your money" |
| `cm-wallet-stack` (Wallet stack) | familiar pattern made expressive, privacy as comfort | Apple Wallet, bunq pictures per account, Revolut flip-to-blur |
| `cm-passbook` (Passbook) | labelled passbook (Ghana), fresh start, the ledger as the most trusted money document **[inference]** | savings passbooks, Robinhood's serif-over-sober |
