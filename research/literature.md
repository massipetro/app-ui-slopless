# app-ui-slopless: research literature

The studied basis for the skill: authors, their rules phrased for a mobile UI agent, and the numbers behind them.
Compiled 2026-10-18 from web research.

**Verification tags**
- **[V]**: checked this session against a primary source (the paper, the author's own page, the standard, or the platform's own docs/source code).
- **[S]**: checked only against a reputable secondary source (NN/g, a publisher page, an author summary, or a citing paper).
- **[U]**: not verified this session. It comes from the book or general knowledge. Treat it as a pointer, not a citation.

Quotes are kept under 15 words.

---

## 0. The skill's stance in five sentences (what the evidence supports)

1. People judge attractive interfaces as more usable, before use and often after it (Kurosu & Kashimura 1995; Tractinsky 1997; Tractinsky et al. 2000). The effect has limits: bad usability can lower perceived beauty (Tuch et al. 2012).
2. Visual appeal is judged in about 50 ms (Lindgaard et al. 2006). A first screen that looks bland or generic has already lost points.
3. Flat, signifier-poor UI measurably costs time and attention: about 22% more time and 25% more fixations (Moran / NN/g 2017). Minimal is fine; **signifier-less** is not.
4. Google's own research behind M3 Expressive reports that bolder, more expressive UI helped people find key elements up to 4x faster, closed the age gap, and was preferred across ages. This is company-reported, not peer-reviewed. Google also says expressiveness never beats basic functionality.
5. Delight sits on top of function, reliability and usability (Walter 2011; Fessenden / NN/g 2017). Personality is the *last* layer, and it is a required layer, not an optional one.

---

## 1. Cognition and perception

### Don Norman: *The Design of Everyday Things* (rev. ed. 2013), *Emotional Design* (2004)
Norman is Professor Emeritus at UC San Diego, a former VP of Advanced Technology at Apple, and co-founder of Nielsen Norman Group. Sources: [jnd.org DOET page](https://jnd.org/the-design-of-everyday-things-revised-and-expanded/) [S, table of contents]. The concept definitions below are [U] from the book.

- **Affordance ≠ signifier.** An affordance is the relationship between a person and an object that allows an action. A signifier is the perceivable cue that tells people the action is possible. The 2013 edition added signifiers because designers had misused "affordance". *Rule:* every tappable thing on a screen needs a visible signifier: shape, container, colour contrast, an icon plus label, or an underline. Never rely on "users will discover it".
- **Mapping.** Controls should relate spatially and logically to their effects. *Rule:* put the control next to the thing it changes, and make swipe direction match content movement. A stepper's `+` goes on the side where the number grows.
- **Feedback.** Every action needs an immediate, informative response. Too much feedback is as bad as none. *Rule:* acknowledge each tap within 100 ms (pressed state, ripple, haptic). Show progress for anything over about 1 s.
- **Constraints.** Norman names four kinds: physical, cultural, semantic and logical. Forcing functions (interlocks, lock-ins, lock-outs) are a special case. *Rule:* make invalid states impossible rather than validating after the fact. Examples: disable impossible dates, and use the right keyboard type.
- **Conceptual model.** The UI must convey how the system works (the "system image"). *Rule:* the screen structure should match the user's mental model of the domain, not the database schema.
- **Gulfs of execution and evaluation; seven stages of action.** *Rule:* for each screen, check whether the user can tell what to do and whether they can tell what happened.
- **Errors: slips vs mistakes.** Slips are the right goal with the wrong action. They split into action-based slips and memory-lapse slips. Mistakes are the wrong goal or plan, and are rule-based, knowledge-based or memory-lapse [S for the first categories; the third mistake type is U]. *Rule:* prevent slips with spacing, confirmation only for destructive actions, and undo. Prevent mistakes with clear conceptual models and good defaults. Prefer **undo over "Are you sure?"**.
- **Emotional Design: three levels.** *Visceral* is appearance and the instant reaction. *Behavioral* is use and performance. *Reflective* is meaning, self-image and memory. Norman argues a design must work at all three levels. *Rule:* make deliberate choices at each level. Visceral: colour, type and shape signature. Behavioral: speed, feedback, ergonomics. Reflective: brand voice, and the stories users tell about the product. Sources: [getAbstract summary](https://www.getabstract.com/en/summary/emotional-design/6416) [S]; the 2002 *Interactions* essay "Emotion & Design: Attractive Things Work Better" [U].

### Jakob Nielsen: 10 Usability Heuristics (1994, text updated 2020, reviewed 2024)
Nielsen co-founded Nielsen Norman Group and holds a PhD in HCI from the Technical University of Denmark. Source: [NN/g](https://www.nngroup.com/articles/ten-usability-heuristics/) [V].

1. Visibility of system status
2. Match between the system and the real world
3. User control and freedom (clear exits, undo)
4. Consistency and standards (follow **platform** conventions)
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency of use (accelerators)
8. Aesthetic and minimalist design
9. Help users recognize, diagnose and recover from errors
10. Help and documentation

*Mobile reading of #8:* the heuristic says remove *irrelevant* information. It does **not** say remove visual character. NN/g's own flat-design research (§5) shows that stripping signifiers hurts. Minimalism is about content; it is not a licence to be bland.

**Response-time limits.** Sources: [NN/g](https://www.nngroup.com/articles/response-times-3-important-limits/) [V]; originally Miller 1968 (AFIPS) and Card, Robertson & Mackinlay 1991 (CHI).
- **0.1 s** feels instantaneous.
- **1 s** keeps the flow of thought intact, though the delay is noticed.
- **10 s** is the limit of attention. Beyond it, show a percent-done indicator.

*Rule:* touch feedback at or under 100 ms. Use skeletons or optimistic UI for waits of 1–10 s. Anything longer needs determinate progress and must be cancellable.

### Doherty threshold (~400 ms)
Doherty, W. J. & Thadani (also spelled Thadhani), A. J. (1982). *The Economic Value of Rapid Response Time*, IBM report / IBM Systems Journal.
- The IBM text argues that productivity rises sharply when system response drops below the old 2-second norm [S, from a Computer History Museum scan excerpt].
- **The specific "400 ms" figure is attributed to it by secondary sources (e.g., lawsofux.com). I could not confirm it in the visible original text [U].**
- Kent Beck notes it is a practical threshold, not a cognitive constant.

*Rule:* aim for system responses under ~400 ms so that interaction feels conversational. Treat this as a target, not a law.

### Miller (1956) → Cowan (2001): working memory is about 4 chunks, not 7
Cowan, N. (2001). The magical number 4 in short-term memory. *Behavioral and Brain Sciences* 24(1), 87–114 (commentary to p. 185) [V, PubMed abstract]. Cowan is Curators' Professor of Psychology at the University of Missouri.
- Miller's "7±2" was partly rhetorical. Cowan's synthesis puts capacity at about **3–5 chunks** (about 4).
- **Caveat:** neither number is a rule like "max 7 menu items". Menus and tabs rely on *recognition*, not recall.

*Rules:*
- Don't make users carry information across screens. Keep the key context visible: the selected trip, the filters in force, the totals.
- Chunk long codes and numbers in groups of 3–4.
- Mobile makes this worse. Budiu (NN/g) notes a small screen is a smaller "external memory", so users must remember more of what is off-screen ([Mobile UX limitations](https://www.nngroup.com/articles/mobile-ux/), [Working memory & external memory](https://www.nngroup.com/articles/working-memory-external-memory/)) [S].

### Hick–Hyman law
- Hick, W. E. (1952). On the rate of gain of information. *Quarterly Journal of Experimental Psychology* 4, 11–26.
- Hyman, R. (1953). Stimulus information as a determinant of reaction time. *Journal of Experimental Psychology* 45, 188–196. [S, citation records]

Choice reaction time grows with the **log₂ of the number of equally likely alternatives**. Hyman showed it is linear in *information* (bits), so unequal probabilities cut the time.

*Rules:*
- Reduce the *effective* choices on a decision screen, and give one obvious primary action.
- Make the likely choice prominent. Probability skews the cost.
- It applies to simple choice reaction. It does not apply to scanning an unfamiliar list. Don't use it to justify hiding navigation (see the hamburger data in §2).

### Jeff Johnson: *Designing with the Mind in Mind* (3rd ed., 2020)
Johnson is an Assistant Professor of CS at the University of San Francisco, a member of the ACM SIGCHI Academy, and holds SIGCHI's Lifetime Achievement in Practice award. Source: [Elsevier](https://shop.elsevier.com/books/designing-with-the-mind-in-mind/johnson/978-0-12-818202-4) [V, table of contents and credentials].

The chapter titles are the rules. Each is phrased below as an agent rule.
- **Perception is biased** by expectation, context and goals. Users see what they expect. *Rule:* put critical state changes where the eye already is, and make them salient.
- **Vision is optimised for structure; we seek visual structure.** *Rule:* use hierarchy, grouping and alignment so screens are scannable. Walls of uniform rows are not.
- **Colour vision is limited.** We see edges and contrast better than absolute colour, and about 8% of men have colour-vision deficiency [U for the %]. *Rule:* never use colour alone. Pair hue with shape, icon or text.
- **Peripheral vision is poor.** Resolution falls off fast outside the fovea (about 1–2° of sharp vision) [U for the degrees]. *Rule:* errors and toasts far from the point of action get missed. Show feedback **at the point of action**. Motion or a pop of colour can pull attention when the location must be far away.
- **Reading is unnatural.** *Rule:* write short, front-loaded labels. Use sentence case and no all-caps body text. Don't centre long text.
- **Attention is limited; memory is imperfect.** *Rule:* support interruptions (mobile microsessions). Restore state, and show where the user was.
- **Recognition is easy; recall is hard.** *Rule:* show choices with icons **and** labels, keep recent and suggested items, and never use a bare icon for a rare action.
- **Hand–eye coordination follows laws** (Fitts, steering). *Rule:* see §2.
- **We have time requirements.** *Rule:* see the response-time limits above.

### Gestalt principles applied to UI
The original sources are Wertheimer (1923) [U], plus Palmer (1992) on common region and Palmer & Rock (1994) on uniform connectedness [U]. The UI applications are from NN/g: [Proximity](https://www.nngroup.com/articles/gestalt-proximity/), [Similarity](https://www.nngroup.com/articles/gestalt-similarity/), [Common region](https://www.nngroup.com/articles/common-region/) [S].
- **Proximity:** spacing *is* grouping. Keep space inside a group clearly smaller than space between groups. A ratio of at least 1:2 is a practical heuristic [U]. *Rule:* the label sits nearer its field than the previous field does.
- **Similarity:** same look means same function. *Rule:* all tappable items share one treatment. Non-interactive items must not mimic it.
- **Common region:** a card or container groups more strongly than proximity alone. *Rule:* use cards or sections to bind related controls. Don't box everything, or containment stops meaning anything.
- **Connectedness:** a line or connector beats both similarity and proximity. *Rule:* use it for steppers, timelines and route legs.
- **Figure/ground and closure:** elevation, scrim and shadow separate layers. *Rule:* sheets and dialogs need a clear figure/ground difference. Flat-on-flat with no edge fails here.
- **Continuity / common fate:** things that move together belong together. This is the Gestalt basis for staggered motion (§4).

---

## 2. Interaction and touch

### Fitts's law
Fitts, P. M. (1954). The information capacity of the human motor system in controlling the amplitude of movement. *Journal of Experimental Psychology* 47(6), 381–391. [V, PubMed; PDF at [Stanford](https://cs303.stanford.edu/papers/1954-Fitts.pdf)]

Movement time = a + b·log₂(D/W + 1) in MacKenzie's Shannon formulation [U for the formulation attribution]. D is the distance to the target and W is its width.

*Rules:*
- Frequent and primary actions get **big targets close to the thumb's resting position**.
- Screen edges are *not* "infinitely deep" on touch as they are for a mouse. The bezel gives no stopping benefit to a finger.
- Make the whole row tappable, not just the chevron or text.
- Put destructive actions *far* from frequent ones. Fitts works in reverse too.

### Steven Hoober: field research on how people hold and touch phones
Hoober is a mobile UX researcher (4ourth Mobile), co-author of *Designing Mobile Interfaces* (O'Reilly 2011), and author of *Touch Design for Mobile Interfaces* (Smashing, 2021/22).

**[UXmatters 2013](https://www.uxmatters.com/mt/archives/2013/02/how-do-users-really-hold-mobile-devices.php) [V]:**
- 1,333 observations in public places, 780 of them people touching the screen.
- Grip among touching users: **one-handed 49%**, **cradled 36%** (one hand holds, the other taps or the holding thumb taps), **two-handed 15%**.
- One-handed users: right thumb 67%, left thumb 33%.
- People change grip "very often", sometimes every few seconds.

**[UXmatters 2017, "Design for Fingers, Touch, and People"](https://www.uxmatters.com/mt/archives/2017/03/design-for-fingers-touch-and-people-part-1.php) [V]:**
- **75%** of touches are made with one thumb.
- People **prefer to look at and touch the centre** of the screen.
- Accuracy is best at the centre: targets can be **~7 mm**. **Corners need ~12 mm.** These sizes capture 95% of taps.
- A secondary source cites **11 mm at the top and 12 mm at the bottom** [S, Smashing cheatsheet; it conflicts with an IxDF summary of 9 mm on edges, so treat it as U].
- He calls the classic "thumb-sweep" heat-map chart "well-known, but incorrect". People do reach the top (e.g., Back at upper left).
- Specify sizes in physical units and allow about ±20% variation across platforms.

*Rules from Hoober:*
1. Put primary content in the centre of the screen.
2. Put secondary actions along the top and bottom edges, and tertiary actions in corner menus.
3. Keep dangerous controls physically isolated.
4. Don't assume one-thumb use. Design for grip switching.
5. Measure in mm, then convert: 7 mm is about 40 pt/dp, and 9 mm is about 48 dp. Android states 48 dp is about 9 mm [V].

### Josh Clark: *Designing for Touch* (A Book Apart, 2015)
Clark is the founder of Big Medium. Sources: [A List Apart excerpt "How We Hold Our Gadgets"](https://alistapart.com/article/how-we-hold-our-gadgets/) [V], [publisher page](https://abookapart.com/products/designing-for-touch) [S].
- **"Always accommodate the most constrained grip"**, which is the single thumb.
- About **a third of a phone screen is effortless**: the bottom area, on the side opposite the thumb. The top takes a stretch on any phone size.
- **Top vs bottom matters more than left vs right.** Put core and frequent actions in the lower-middle, where both hands' zones overlap.
- **Phablets:** used two-handed about 70% of the time, yet you still design for the one-thumb case. Choking up the grip pushes the bottom out of reach.
- If a control must live in a hard-to-reach area, make its target larger.
- Gestures are the "keyboard shortcuts" of touch: accelerators that need a visible alternative [U as a phrasing]. His talk title "Buttons are a hack" is [U].
- *Tension with Hoober:* Clark emphasises the bottom thumb zone and Hoober emphasises the centre. **Reconciled rule:** content in the centre, primary actions low (bottom bar, FAB, bottom sheet), rare and navigational actions high. Never put a primary CTA only in the top corner.

### Raluca Budiu and NN/g: mobile navigation research
Budiu is VP of Research at NN/g and holds a PhD from Carnegie Mellon [U for degree details].
- **Hidden vs visible navigation.** Source: [Pernice & Budiu 2016](https://www.nngroup.com/articles/hamburger-menus/) [V]. 179 participants on 6 live sites, on mobile and desktop.
  - Hidden navigation cut **discoverability by more than 20%** on both platforms.
  - On mobile, navigation was used 57% of the time when hidden vs 86% with a combo (partly visible) design. Tasks took 15% longer with hidden navigation.
  - On desktop, hidden navigation was at least 39% slower.
  - Perceived difficulty was 2.6 hidden, 2.3 combo, 2.1 visible on a 7-point scale.
  - **Recommendation:** with 4 or fewer top-level destinations on mobile, show them all. Hide only the overflow.
- **Patterns.** Source: [Budiu 2015](https://www.nngroup.com/articles/mobile-navigation-patterns/) [V].
  - Tab or navigation bars suit about 4–5 options or fewer; beyond that, targets shrink.
  - Hamburger menus suit content-heavy, browse-mostly apps, and need supporting in-page links.
  - A navigation hub suits task apps where one branch is used per session.
  - Choose the pattern whose downsides hurt the most common tasks least.
- **Interaction cost and microsessions.** Every scroll, tap and memory demand costs effort. Mobile sessions under 15 s are normal, and good mobile design supports them with notifications and widgets ([NN/g microsessions](https://www.nngroup.com/articles/mobile-microsessions/)) [S].

*Rules:*
- Use a persistent bottom tab bar or navigation bar for 3–5 destinations.
- Don't hide primary navigation behind ☰.
- Design glanceable states (widgets, Live Activities, notifications) for microsessions.

### Ben Shneiderman: Eight Golden Rules; direct manipulation
Shneiderman is Distinguished University Professor (emeritus) at the University of Maryland and founder of its HCI Lab. He wrote *Designing the User Interface* (6th ed., 2016, with Plaisant et al.). Source: [UMD golden rules page](https://www.cs.umd.edu/users/ben/goldenrules.html) [V].

The Eight Golden Rules:
1. Strive for consistency.
2. Seek universal usability.
3. Offer informative feedback, modest for frequent actions and substantial for major ones.
4. Design dialogs to yield closure (beginning, middle, end, then confirmation).
5. Prevent errors.
6. Permit easy reversal of actions.
7. Keep users in control (no surprises).
8. Reduce short-term memory load.

**Direct manipulation** (IEEE *Computer* 16(8), 1983) [S, via Shneiderman's UMD page]:
- Continuous visible representation of the objects of interest.
- Physical actions instead of syntax.
- Rapid, incremental, reversible actions with immediately visible effects.

*Mobile rules:*
- Drag the map, scrub the timeline, swipe the card, pinch the photo. The object moves *with* the finger at 1:1 and the gesture can be cancelled mid-way.
- Every successful flow ends on a closure state (a success screen or confirmation with a summary), not a silent pop back.
- Feedback scales with the weight of the action: a light haptic for a toggle, a full success moment for a booking.

### Alan Cooper: *About Face* (4th ed., 2014, with Reimann, Cronin, Noessel)
Cooper is the "father of Visual Basic", founder of Cooper (design consultancy), and originator of goal-directed design and personas. Publisher: Wiley. Sources: [Wikipedia: Application posture](https://en.wikipedia.org/wiki/Application_posture) [S]; the concept details are [U] from the book.
- **Goal-directed design.** Design for users' *goals* (end states, life goals), not for tasks or features. *Rule:* for each screen, name the persona's goal and cut anything that doesn't serve it.
- **Personas.** Use a specific, research-based archetype rather than "the user", with one primary persona per interface. *Rule:* decide hierarchy by what the primary persona needs most often.
- **Posture.** Cooper names four: *sovereign* (full attention for long periods), *transient* (brief, single-purpose), *daemonic* (background), and *parasitic/auxiliary* (persistent but small).
  - Most phone apps are used transiently even when full-screen [U for how the 4th ed. frames mobile].
  - *Rule:* transient-use screens need big, bold, self-explanatory controls and an instant path to the answer.
  - Sovereign tools (editors, maps in navigation) can afford density and learned accelerators.
- **Excise.** Excise is work that serves the tool, not the goal. Types include navigational, skeuomorphic, modal and stylistic [S, course material citing Cooper].
  - *Rule:* hunt down excise. Watch for confirmation dialogs for reversible acts, re-entering known data, forced tours, needless mode switches, and permission prompts before the value has been shown.
- "Don't stop the proceedings with idiocy" (dialog boxes) [U, book maxim].

### Luke Wroblewski: *Mobile First* (A Book Apart 2011), *Web Form Design* (Rosenfeld 2008)
Wroblewski is a product director at Google (via acquisitions of Polar and Input) and was formerly at Yahoo and eBay. Sources: [Mobile First deck](https://static.lukew.com/MobileFirst_LukeW.pdf), [Web forms deck](https://static.lukew.com/WebForms_LukeW_101209.pdf) [S].
- **Mobile First = growth, constraints, capabilities.** Constraints (screen, bandwidth, attention) force **focus** on what matters. Capabilities (GPS, camera, sensors, touch) enable things desktop can't do. *Rule:* design the phone screen first. Use device capabilities to *remove* input, for example location instead of typing a city, or the camera instead of typing a number.
- **Actions first, content as interface.** Put the top tasks on the first screen.
- **Forms: label placement.** Top-aligned labels gave the fastest completion in Penzo's 2006 eyetracking study, because one fixation captures both label and field. Left-aligned labels slow people down, which suits unfamiliar data [S; a small 11-person replication (Das et al., Napier) disagreed for multi-column forms]. *Rule:* on mobile, use top-aligned, persistent labels.
- **Inputs:** use the right keyboard type, sensible defaults, input masks, and inline validation after the field is finished, not on each keystroke [U for exact book wording].
- **Placeholder text is not a label.** Source: [Sherwin / NN/g 2014](https://www.nngroup.com/articles/form-design-placeholders/) [V]. Placeholders disappear and strain memory, hinder review and error correction, often have low contrast, and are not reliably announced by screen readers. *Rule:* use persistent labels outside the field. Floating labels are acceptable second best.

---

## 3. Visual hierarchy, typography and colour

### Robert Bringhurst: *The Elements of Typographic Style* (1992; v4.0, 2012)
Bringhurst is a Canadian typographer, poet and book designer. Sources: [webtypography.net 2.1.2](https://webtypography.net/2.1.2) [S, adapts Bringhurst for screen]; the remaining items are [U] from the book.
- **Measure:** 45–75 characters per line for single-column text, with **~66 as ideal**. Use 40–50 for multi-column text. Alternatively the measure is about 30 times the type size, within a range of 20 to 40 times.
  - *Mobile:* a 390 pt-wide phone at 17 pt body gives about 35–45 characters, which is on the short side and fine.
  - *Rule:* on tablets and landscape layouts, **cap the text column width** (e.g., ~600–680 pt) rather than stretching full-width.
- **Scale:** choose sizes from a deliberate, limited scale (the classic scale is 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 21, 24, 36, 48, 60, 72), not arbitrary values. *Rule:* use 4–6 type sizes per app with clear ratios between them. A timid 15/16/17 ladder produces no hierarchy.
- **Hierarchy with restraint.** Change one variable at a time (size *or* weight *or* colour) for each hierarchy level. Avoid stacking all three for a minor distinction.
- **Vertical rhythm / leading:** body leading should be about 120–145% of size. Rhythm comes from consistent spacing units.
- "Typography exists to honor content" [U, paraphrase]. Typography serves reading, and character comes from choice, not decoration.

### Ellen Lupton: *Thinking with Type* (3rd ed., 2024)
Lupton is Senior Curator of Contemporary Design at Cooper Hewitt and was director of the Graphic Design MFA at MICA [U for exact current titles]. Items are [U] from the book.
- Build hierarchy through **contrast**: size, weight, colour, spacing and position. A strong hierarchy uses a few large, confident jumps.
- Use letter-spacing for all-caps and small text, and tighten it on large display text.
- A grid gives structure *and* permits deliberate breaks for emphasis.
- Pairing: contrast one display face with a workhorse text face. Don't pair two near-identical sans faces.

*Agent rules (Bringhurst + Lupton + platform):*
- Pick a **display face with character** for large titles and numbers, and keep the system face (SF Pro / Roboto Flex) or a robust text face for body and UI. Scale every custom font through Dynamic Type (`UIFontMetrics` / `.font(.custom(_, size:, relativeTo:))`) and Android `sp`.
- **Make big things big.** A key number, such as a departure time or a price, can be 34–60 pt.
- Use tabular (monospaced) figures for times and prices that update or align.

### Josef Albers: *Interaction of Color* (Yale University Press, 1963)
Albers taught at the Bauhaus and later chaired Yale's design department from 1950. Sources: [David Zwirner / Yale UP edition notes](https://www.davidzwirner.com/collect/josef-albers-interaction-of-color-book) [S]; the principles are [U] from the book.
- **Colour is relative.** The same colour looks different on different grounds, and different colours can look the same.
- Colours interact through intensity, temperature and boundaries (vibrating and vanishing edges).
- *Rules:*
  - Judge colours **in context** (on the actual surface, in light and dark mode), never as isolated swatches.
  - Saturated complementary hues at equal lightness "vibrate", so avoid that pairing for text.
  - A brand colour needs separate tuned values for light and dark surfaces.

### Perceptual colour: OKLCH, and APCA vs WCAG 2 contrast
- **Oklab / OKLCH.** Björn Ottosson introduced it in December 2020 ([blog](https://bottosson.github.io/posts/oklab/)). It is fitted on CAM16 (lightness, chroma) and IPT (hue). It is now in CSS Color 4/5 ([Wikipedia summary](https://en.wikipedia.org/wiki/Oklab_color_space)) [S].
  - *Rule:* generate tonal palettes in OKLCH. Step L evenly and keep hue stable, so you get even ramps without the muddy midtones HSL gives.
  - **Caveat:** OKLCH lightness does **not** predict contrast. Still check contrast with WCAG/APCA.
  - Material 3 itself uses HCT (CAM16 hue/chroma + L* tone) for dynamic colour [U].
- **WCAG 2.x contrast** (normative today): text **4.5:1**, large text **3:1**, UI components and graphics **3:1** ([WCAG 2.2](https://www.w3.org/TR/WCAG22/)) [V]. Apple's HIG uses these AA values: 4.5:1 up to 17 pt, and 3:1 at 18 pt or above, or for bold text [V].
- **APCA** (Accessible Perceptual Contrast Algorithm) is by Andrew Somers (Myndex). It is the *candidate* method for WCAG 3, **not normative** ([APCA in a Nutshell](https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html)) [V]. It is polarity-aware (dark-on-light ≠ light-on-dark) and accounts for font size and weight. The Lc levels:
  - **Lc 90**: preferred for body text.
  - **Lc 75**: minimum for body columns.
  - **Lc 60**: minimum for other content text.
  - **Lc 45**: large or bold headlines and fine icons.
  - **Lc 30**: absolute minimum for placeholder or disabled text and solid icons.
  - **Lc 15**: discernible non-text such as dividers and focus rings.
  - Apple's HIG names APCA alongside WCAG as an accepted measure [V].
- *Rule:* pass WCAG 2 AA (legally referenced). Use APCA as a sanity check, especially in **dark mode**, where WCAG 2 overstates the contrast of light-on-dark pairs and understates dark-on-light [S, APCA docs].

### Edward Tufte: data display (only the parts that apply to mobile)
Tufte is Professor Emeritus of Political Science, Statistics and Computer Science at Yale. He wrote *The Visual Display of Quantitative Information* (1983), *Envisioning Information* (1990) and *Beautiful Evidence* (2006). Concepts are [S] via course notes; details are [U].
- **Data-ink ratio:** maximise the share of ink that shows data. Erase non-data ink and redundant data ink. *Rule:* use no 3D, drop the heavy gridlines and chart borders, and label data directly instead of using legends (legends cost scarce screen space and eye travel).
- **Chartjunk:** decoration that carries no information. **Caveat for this skill:** data-ink applies to *charts*, not to the UI shell. A bold brand colour in a header is not chartjunk.
- **Small multiples:** repeat a small chart with the same scale for comparison. *Rule:* on phones, prefer a vertical stack of small multiples over one dense multi-series chart.
- **Sparklines:** "word-sized" graphics inline with text. *Rule:* use them in list rows and cards (trend next to the value).
- **Lie factor:** the effect shown must match the effect in the data. *Rule:* start bar charts at zero. Don't make small differences look large by cropping the axis.
- "Content is interface". Tufte praised the iPhone's content-dense screens (2008) [U].

---

## 4. Motion and microinteraction

### Disney's 12 principles → UI
The source text is Thomas, F. & Johnston, O. (1981), *The Illusion of Life: Disney Animation* [U]. The first HCI adaptation was Chang, B.-W. & Ungar, D. (1993), "Animation: from cartoons to the user interface", *UIST '93*, pp. 45–55 ([PDF](https://bibliography.selflanguage.org/_static/animation.pdf)) [S]. It won the UIST lasting-impact award in 2004 [S].
- Chang & Ungar's three principles: **solidity** (objects shouldn't pop in or out; they move continuously), **exaggeration** (amplify actions so they're perceived), and **reinforcement** (effects such as motion blur, anticipation, slow-in/slow-out, follow-through and arcs).
- *Rules:*
  - Objects travel. They don't teleport.
  - Use slow-in/slow-out (easing), never linear motion for spatial moves.
  - Use small anticipation or overshoot only on playful, low-frequency moments.

### Issara Willenskomer: "Creating Usability with Motion: The UX in Motion Manifesto"
Willenskomer is the founder of UX in Motion. Source: [UX Magazine](https://uxmag.com/articles/creating-usability-with-motion-the-ux-in-motion-manifesto) [S].

There are 12 principles, grouped by what they support:
- **Timing:** Easing; Offset & Delay.
- **Object relationship:** Parenting.
- **Object continuity:** Transformation; Value Change; Masking; Overlay; Cloning.
- **Temporal hierarchy:** Parallax.
- **Spatial continuity:** Obscuration; Dimensionality; Dolly & Zoom.

Rules for an agent:
- **Easing always.** Every temporal behaviour eases.
- **Offset & delay (stagger)** reveals grouping and hierarchy. Items that share a delay read as one group. Keep stagger steps short (~20–50 ms each [U]).
- **Parenting:** child elements move with their parent (header collapses → title shrinks).
- **Transformation / Cloning / Masking:** a FAB becomes a sheet, a card expands into a detail screen (shared-element / container transform). This preserves the user's sense of where they are.
- **Value change:** animate numbers when they change, such as a countdown or price, so the change is noticed.
- **Parallax / Dimensionality:** only for depth hierarchy, used sparingly, and disabled under Reduce Motion.

### Material Design 3: motion tokens (from the Compose source code)
Source: `androidx/compose/material3/tokens/MotionTokens.kt`, `ExpressiveMotionTokens.kt`, `StandardMotionTokens.kt` ([androidx GitHub](https://github.com/androidx/androidx/tree/androidx-main/compose/material3/material3/src/commonMain/kotlin/androidx/compose/material3/tokens)) [V].

**Durations:**
| Group | Steps |
|---|---|
| Short | 50 / 100 / 150 / 200 ms |
| Medium | 250 / 300 / 350 / 400 ms |
| Long | 450 / 500 / 550 / 600 ms |
| Extra-long | 700–1000 ms |

**Easing curves:**
| Name | Cubic bezier |
|---|---|
| Emphasized | (0.2, 0, 0, 1) |
| Emphasized decelerate | (0.05, 0.7, 0.1, 1) |
| Emphasized accelerate | (0.3, 0, 0.8, 0.15) |
| Standard | (0.2, 0, 0, 1) |
| Legacy | (0.4, 0, 0.2, 1) |

**M3 Expressive spring motion scheme:**
| Spring | Expressive (damping, stiffness) | Standard (damping, stiffness) |
|---|---|---|
| Spatial default | 0.8, 380 | 0.9, 700 |
| Spatial fast | 0.6, 800 | 0.9, 1400 |
| Spatial slow | 0.8, 200 | 0.9, 300 |
| Effects (opacity/colour), all schemes | 1.0 (no bounce); stiffness 1600 / 3800 / 800 | same |

*Rules:*
- Spatial movement can bounce slightly in an expressive scheme. Colour and opacity never bounce.
- Use springs for gesture-driven motion, because they are interruptible and keep velocity.
- Enter with decelerate, exit with accelerate. Exits are shorter than entrances.

### Apple HIG: motion
Source: [HIG Motion](https://developer.apple.com/design/human-interface-guidelines/motion) and [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) [V, read via Apple's JSON].
- **Purposeful motion.** "Don't add motion for the sake of adding motion."
- **Make motion optional.** Never make it the only carrier of information; pair it with haptics or text.
- **Realistic, gesture-following feedback.** Dismiss in the direction the view came from.
- **Brief and precise** feedback animations. **Avoid motion on very frequent interactions.**
- **Let people cancel motion.** Don't block input until an animation ends.
- **Reduce Motion:** cut automatic and repetitive animation (zoom, scale, peripheral motion). Track animations to gestures directly, and **replace x/y/z transitions with fades**.
- SwiftUI: `@Environment(\.accessibilityReduceMotion)`.
- **Android equivalent:** "Remove animations" sets the animator duration scale to 0. Compose animations honour it through `MotionDurationScale` (since Compose 1.2) [S, Kotlin Slack, Google maintainer]. Some APIs, such as `basicMarquee`, don't, so check them manually [S].

### Dan Saffer: *Microinteractions: Designing with Details* (O'Reilly, 2013)
Saffer is an interaction designer and author, now teaching at Carnegie Mellon HCII [U for current role]. Source: [O'Reilly](https://www.oreilly.com/library/view/microinteractions/9781449342760/) [S].

The structure is **Trigger → Rules → Feedback → Loops & Modes**.
- **Trigger:** manual (a control) or system (data or condition). A manual trigger should look the same every time and show its current state, e.g., a toggle that *shows* it's on.
- **Rules:** what can and can't happen. Use smart defaults, and don't make users start from zero (prefill, remember).
- **Feedback:** visual, haptic or audio. Feedback should illuminate the rules. Use the least feedback that communicates, and put it on the thing being acted on.
- **Loops & modes:** loops govern duration and repetition. Use long loops to adapt over time (e.g., the 5th use differs from the 1st). **Avoid modes**, and if one is unavoidable make it visually obvious.
- *Rule:* treat every toggle, pull-to-refresh, favourite, copy-to-clipboard and error as a designed microinteraction. This is where personality lives cheaply and safely.

---

## 5. Emotion, delight and aesthetics: the evidence against blandness

### Kurosu & Kashimura (1995): the original aesthetic-usability finding
Kurosu, M. & Kashimura, K. (1995). Apparent usability vs. inherent usability. *CHI '95 Conference Companion*, 292–293. Hitachi Design Center. [S, ACM record and NN/g]
- **26 ATM layouts** and **252 participants** (numbers per [NN/g, Moran 2024](https://www.nngroup.com/articles/aesthetic-usability-effect/) [S]).
- Perceived ease of use correlated more with **aesthetic appeal** than with inherent usability features.

### Tractinsky (1997); Tractinsky, Katz & Ikar (2000)
Tractinsky is Professor of Information Systems at Ben-Gurion University.
- **1997** (*CHI '97*): replicated the study in Israel to test cultural bias, and found an even stronger aesthetics–apparent usability correlation (**r ≈ .59** reported) [S].
- **2000.** "What is beautiful is usable", *Interacting with Computers* 13(2), 127–145 ([OUP](https://academic.oup.com/iwc/article/13/2/127/898608)) [S, abstract]. An ATM simulator was rated before and after use.
  - Strong aesthetics–usability correlation **before and after** use.
  - A MANCOVA showed that the system's aesthetics affected post-use perceived usability, **while actual usability did not**.
  - The authors compare it to the physical-attractiveness halo in social psychology.

### Lindgaard et al. (2006): 50 ms judgements
Lindgaard, Fernandes, Dudek & Brown. *Behaviour & Information Technology* 25, 115–126 [S].
- Visual-appeal ratings after **50 ms** of exposure tracked ratings after 500 ms.
- **Caveat:** this concerns appeal only, not credibility or usability.
- *Rule:* the first screen (onboarding, home) must make a confident visual impression immediately.

### Sonderegger & Sauer (2010): mobile phone specifically
"The influence of design aesthetics in usability testing", *Applied Ergonomics* 41 ([PDF](https://sonar.ch/documents/302271/files/Sonderegger_Sauer2010.pdf)) [S].
- 60 adolescents used a simulated phone with identical functions and two appearances.
- The attractive version was rated more usable **and gave faster task completion**.
- **Counter-finding:** their 2011 follow-up found higher aesthetics raised perceived usability but *lengthened* completion times. The performance effect is inconsistent; the perception effect is robust.

### Tuch et al. (2012): the important counterweight
"Is beautiful really usable?", *Computers in Human Behavior* 28(5), 1596–1607 [S]. 80 participants used one of four online-shop variants (aesthetics × usability).
- Aesthetics had **no effect** on perceived usability. Instead, **poor usability lowered perceived beauty**, mediated by frustration.
- *Implication:* beauty doesn't excuse friction. Bold styling on a broken flow makes the product look worse.

### Hassenzahl: pragmatic vs hedonic quality
Hassenzahl, M. (2004). The interplay of beauty, goodness, and usability in interactive products. *Human–Computer Interaction* 19(4) [U for exact citation]. AttrakDiff (2003) has 28 items [S].
- Users judge products on **pragmatic** quality (usable, useful) and **hedonic** quality (stimulation, identification) as separate dimensions. Beauty links strongly to **identification**: what the product says about me.
- *Rule:* hedonic quality is a measurable, independent product attribute, not frosting. Generic UI scores low on *stimulation* and *identity*.

### NN/g on flat design: weak signifiers cost time
- **[Moran 2017](https://www.nngroup.com/articles/flat-ui-less-attention-cause-uncertainty/) [V].** Eyetracking with 71 users on 9 page pairs (strong vs weak signifiers), using a between-subjects design.
  - Weak signifiers took **~22% more time** and produced **~25% more fixations** (p < .05). Gaze spread more widely.
  - In one pair, 86% of users went from the heading to the target with strong signifiers, vs 50% with weak.
  - Flat works only with low information density, conventional layouts, and high-contrast interactive elements.
  - (The study was on desktop, but the mechanism, uncertainty about what's tappable, is worse on touch, where there is no hover.)
- **[Moran 2015, Long-term exposure](https://www.nngroup.com/articles/flat-design-long-exposure/) [V].** Weak clickability cues train users into slow, exploratory tapping, and the habit carries over to other apps. Always include *some* signifier, and don't rely on hover.
- **[Flat 2.0](https://www.nngroup.com/articles/flat-design/) [S].** NN/g recommends mostly-flat design with subtle depth: shadows, contrast and button shapes.

### Google, Material 3 Expressive research (2022–2025)
Source: ["Better, Easier, Emotional UX"](https://design.google/library/expressive-material-design-google-research) [V for the page content]. **Company-reported, not peer-reviewed; no per-study n or statistics.**
- 46 studies, more than 18,000 participants. Methods: eyetracking, surveys, focus groups, experiments and usability tests.
- Key elements were spotted **up to 4x faster** (e.g., email Send). Users aged 45+ spotted elements as fast as younger users.
- Expressive design was preferred across all ages, **up to 87%** among 18–24-year-olds. It scored higher on energetic, playful and friendly attributes.
- **Their own caveats:**
  - It is not one-size-fits-all; banking, for example, relies on familiar patterns.
  - Breaking standard patterns (album-art grid replacing a song list) or **removing text labels** reduced usability.
  - A "strong minority" prefers calmer UI.
  - "No amount of expressive design will beat basic functionality."
- *Rule:* be expressive **through** standard patterns (bolder size, shape, colour and motion on familiar components), not by replacing them.

### Aarron Walter: *Designing for Emotion* (A Book Apart, 2011; 2nd ed. 2020)
Walter is the former UX lead at MailChimp (the Freddie mascot and voice) and a former InVision VP of Design Education [U for titles]. Source: [NN/g Theory of User Delight](https://www.nngroup.com/articles/theory-user-delight/) [S].
- **Hierarchy of user needs** (a remix of Maslow), from the bottom: **functional → reliable → usable → pleasurable**. Pleasure is the top tier and only counts once the lower ones hold.
- **Personality as a design asset.** Write a design persona (traits, voice, the "this but not that" pairs) that guides copy, colour, type and motion. Emotion creates memorable experiences, and people forgive problems when they feel positive (cf. Norman) [U for exact framing].
- *Rule:* write a one-paragraph **app persona** and a "this, not that" table (e.g., "confident, not arrogant; playful, not silly"). Apply it consistently to empty states, errors, success moments and loading states.

### NN/g: surface vs deep delight
Source: [Fessenden 2017](https://www.nngroup.com/articles/theory-user-delight/) [V].
- **Surface delight** is animations, microcopy, imagery and sound. It is cheap and easily gimmicky, and it fails on a weak product.
- **Deep delight** is flow: the interface meets the need and gets out of the way.
- *Rule:* deep delight is the goal. Surface delight goes on low-frequency moments (first success, an empty state, completion) and **never on high-frequency paths** (Apple says the same about motion). Tone it down for serious contexts such as money, health and strikes/disruptions.

### Stephen Anderson: *Seductive Interaction Design* (New Riders, 2011)
Anderson is a design consultant and author of the *Mental Notes* psychology card deck. Source: [Peachpit](https://www.peachpit.com/store/seductive-interaction-design-creating-playful-fun-and-9780321725523) [S].
- He applies psychology of motivation to UI: aesthetics, playfulness, curiosity, surprise, arousal, rewards, feedback loops, and the "stages of seduction" (attract → engage → retain).
- **Caveat:** a review notes the book is light on references. Use it for *techniques*, and cite Tractinsky, Hassenzahl and Google for *evidence*.
- *Rule:* use curiosity and progressive reveal for onboarding, variable reward sparingly and never manipulatively, and give completion a sense of accomplishment.

---

## 6. Platform guidelines: Apple HIG and Material Design 3

**Distinguish hard requirements from conventions.**
- **Hard (or close to hard):** these come from accessibility law/standards, store review, or OS enforcement: safe areas and insets, system back, Dynamic Type / font scale, VoiceOver/TalkBack labels, contrast.
- **Conventions:** expected patterns the skill can restyle boldly but should not *replace*: tab bar placement, navigation stacks, sheet behaviour.

### Apple Human Interface Guidelines (iOS/iPadOS)
Sources were read via Apple's own HIG JSON [V]: [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Typography](https://developer.apple.com/design/human-interface-guidelines/typography), [Layout](https://developer.apple.com/design/human-interface-guidelines/layout), [Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars), [Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures), [Motion](https://developer.apple.com/design/human-interface-guidelines/motion).

**Control size**
- **Default 44×44 pt; minimum 28×28 pt** (iOS/iPadOS table).
- **Spacing:** about 12 pt padding around bezelled controls, and about 24 pt around borderless ones.

**Text**
- **Default 17 pt, minimum 11 pt.** Avoid Ultralight, Thin and Light weights at small sizes.
- Support enlargement of **at least 200%**.
- Use text styles. Custom fonts must implement Dynamic Type and Bold Text.
- Layouts must adapt up to the AX sizes. Icons that carry meaning must scale with text.
- Don't use tight leading for 3 or more lines.
- iOS text styles at the default (Large) size [U for the table; standard values]: Large Title 34, Title1 28, Title2 22, Title3 20, Headline 17 semibold, Body 17, Callout 16, Subheadline 15, Footnote 13, Caption1 12, Caption2 11.

**Contrast**
- WCAG AA: 4.5:1 for text up to 17 pt; 3:1 at 18 pt or above, or bold. APCA is acknowledged.
- At minimum, honour Increase Contrast, and check both light and dark appearances.
- **Never use colour alone** (red–green and blue–orange are the problem pairs).

**Safe areas**
- Respecting safe areas is "essential" (Dynamic Island, home indicator, bars).
- Full-screen backgrounds extend under bars.
- iOS 26 **Liquid Glass**: controls float on glass above content, with scroll-edge effects instead of opaque bar backgrounds.

**Tab bars**
- They are for **navigation, not actions**. Keep them **visible** across sections (except under modals).
- **Never disable or hide tabs.** Explain empty sections instead.
- Always use labels, single words where possible. Use filled SF Symbols.
- Aim for five or fewer tabs when customisable. Use a sidebar or adaptive tab bar on iPad.

**Gestures**
- Don't repurpose standard gestures, and don't invent custom gestures for standard actions.
- Custom gestures **supplement**, never replace, e.g., keep the Back button as well as edge-swipe.
- Don't conflict with system edge gestures.
- **Always offer an on-screen alternative** to gestures.

**Motion**
- See §4. Honour Reduce Motion by swapping movement for fades.

### Material Design 3 / Android (Compose)
- **Touch target ≥ 48×48 dp (~9 mm), spacing ≥ 8 dp.** Recommended physical range 7–10 mm. Source: [Android Accessibility Help](https://support.google.com/accessibility/android/answer/7101858) [V]. Compose's `minimumInteractiveComponentSize()` enforces 48 dp for M3 components [U].
- **Navigation bar** for **3–5 destinations of equal importance** at compact width ([Compose docs](https://developer.android.com/develop/ui/compose/components/navigation-bar)) [V]. Use a navigation rail at medium/expanded widths and a drawer for many destinations or rare access [U for M3 breakpoint details: compact < 600 dp, medium 600–839, expanded ≥ 840].
- **Edge-to-edge is enforced** for apps targeting SDK 35 on Android 15. The opt-out is disabled when targeting Android 16 ([Android 15 behavior changes](https://developer.android.com/about/versions/15/behavior-changes-15)) [S]. **Hard requirement:** handle `WindowInsets` (status, navigation and IME). `Scaffold` helps.
- **Predictive back.** System animations (back-to-home, cross-activity) are **on by default for apps targeting Android 16 (API 36)** ([Android 16 behavior changes](https://developer.android.com/about/versions/16/behavior-changes-16)) [S].
  - *Rule:* never intercept back for anything except dismissing your own transient UI. Use `BackHandler` / `PredictiveBackHandler` correctly.
  - The system back gesture works from both screen edges, so don't put horizontal-swipe content at the very edges.
- **Font scale up to 200%** with **nonlinear scaling** since Android 14 ([Android 14 features](https://developer.android.com/about/versions/14/features)) [S].
  - Text in `sp` (including lineHeight), padding in `dp`, never `sp`.
  - Test at 200%.
  - Don't compute from `fontScale` / `scaledDensity`; use `TypedValue` / `FontScaleConverter`.
- **Motion:** use the tokens and springs above. M3 Expressive (2025) adds shape morphing, a larger type scale, and emphasised components ([Inside M3 Expressive](https://design.google/library/design-notes-material-3-expressive-liam-spradlin)) [S].
- **Colour:** use dynamic colour (Material You, from wallpaper) where it fits. A strong brand colour scheme is legitimate. Expressive guidance encourages bolder colour roles [U].

### Platform-fidelity rules for a cross-platform (KMP/CMP) agent
- **Keep each platform's mechanics:**
  - Back: iOS uses a top-left Back button plus edge swipe; Android uses system back and predictive back.
  - Sheets: iOS has detents; Android uses M3 modal bottom sheets.
  - Pickers, date/time inputs, haptics (`UIImpactFeedbackGenerator` vs `HapticFeedbackConstants`).
  - Typography scaling.
- **The brand layer can be shared:** colour, display type, iconography style, illustration and motion personality.
- Bold ≠ non-native. Google's own data says breaking standard patterns hurts. Express personality *on* native skeletons.

---

## 7. Accessibility: WCAG 2.2 mobile-relevant criteria

Source: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [What's new in 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/), [Understanding 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) [V]. Native apps are evaluated against WCAG via W3C's WCAG2ICT guidance, and the EU EN 301 549 / European Accessibility Act (applies from June 2025) [U for legal specifics].

| SC | Level | Mobile rule |
|---|---|---|
| 1.3.4 Orientation | AA | Don't lock to portrait or landscape unless essential. |
| 1.4.3 Contrast (Minimum) | AA | Text 4.5:1; large text 3:1. |
| 1.4.4 Resize Text | AA | Text resizable to 200% without loss. Use Dynamic Type / `sp`. |
| 1.4.10 Reflow | AA | Content works at 320 CSS px width without 2-D scrolling. Natively, this means layouts reflow at large text sizes. |
| 1.4.11 Non-text Contrast | AA | UI components, focus indicators, icons and chart marks 3:1 against adjacent colours. **Ghost buttons and pale outlines often fail.** |
| 1.4.12 Text Spacing | AA | No clipping when line or letter spacing increases. Avoid fixed-height text boxes. |
| 2.2.2 Pause, Stop, Hide | A | Auto-moving, blinking or auto-updating content (carousels, marquees, tickers) must be pausable. |
| 2.3.3 Animation from Interactions | AAA | Interaction-triggered motion can be disabled. Honour Reduce Motion / Remove animations. |
| 2.4.11 Focus Not Obscured (Min) | AA | Sticky bars or sheets must not fully hide the focused element (keyboard or switch users). |
| 2.5.1 Pointer Gestures | A | Multi-point or path gestures need a single-pointer alternative (e.g., ± buttons for pinch-zoom). |
| 2.5.2 Pointer Cancellation | A | Activate on the up-event. Sliding off cancels. |
| 2.5.3 Label in Name | A | The accessible name contains the visible label text (Voice Control: "tap Book"). |
| 2.5.4 Motion Actuation | A | Shake-to-undo or tilt features need a UI alternative and a way to disable them. |
| 2.5.5 Target Size (Enhanced) | AAA | 44×44 CSS px [U for the number on this fetch; it is the standard value]. |
| **2.5.7 Dragging Movements** | AA (new) | Every drag (reorder, slider, map pin, swipe-to-delete) needs a non-drag single-pointer alternative. |
| **2.5.8 Target Size (Minimum)** | AA (new) | **≥24×24 CSS px**, or pass the spacing exception (a 24 px circle on each undersized target doesn't intersect another target or circle). Other exceptions: equivalent, inline, user-agent, essential. Platform 44 pt / 48 dp exceeds this. Treat 24 as the legal floor, not the design target. |
| **3.2.6 Consistent Help** | A (new) | Help/contact appears in the same relative place across screens. |
| **3.3.7 Redundant Entry** | A (new) | Don't make users re-enter info already given in the same process. Autofill or offer it for selection. |
| **3.3.8 Accessible Authentication (Min)** | AA (new) | No cognitive-function test (memorising, transcribing, puzzles) to log in, unless an alternative is offered. Support paste, password managers, passkeys and biometrics. |
| 4.1.1 Parsing | (removed in 2.2) | — |

**Additional native-a11y rules** (from the HIG/Android sections above):
- Every icon-only control has an accessibility label.
- Group related elements for screen readers.
- Expose state (selected, expanded).
- Respect Bold Text, Increase Contrast, Reduce Transparency, Reduce Motion and font scale.
- Pair audio cues with haptics.

---

## 8. Cross-cutting numbers cheat-sheet

| Thing | Number | Source / status |
|---|---|---|
| iOS default control | 44×44 pt (min 28×28) | Apple HIG [V] |
| Android target | 48×48 dp ≈ 9 mm, ≥ 8 dp apart | Android a11y help [V] |
| WCAG 2.2 AA target | ≥ 24×24 CSS px | W3C [V] |
| Touch accuracy | centre ~7 mm, corners ~12 mm (95% of taps) | Hoober 2017 [V] |
| Grip | 49% one-hand, 36% cradle, 15% two-hand; 75% thumb | Hoober 2013/2017 [V] |
| Hidden nav cost | >20% lower discoverability; mobile tasks 15% slower | NN/g 2016 [V] |
| Weak signifiers | +22% time, +25% fixations | NN/g 2017 [V] |
| Response limits | 0.1 s / 1 s / 10 s | Miller 1968; Nielsen [V] |
| Doherty | < 400 ms | IBM 1982 [400 figure U] |
| Working memory | ~4 chunks (3–5) | Cowan 2001 [V] |
| First impression | appeal judged in 50 ms | Lindgaard 2006 [S] |
| iOS body | 17 pt default, 11 pt min; support ≥ 200% | Apple HIG [V] |
| Android font scale | up to 200%, nonlinear | Android 14 [S] |
| Text contrast | 4.5:1 (large 3:1); non-text 3:1 | WCAG 2.2 [V] |
| APCA | body Lc 75–90; headlines Lc 45–60; min Lc 30 | Myndex [V], not normative |
| Measure | 45–75 chars, ~66 ideal | Bringhurst [S] |
| M3 durations | 50–200 / 250–400 / 450–600 / 700–1000 ms | Compose tokens [V] |
| M3 emphasized easing | cubic (0.2, 0, 0, 1) | Compose tokens [V] |
| M3 Expressive spring (default spatial) | damping 0.8, stiffness 380 | Compose tokens [V] |
| Nav bar destinations | 3–5 | Android docs [V]; NN/g ≤ 4–5 [V] |
| M3 Expressive | key elements found up to 4x faster; preferred up to 87% (18–24) | Google, self-reported [V page, S evidence] |

---

## 9. Bibliography

### Books
- Albers, J. (1963). *Interaction of Color*. Yale University Press. https://www.davidzwirner.com/collect/josef-albers-interaction-of-color-book
- Anderson, S. P. (2011). *Seductive Interaction Design*. New Riders. https://www.peachpit.com/store/seductive-interaction-design-creating-playful-fun-and-9780321725523
- Bringhurst, R. (1992/2012). *The Elements of Typographic Style* (v4.0). Hartley & Marks. Web adaptation: https://webtypography.net/2.1.2
- Clark, J. (2015). *Designing for Touch*. A Book Apart. https://abookapart.com/products/designing-for-touch ; excerpt: https://alistapart.com/article/how-we-hold-our-gadgets/
- Cooper, A., Reimann, R., Cronin, D., Noessel, C. (2014). *About Face: The Essentials of Interaction Design* (4th ed.). Wiley. https://en.wikipedia.org/wiki/Application_posture
- Hoober, S. & Berkman, E. (2011). *Designing Mobile Interfaces*. O'Reilly.
- Hoober, S. (2021/2022). *Touch Design for Mobile Interfaces*. Smashing. https://www.smashingmagazine.com/ebooks/touch-design-for-mobile-interfaces-ebook/
- Johnson, J. (2020). *Designing with the Mind in Mind* (3rd ed.). Morgan Kaufmann/Elsevier. https://shop.elsevier.com/books/designing-with-the-mind-in-mind/johnson/978-0-12-818202-4
- Lupton, E. (2024). *Thinking with Type* (3rd ed.). Princeton Architectural Press.
- Norman, D. A. (2013). *The Design of Everyday Things* (rev. & exp.). Basic Books. https://jnd.org/the-design-of-everyday-things-revised-and-expanded/
- Norman, D. A. (2004). *Emotional Design*. Basic Books. https://www.getabstract.com/en/summary/emotional-design/6416
- Saffer, D. (2013). *Microinteractions: Designing with Details*. O'Reilly. https://www.oreilly.com/library/view/microinteractions/9781449342760/
- Shneiderman, B., Plaisant, C., et al. (2016). *Designing the User Interface* (6th ed.). Pearson. https://www.cs.umd.edu/users/ben/goldenrules.html
- Thomas, F. & Johnston, O. (1981). *The Illusion of Life: Disney Animation*. Abbeville.
- Tufte, E. R. (1983). *The Visual Display of Quantitative Information*; (1990) *Envisioning Information*; (2006) *Beautiful Evidence*. Graphics Press. https://www.edwardtufte.com/
- Walter, A. (2011; 2nd ed. 2020). *Designing for Emotion*. A Book Apart.
- Wroblewski, L. (2008). *Web Form Design*. Rosenfeld Media. https://static.lukew.com/WebForms_LukeW_101209.pdf
- Wroblewski, L. (2011). *Mobile First*. A Book Apart. https://static.lukew.com/MobileFirst_LukeW.pdf

### Papers
- Card, S. K., Robertson, G. G., Mackinlay, J. D. (1991). The information visualizer. *CHI '91*, 181–188.
- Chang, B.-W. & Ungar, D. (1993). Animation: from cartoons to the user interface. *UIST '93*, 45–55. https://bibliography.selflanguage.org/_static/animation.pdf
- Cowan, N. (2001). The magical number 4 in short-term memory. *Behavioral and Brain Sciences* 24(1), 87–185. https://pubmed.ncbi.nlm.nih.gov/11515286/
- Doherty, W. J. & Thadani, A. J. (1982). The economic value of rapid response time. IBM. https://www.vm.ibm.com/devpages/jelliott/evrrt10.html
- Fitts, P. M. (1954). The information capacity of the human motor system... *J. Exp. Psych.* 47(6), 381–391. https://cs303.stanford.edu/papers/1954-Fitts.pdf
- Hassenzahl, M. (2004). The interplay of beauty, goodness, and usability in interactive products. *Human–Computer Interaction* 19(4).
- Hick, W. E. (1952). On the rate of gain of information. *QJEP* 4, 11–26.
- Hyman, R. (1953). Stimulus information as a determinant of reaction time. *J. Exp. Psych.* 45, 188–196.
- Kurosu, M. & Kashimura, K. (1995). Apparent usability vs. inherent usability. *CHI '95 Companion*, 292–293. https://chi1995.chistatic.hosting.acm.org/proceedings/shortppr/mk_bdy.htm
- Lindgaard, G., Fernandes, G., Dudek, C., Brown, J. (2006). Attention web designers: You have 50 milliseconds... *Behaviour & IT* 25, 115–126. doi:10.1080/01449290500330448
- Miller, G. A. (1956). The magical number seven, plus or minus two. *Psychological Review* 63(2), 81–97.
- Miller, R. B. (1968). Response time in man-computer conversational transactions. *AFIPS FJCC* 33, 267–277.
- Shneiderman, B. (1983). Direct manipulation: A step beyond programming languages. *IEEE Computer* 16(8), 57–69. doi:10.1109/MC.1983.1654471
- Sonderegger, A. & Sauer, J. (2010). The influence of design aesthetics in usability testing. *Applied Ergonomics* 41. https://sonar.ch/documents/302271/files/Sonderegger_Sauer2010.pdf
- Tractinsky, N. (1997). Aesthetics and apparent usability. *CHI '97*. https://chi1997.acm.org/proceedings/paper/nt.html
- Tractinsky, N., Katz, A. S., Ikar, D. (2000). What is beautiful is usable. *Interacting with Computers* 13(2), 127–145. https://academic.oup.com/iwc/article/13/2/127/898608
- Tuch, A. N., Roth, S. P., Hornbæk, K., Opwis, K., Bargas-Avila, J. A. (2012). Is beautiful really usable? *Computers in Human Behavior* 28(5), 1596–1607. https://research.google/pubs/is-beautiful-really-usable-toward-understanding-the-relation-between-usability-aesthetics-and-affect-in-hci/

### Research articles and essays
- Budiu, R. (2015). Basic patterns for mobile navigation. NN/g. https://www.nngroup.com/articles/mobile-navigation-patterns/
- Budiu, R. Mobile UX: limitations and strengths. NN/g. https://www.nngroup.com/articles/mobile-ux/
- Fessenden, T. (2017). A theory of user delight. NN/g. https://www.nngroup.com/articles/theory-user-delight/
- Google Design. Better, easier, emotional UX (M3 Expressive research). https://design.google/library/expressive-material-design-google-research
- Google Design. Inside M3 Expressive. https://design.google/library/design-notes-material-3-expressive-liam-spradlin
- Hoober, S. (2013). How do users really hold mobile devices? UXmatters. https://www.uxmatters.com/mt/archives/2013/02/how-do-users-really-hold-mobile-devices.php
- Hoober, S. (2017). Design for fingers, touch, and people, Part 1. UXmatters. https://www.uxmatters.com/mt/archives/2017/03/design-for-fingers-touch-and-people-part-1.php
- Moran, K. (2015). Long-term exposure to flat design. NN/g. https://www.nngroup.com/articles/flat-design-long-exposure/
- Moran, K. (2017). Flat UI elements attract less attention and cause uncertainty. NN/g. https://www.nngroup.com/articles/flat-ui-less-attention-cause-uncertainty/
- Moran, K. (2024). The aesthetic-usability effect. NN/g. https://www.nngroup.com/articles/aesthetic-usability-effect/
- NN/g. Flat design: its origins, its problems, and why Flat 2.0 is better. https://www.nngroup.com/articles/flat-design/
- NN/g. Gestalt: proximity https://www.nngroup.com/articles/gestalt-proximity/ ; similarity https://www.nngroup.com/articles/gestalt-similarity/ ; common region https://www.nngroup.com/articles/common-region/
- Nielsen, J. (1993/2014). Response times: the 3 important limits. NN/g. https://www.nngroup.com/articles/response-times-3-important-limits/
- Nielsen, J. (1994/2024). 10 usability heuristics. NN/g. https://www.nngroup.com/articles/ten-usability-heuristics/
- Ottosson, B. (2020). A perceptual color space for image processing (Oklab). https://bottosson.github.io/posts/oklab/
- Pernice, K. & Budiu, R. (2016). Hamburger menus and hidden navigation hurt UX metrics. NN/g. https://www.nngroup.com/articles/hamburger-menus/
- Sherwin, K. (2014). Placeholders in form fields are harmful. NN/g. https://www.nngroup.com/articles/form-design-placeholders/
- Somers, A. / Myndex. APCA in a nutshell. https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html
- Willenskomer, I. Creating usability with motion: the UX in Motion manifesto. UX Magazine. https://uxmag.com/articles/creating-usability-with-motion-the-ux-in-motion-manifesto

### Standards and platform documentation
- Android: touch target size. https://support.google.com/accessibility/android/answer/7101858
- Android: navigation bar (Compose). https://developer.android.com/develop/ui/compose/components/navigation-bar
- Android 14 features (nonlinear font scaling). https://developer.android.com/about/versions/14/features
- Android 15 behavior changes (edge-to-edge). https://developer.android.com/about/versions/15/behavior-changes-15
- Android 16 behavior changes (predictive back). https://developer.android.com/about/versions/16/behavior-changes-16
- AndroidX Compose Material3 motion tokens. https://github.com/androidx/androidx/tree/androidx-main/compose/material3/material3/src/commonMain/kotlin/androidx/compose/material3/tokens
- Apple HIG: Accessibility https://developer.apple.com/design/human-interface-guidelines/accessibility ; Typography https://developer.apple.com/design/human-interface-guidelines/typography ; Layout https://developer.apple.com/design/human-interface-guidelines/layout ; Tab bars https://developer.apple.com/design/human-interface-guidelines/tab-bars ; Gestures https://developer.apple.com/design/human-interface-guidelines/gestures ; Motion https://developer.apple.com/design/human-interface-guidelines/motion
- Material Design 3. https://m3.material.io/
- W3C (2023). WCAG 2.2. https://www.w3.org/TR/WCAG22/ ; What's new: https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/ ; Understanding 2.5.8: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
