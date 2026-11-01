# Accessibility references: conformance reports, store labels, assistive tech, text scaling

Researched 2026-10-23 for the accessibility work on the `accessibility` branch: what an Accessibility
Conformance Report (ACR, written on the ITI VPAT template) asks of a native app, what the platforms and
stores ask, and what assistive technologies need from custom SwiftUI and Compose controls. The last
section is the gap audit: what the skill enforced at `dcf1211`, criterion by criterion, and what this
branch adds.

**Method.** Two research passes read primary sources (w3.org, itic.org, access-board.gov, etsi.org,
developer.apple.com, developer.android.com, kotlinlang.org, AOSP) and noted the URL each claim was read
on. Anything not confirmed on a fetched page is marked **(unverified)**. Apple developer pages were read
through their DocC JSON endpoints, which serve the same text as the page. Short quotes only. Section 8
adds one local measurement. Citation keys in sections 7–11 (`[A-label]`, `[D-sem]` …) resolve in the
second source list at the end.

**Read this first: what a skill can and can't claim.** Every conformance answer this skill writes comes
from code review, lint and renders. None of it is a test with VoiceOver, TalkBack, Switch Control, Voice
Control or a keyboard on a device. An ACR built on it is a draft for a human evaluator to verify, and the
report says so (SKILL.md, Accessibility line; `scripts/acr.py`).

# Part A: conformance, stores and platform guidance

## 1. VPAT 2.5 (ITI)

Sources: ITI VPAT page https://www.itic.org/policy/accessibility/vpat. Template text was read from the ITI-hosted .docx files linked there (INT https://www.itic.org/dotAsset/2434a080-87fe-4db1-815e-1e032bf7ac09.docx, 508 https://www.itic.org/dotAsset/c9497d16-4684-480c-bae2-99256283731c.docx, WCAG https://www.itic.org/dotAsset/67270ffc-91e8-4812-9481-8067621f24fd.docx).

**Version**
- The current version is **VPAT 2.5Rev**. ITI's page dates it **April 2025**, and the template files are listed as "(April 2025)". There is also a "Change Tracking" docx. (itic.org/policy/accessibility/vpat)
- Mirrors on other sites carry an earlier "February 2025" 2.5Rev, so April 2025 is the latest ITI posting. Whether the two differ in content is **(unverified)**.

**Editions** (itic.org/policy/accessibility/vpat)
- **508**: Revised Section 508. The ITI page says this edition incorporates WCAG 2.0.
- **EU**: EN 301 549, incorporating WCAG 2.1. The INT template lists V3.1.1 (2019-11) and V3.2.1 (2021-03) and says "the criteria are identical" (INT docx).
- **WCAG**: WCAG 2.x, incorporating WCAG 2.2.
- **INT**: combines all three.

**Report sections** (INT docx)
- Heading info: Name of Product/Version, Report Date, Product Description, Contact Information, Notes, Evaluation Methods Used.
- Applicable Standards/Guidelines table: WCAG 2.0, 2.1 and 2.2 at Level A, AA and AAA (each Yes/No), Revised 508, EN 301 549.
- Terms.
- WCAG 2.x Report: Table 1 Level A, Table 2 Level AA, Table 3 Level AAA. Tables 1 and 2 also document EN 301 549 clause 9, 10.1-10.4, 11.1-11.4 and 11.8.2, 12.1.2 and 12.2.4, and 508 sections 501.1, 504.2 and 602.3.
- Revised Section 508 Report: Chapter 3 Functional Performance Criteria, Chapter 4 Hardware, Chapter 5 Software, Chapter 6 Support Documentation and Services.
- EN 301 549 Report: Clause 4 Functional Performance Statements, then Clauses 5 Generic, 6 Two-Way Voice, 7 Video, 8 Hardware, 9 Web (refers to the WCAG section), 10 Non-Web Documents, 11 Software, 12 Documentation and Support Services, 13 Relay/Emergency.
- Legal Disclaimer.
- Each table has three columns: Criteria | Conformance Level | Remarks and Explanations.
- Example from the template: 4.1.1 Parsing is "Always answer 'Supports'" for WCAG 2.0 and 2.1, and is marked obsolete for WCAG 2.2 (INT docx).

**Conformance terms**: exact ITI definitions, the same in the INT, 508 and WCAG docx
- **Supports**: "at least one method that meets the criterion without known defects", or meets it "with equivalent facilitation".
- **Partially Supports**: "Some functionality of the product does not meet the criterion."
- **Does Not Support**: "The majority of product functionality does not meet the criterion."
- **Not Applicable**: "The criterion is not relevant to the product."
- **Not Evaluated**: "has not been evaluated against the criterion." It "can only be used in WCAG Level AAA criteria." This AAA-only restriction appears in the INT, 508 and WCAG templates I extracted. The EU edition was not opened. A search snippet of a third-party copy of the EU template shows the same wording **(unverified on ITI's EU docx)**.
- The template notes that in the WCAG tables a report "may use 'Supports'" where N/A seems natural, because WCAG treats a criterion with no applicable content as satisfied.
- If a vendor deviates from these definitions, it must say so in the heading Notes section.

**Remarks and Explanations column** (INT docx)
- Its purpose is to "justify your answer in the Conformance Level column."
- For Partially Supports or Does Not Support, the remarks should identify the affected functions or features and how they fall short.
- If the criterion does not apply, explain why. If an accessible alternative is used, describe it.
- It may also hold:
  - testing information;
  - dependencies such as OS, app frameworks or browsers;
  - bug IDs;
  - known workarounds.
- Every criterion must have both a Conformance Level and a Remarks response. Sections, but not individual criteria, may be removed.

---

## 2. WCAG2ICT and the mobile guidance (MATF)

Source: https://www.w3.org/TR/wcag2ict-22/

**Status**
- W3C Group Note, current version **11 December 2025**.
- Earlier versions are dated 21 Aug 2025 and **15 Nov 2024** (the 2024 update covering WCAG 2.1 and 2.2).
- It is informative and non-normative. The AG Working Group endorses it, but W3C as a whole does not.

**Word substitution**
- "web page(s)" becomes "document(s)" or "software". "Set of web pages" becomes "set of documents" or "set of software programs".
- Examples on the page:
  - 1.4.2 Audio Control: "web page" becomes "non-web document or software".
  - 1.4.10 Reflow: "web content" becomes "content".
  - 4.1.2: the user-agent wording becomes "assistive technologies and accessibility features of underlying software".
  - 2.5.8: "user agent" becomes "user agent or other platform software".

**Criteria that only apply to a "set of software programs"**
- WCAG2ICT names these as 2.4.1, 2.4.5, 3.2.3, 3.2.4 and 3.2.6.
- A set's programs must be independently launchable and linked by a consistent navigation method. Such sets are "extremely rare".
- If it is ambiguous whether the group is a set, "then the group is not a set."
- **2.4.1 Bypass Blocks**: a standalone program meets it automatically. Bypassing repeated blocks within a program is recommended but not required.
- **2.4.5 Multiple Ways**: applies only to sets. Navigation and search count, including file directories and file-system search.
- **3.2.3 and 3.2.4**: apply across a set. Consistency within a single program is best practice.
- **2.4.2 Page Titled**: direct substitution is problematic, so WCAG2ICT gives replacement text. For non-web software, on platforms that support window or screen titles, each window or screen gets a title that "describe[s] the name, topic or purpose."
- WCAG2ICT notes that Section 508 and EN 301 549 exclude 2.4.1, 2.4.5, 3.2.3 and 3.2.4 for software. It also notes that EN 301 549 excludes 2.4.2 and 3.1.2 for non-web software. (The latter matches V3.2.1. V4.1.1 differs; see section 3.)

**Notes on specific criteria**
- **1.4.4 Resize Text**: if the platform scales only some text to 200%, the software should follow the platform's text sizing to that extent. Software can meet it through its own zoom or by working with platform features.
- **1.4.10 Reflow**: 320 CSS px wide for vertical scrolling and 256 CSS px tall for horizontal scrolling (equal to a 1280 px viewport at 400%). Exceptions are content that needs two-dimensional layout: maps, diagrams, video, games, presentations, data tables, and toolbars that must stay in view. For non-web software, it applies when users scale content, resize a window, or change resolution.
- **2.5.8 Target Size (Minimum)**: 24×24 CSS px. Exceptions are spacing, equivalent control, inline, size set by the user agent or platform software, and essential.
- **"CSS pixel" for software**: use the platform's density-independent unit: "points (pt) for iOS and macOS", dp for Android, epx for Windows. Otherwise, derive it from a plausible viewing distance (about 28 in / 71 cm for touchscreens) divided by 2688. The page also states that 1 pt equals 1.333 CSS px.
- **4.1.2 Name, Role, Value**:
  - "Standard user interface components on most accessibility-supported platforms already satisfy" it.
  - Using platform accessibility services or APIs is best practice. They can also expose available actions.
  - The glossary cites AccessibleName and AccessibleRole as examples.
  - 1.3.1 programmatic determination is best achieved through platform accessibility APIs.
- **4.1.3 Status Messages**: still applies without markup. Expose status messages through platform accessibility services.
- **Closed functionality**: there is an appendix of criteria that need alternate provisions when AT can't be attached (listed starting 1.1.1, 1.2.1, 1.2.3, 1.3.1, 1.3.2…). The full list was truncated in my fetch **(unverified beyond those)**.

**Mobile Accessibility Task Force (MATF)**
- **"Guidance on Applying WCAG 2.2 to Mobile Applications (WCAG2Mobile)"** is a W3C **Group Draft Note dated 06 May 2025**. https://www.w3.org/TR/wcag2mobile-22/ It covers WCAG 2.2 A and AA for native, mobile-web and hybrid apps on phones and tablets. It is modelled on WCAG2ICT. It replaces the 2015 draft "Mobile Accessibility: How WCAG 2.0… Apply to Mobile".
- Mobile-specific choices in the draft (w3.org/TR/wcag2mobile-22):
  - "set of web pages" becomes **"set of screens"**, and the unit of conformance is a single screen. That definition is marked Work in Progress.
  - 1.4.12: not applicable if the platform offers no way to override text style.
  - 1.4.10 guidance is still Work in Progress.
- The **Editor's Draft dated 14 October 2026** is at https://w3c.github.io/matf/. Its 1.4.4 text: resize up to 200% or "up to the text sizing capabilities of the platform". This is still marked Work in Progress. I couldn't read its 2.5.8 mobile text (page truncated) **(unverified)**.

---

## 3. Section 508, EN 301 549 and the European Accessibility Act

### Revised Section 508 (36 CFR 1194, Appendices A, C)

Source: https://www.access-board.gov/ict/

- **E205.4**: electronic content conforms to **WCAG 2.0 Level A and AA**. Non-web documents are exempt from 2.4.1, 2.4.5, 3.2.3 and 3.2.4.
- **E207.2**: software UI components and content conform to WCAG 2.0 A and AA. Non-web software is exempt from 2.4.1, 2.4.5, 3.2.3 and 3.2.4, and from Conformance Requirement 3 (Complete processes). E207.2.1 replaces "Web page" or "page" with "software".
- **502 Interoperability with AT** 502.2.1: user control over platform accessibility features. 502.2.2: software "shall not disrupt platform features" documented as accessibility features. 502.3: documented accessibility services. 502.3.1-502.3.14: object information (name, role, state, boundary), values, text, label and parent-child relationships, actions, focus and selection, event notification. 502.4: platform features per ANSI/HFES 200.2.
- **503 Applications** **503.2 User Preferences**: applications must "permit user preferences from platform settings" for **color, contrast, font type, font size, and focus cursor**. This doesn't apply to applications designed to be isolated from the platform, including web apps. 503.3: an alternative UI that works as AT must use platform accessibility services. **503.4**: where video with synchronized audio is shown, provide "user controls for closed captions and audio descriptions".
    - 503.4.1: caption controls at the same menu level as volume or program selection.
    - 503.4.2: audio description controls at the same menu level as program selection.

### EN 301 549 (ETSI/CEN/CENELEC)

Source: ETSI deliver directory https://www.etsi.org/deliver/etsi_en/301500_301599/301549/

- The directory lists V3.2.1 (03.02.01_60, 2021-03), a V4.1.0 draft (04.01.00_20, Nov 2025; 04.01.00_30, Jun 2026), and **V4.1.1 (04.01.01_60, published 2 Sep 2026)**.
- I extracted text from both PDFs:
  - https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf
  - https://www.etsi.org/deliver/etsi_en/301500_301599/301549/04.01.01_60/en_301549v040101p.pdf

**V3.2.1 (2021-03)** (V3.2.1 PDF)
- Clauses 9-11 are based on **WCAG 2.1**.
- Software clauses 11.2.4.1, 11.2.4.2, 11.2.4.5, 11.3.2.3 and 11.3.2.4 are Void.
- 11.5 is "Interoperability with assistive technology" (11.5.2.1-11.5.2.17). 11.6 is "Documented accessibility usage".
- **11.7 User preferences**: software that isn't isolated from its platform "shall follow the values of the user preferences for platform settings" for units of measurement, colour, contrast, font type, font size and focus cursor, "except where they are overridden by the user".

**V4.1.1 (2026-09)** (V4.1.1 PDF)
- It is a "HARMONISED EUROPEAN STANDARD". Clauses 9, 10 and 11 are "updated to align with the WCAG 2.2".
- It was prepared under standardisation request M/587 (C(2022) 6456) for **Directive (EU) 2019/882 (EAA)**. It adds Annex ZB (EAA mapping), clause A.2 (EAA conformance) and Annex ZA (Web Accessibility Directive 2016/2102).
- Presumption of conformity applies only "Once the present document is cited in the Official Journal".
- Dates: adoption 24 Aug 2026; latest announcement 30 Nov 2026; national publication 31 May 2027; withdrawal of conflicting standards 31 May 2028.
- **5.2 Activation of accessibility features**: documented accessibility features must be activatable "without relying on a method that does not support that need". The text is the same in substance as V3.2.1.
- Software changes from V3.2.1:
  - 11.2.4.1 Bypass blocks and 11.2.4.5 Multiple ways stay Void ("extremely rare" sets).
  - **11.2.4.2 is now "Non-web software titled"**: titles for each window or screen where the platform supports titles.
  - 11.3.2.3 Consistent navigation and 11.3.2.6 Consistent help are Void.
  - **11.3.2.4 Consistent identification is now a requirement**, scoped to "a non-web software program".
  - **11.2.5.8 Target size (minimum)**: 24×24 CSS px with WCAG 2.2's exceptions, plus "User agent or other platform software control".
  - **11.1.4.4 Resize text**: up to 200%, or "up to the text sizing capabilities of the platform".
  - **11.1.4.10 Reflow**: 320/256 CSS px. Its Note 3 points to the WCAG2ICT CSS-pixel guidance.
  - 11.4.1.2 Name, role, value: notes match WCAG2ICT ("Standard user interface components… already satisfy").
- **11.5** is renamed "Interoperability with keyboards and assistive technology". 11.5.2.2 is Void, merged into 11.5.2.1. 11.5.2.3 "Use of accessibility services" is now a recommendation ("should"). 11.5.2.5-11.5.2.17 (object information … modifications of values and text) are kept.
- **11.6 Documented accessibility features**: 11.6.1 user control, and 11.6.2 non-web software "shall not disrupt" platform accessibility features.
- **11.7 User preferences**: rewritten as generic. Non-web software that isn't isolated from its platform "shall follow the values of the user preference settings for documented platform accessibility features" unless that is essential. Note 6 gives examples: colour filters, contrast, text size, pointer size, text cursor.

### European Accessibility Act (Directive (EU) 2019/882)
- AccessibleEU (European Commission) says the EAA "will come into effect on 28 June 2025". https://accessible-eu-centre.ec.europa.eu/content-corner/news/eaa-comes-effect-june-2025-are-you-ready-2025-01-31_en
- The Commission's EAA page says member states had to transpose it by June 2022. https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en
- Neither page names EN 301 549.
- **Which EN 301 549 version the EAA references** The directive doesn't name a version. Presumption of conformity comes from harmonised standards cited in the OJEU (Art. 15) **(unverified; the EUR-Lex text didn't load)**. V4.1.1 is the first edition prepared for the EAA, and it isn't effective until OJEU citation. V3.2.1 was prepared for the Web Accessibility Directive 2016/2102 (V4.1.1 foreword). A third-party source expects V4.1.1 to be cited around Nov-Dec 2026 and advises V3.2.1 until then **(unverified)**. https://www.dwt.com/insights/2026/09/european-accessibility-act-ict-standards-update (search snippet only)

---

## 4. Apple App Store Accessibility Nutrition Labels

Overview: https://developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels

**Announcement and rollout**
- Announced in an Apple Newsroom post on **13 May 2025** (ahead of WWDC25). https://www.apple.com/newsroom/2025/05/apple-unveils-powerful-accessibility-features-coming-later-this-year/
- WWDC25 session 224 is "Evaluate your app for Accessibility Nutrition Labels". https://developer.apple.com/videos/play/wwdc2025/224/ (not opened)
- App Store Connect release notes, 8 June 2026: "Apps in tvOS now support the Larger Text Accessibility Nutrition Label." https://developer.apple.com/help/app-store-connect/release-notes

**The nine features** (overview page)
- VoiceOver
- Voice Control (not on Apple TV or Apple Watch)
- Larger Text (overview says "not supported on Mac")
- Dark Interface
- Differentiate Without Color Alone
- Sufficient Contrast
- Reduced Motion
- Captions
- Audio Descriptions

**How declarations work** (overview page)
- Developers declare **per device** in App Store Connect and are prompted only for features that apply to that device.
- The App Store shows the label for the device the viewer is browsing on.
- If nothing is declared, the section still appears, saying support isn't indicated yet.
- A feature can be claimed only if users "can complete all of the app's common tasks" with it. Common tasks are:
  - primary functionality;
  - first launch and onboarding;
  - login, including account creation and password reset;
  - purchase;
  - settings.
- Uncommon tasks are described via the accessibility URL instead. Third-party or user-generated content counts only when it is part of a common task.

**Per-feature criteria** (each page is under https://developer.apple.com/help/app-store-connect/manage-app-accessibility/)
- **VoiceOver** (voiceover-evaluation-criteria) Every element has a concise label ("New Message"), with no control type or state in the label (use traits). Decorative images are hidden. Charts need a chart API or a text alternative. Element type, state and value are announced. Logical swipe order with no skipping or looping. Grouped items are reachable or exposed as custom actions. Long-press and context actions are custom actions. Complex gestures have alternatives. Modals hide background content and dismiss with escape / `accessibilityPerformEscape`. Status alerts are posted via `AccessibilityNotification`. Background refreshes don't reset the cursor.
- **Voice Control** (voice-control-evaluation-criteria) All controls can be activated via "Show names" / "Show numbers". Labels match visible text; use `accessibilityInputLabels(_:)`. Speakable alternatives for swipes, long presses and multi-touch. Dictation and text editing work in custom text fields.
- **Larger Text** (larger-text-evaluation-criteria) Text enlarges to "at least 200% or the maximum font size for the system". Dynamic Type, or an equivalent in-app control. iOS Dynamic Type goes beyond 200% at AX3 and beyond 300% at AX5. watchOS's largest size is "larger than 140%" of default. tvOS: support the largest Dynamic Type size, and headings stay larger than descriptions. No overlapping text. No truncation that makes text unreadable or ambiguous (prefer wrapping). Truncated list text must be available in full in a detail view. Stack side-by-side elements at large sizes. Tab bars don't scale, so use the Large Content Viewer. System Zoom or Hover Text can't be used to claim support. This page mentions Mac body text, which conflicts with the overview's "not supported on Mac". Treat Mac as excluded.
- **Dark Interface** (dark-interface-evaluation-criteria) Dark by default for common tasks, or a user-enabled dark mode (system Dark Mode or a custom scheme). Smart Invert is "a last resort". An in-app setting must match or exceed the system setting.
- **Differentiate Without Color Alone** (differentiate-without-color-alone-evaluation-criteria) Common tasks don't use color as the only cue; add shape, icon, position or text. Where color is essential (charts), offer alternate schemes. Test with the Grayscale filter.
- **Sufficient Contrast** (sufficient-contrast-evaluation-criteria) Meet contrast by default: "usually 4.5 to 1" for text, and 3:1 commonly recommended for non-text (control states). Check both light and dark modes. With Apple frameworks, verify Increase Contrast. With custom frameworks, offer compliant color schemes. Test with Increase Contrast and Reduce Transparency.
- **Reduced Motion** (reduced-motion-evaluation-criteria) Honour Reduce Motion: disable or replace parallax, animated blur, depth-of-field, multi-axis motion, spinning and vortex effects. Stop auto-advancing carousels or provide a stop control. Replace meaningful motion with a "dissolve, highlight fade, or color shift".
- **Captions** (captions-evaluation-criteria) Caption video and dialogue in the app, including game interstitials. Enable captions by default when the system setting is on. Untimed transcripts of audio-only content count. Captioned media must be identifiable. Don't claim support if little content is captioned.
- **Audio Descriptions** (audio-descriptions-evaluation-criteria) Narrate relevant visual-only content. Enable by default when the system setting is on. Mark described media (for example with an "AD" icon). Don't claim support if little content is described.

---

## 5. Google Play

**Pre-launch report: accessibility section** (https://support.google.com/googleplay/android-developer/answer/9844487?hl=en)
- Categories:
  - **Content labeling** ("labelled incorrectly for screen readers")
  - **Touch target size** ("don't meet the recommended touch target size")
  - **Implementation** ("Layout issues")
  - **Low contrast**
- These are reported as minor issues ("missing content labels, color contrast issues, small touch target sizes, implementation issues"). Screen clusters are coloured red, yellow, blue or green by severity.
- The page points developers to Accessibility Scanner. It doesn't name ATF or give thresholds.
- Setup page: https://support.google.com/googleplay/android-developer/answer/7002270 says only that the report "includes tests for" accessibility issues.
- That the pre-launch report runs exactly the ATF check set below is **(unverified)**. Play's help doesn't say so.

**Accessibility Test Framework for Android (ATF)** (https://github.com/google/Accessibility-Test-Framework-for-Android)
- Check classes in the `framework/checks` directory listing:
  - ClassNameCheck
  - ClickableSpanCheck
  - DuplicateClickableBoundsCheck
  - DuplicateSpeakableTextCheck
  - EditableContentDescCheck
  - ImageContrastCheck
  - LinkPurposeUnclearCheck
  - RedundantDescriptionCheck
  - SpeakableTextPresentCheck
  - TextContrastCheck
  - TextSizeCheck
  - TouchTargetSizeCheck
  - TraversalOrderCheck
  - UnexposedTextCheck
- The listing may be partial. The README's preset is `AccessibilityCheckPreset.LATEST`.
- **TouchTargetSizeCheck.java** `TOUCH_TARGET_MIN_HEIGHT/WIDTH = 48` dp. 32 dp when the view touches the screen edge, or for IME windows. Clipped by an ancestor, or with a clickable ancestor: WARNING.
- **ContrastUtils.java** Normal text **4.5**, large text **3.0**. Large means **18** (sp-equivalent) or **14** bold.
- **ImageContrastCheck.java**: uses the large-text ratio (**3.0**), with 0.01 tolerance.
- No release version is shown on the README page **(unverified)**.

**Play declaration comparable to Apple's labels**
- I found none.
- Play does have a policy declaration for apps using the AccessibilityService API / `isAccessibilityTool`. https://support.google.com/googleplay/android-developer/answer/10964491 (search snippet only)
- A Google blog mentions accessibility tags on the store. How developers set them is **(unverified)**. https://blog.google/products-and-platforms/platforms/google-play/google-play-accessibility-features/

---

## 6. Platform design guidance

**Apple HIG: Accessibility** (https://developer.apple.com/design/human-interface-guidelines/accessibility, read via its JSON at https://developer.apple.com/tutorials/data/design/human-interface-guidelines/accessibility.json)
- Change log:
  - 9 Jun 2025: added Assistive Access, Switch Control and Nutrition Labels.
  - 7 Mar 2025: Dynamic Type guidance moved to the Typography page, and VoiceOver guidance moved to a new VoiceOver page.
- **Text enlargement**: "Ideally" at least **200%**, or **140% on watchOS**, via Dynamic Type or custom UI.
- **Type sizes**:

  | Platform | Default | Minimum |
  |---|---|---|
  | iOS / iPadOS | 17 pt | 11 pt |
  | macOS | 13 pt | 10 pt |
  | tvOS | 29 pt | 23 pt |
  | visionOS | 17 pt | 12 pt |
  | watchOS | 16 pt | 12 pt |

- **Contrast** (WCAG AA as guidance):
  - up to 17 pt: **4.5:1**
  - 18 pt and up: **3:1**
  - bold at any size: **3:1**
  - If defaults fall short, Increase Contrast must provide it. Check light and dark. Prefer system colors. APCA is mentioned.
- **Control sizes**:

  | Platform | Default | Minimum |
  |---|---|---|
  | iOS / iPadOS | **44×44 pt** | 28×28 pt |
  | macOS | 28×28 pt | 20×20 pt |
  | tvOS | 66×66 pt | 56×56 pt |
  | visionOS | 60×60 pt | 28×28 pt |
  | watchOS | 44×44 pt | 28×28 pt |

- **Spacing**: about 12 pt of padding around bezeled elements, and about 24 pt around non-bezeled ones.
- **Also**:
  - convey information with more than color alone;
  - Reduce Motion (reduce zoom, scaling and peripheral motion; use fades instead of x/y/z transitions);
  - Dim Flashing Lights;
  - captions, audio descriptions and transcripts;
  - haptics alongside audio cues;
  - label elements for Voice Control;
  - Full Keyboard Access and Switch Control;
  - Assistive Access.

**Material 3** (rendered in a browser)
- https://m3.material.io/foundations/designing/structure Touch targets "at least 48 x 48dp" (about 9 mm). For example, a 24 dp icon sits in a 48 dp target. Pointer targets at least **44×44 dp**. Targets separated by **8 dp** or more. The page notes that iOS recommends 44×44.
- https://m3.material.io/foundations/designing/color-contrast Small text **4.5:1**. Large text (14 pt bold / 18 pt regular and up) and graphics **3:1**. Disabled states are exempt. Clustered button containers need 3:1 against the background. A standalone FAB doesn't.

**Android developer docs (Compose)**
- https://developer.android.com/guide/topics/ui/accessibility/apps Touch target at least 48dp × 48dp. Contrast 4.5:1 below 18sp (or bold below 14sp), and 3:1 otherwise. `contentDescription` describes purpose, not visuals. Use `null` for decorative elements, none on `Text`, and keep descriptions unique in lists.
- https://developer.android.com/develop/ui/compose/accessibility/api-defaults Material components (Checkbox, RadioButton, Switch, Slider, Surface) enforce 48dp only when interactive. Compose expands undersized clickable touch targets. `clickable` / `toggleable` merge child semantics. `onClickLabel` customises the TalkBack action.

---

# Part B: assistive technologies, text scaling, settings, focus

## 7. Custom controls and assistive technologies

### What every AT needs from a control (the 4.1.2 Name, Role, Value contract)
- **Name:** "name and role can be programmatically determined" [W-spec]. VoiceOver/TalkBack speak it. Voice Control and Voice Access match spoken commands against it.
- **Role/trait:** tells the user it's a button, toggle, etc. Don't repeat the role in the label. Apple: don't use "Play button", because "a button already has a trait" [A-label]. Android: use "Submit," not "Submit button" [D-apps].
- **Value/state:** use it only when it differs from the label. Example: label "Volume", value "60%" [A-value]. Compose equivalent: `stateDescription` [D-sem].
- **Actions:** every gesture-only interaction must also exist as an accessibility action. TalkBack, Switch Access and Voice Access users "perform actions that might otherwise be available only through gestures" through custom actions [D-princ].
- **Focusability:** Full Keyboard Access, Switch Control and Voice Control need to know an element is interactive. `accessibilityRespondsToUserInteraction(_:)` covers "Switch Control, Voice Control or Full Keyboard Access" [A-responds].

### SwiftUI APIs (exact names)
- `.accessibilityLabel(_:)` (iOS 16 / macOS 13 overload). Use it for views without text, like icons [A-label].
- `.accessibilityAddTraits(.isButton)`. `AccessibilityTraits.isButton` means "The accessibility element is a button" [A-traits] [A-isbutton].
- `.accessibilityValue(_:)` [A-value].
- `.accessibilityElement(children:)`. The default is `.ignore` [A-elem].
  - `.combine` merges properties from all non-hidden children, and "not all of AccessibilityTraits are merged" [A-combine].
  - `.ignore` hides the children, so you must add a label yourself [A-ignore].
  - `.contain` makes a container: "all children ... are navigated in order before" the next container [A-contain].
- `.accessibilityRepresentation(representation:)` (iOS 15 / macOS 12). It replaces a custom view's AX elements with a standard control's, e.g. a `Slider` [A-repr]. A custom `ToggleStyle`/`ButtonStyle` inherits the accessibility of `Toggle`/`Button` automatically [A-repr].
- `.accessibilityAdjustableAction(_:)` adds increment/decrement for VoiceOver [A-adjust].
- `.accessibilityAction(named:_:)` (iOS 16 / macOS 13) and `.accessibilityActions(_:)` for dynamic lists [A-action] [A-actions]. Use these for swipe-to-delete and other gesture-only actions.
- `.accessibilityInputLabels(_:)` (iOS 14 / macOS 11): "Voice Control and Full Keyboard Access use the input labels". Give them in descending importance. When none are set, the user can still say the `accessibilityLabel` [A-input].
- `.accessibilitySortPriority(_:)`: "Higher numbers are sorted first. The default sort priority is zero." The priority is relative to elements at the same level [A-sort].
- `.accessibilityHidden(_:)` [A-hidden]. `Image(decorative:bundle:)`: "SwiftUI ignores this image for accessibility" [A-decorative]. The HIG says to exclude decorative images [H-vo].
- `.accessibilityHeading(_:)`: VoiceOver speaks the level for h1 through h6 [A-heading]. Support the rotor (`AccessibilityRotorEntry`) where possible [H-vo].
- `.focusable(_:)` (iOS 17 / macOS 12) and `.focusable(_:interactions:)` (iOS 17 / macOS 14) [A-focusable] [A-focusable2].
  - On iOS and macOS, button-like views conventionally take focus only when keyboard navigation is enabled system-wide. Reproduce that with `.activate` interactions [A-focusable2].
  - Since the macOS 14 SDK, custom views "will always be focusable" unless you restrict their interactions [A-focusable2].
- `.accessibilityShowsLargeContentViewer()` is for items that must stay small, such as tab bars. It is "not a replacement for proper Dynamic Type support" [A-lcv].
- Environment flags: `accessibilityVoiceOverEnabled` and `accessibilitySwitchControlEnabled` [A-voenv] [A-swenv].

### Why `.onTapGesture` on a plain view is a problem (Apple)
- Apple's `onTapGesture` doc: "If you create a control that's functionally equivalent to a Button, use ButtonStyle" instead [A-tap].
- Correction to the brief: on Apple the view is **not strictly invisible**. `accessibilityRespondsToUserInteraction` "is inferred from ... the presence of gestures" [A-responds]. What the view does lack is the `.isButton` trait, so it is not announced as a button.
- Whether VoiceOver double-tap fires an `onTapGesture` on a `Text`/shape: **(unverified)**.
- Whether Voice Control's "show names" lists such a view: **(unverified)**.
- Fix: use `Button` + a custom `ButtonStyle`. Otherwise add `.accessibilityAddTraits(.isButton)` plus a label, and `.accessibilityAction` for any non-tap gestures.

### Compose APIs (exact names)
- `Modifier.semantics { }` and `Modifier.semantics(mergeDescendants = true) {}` [D-sem] [D-merge].
- `contentDescription`: use "a localized string". Set it to `null` for decorative graphics [D-defaults].
- `stateDescription` [D-sem]. `role = Role.Button` / `Role.Switch` [D-apps] [D-merge].
- `heading()` [D-sem]. `paneTitle`, and `liveRegion` (which tells AT to "automatically notify the user about changes") [D-semref] [D-princ].
- `customActions = listOf(CustomAccessibilityAction(label, action))`. The page's swipe-to-dismiss example labels it "Remove article from list" [D-princ].
- `traversalIndex` (Float, default `0f`) and `isTraversalGroup` [D-trav]. `isContainer` is deprecated: "Use `isTraversalGroup` instead" [D-semref].
- `hideFromAccessibility()` (added in ui 1.8.0) [D-semref].
  - `invisibleToUser()` is "deprecated. Use `hideFromAccessibility()` instead" (deprecated in 1.8.0) [D-semref].
  - `hideFromAccessibility` keeps semantics for testing; `clearAndSetSemantics {}` removes them for all consumers [D-merge].
- `clearAndSetSemantics { }`: "the new semantics replace all previous semantics of the element and its descendants" [D-merge].
  - The page warns that AI agents may use semantics, so clear them "only ... when necessary" [D-merge].
- `Modifier.clickable(enabled, onClickLabel, role, interactionSource, onClick)` [D-clickable].
  - `onClickLabel` changes TalkBack's hint to "Double tap to open this article" [D-defaults].
  - `combinedClickable(onClickLabel, onLongClick, onLongClickLabel)` labels both gestures [D-defaults].
  - Nested clickables can set the label with `semantics { onClick(label = …, action = …) }` [D-defaults].
- `Modifier.toggleable(value, enabled, role, interactionSource, onValueChange)` [D-toggle].
  - `clickable` and `toggleable` "merge their children's semantics by default" [D-defaults].
  - For a Checkbox/Switch row: set the control's callback to `null` and put `toggleable`/`selectable` on the parent row [D-defaults].
- `Modifier.focusable(enabled, interactionSource)`: "focusable via focus system or accessibility 'focus' event" [D-focusable].
- `Modifier.focusProperties { next; previous; up; down; start; end; left; right }` with `FocusRequester`. Use `FocusRequester.Cancel` to block a direction and `FocusRequester.Default` to keep the default [D-focus].

### Why `pointerInput { detectTapGestures }` is invisible (Compose)
- `clickable` "Allows accessibility services to interact with the element by setting the semantics information." It also supports focus and Enter/D-pad activation [D-tap].
- The `pointerInput` + `detectTapGestures` scrim sample has to add `semantics { contentDescription; onClick {…} }` and `onKeyEvent` by hand [D-tap].
- So raw pointer input carries no semantics, keyboard or focus support. The page implies this rather than stating it outright.
- For custom low-level composables, "you have to manually provide its semantics" [D-sem].

### Speech input: Voice Control / Voice Access and Label in Name (WCAG 2.5.3)
- 2.5.3: "the name contains the text that is presented visually" [W-spec].
- Best practice: put the label text "at the start of the name" [W-label]. Case and punctuation are ignored, and a trailing ellipsis may be dropped [W-label].
- A mismatched name can act as a hidden command that gets activated by accident [W-label].
- Apple: `accessibilityInputLabels` adds spoken synonyms. Keep the visible text among them (inference from [A-input] + [W-label]).
- HIG on Voice Control: "label interface elements appropriately" [H-a11y].
- Android Voice Access: the principles page lists it only as a user of custom actions. I found **no Android page on label/visible-text matching (unverified)**, so rely on WCAG 2.5.3.

### Switch Control / Switch Access / keyboards
- Switch Access "highlights interactive elements" and works with "one or two buttons". Nested gesture actions must be exposed as custom actions [D-princ].
- iOS Full Keyboard Access (Settings > Accessibility > Keyboards): Tab to move, Space to activate [K-ios].
- HIG: don't override system shortcuts, and test with Full Keyboard Access [H-a11y].
- Compose keyboard: Tab follows "one-dimensional appearance order" and wraps around. Arrow/D-pad keys move two-dimensionally and do "not wrap around" [D-focus].

### Compose Multiplatform specifics
- **iOS:** Compose semantics map to native iOS accessibility objects, and VoiceOver gestures work as they do natively [K-ios].
  - `testTag` maps to `accessibilityIdentifier` [K-ios].
  - `ComposeUIViewController(configure = { accessibilitySyncOptions = AccessibilitySyncOptions.Always(debugLogger) })` controls tree sync. The options are `Never` / `WhenRequiredByAccessibilityServices` (the default) / `Always`, and `Always` can "degrade the performance" [K-ios].
- **Desktop:** macOS is "Fully supported". Windows works "via Java Access Bridge", which is disabled by default (`jabswitch.exe /enable`, `modules("jdk.accessibility")`). Linux is "Not supported" [K-desk].
- **Traversal:** the CMP overview shows a FAB in a `Box` given `isTraversalGroup = true; traversalIndex = -1f` so it is read first [K-ov].
- **Dynamic Type on CMP iOS:** whether it maps into `LocalDensity.fontScale` is **(unverified)**; neither CMP page covers it.

---

## 8. Text scaling

### iOS Dynamic Type (HIG Typography) [H-typo]
- Sizes: xSmall, Small, Medium, **Large (default)**, xLarge, xxLarge, xxxLarge. The accessibility sizes are AX1–AX5 (turn on Larger Accessibility Text Sizes in Settings > Accessibility > Display & Text Size > Larger Text).
- iOS/iPadOS point sizes (size/leading, pt). The HIG calls the style "Subhead" on iOS and "Subheadline" in the macOS table.

| Style | Weight | Large (default) | AX5 |
|---|---|---|---|
| Large Title | Regular | 34 / 41 | 60 / 70 |
| Title 1 | Regular | 28 / 34 | 58 / 68 |
| Title 2 | Regular | 22 / 28 | 56 / 66 |
| Title 3 | Regular | 20 / 25 | 55 / 65 |
| Headline | Semibold | 17 / 22 | 53 / 62 |
| Body | Regular | 17 / 22 | 53 / 62 |
| Callout | Regular | 16 / 21 | 51 / 60 |
| Subhead(line) | Regular | 15 / 20 | 49 / 58 |
| Footnote | Regular | 13 / 18 | 44 / 52 |
| Caption 1 | Regular | 12 / 16 | 43 / 51 |
| Caption 2 | Regular | 11 / 13 | 40 / 48 |

- Body grows ~3.1× from Large to AX5, while Large Title grows only ~1.8×, so the hierarchy compresses at AX sizes (computed from the table above).
- HIG guidance [H-typo]:
  - "Make sure your app's layout adapts to all font sizes."
  - Keep truncation minimal, and aim to show as much text at the largest AX size as at the largest standard size.
  - Consider "a stacked layout where text appears above secondary items" and fewer columns at large sizes.
  - Scale meaningful icons; SF Symbols scale automatically.
  - Keep primary elements toward the top.
- HIG Accessibility: enlarge text "by at least 200 percent". Default/minimum sizes are iOS 17/11 pt and macOS 13/10 pt [H-a11y].
- Custom fonts must implement Dynamic Type and Bold Text themselves [H-typo].

### SwiftUI APIs
- `@ScaledMetric` is "A dynamic property that scales a numeric value" (iOS 14) [A-scaled]. Use it for padding, icon sizes and fixed frames.
- `Font.custom(_:size:relativeTo:)` creates a custom font that "scales relative to the given textStyle" [A-fontcustom].
- `.dynamicTypeSize(_:)` accepts a value or a range. A range applied after a value limits that value. When you limit sizes, consider the large content viewer [A-dts-mod].
- `DynamicTypeSize` is ordered, so sizes can be compared. "The five sizes whose names begin with `accessibility` are much larger". Check `isAccessibilitySize` to change layout [A-dts-enum] [A-isax].
  - Pattern: `@Environment(\.dynamicTypeSize)` → `isAccessibilitySize ? AnyLayout(VStackLayout()) : AnyLayout(HStackLayout())`. The `AnyLayout` API names are **(unverified)**; I didn't fetch them.
- `ViewThatFits` "selects the first child whose ideal size on the constrained axes fits". Order the children by preference, usually largest first [A-vtf].

### macOS
- HIG: "macOS doesn't support Dynamic Type" [H-typo]. Fixed text styles: Body 13/16, Headline Bold 13/16, Large Title 26/32, Caption 1 10/13 [H-typo].
- `EnvironmentValues.dynamicTypeSize`: "On macOS, this value cannot be changed by users and does not affect the text size" [A-dts-env].
  - This confirms what you saw on macOS 26: setting the value doesn't change how `Font.body` renders.
- What macOS offers instead (System Settings > Accessibility > Display > Text > **Text size**), present on the macOS 14 Sonoma page [M-14]:
  - The slider affects "the desktop, in sidebars, and in the listed apps".
  - It applies to apps "if they are set to Use Preferred Reading Size".
  - Each listed app has its own pop-up menu.
  - The current page adds that an app may show "Customised in App" [M-cur].
- Whether third-party SwiftUI apps can join the Text size list or read that value through a public API: **(unverified)**. Treat it as Apple-apps-only.
- Other Mac options: Display zoom/resolution, Sidebar icon size (Appearance), and app ⌘+/⌘− [M-cur].

### Measured here: `.dynamicTypeSize` on macOS (2026-10-23, macOS 26.3, Xcode 26.2 SDK)

`scripts/render_swiftui.py` rendered one view twice: as is, and with `.dynamicTypeSize(.accessibility5)`
on it. The view held `.body`, `.largeTitle`, `.custom("Georgia", size: 17, relativeTo: .body)` and
`.system(size: 17)` text. The two PNGs were identical. This matches Apple's note on the environment
value quoted above [A-dts-env]. So on a Mac, Dynamic Type can't be rendered, and an in-app zoom has to
scale sizes itself (a zoom factor multiplied into the font sizes), not set `dynamicTypeSize`.
`references/platform-macos.md` §6 said the opposite before this branch. It is corrected.

### Android / Compose
- Android 14 supports font scaling "up to 200%" with "a nonlinear scaling curve" so that large text "doesn't scale at the same rate as smaller text" [D-14].
- Rules from that page [D-14]:
  - Use sp for text.
  - "Don't use sp units for padding or define view heights assuming implicit padding", because "4sp + 20sp might not equal 24sp".
  - Define line height in sp.
  - `Configuration.fontScale` is "for informational purposes only"; `scaledDensity` "is no longer accurate".
  - Convert with `TypedValue.applyDimension()` / `TypedValue.deriveDimension()`.
- The official 2.0× lookup table (AOSP `FontScaleConverterFactory`, android14-release) maps sp → dp:
  - Table points: `8→16, 10→20, 12→24, 14→26, 18→30, 20→34, 24→36, 30→38, 100→100` [AOSP].
  - Effective scale: 14sp ≈1.86×, 24sp 1.5×, 30sp ≈1.27×.
  - Other tables exist at 1.15, 1.3, 1.5 and 1.8. Non-linear curves start just below the first table key: 1.15 − 0.02 = 1.13 (`sMinScaleBeforeCurvesApplied`) [AOSP].
  - Interpolation between table points, and whether Compose's own `fontscaling` package uses identical tables: **(unverified)**.
- `LocalDensity.current.fontScale` is available through `Density(density, fontScale)` [D-scal]. Read it only to inform layout decisions, not for manual math [D-14].
- Avoid fixed heights on text containers: use `heightIn(min=…)` / `defaultMinSize` rather than `height()`. This is inferred from [D-14]'s padding/height rule; the modifier names are **(unverified)** against a fetched page.
- Previews:
  - `@PreviewFontScale` (ui-tooling-preview 1.6.0) renders 85%, 100%, 115%, 130%, 150%, 180% and 200% [D-pfs].
  - `@Preview(fontScale = 2f)`: `FloatRange(from = 0.01)`, default `1.0f` [D-prev].
- In-app pinch-zoom (optional): use `Modifier.transformable` plus a custom `LocalDensity`. The density strategy scales everything; the fontScale strategy scales text only [D-scal].

---

## 9. System accessibility settings → APIs

| Setting | SwiftUI | UIKit / AppKit | Android / Compose |
|---|---|---|---|
| Reduce Motion | `@Environment(\.accessibilityReduceMotion)`: "avoid large animations, especially those that simulate the third dimension" [A-rm] | `UIAccessibility.isReduceMotionEnabled` [A-uirm]; `NSWorkspace.accessibilityDisplayShouldReduceMotion` [A-nsrm] | `Settings.Global.ANIMATOR_DURATION_SCALE`: `0.0f` makes animations "end immediately", default `1.0f` [D-glob]. "Remove animations" user setting [G-a11y]. Compose `MotionDurationScale.scaleFactor` 0 → ends next frame [D-mds]. Whether Remove animations sets the scale to 0 and Compose reads it automatically: **(unverified)** |
| Reduce Transparency | `accessibilityReduceTransparency`: backgrounds "should be opaque" [A-rt] | `UIAccessibility.isReduceTransparencyEnabled` [A-uirt] | No equivalent found **(unverified)** |
| Increase Contrast | `colorSchemeContrast` → `ColorSchemeContrast.standard` / `.increased`; "you can't change it"; prefer Asset Catalog variants [A-csc] [A-csc-enum] | `UIAccessibility.isDarkerSystemColorsEnabled` ("Increase Contrast") [A-darker]; `NSWorkspace.accessibilityDisplayShouldIncreaseContrast` [A-nsic]. **No `accessibilityHighContrast` API found**; the names above are the real ones | `UiModeManager.getContrast()` (API 34), float in [-1, 1], 0 = default, 1 = max; `addContrastChangeListener(Executor, …)` [D-uim]. "query this only if your application is doing its own rendering". MDC `ColorContrast`: applied automatically with dynamic color on U+; branded themes supply medium/high overlays [D-cc]. Compose M3 has no auto contrast schemes **(unverified)**. CMP iOS: read `UIAccessibilityDarkerSystemColorsEnabled` [K-ios] |
| High contrast text (Android) | – | – | User setting exists [G-a11y]. No public `AccessibilityManager` API found **(unverified)** |
| Differentiate Without Colour | `accessibilityDifferentiateWithoutColor`: "use shapes or glyphs" [A-dwc] | `UIAccessibility.shouldDifferentiateWithoutColor` [A-uidwc] | No setting. "use cues other than color" [D-princ] |
| Bold Text | `legibilityWeight` (`LegibilityWeight` `.regular`/`.bold`) reflects Bold Text [A-lw] [A-lw-enum] | `UIAccessibility.isBoldTextEnabled` [A-uibold] | `Configuration.fontWeightAdjustment` (API 31) [D-config] |
| Smart Invert | `.accessibilityIgnoresInvertColors(_:)`; env `accessibilityInvertColors` [A-inv] [A-invenv] | – | – |
| Button Shapes | `accessibilityShowButtonShapes`: edges and borders "clearly visible" [A-bs] | `UIAccessibility.buttonShapesEnabled` (iOS 14) [A-uibs] | – |
| On/Off Labels | No SwiftUI env value found **(unverified)** | `UIAccessibility.isOnOffSwitchLabelsEnabled` (iOS 13) [A-onoff] | – |
| Timeouts | – | – | `AccessibilityManager.getRecommendedTimeoutMillis(originalTimeout, uiContentFlags)` (API 29) [D-am] |

- HIG Reduce Motion practices: tighten springs, track gestures directly, avoid z-axis depth animation, replace x/y/z transitions "with fades", and avoid animating blurs [H-a11y].
- HIG contrast: 4.5:1 for text up to 17 pt, 3:1 for 18 pt+ or bold. If the default falls short, offer a higher-contrast scheme under Increase Contrast [H-a11y]. Android: 4.5:1 under 18sp (or bold under 14sp), otherwise 3:1 [D-apps].

---

## 10. Focus order, reading order, target size

### WCAG criteria [W-spec]
- **1.3.2 Meaningful Sequence (A):** "a correct reading sequence can be programmatically determined". https://www.w3.org/WAI/WCAG22/Understanding/meaningful-sequence.html
- **2.4.3 Focus Order (A):** focus order "preserves meaning and operability". https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html
- **2.4.7 Focus Visible (AA):** "the keyboard focus indicator is visible". https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html
- **2.4.11 Focus Not Obscured (Minimum) (AA):** focused component "not entirely hidden due to author-created content". https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
  - Sticky headers/footers and non-modal overlays are the typical failures. Partial cover passes AA; 2.4.12 (AAA) is the "preferred outcome" [W-fno].
  - Native analogue: a floating bottom bar or FAB must not completely cover a keyboard-focused row. Inset scroll content by the bar's height (e.g. SwiftUI `.safeAreaInset`, Compose `contentPadding`), which is **(unverified)** as a documented fix.
- **2.5.8 Target Size (Minimum) (AA):** 24×24 CSS px. Exceptions: Spacing (a 24 px circle centred on the target doesn't intersect other targets or circles), Equivalent, Inline, User-agent control, Essential. https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html [W-ts]
- **WCAG2ICT:** non-web software should "use platform-defined density-independent pixel measurements", i.e. **pt for iOS and macOS, dp for Android** [W-ict]. So 24×24 means 24 pt / 24 dp.

### SwiftUI reading order
- VoiceOver reads "in the same order people read content" in the active locale: top-to-bottom, left-to-right in US English [H-vo].
- Override it with `.accessibilitySortPriority` (higher first, default 0) among siblings at the same level [A-sort]. Wrap a region in `.accessibilityElement(children: .contain)` so its children are read together before moving on [A-contain].
- Whether order follows declaration order or geometry for `HStack`/`VStack`/`ZStack`/`.overlay`: **(unverified)**.
  - Practical rule: a `ZStack { content; FloatingButton().frame(maxHeight: .infinity, alignment: .bottom) }` may read the button last, or first, depending on implementation. Test with VoiceOver, then pin it with `.accessibilitySortPriority` on a `.contain` group **(unverified behaviour)**.

### Compose reading/traversal order [D-trav]
- Default: "expected reading order, which is usually left-to-right, then top-to-bottom", i.e. by layout position.
- `isTraversalGroup = true` on a container: "all children of that node are visited before moving to other elements".
  - It is on by default for scroll containers (`LazyColumn`) and Material surfaces.
- `traversalIndex`: "lower ... prioritized first", can be negative, default `0f`. Indices are relative to siblings in the same group.
  - It must sit on a focusable child; on a `Column` it does nothing unless that column is also a traversal group.
- Keep compared elements "at the same `zIndex`" and avoid unnecessary merging.
- **Box + bottom-aligned FAB:** by position the FAB is read after the content above it. Under that position-based reading the FAB comes last, an inference from the default rule, **(unverified)** for overlapping cases.
  - To read it first (CMP's example), give the FAB `Modifier.semantics { isTraversalGroup = true; traversalIndex = -1f }` [K-ov].
- **Keyboard (Tab/arrows):** follows "appearance order" independently of TalkBack traversal. Override it with `focusProperties { next/previous/... }` [D-focus].

### Platform target sizes
- Apple HIG, default / minimum [H-a11y]:
  - iOS/iPadOS **44×44 / 28×28 pt**; macOS **28×28 / 20×20 pt**; watchOS 44/28; visionOS 60/28; tvOS 66/56.
  - Padding: "about 12 points" around bezelled elements and "about 24 points" around unbezelled ones.
- Android: "at least 48dpx48dp" for touch, and the target "can be smaller" for mouse/trackpad [D-apps].
  - `Button`, `IconButton`, `ListItem`, Checkbox, Switch, Slider and `Surface` enforce it when interactive [D-apps] [D-defaults].
  - Compose expands a small clickable's touch target beyond its bounds [D-defaults].
- `Modifier.minimumInteractiveComponentSize()` (material3 1.1.0) [D-mics]:
  - It "Reserves at least 48.dp". It is layout-only, because touch expansion happens anyway.
  - It "must come before any size modifiers".
- `LocalMinimumInteractiveComponentSize` (Dp). Set it to `0.dp` to turn enforcement off; `LocalMinimumInteractiveComponentEnforcement` is deprecated [D-m3].
- Custom elements: `sizeIn(minWidth = 48.dp, minHeight = 48.dp)` [D-apps] [D-defaults].

---

## 11. WCAG 2.2 criteria for native mobile/desktop [W-spec]
URL pattern: `https://www.w3.org/WAI/WCAG22/Understanding/<slug>.html`. The slugs are taken from the spec's own "Understanding" links.

| SC | Lvl | Slug | One-line requirement (paraphrased from spec) |
|---|---|---|---|
| 1.1.1 Non-text Content | A | non-text-content | Non-text content has a text alternative; controls have a name describing purpose |
| 1.3.1 Info and Relationships | A | info-and-relationships | Structure and relationships conveyed visually are programmatically determinable (headings, groups) |
| 1.3.2 Meaningful Sequence | A | meaningful-sequence | Correct reading order programmatically determinable when order affects meaning |
| 1.3.3 Sensory Characteristics | A | sensory-characteristics | Instructions don't rely solely on shape, colour, size, location, orientation or sound |
| 1.3.4 Orientation | AA | orientation | Don't lock to portrait/landscape unless essential |
| 1.3.5 Identify Input Purpose | AA | identify-input-purpose | Purpose of user-data fields programmatically determinable (content types / autofill hints) |
| 1.4.1 Use of Color | A | use-of-color | Colour is not the only visual means of conveying information or state |
| 1.4.3 Contrast (Minimum) | AA | contrast-minimum | Text 4.5:1; large text 3:1 |
| 1.4.4 Resize Text | AA | resize-text | Text resizable to 200% without loss of content/function |
| 1.4.5 Images of Text | AA | images-of-text | Use real text, not images of text, unless customizable/essential |
| 1.4.10 Reflow | AA | reflow | No two-dimensional scrolling at 320 CSS px width (≈320 pt/dp per WCAG2ICT) [W-ict] |
| 1.4.11 Non-text Contrast | AA | non-text-contrast | UI component boundaries/states and meaningful graphics 3:1 against adjacent colours |
| 1.4.12 Text Spacing | AA | text-spacing | Survive increased line/paragraph/letter/word spacing; for non-web software, applies only to markup-based content [W-ict] |
| 1.4.13 Content on Hover or Focus | AA | content-on-hover-or-focus | Tooltips/popovers dismissible, hoverable, persistent |
| 2.1.1 Keyboard | A | keyboard | All functionality operable via a keyboard interface (FKA, Switch, hardware keyboard) |
| 2.1.2 No Keyboard Trap | A | no-keyboard-trap | Focus can always be moved away using the keyboard |
| 2.1.4 Character Key Shortcuts | A | character-key-shortcuts | Single-character shortcuts can be turned off, remapped, or are active only on focus |
| 2.2.1 Timing Adjustable | A | timing-adjustable | Time limits can be turned off, adjusted (≥10×) or extended |
| 2.2.2 Pause, Stop, Hide | A | pause-stop-hide | Auto-moving content lasting >5 s, or auto-updating content, can be paused/stopped/hidden |
| 2.3.1 Three Flashes or Below Threshold | A | three-flashes-or-below-threshold | Nothing flashes more than 3 times per second |
| 2.4.3 Focus Order | A | focus-order | Focus order preserves meaning and operability |
| 2.4.4 Link Purpose (In Context) | A | link-purpose-in-context | Link purpose clear from its text plus context |
| 2.4.6 Headings and Labels | AA | headings-and-labels | Headings and labels describe topic or purpose |
| 2.4.7 Focus Visible | AA | focus-visible | Keyboard focus indicator is visible |
| 2.4.11 Focus Not Obscured (Minimum) | AA | focus-not-obscured-minimum | Focused component not entirely hidden by author content |
| 2.5.1 Pointer Gestures | A | pointer-gestures | Multipoint/path gestures have a single-pointer, non-path alternative |
| 2.5.2 Pointer Cancellation | A | pointer-cancellation | Don't fire on down-event; allow abort/undo or up-reversal |
| 2.5.3 Label in Name | A | label-in-name | Accessible name contains the visible label text |
| 2.5.4 Motion Actuation | A | motion-actuation | Shake/tilt functions also have UI controls and can be disabled |
| 2.5.7 Dragging Movements | AA | dragging-movements | Dragging has a single-pointer, non-drag alternative |
| 2.5.8 Target Size (Minimum) | AA | target-size-minimum | Targets ≥24×24 CSS px (pt/dp), or spacing/equivalent/inline exceptions |
| 3.1.1 Language of Page | A | language-of-page | Default language programmatically determinable |
| 3.1.2 Language of Parts | AA | language-of-parts | Language of passages programmatically determinable |
| 3.2.1 On Focus | A | on-focus | Receiving focus doesn't trigger a change of context |
| 3.2.2 On Input | A | on-input | Changing a setting doesn't auto-change context unless the user was advised |
| 3.2.6 Consistent Help | A | consistent-help | Help mechanisms appear in the same relative order across screens |
| 3.3.1 Error Identification | A | error-identification | Detected errors are identified and described in text |
| 3.3.2 Labels or Instructions | A | labels-or-instructions | Inputs have labels or instructions |
| 3.3.3 Error Suggestion | AA | error-suggestion | Suggest corrections when they are known |
| 3.3.4 Error Prevention (Legal, Financial, Data) | AA | error-prevention-legal-financial-data | Reversible, checked, or confirmed submissions |
| 3.3.7 Redundant Entry | A | redundant-entry | Don't make users re-enter information in the same process; auto-fill or offer it |
| 3.3.8 Accessible Authentication (Minimum) | AA | accessible-authentication-minimum | No cognitive-test login without an alternative or assistance (allow paste/password managers) |
| 4.1.2 Name, Role, Value | A | name-role-value | Name and role determinable; states/values settable; changes notified to AT |
| 4.1.3 Status Messages | AA | status-messages | Status messages announced without moving focus. Non-web software still needs this, "through ... accessibility services" [W-ict]. Use Compose `liveRegion` / SwiftUI `AccessibilityNotification` [D-semref] [H-vo] |

- The parenthetical mappings to native (FKA, autofill hints, pt/dp) are my annotations, not spec text.
- New in 2.2 (spec marks these "New"): 2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8 [W-spec].

---

## 12. Gap audit: what the skill enforced, criterion by criterion

The baseline is `dcf1211`, the start of this branch. Before then the skill covered accessibility in five places:
- Rule ids in `references/principles.md`: R-A11Y-1–7, plus R-COG-8, R-FORM-1/2/4/5, R-TOUCH-2/5, R-MOT-7, R-PLAT-1 and R-MAC-3/4.
- Seven lint rules: `unlabelled-icon-button`, `placeholder-only-field`, `small-target`, `fixed-font-size`, `tiny-text`, `no-reduce-motion` and `pinned-bottom-overlap`.
- The palette contrast that `deal.py` measures on every sheet.
- The critique's "Platform & access" criterion, through pass 8 (targets) and pass 11 ("at large text, does the layout reflow or does it clip?").
- The report's Warnings and Not verified lines.

There was no accessibility pass in the critique, no large-text render, and no conformance statement.

**Scope.** The table covers WCAG 2.2 Level A and AA as WCAG2ICT applies them to non-web software (§2): the "CSS pixel" is a pt or dp, and the "web page" is the screen or window.

**Status key.**
- **✓** a rule and a check that can fail.
- **◐** a rule but no check, or a check on part of the criterion.
- **✗** nothing.
- **n/a** WCAG2ICT or WCAG2Mobile says the criterion doesn't apply to a single native app (§2).

**What changes on this branch** (last column):
- **Lint** is a `scripts/lint.py` rule, run with `--a11y` in the audit mode.
- **A11y** is a check in `references/accessibility.md`, the new accessibility audit mode.
- **Pass 15** is the critique's new Access pass.
- **Large text** is the large-text render (`fold.py --text-scale`, `render_swiftui.py --dynamic-type`).
- **Line** is the report's Accessibility line.

| SC | Lvl | Applies to a native screen | At `dcf1211` | Was | This branch |
|---|---|---|---|---|---|
| 1.1.1 Non-text Content | A | Yes: images, icons, drawn gauges, mascots | `unlabelled-icon-button` (icon buttons only); "hide decorative mascots" in the platform files | ◐ | Lint `image-no-label` (named images, `AsyncImage`, `Canvas`, labelled at the call site counts), `unlabelled-icon-button` on tap-gesture icons; Pass 15 |
| 1.2.1–1.2.5 Media | A/AA | Only with video or audio | nothing | ✗ | A11y: captions and audio description controls (508 503.4) when media is present; otherwise Not Applicable on the Line |
| 1.3.1 Info and Relationships | A | Yes: headings, groups, field labels | R-FORM-1 and `placeholder-only-field` (labels) | ◐ | Lint `heading-missing`; A11y grouping (`.accessibilityElement(children:)`, `mergeDescendants`) |
| 1.3.2 Meaningful Sequence | A | Yes: reading order | nothing | ✗ | Lint `overlay-not-modal`; A11y reading-order check (ZStack/Box overlays, `accessibilitySortPriority`, `traversalIndex`); Pass 15 reads the order off the code |
| 1.3.3 Sensory Characteristics | A | Yes: copy | nothing | ✗ | A11y and Pass 15: no "tap the green button" or "swipe right" as the only instruction |
| 1.3.4 Orientation | AA | Yes | R-A11Y-6 (rule only) | ◐ | Lint `orientation-locked` |
| 1.3.5 Identify Input Purpose | AA | Yes: personal-data fields | R-FORM-2 (rule only) | ◐ | Lint `field-no-content-type` |
| 1.4.1 Use of Color | A | Yes | R-COG-8 and the core rule (rule only) | ◐ | Lint `colour-only-state` (status hues), Pass 15 grayscale squint; Apple's Differentiate Without Color Alone label |
| 1.4.2 Audio Control | A | Only with auto-playing audio | nothing | ✗ | A11y note; Not Applicable on the Line otherwise |
| 1.4.3 Contrast (Minimum) | AA | Yes | R-A11Y-1; `deal.py` measures the dealt palette; Warnings line | ◐ (palette, not the pairs on screen) | Pass 15 measures the on-screen pairs from the render, in light and dark; Line gives the worst ratio |
| 1.4.4 Resize Text | AA | Yes, "up to the text sizing capabilities of the platform" (WCAG2ICT) | `fixed-font-size`; R-A11Y-2; a preview hint in the platform files | ◐ (code only, never rendered) | Lint `fixed-text-frame`, `dynamic-type-capped`; Large text (iOS AX5 table, Android fontScale 2.0 table) with `fold.py` on it; Pass 15 |
| 1.4.5 Images of Text | AA | Yes | nothing | ✗ | A11y and Pass 15: no type baked into pictures or SVG rigs (a mascot's speech bubble stays real text) |
| 1.4.10 Reflow | AA | Yes, when text is scaled or the window resized (WCAG2ICT) | R-A11Y-2; macOS minimum-window renders | ◐ | Large text render (it must reflow, not clip or scroll sideways); Mac minimum-size render as before |
| 1.4.11 Non-text Contrast | AA | Yes: control boundaries, states, meaningful graphics | the signifier rule (≥3:1, rule only) | ◐ | Pass 15 measures the lip, stroke or fill of each control against its surface |
| 1.4.12 Text Spacing | AA | n/a: no platform mechanism to override spacing (WCAG2Mobile draft; WCAG2ICT limits it to markup content) | — | n/a | Line: Not Applicable, with that reason |
| 1.4.13 Content on Hover or Focus | AA | Mac popovers and custom tooltips | `.help` tooltips recommended (system, compliant) | ◐ | A11y: custom hover cards are dismissible (Esc), hoverable and persistent |
| 2.1.1 Keyboard | A | Yes: Full Keyboard Access, Switch Control, hardware keyboards, D-pad | R-MAC-4 (Mac only) | ◐ | Lint `tap-no-role` (gesture-only controls aren't focusable or activatable by keyboard); A11y FKA/Switch check |
| 2.1.2 No Keyboard Trap | A | Yes | nothing | ✗ | A11y: custom overlays close with Escape (`accessibilityAction(.escape)` / `onExitCommand` / `BackHandler`) |
| 2.1.4 Character Key Shortcuts | A | Mac and iPad keyboards | nothing | ✗ | Lint `character-key-shortcut` |
| 2.2.1 Timing Adjustable | A | Yes: auto-dismissing toasts with actions, timed sessions | nothing | ✗ | A11y: an Undo toast stays while VoiceOver is on (Compose `SnackbarHost` already does; a hand-made one must) |
| 2.2.2 Pause, Stop, Hide | A | Yes: ambient loops, tickers, carousels | `no-reduce-motion`; the motion budget stops loops under Reduce Motion | ◐ (relies on the system setting, not a control in the app) | A11y: a loop longer than 5 s that sits next to content has a pause, or stops after 5 s; the Line says which |
| 2.3.1 Three Flashes | A | Yes: retro CRT flicker, celebrations | the retro preset turns effects off under Reduce Motion | ◐ | A11y and the filmstrip: flicker under 3 Hz whatever the setting |
| 2.4.1 Bypass Blocks | A | n/a for one program (WCAG2ICT "sets of software") | — | n/a | Line: Not Applicable |
| 2.4.2 Page Titled | A | Yes, as "software titled": each screen or window has a title (WCAG2ICT; EN 301 549 V4.1.1 11.2.4.2) | nothing | ✗ | A11y and Pass 15: a navigation or window title exists even when hidden behind a custom header |
| 2.4.3 Focus Order | A | Yes | nothing | ✗ | Lint `overlay-not-modal`; A11y focus order; Pass 15 |
| 2.4.4 Link Purpose | A | In-text links | `generic-button-label` (buttons) | ◐ | A11y: link text names its destination |
| 2.4.5 Multiple Ways | AA | n/a (sets only) | — | n/a | Line: Not Applicable |
| 2.4.6 Headings and Labels | AA | Yes | `generic-button-label` | ◐ | Lint `heading-missing`, `label-in-name` |
| 2.4.7 Focus Visible | AA | Yes (keyboard focus on iOS, Mac, Android) | nothing | ✗ | Lint `focus-ring-removed` |
| 2.4.11 Focus Not Obscured (Min) | AA | Yes: pinned bars, FABs, sheets | `pinned-bottom-overlap`, `fold.py` end frame (the last row clears the bar) | ✓ | Mapped on the Line; Large text reruns `fold.py` at the large size, where bars grow |
| 2.5.1 Pointer Gestures | A | Yes | R-A11Y-5, R-TOUCH-5 (rules only) | ◐ | Lint `gesture-no-alternative` |
| 2.5.2 Pointer Cancellation | A | Yes: custom press handling | nothing | ✗ | A11y: actions fire on release (a `DragGesture(minimumDistance: 0)` press state or `onPress` must not trigger the action) |
| 2.5.3 Label in Name | A | Yes: Voice Control, Voice Access | nothing | ✗ | Lint `label-in-name`; A11y `accessibilityInputLabels` |
| 2.5.4 Motion Actuation | A | Shake or tilt features | nothing | ✗ | A11y note; Not Applicable otherwise |
| 2.5.7 Dragging Movements | AA | Yes | R-A11Y-5 (rule only) | ◐ | Lint `gesture-no-alternative` (drag, swipe, `anchoredDraggable`, `SwipeToDismissBox`) |
| 2.5.8 Target Size (Minimum) | AA | Yes, 24×24 pt/dp; the platforms ask 44 pt / 48 dp | `small-target`, R-TOUCH-2, R-MAC-5, critique pass 8 | ✓ | Unchanged; mapped on the Line |
| 3.1.1 Language of Page | A | Set by the app bundle's localisation | nothing | ◐ (system) | Line: Supports when the bundle declares its language |
| 3.1.2 Language of Parts | AA | Mixed-language content (a translator's two columns) | nothing | ✗ | A11y: `.environment(\.locale)` / `accessibilitySpeechLanguage` on SwiftUI text, `LocaleSpanStyle` / `localeList` in Compose |
| 3.2.1 On Focus · 3.2.2 On Input | A | Yes | nothing | ✗ | A11y: no navigation on focus or on picker change without warning |
| 3.2.3, 3.2.4, 3.2.6 | AA/A | n/a for one program (sets only); EN 301 549 V4.1.1 makes 3.2.4 apply within a program | — | n/a | A11y: consistent identification within the app (the same icon means the same thing) |
| 3.3.1 Error Identification · 3.3.3 Error Suggestion | A/AA | Yes | R-FORM-5 (rule only) | ◐ | A11y and Pass 15: errors in text next to the field, and announced (4.1.3) |
| 3.3.2 Labels or Instructions | A | Yes | `placeholder-only-field` | ✓ | Unchanged |
| 3.3.4 Error Prevention (Legal, Financial, Data) | AA | Payments, bookings | R-FORM-4 (undo over confirm) | ◐ | A11y: a review step or undo for payments |
| 3.3.7 Redundant Entry | A | Yes | R-NAV-4 (rule only) | ◐ | Lint `field-no-content-type` (autofill) |
| 3.3.8 Accessible Authentication (Min) | AA | Login screens | nothing | ✗ | Lint `field-no-content-type` (password managers need `.password` / `ContentType.Password`); A11y: paste allowed, no cognitive puzzle |
| 4.1.2 Name, Role, Value | A | Yes: standard controls satisfy it, custom ones must (WCAG2ICT) | `unlabelled-icon-button`; platform files §8 | ◐ | Lint `tap-no-role`, `clickable-no-role`, `toggle-no-state`, `a11y-hidden-control`; Pass 15 |
| 4.1.3 Status Messages | AA | Yes: toasts, saved states, timers ending | nothing | ✗ | Lint `status-not-announced` |

**Section 508 and EN 301 549, beyond WCAG.**
- *503.2 / 11.7 User preferences* (colour, contrast, font size, focus cursor): before this branch, Dynamic Type and `sp` were required and Reduce Motion was linted. The branch adds the Increase Contrast, Reduce Transparency, Bold Text and Differentiate Without Colour checks to the A11y mode, and lint `no-reduce-transparency` for home-made blur.
- *502 / 11.5 Interoperability with AT*: the same evidence as 4.1.2.
- *503.4 Caption controls*: as 1.2.x.
- *5.2 Activation of accessibility features*: system features, so nothing for a screen to do. Not Applicable unless the app adds its own accessibility settings.

**Apple's Accessibility Nutrition Labels** (§4), and what the skill can now back:

| Label | What the skill checks | What it can't check |
|---|---|---|
| VoiceOver | Labels, traits, values, hidden decoration, modals, announcements, custom actions (lint and A11y) | Anything only VoiceOver shows: swipe order on device, rotor, cursor stability on refresh |
| Voice Control | `label-in-name`, gesture alternatives, `accessibilityInputLabels` | "Show names" on device |
| Larger Text | Large text render at AX5, `fold.py` at that size, the lint text rules | Every screen of the app; the skill renders the ones it builds |
| Dark Interface | Light and dark renders (already in step 5) | — |
| Differentiate Without Color Alone | `colour-only-state`; Pass 15 grayscale squint | — |
| Sufficient Contrast | Palette measured by `deal.py`; on-screen pairs measured in Pass 15 | Increase Contrast variants, unless rendered |
| Reduced Motion | `no-reduce-motion`; the motion budget; filmstrip | — |
| Captions, Audio Descriptions | Noted when media is present | The media itself |

Apple allows a label only when *all common tasks* work with the feature (§4). A skill build covers one screen or flow, so the report never claims a label. It says which checks the built screens pass.

**What's left after this branch.**
- No check runs an assistive technology. VoiceOver, TalkBack, Switch Control and Voice Control are not run.
- Reading order is inferred from the code, not heard.
- Contrast is measured from the render by eye-dropper, not computed for every pixel pair.
- These limits are the reason the Line and `acr.py` say "from code and renders; not tested with assistive technology", and leave the evaluation method for a human to complete.


# Sources

### Part A
- https://www.itic.org/policy/accessibility/vpat
- https://www.itic.org/dotAsset/2434a080-87fe-4db1-815e-1e032bf7ac09.docx (VPAT 2.5Rev INT)
- https://www.itic.org/dotAsset/c9497d16-4684-480c-bae2-99256283731c.docx (VPAT 2.5Rev 508)
- https://www.itic.org/dotAsset/67270ffc-91e8-4812-9481-8067621f24fd.docx (VPAT 2.5Rev WCAG)
- https://www.w3.org/TR/wcag2ict-22/
- https://www.w3.org/TR/wcag2mobile-22/
- https://w3c.github.io/matf/
- https://www.access-board.gov/ict/
- https://www.etsi.org/deliver/etsi_en/301500_301599/301549/
- https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf
- https://www.etsi.org/deliver/etsi_en/301500_301599/301549/04.01.01_60/en_301549v040101p.pdf
- https://accessible-eu-centre.ec.europa.eu/content-corner/news/eaa-comes-effect-june-2025-are-you-ready-2025-01-31_en
- https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en
- https://www.dwt.com/insights/2026/09/european-accessibility-act-ict-standards-update (search snippet only, secondary)
- https://developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels
- https://developer.apple.com/help/app-store-connect/manage-app-accessibility/voiceover-evaluation-criteria
- https://developer.apple.com/help/app-store-connect/manage-app-accessibility/voice-control-evaluation-criteria
- https://developer.apple.com/help/app-store-connect/manage-app-accessibility/larger-text-evaluation-criteria
- https://developer.apple.com/help/app-store-connect/manage-app-accessibility/dark-interface-evaluation-criteria
- https://developer.apple.com/help/app-store-connect/manage-app-accessibility/differentiate-without-color-alone-evaluation-criteria
- https://developer.apple.com/help/app-store-connect/manage-app-accessibility/sufficient-contrast-evaluation-criteria
- https://developer.apple.com/help/app-store-connect/manage-app-accessibility/reduced-motion-evaluation-criteria
- https://developer.apple.com/help/app-store-connect/manage-app-accessibility/captions-evaluation-criteria
- https://developer.apple.com/help/app-store-connect/manage-app-accessibility/audio-descriptions-evaluation-criteria
- https://developer.apple.com/help/app-store-connect/release-notes
- https://www.apple.com/newsroom/2025/05/apple-unveils-powerful-accessibility-features-coming-later-this-year/
- https://developer.apple.com/design/human-interface-guidelines/accessibility (+ .json data endpoint)
- https://support.google.com/googleplay/android-developer/answer/9844487?hl=en
- https://support.google.com/googleplay/android-developer/answer/7002270
- https://support.google.com/googleplay/android-developer/answer/10964491 (search snippet only)
- https://github.com/google/Accessibility-Test-Framework-for-Android (+ raw TouchTargetSizeCheck.java, TextContrastCheck.java, ImageContrastCheck.java, ContrastUtils.java)
- https://m3.material.io/foundations/designing/structure
- https://m3.material.io/foundations/designing/color-contrast
- https://developer.android.com/guide/topics/ui/accessibility/apps
- https://developer.android.com/develop/ui/compose/accessibility/api-defaults

### Part B
Apple HIG
- [H-typo]: https://developer.apple.com/design/human-interface-guidelines/typography
- [H-a11y]: https://developer.apple.com/design/human-interface-guidelines/accessibility
- [H-vo]: https://developer.apple.com/design/human-interface-guidelines/voiceover

Apple API docs (all under https://developer.apple.com/documentation/)
- [A-label] swiftui/view/accessibilitylabel(_:) · [A-traits] swiftui/view/accessibilityaddtraits(_:) · [A-isbutton] swiftui/accessibilitytraits/isbutton
- [A-value] swiftui/view/accessibilityvalue(_:) · [A-elem] swiftui/view/accessibilityelement(children:) · [A-combine] swiftui/accessibilitychildbehavior/combine · [A-ignore] swiftui/accessibilitychildbehavior/ignore · [A-contain] swiftui/accessibilitychildbehavior/contain
- [A-repr] swiftui/view/accessibilityrepresentation(representation:) · [A-adjust] swiftui/view/accessibilityadjustableaction(_:) · [A-action] swiftui/view/accessibilityaction(named:_:) · [A-actions] swiftui/view/accessibilityactions(_:)
- [A-input] swiftui/view/accessibilityinputlabels(_:) · [A-sort] swiftui/view/accessibilitysortpriority(_:) · [A-hidden] swiftui/view/accessibilityhidden(_:) · [A-decorative] swiftui/image/init(decorative:bundle:) · [A-heading] swiftui/view/accessibilityheading(_:)
- [A-focusable] swiftui/view/focusable(_:) · [A-focusable2] swiftui/view/focusable(_:interactions:) · [A-responds] swiftui/view/accessibilityrespondstouserinteraction(_:) · [A-tap] swiftui/view/ontapgesture(count:perform:) · [A-lcv] swiftui/view/accessibilityshowslargecontentviewer()
- [A-voenv] swiftui/environmentvalues/accessibilityvoiceoverenabled · [A-swenv] swiftui/environmentvalues/accessibilityswitchcontrolenabled
- [A-scaled] swiftui/scaledmetric · [A-fontcustom] swiftui/font/custom(_:size:relativeto:) · [A-dts-mod] swiftui/view/dynamictypesize(_:) · [A-dts-env] swiftui/environmentvalues/dynamictypesize · [A-dts-enum] swiftui/dynamictypesize · [A-isax] swiftui/dynamictypesize/isaccessibilitysize · [A-vtf] swiftui/viewthatfits
- [A-rm] swiftui/environmentvalues/accessibilityreducemotion · [A-rt] swiftui/environmentvalues/accessibilityreducetransparency · [A-csc] swiftui/environmentvalues/colorschemecontrast · [A-csc-enum] swiftui/colorschemecontrast · [A-dwc] swiftui/environmentvalues/accessibilitydifferentiatewithoutcolor
- [A-lw] swiftui/environmentvalues/legibilityweight · [A-lw-enum] swiftui/legibilityweight · [A-inv] swiftui/view/accessibilityignoresinvertcolors(_:) · [A-invenv] swiftui/environmentvalues/accessibilityinvertcolors · [A-bs] swiftui/environmentvalues/accessibilityshowbuttonshapes
- [A-uirm] uikit/uiaccessibility/isreducemotionenabled · [A-uirt] uikit/uiaccessibility/isreducetransparencyenabled · [A-darker] uikit/uiaccessibility/isdarkersystemcolorsenabled · [A-uidwc] uikit/uiaccessibility/shoulddifferentiatewithoutcolor · [A-uibold] uikit/uiaccessibility/isboldtextenabled · [A-uibs] uikit/uiaccessibility/buttonshapesenabled · [A-onoff] uikit/uiaccessibility/isonoffswitchlabelsenabled
- [A-nsrm] appkit/nsworkspace/accessibilitydisplayshouldreducemotion · [A-nsic] appkit/nsworkspace/accessibilitydisplayshouldincreasecontrast

Apple Support (macOS Text size)
- [M-14]: https://support.apple.com/guide/mac-help/mchld786f2cd/14.0/mac/14.0
- [M-cur]: https://support.apple.com/en-gb/guide/mac-help/mchld786f2cd/mac

Android / Compose
- [D-sem]: https://developer.android.com/develop/ui/compose/accessibility/semantics
- [D-trav]: https://developer.android.com/develop/ui/compose/accessibility/traversal
- [D-defaults]: https://developer.android.com/develop/ui/compose/accessibility/api-defaults
- [D-merge]: https://developer.android.com/develop/ui/compose/accessibility/merging-clearing
- [D-scal]: https://developer.android.com/develop/ui/compose/accessibility/scalable-content
- [D-tap]: https://developer.android.com/develop/ui/compose/touch-input/pointer-input/tap-and-press
- [D-focus]: https://developer.android.com/develop/ui/compose/touch-input/focus/change-focus-traversal-order
- [D-princ]: https://developer.android.com/guide/topics/ui/accessibility/principles
- [D-apps]: https://developer.android.com/guide/topics/ui/accessibility/apps
- [D-14]: https://developer.android.com/about/versions/14/features
- [D-semref]: https://developer.android.com/reference/kotlin/androidx/compose/ui/semantics/package-summary
- [D-clickable]: https://developer.android.com/reference/kotlin/androidx/compose/foundation/clickable.modifier
- [D-toggle]: https://developer.android.com/reference/kotlin/androidx/compose/foundation/selection/toggleable.modifier
- [D-focusable]: https://developer.android.com/reference/kotlin/androidx/compose/foundation/focusable.modifier
- [D-mics]: https://developer.android.com/reference/kotlin/androidx/compose/material3/minimumInteractiveComponentSize.modifier
- [D-m3]: https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary
- [D-pfs]: https://developer.android.com/reference/kotlin/androidx/compose/ui/tooling/preview/PreviewFontScale
- [D-prev]: https://developer.android.com/reference/kotlin/androidx/compose/ui/tooling/preview/Preview
- [D-mds]: https://developer.android.com/reference/kotlin/androidx/compose/ui/MotionDurationScale
- [D-uim]: https://developer.android.com/reference/android/app/UiModeManager
- [D-glob]: https://developer.android.com/reference/android/provider/Settings.Global
- [D-config]: https://developer.android.com/reference/android/content/res/Configuration
- [D-am]: https://developer.android.com/reference/android/view/accessibility/AccessibilityManager
- [D-cc]: https://developer.android.com/reference/com/google/android/material/color/ColorContrast
- [AOSP]: https://android.googlesource.com/platform/frameworks/base/+/refs/heads/android14-release/core/java/android/content/res/FontScaleConverterFactory.java
- [G-a11y]: https://support.google.com/accessibility/android/answer/16323943?hl=en

Kotlin / JetBrains
- [K-ov]: https://kotlinlang.org/docs/multiplatform/compose-accessibility.html
- [K-ios]: https://kotlinlang.org/docs/multiplatform/compose-ios-accessibility.html
- [K-desk]: https://kotlinlang.org/docs/multiplatform/compose-desktop-accessibility.html

W3C
- [W-spec]: https://www.w3.org/TR/WCAG22/
- [W-ts]: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- [W-label]: https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html
- [W-fno]: https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
- [W-ict]: https://www.w3.org/TR/wcag2ict-22/

Not readable: m3.material.io pages (color-contrast, color roles) render client-side and returned only the title. The M3 medium/high contrast-scheme details therefore rest on MDC `ColorContrast` [D-cc] alone.
