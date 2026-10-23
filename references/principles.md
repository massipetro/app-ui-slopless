# Principles: the studied basis, with sources

The condensed, citable rule set. Read it for Audit mode, when you need to justify a decision, or when two rules seem to conflict. For credentials, verification tags and the full bibliography, see `../research/literature.md`.

Cite the **ID** in audits (e.g. "breaks R-TOUCH-2"), so findings trace back to a source.

## Contents
- Evidence for the stance (why bold, why not broken)
- Cognition & perception (R-COG)
- Touch & reach (R-TOUCH)
- Navigation & structure (R-NAV)
- Forms & errors (R-FORM)
- Feedback & time (R-TIME)
- Type, colour, hierarchy (R-VIS)
- Motion (R-MOT)
- Emotion & delight (R-EMO)
- Platform (R-PLAT)
- macOS (R-MAC)
- Accessibility (R-A11Y)
- Resolving conflicts

---

## Evidence for the stance
| Finding | Source | Use it to argue |
|---|---|---|
| Aesthetics predicted perceived usability more than actual usability features (26 ATM layouts, 252 people) | Kurosu & Kashimura, CHI '95 | Look matters to how usable it *feels* |
| Aesthetics affected *post-use* perceived usability; actual usability didn't | Tractinsky, Katz & Ikar 2000, *Interacting with Computers* | The effect survives use |
| Visual appeal judged in 50 ms | Lindgaard et al. 2006 | First screen must land immediately |
| Weak signifiers took ~22% more time and ~25% more fixations | Moran, NN/g 2017 (eyetracking, n=71) | Bland flat UI has a measurable cost |
| Expressive UI: key elements found up to 4× faster, preferred by up to 87% of 18–24-year-olds; breaking patterns or removing labels hurt | Google M3 Expressive research, 2025 (company-reported) | Be bold *through* familiar patterns |
| Poor usability lowers perceived beauty | Tuch et al. 2012 | Bold can't rescue a broken flow |
| Hedonic quality (stimulation, identity) is distinct from pragmatic quality | Hassenzahl 2004; AttrakDiff | Personality is a product attribute |
| Functional → reliable → usable → pleasurable | Walter, *Designing for Emotion* | Order of work |

## Cognition & perception
- **R-COG-1 Signifiers.** Every action has a perceivable cue; affordance alone isn't enough. *Norman, DOET 2013.*
- **R-COG-2 Mapping.** Controls sit next to, and move like, what they change. *Norman.*
- **R-COG-3 Conceptual model.** Structure the screen around the user's domain model, not the data schema. *Norman; Cooper.*
- **R-COG-4 Working memory ~4 chunks.** Keep context visible, and chunk numbers in 3–4. *Cowan 2001; Budiu/NN/g on mobile external memory.*
- **R-COG-5 Recognition over recall.** Show options, recents and labels. Icon-only is for universal actions only. *Nielsen #6; Johnson.*
- **R-COG-6 Gestalt.** Proximity groups (gaps within a group < gaps between groups); similarity means same function; common region (cards) binds; connectedness beats both. *Wertheimer; Palmer; NN/g.*
- **R-COG-7 Feedback at the point of action.** Peripheral vision is poor; use motion or colour when the feedback must be far away. *Johnson, Designing with the Mind in Mind.*
- **R-COG-8 Colour vision is limited.** Never use colour alone. *Johnson; WCAG 1.4.1.*

## Touch & reach
- **R-TOUCH-1 Content in the centre, primary actions low, rare actions high.** People prefer looking at and touching the centre. 75% of touches are one-thumb. Grip changes often (49% one-handed, 36% cradled, 15% two-handed). *Hoober 2013/2017; Clark, Designing for Touch.*
- **R-TOUCH-2 Size by position.** ~7 mm in the centre, ~12 mm at the corners. Minimum 44 pt (iOS) / 48 dp ≈ 9 mm (Android), ≥8 dp spacing. *Hoober; Apple HIG; Android a11y.*
- **R-TOUCH-3 Fitts.** Big and close for frequent actions. Separate destructive actions from frequent ones. Make whole rows tappable. *Fitts 1954.*
- **R-TOUCH-4 Direct manipulation.** The object follows the finger 1:1, gestures can be cancelled mid-way, and effects are immediate and reversible. *Shneiderman 1983.*
- **R-TOUCH-5 Gestures are accelerators.** Always provide a visible alternative. Don't repurpose system gestures. *Apple HIG; Clark.*

## Navigation & structure
- **R-NAV-1 Visible navigation for ≤5 destinations.** Hidden navigation cut discoverability by >20%, and tasks took 15% longer on mobile. *Pernice & Budiu, NN/g 2016.*
- **R-NAV-2 One primary action per screen.** Hick–Hyman: choice time grows with log₂(n), and probability skew helps, so make the likely choice prominent. *Hick 1952; Hyman 1953.*
- **R-NAV-3 Goal-directed.** Name the primary persona's goal on each screen and cut what doesn't serve it. *Cooper, About Face.*
- **R-NAV-4 Remove excise.** No confirmations for reversible actions, no re-entering known data, no forced tours, no permission prompt before the value is shown. *Cooper.*
- **R-NAV-5 Microsessions.** Mobile sessions are often under 15 s. Design glanceable states (widgets, notifications, Live Activities) and restore state after interruptions. *NN/g; Johnson.*
- **R-NAV-6 Mobile first.** Use device capabilities (location, camera, autofill) to remove input. *Wroblewski.*

## Forms & errors
- **R-FORM-1 Persistent labels above fields.** Placeholders vanish, strain memory, often fail contrast, and aren't reliably read by screen readers. *Sherwin/NN/g 2014; Wroblewski; Penzo 2006.*
- **R-FORM-2 Right input.** Correct keyboard, autofill/content types, masks, defaults. Validate when the field is finished, not on each keystroke. *Wroblewski.*
- **R-FORM-3 Prevent errors with constraints.** Make invalid states impossible. *Norman; Nielsen #5; Shneiderman 5.*
- **R-FORM-4 Undo over confirm.** Confirm only destructive, irreversible actions. *Norman (slips); Shneiderman 6.*
- **R-FORM-5 Recoverable errors.** Say what happened and how to fix it, next to the cause, in plain words. *Nielsen #9.*
- **R-FORM-6 Closure.** Flows end in a clear success state with a summary. *Shneiderman 4.*

## Feedback & time
- **R-TIME-1 0.1 s / 1 s / 10 s.** Instant tap feedback; keep the flow of thought below 1 s; show determinate, cancellable progress beyond 10 s. *Miller 1968; Card et al. 1991; NN/g.*
- **R-TIME-2 ~400 ms for system responses** (a target, not a law). *Doherty & Thadani 1982, via secondary sources.*
- **R-TIME-3 Proportional feedback.** Modest for frequent actions, substantial for major ones. *Shneiderman 3.*
- **R-TIME-4 Visibility of system status.** Show sync, loading, offline and stale states. *Nielsen #1.*

## Type, colour, hierarchy
- **R-VIS-1 Deliberate scale.** 4–6 sizes with real jumps, and a display moment. Change one variable per level. *Bringhurst; Lupton.*
- **R-VIS-2 Measure.** 45–75 characters per line; cap the text column on tablets (~600–680 pt). *Bringhurst.*
- **R-VIS-3 Leading.** Body line height ~120–145%. No tight leading at 3 or more lines. *Bringhurst; HIG.*
- **R-VIS-4 Pairing.** One display face with character plus one workhorse text face. Never two near-identical sans faces. *Lupton.*
- **R-VIS-5 Colour is relative.** Judge it in context and in both themes. Tune brand colour separately for dark mode. Avoid equal-lightness complementary text pairs, because they vibrate. *Albers.*
- **R-VIS-6 Perceptual ramps.** Build palettes in OKLCH (even L steps, stable hue). Then check contrast, because L doesn't predict it. *Ottosson 2020.*
- **R-VIS-7 Data display.** Label data directly, use no 3D, start bars at zero, use sparklines in rows and small multiples over a dense multi-series chart. Data-ink applies to charts, not to the UI shell. *Tufte.*

## Motion
- **R-MOT-1 Solidity.** Objects travel; they don't teleport. *Chang & Ungar 1993.*
- **R-MOT-2 Easing always.** Enter decelerating, exit accelerating, exits shorter than entrances. *Willenskomer; M3 motion tokens.*
- **R-MOT-3 Springs for gestures.** Interruptible and velocity-preserving. M3 Expressive spatial springs are default (0.8, 380), fast (0.6, 800), slow (0.8, 200). Colour and alpha never bounce. *androidx MotionTokens.*
- **R-MOT-4 Stagger shows grouping.** Short offsets; things that move together belong together. *Willenskomer; Gestalt common fate.*
- **R-MOT-5 Continuity.** Container transforms and shared elements preserve place. *Willenskomer.*
- **R-MOT-6 Purposeful, brief, cancellable.** No motion on very frequent interactions. Never block input. *Apple HIG Motion.*
- **R-MOT-7 Reduce Motion.** Swap x/y/z moves for fades, and stop loops and parallax. *Apple HIG; WCAG 2.3.3.*

## Emotion & delight
- **R-EMO-1 Three levels.** Make deliberate choices at the visceral (look), behavioural (use) and reflective (meaning) levels. *Norman, Emotional Design.*
- **R-EMO-2 Personality persona.** Write a one-paragraph app persona with "this, not that" pairs, and apply it to copy, empty states, errors and success. *Walter.*
- **R-EMO-3 Surface vs deep delight.** Deep delight is flow. Surface delight belongs on low-frequency moments only, never on frequent paths. *Fessenden/NN/g 2017.*
- **R-EMO-4 Microinteractions.** Trigger → rules → feedback → loops/modes. Personality lives here cheaply. Avoid modes. *Saffer.*
- **R-EMO-5 Seduction without manipulation.** Curiosity, progressive reveal, earned rewards. No dark patterns or manipulative variable rewards. *Anderson.*
- **R-EMO-6 Context.** Calm the tone for money, health, safety and bad news. *Google M3E caveats; NN/g.*

## Platform
- **R-PLAT-1 Hard requirements.** Safe areas/insets (edge-to-edge enforced from Android SDK 35), system back and predictive back (default when targeting API 36), Dynamic Type / `sp` to 200%, screen-reader labels.
- **R-PLAT-2 Conventions you can restyle, not replace.** Bottom tab/navigation bar (3–5 labelled destinations, always visible, never disabled), navigation stack, sheets, system pickers. *Apple HIG Tab bars; M3 Navigation bar.*
- **R-PLAT-3 Share the brand layer, keep native mechanics.** Colour, type, icons, illustration and motion personality are shared; back, sheets, pickers and haptics are native. *Google M3E research; HIG.*
- **R-PLAT-4 macOS hard requirements.** Visible, clickable traffic lights and a draggable title area; the standard menu bar (App, File, Edit, View, Window, Help) with the system commands intact; full keyboard access; VoiceOver labels; Reduce Motion and Reduce Transparency honoured. See R-MAC-*.

## macOS
The R-TOUCH rules are about thumbs. On a Mac the input is a pointer and a keyboard, and the unit of design is a resizable window. Sources: Apple HIG (macOS sections: Windows, Sidebars, Toolbars, Menus, Keyboards, Pointing devices, Typography), Fitts 1954 (pointer targets), Nielsen heuristics #6 and #7 (recognition, accelerators).
- **R-MAC-1 Windows, not screens.** Declare a minimum window size, compose at minimum, typical and full-screen sizes, and reflow (adaptive grids, a capped reading column) rather than scale. A stretched phone layout fails. *HIG Windows; Cooper on posture (sovereign apps).*
- **R-MAC-2 Sidebar for navigation, toolbar for actions, inspector for properties.** Sidebars hold many destinations, so the R-NAV-1 limit of five is relaxed; keep labels visible. Primary action in the toolbar with a menu twin and a shortcut. *HIG Sidebars, Toolbars.*
- **R-MAC-3 Hover and right-click are signifiers.** Every clickable custom control shows hover, pressed, focus and disabled states; rows and cards with actions have a context menu; icon-only controls have a tooltip. Hover can't be the *only* signifier: keyboard and VoiceOver users never see it, and a still can't show it. *Norman R-COG-1; HIG Pointing devices.*
- **R-MAC-4 Keyboard and menu bar are the accelerators.** Every command is in the menu bar; daily actions have shortcuts that never reuse system ones (⌘N/O/S/W/Q/,/Z/X/C/V/A/F/H/M); everything is reachable by keyboard; Return and Escape are the default and cancel actions. *Nielsen #7; HIG Keyboards.*
- **R-MAC-5 Control size and density.** A regular control is 22 pt (small 18, large 28); lists run 22-44 pt rows. Stay ≥24×24 pt for icon buttons including padding (WCAG 2.5.8). Dense is correct on a Mac; sparse phone spacing is a tell. *HIG Layout; Fitts.*
- **R-MAC-6 Fixed type, real scale.** No Dynamic Type: body is 13 pt, smallest 10 pt, secondary 11-12. Keep a decisive display moment (R-VIS-1) and offer in-app zoom where content is dense. *HIG Typography.*
- **R-MAC-7 Appearance is the user's.** Light, dark, accent colour, Increase Contrast and Reduce Transparency are honoured; the sidebar's vibrancy is chrome, and replacing it is a stated convention break. Inactive windows dim. *HIG Dark Mode, Materials.*
- **R-MAC-8 Undo, not confirm.** Reversible actions register with `UndoManager`; only irreversible ones prompt, and the prompt names the object and the verb. *Norman; HIG Managing windows; R-FORM-4.*
- **R-MAC-9 Windows keep their promise.** Window frame and per-window state are restored; settings live in ⌘, with immediate effect; a menu-bar extra shows one glanceable live state. *HIG Settings, Menu bar extras.*

## Accessibility (WCAG 2.2 AA through WCAG2ICT; Section 508; EN 301 549)
Criteria are WCAG 2.2 success criteria read for software (WCAG2ICT, W3C 2025): a "page" is a screen or window, a CSS px is a pt or dp. Sources and the gap audit: `../research/accessibility-references.md`. The checks and the Accessibility line: `accessibility.md`.
- **R-A11Y-1 Contrast.** Text 4.5:1, large text (18 pt, or 14 pt bold) 3:1 (1.4.3). UI component edges, states and meaningful graphics 3:1 against their neighbours (1.4.11). Measure the pairs on screen in light and dark, not only the palette. APCA is the dark-mode sanity check (Lc 75 body, Lc 60 other text, Lc 45 large text). *WCAG 1.4.3/1.4.11; Apple HIG Accessibility; ATF ContrastUtils.*
- **R-A11Y-2 Resize.** Text scales to the platform's largest size with no loss (1.4.4, "up to the text sizing capabilities of the platform", WCAG2ICT): iOS AX5 (body 17 → 53 pt), Android font scale 2.0 (nonlinear). It reflows rather than clipping or scrolling sideways (1.4.10). Render it. macOS has no Dynamic Type; offer in-app zoom. *HIG Typography; Android 14 font scaling; Apple Larger Text criteria (≥200%).*
- **R-A11Y-3 Targets.** Minimum 24×24 pt/dp (2.5.8 AA); use the platform 44/48 instead (macOS: 22 pt controls with ≥24×24 pt hit areas for icon buttons, R-MAC-5).
- **R-A11Y-4 Motion and flashing.** Auto-moving content over 5 s can be paused (2.2.2); interaction motion follows Reduce Motion (2.3.3); nothing flashes more than three times a second (2.3.1).
- **R-A11Y-5 Gestures.** Path and multi-point gestures have single-pointer alternatives (2.5.1); dragging has a non-drag alternative (2.5.7); every gesture-only action is also an accessibility action (`accessibilityAction(named:)`, `customActions`). Actions fire on release (2.5.2). *WCAG; Android accessibility principles.*
- **R-A11Y-6 Orientation.** Don't lock orientation unless it's essential (1.3.4).
- **R-A11Y-7 Focus not obscured.** Sticky bars mustn't hide the focused item (2.4.11).
- **R-A11Y-8 Name, role, value.** Use the real control and style it; a custom one exposes its name, role and state to the accessibility API (4.1.2; 508 502; EN 11.5). A tap gesture on a shape has no role, no state and no keyboard path. *WCAG2ICT 4.1.2; Apple `onTapGesture` docs; Compose tap-and-press docs.*
- **R-A11Y-9 Text alternatives.** Every picture that carries meaning has a text alternative that says what it means; decoration is marked decorative (1.1.1). Drawn gauges and charts carry a value. *Apple VoiceOver evaluation criteria.*
- **R-A11Y-10 Label in name.** The accessible name starts with the visible words, so Voice Control and Voice Access can say it (2.5.3). *WCAG Understanding 2.5.3; Apple Voice Control criteria.*
- **R-A11Y-11 Order and modality.** Reading and focus order follow the meaning (1.3.2, 2.4.3). Custom overlays are modal to assistive tech and close with Escape (2.1.2). Headings are marked (1.3.1, 2.4.6).
- **R-A11Y-12 Colour alone.** See R-COG-8 (1.4.1). Honour Differentiate Without Colour. Test in grayscale. *Apple Differentiate Without Color Alone criteria.*
- **R-A11Y-13 Keyboard.** Everything works with Full Keyboard Access, Switch Control and a hardware keyboard (2.1.1); single-key shortcuts can be turned off or work only on focus (2.1.4); focus is visible (2.4.7).
- **R-A11Y-14 Status and titles.** Status messages are announced without moving focus (4.1.3). Each screen and window has a title (2.4.2; EN 301 549 V4.1.1 11.2.4.2).
- **R-A11Y-15 Input purpose.** Personal-data fields declare their content type, so autofill and password managers work (1.3.5, 3.3.7, 3.3.8).
- **R-A11Y-16 User preferences.** Follow the platform's settings: text size, Bold Text, Increase Contrast, Reduce Transparency, Reduce Motion, dark appearance (508 503.2; EN 301 549 11.7).
- **R-A11Y-17 Claims.** Conformance uses VPAT 2.5Rev's terms: Supports, Partially Supports, Does Not Support, Not Applicable; "Not Evaluated" only at AAA. Each needs a reason. An Apple Accessibility Nutrition Label needs every common task to work. Evidence from code, lint and renders is a draft, not an assistive-technology test: say which it is. *ITI VPAT 2.5Rev; Apple App Store Connect.*

## Resolving conflicts
- **Bold vs Nielsen #8 (minimalist).** #8 is about removing *irrelevant information*, not visual character. Keep the content lean and the visual identity strong.
- **Hoober (centre) vs Clark (bottom).** Put content in the centre and primary actions low. Never put the only primary CTA top-right.
- **Delight vs speed.** Delight goes on low-frequency moments. If a delightful animation sits on a path used 20 times a day, cut it to ≤200 ms or remove it.
- **Style vs contrast (user chose "warn, don't block").** Keep the style, report the exact ratio and the compliant alternative, and mark the criterion "Partially supports" on the Accessibility line. The warning covers contrast, type size and motion intensity only: names, roles, order, scaling, actions and announcements cost nothing visually and are never traded (R-A11Y-8–16).
