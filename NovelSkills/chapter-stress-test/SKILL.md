---
name: chapter-stress-test
description: Stress-test each chapter against bible for errors and traps.
version: 0.1.0
author: quint (quint), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [novel-writing, continuity, quality-gate, moonbound]
    related_skills: [novel-writing-workflow, concept-stress-test]
---

# Chapter Stress-Test

## Purpose

After any chapter is written, run this review before declaring it done. It catches continuity errors, clarity gaps, pacing problems, and reader-complaint traps that would make a reader stop, re-read, or abandon the book.

This is **not** a prose edit. It is a structural/consistency gate. Fix identified issues before moving to the next chapter.

## When to Use

- After finishing a chapter draft — before saving it as final or moving to the next chapter.
- When the user says "review chapter X" or "stress-test this chapter."
- Before sending a chapter to the user for approval.
- When the user suspects a chapter has pacing or clarity issues.

Do NOT use for: concept-level validation (use `concept-stress-test`), line-level prose editing (use `novel-writing-workflow` Phase 3), or series bible creation (use `novel-writing-workflow` Phase 1).

## Prerequisites

- **Series bible** — Load the series bible file first. Default path: `F:/01_Ventures/NovelSeries/series-bible.md`. The user corrects the path when it changes.
- **Finished chapter** — The chapter file to review.
- **Previous chapter (if not Ch 1)** — Read it to check scene transitions and continuity.
- **Chapter beat sheet (if available)** — Read it to check the chapter against its planned outline.

## Procedure

### Phase 1: Continuity Against the Series Bible

Read the series bible. Cross-reference every fact in the chapter against the bible. Check:

1. **Character facts** — Names, relationships, titles, hierarchy, appearance details, pet names, props. Example: Victor's father is Cyrus, not "the old Alpha." Amelia's cat is Luna (female, scarred, slate-black, orange eyes). If anything contradicts the bible, flag it.

2. **Timeline** — Does the chapter's events fit chronologically? Are days/weeks/months consistent with prior chapters? If the chapter says "three days later" but the last chapter happened yesterday, flag it.

3. **World state** — Is the Veil already named? Is the Hollow King already referenced? Does the chapter's lore level match where we are in the story? (See `novel-writing-workflow` Phase 2, steps 14-15, for chapter-specific naming permissions.)

4. **Lore mechanics** — Mate bond stage (Stage One vs. Stage Two), ceremony status, 3-pace boundary. If characters access full sensory awareness or full intimacy before the ceremony, flag it.

5. **Character knowledge** — Does the POV character use terms they wouldn't know? (Amelia: human-limited until Ch 9 Josiah introduces Mate Bond/pack/Veil. After Ch 9, she can use those terms naturally.)

### Phase 2: POV and Perspective Integrity

6. **Close third-person discipline** — Is the chapter inside the POV character's head, or does it drift into omniscient narration? Flag any paragraph that describes a character from the outside when it should be from the inside.

7. **POV character world knowledge** — Scan internal monologue, dialogue assumptions, and reactions. Does the POV character know or say things they couldn't plausibly know? Example: Victor thinking "what Aurela was going to say" in Ch 9 when he hasn't met her yet. Flag and fix.

8. **POV consistency within the chapter** — If the chapter has multiple POV sections (divided by `---`), verify each section stays in its designated POV character's head. No perspective drift within a single section.

9. **Voice distinction** — Does each character's internal voice sound distinct? Amelia: sensory, fragmented, emotional. Victor: analytical, assessing, risk-focused. If two characters sound identical, flag it.

### Phase 3: Reader Clarity and Flow

10. **Opening clarity** — Can a reader immediately understand WHO is WHERE and WHAT is happening in the first 3-5 lines? Flag chapters that open with disorienting scene jumps, unnamed characters, or abrupt context shifts.

11. **Context bridge** — Does the chapter's opening connect to the previous chapter's ending? If Ch N-1 ended with characters in a room, Ch N must not open with characters in separate locations without explaining how we got there. Read the last 5-10 lines of the previous chapter and the first 5-10 lines of this chapter. Flag gaps.

12. **Scene-state continuity** — Who was where at the end of the previous chapter? Does the new chapter respect that? Flag if characters appear/disappear without explanation, or if physical scene setup contradicts the prior chapter.

13. **Exposition vs. action balance** — Does the chapter dump world-building in exposition? Lore should be woven into active scenes, not delivered in lectures. Flag chapters that are more than ~30% exposition without active scenes breaking it up.

14. **Information pacing** — Is too much lore dumped at once? Or is too little explained, leaving readers confused? Check: every new lore concept should be introduced in context (during an active scene, through character experience), not in a standalone info-dump paragraph.

15. **Dialogue clarity** — In back-and-forth exchanges, does every line have a clear speaker attribution? Flag unattributed lines in alternating dialogue. Flag ambiguous pronouns that could confuse the reader about who is being discussed.

16. **Closing hook** — Does the chapter end with a hook (emotional, physical, or mystery-driven)? A question, a shift in power, a new piece of information, or a moment that pulls the reader into the next chapter? Flag flat endings.

### Phase 4: Reader Complaint Traps

17. **Check against known reader complaint patterns.** Scan the chapter for these traps:

| Trap | What it is | How it looks in a chapter |
|------|-----------|--------------------------|
| **Disorienting scene jump** | Reader can't follow where/when things moved | Chapter opens without context for a location/time shift |
| **Knowledge bleed** | Character knows things they shouldn't | Human says "mate bond" before being introduced to it |
| **Info-dump** | Lore delivered in a lecture, not an experience | 3+ paragraphs of exposition with no action/dialogue |
| **Flat ending** | Chapter ends without forward momentum | Last lines resolve everything, no tension remains |
| **POV drift** | Narration slips outside the character's head | Describing what another character "was thinking" |
| **Duplicate beat** | Chapter repeats a scene from the previous one | Same conversation or meeting described in both Ch N and Ch N-1 |
| **Name overload** | Too many new names in one chapter | Reader cannot track who is who after reading |
| **Romance pacing** | Intimacy happens too fast or too slow for the stage | Stage One bond has full sensory/empathy connection |
| **Unearned emotional beat** | Character has a major emotional reaction without setup | Crying/angry/breaking down with no prior tension building |
| **Omniscient leakage** | Narrator reveals information the POV character doesn't know | "She didn't know yet, but in three chapters..." |
| **Prop/character amnesia** | An established object or character disappears without explanation | The cat that was mentioned 2 pages ago is gone |
| **Contradictory description** | Same thing described two different ways in one chapter | "She was terrified" then "she felt calm" in adjacent paragraphs |

18. **For each trap found, provide:**
- **Trap name** — Which trap is triggered
- **Line reference** — Where it occurs (line numbers)
- **Severity** — CRITICAL (breaks the chapter), HIGH (reader will notice), MEDIUM (subtle but accumulates), LOW (polish-level)
- **Fix suggestion** — One specific line the user can apply

### Phase 5: Cross-Chapter Prose Check

19. **Description repetition** — Scan the previous chapter for physical descriptions of characters, settings, or actions. Does this chapter repeat the same phrasing? If so, flag it. Each chapter should show the same character from a new angle.

20. **Internal monologue repetition** — Does a character repeat the same thought or reassurance verbatim within the chapter? Flag identical sentence structures used for the same beat.

21. **Name repetition within a paragraph** — Once a character is named, subsequent references should use pronouns or descriptors. Flag paragraphs where the same name appears more than twice.

### Phase 6: Output the Report

22. **Produce a structured report** with these sections:

```
## Chapter Stress-Test Report: [Chapter X]

### CONTINUITY (against series bible)
- [PASS/FAIL] Character facts — details
- [PASS/FAIL] Timeline — details
- [PASS/FAIL] World state/lore timing — details
- [PASS/FAIL] Lore mechanics (bond stage, ceremony) — details
- [PASS/FAIL] Character knowledge — details

### POV & PERSPECTIVE
- [PASS/FAIL] Close third-person discipline — details
- [PASS/FAIL] POV world knowledge — details
- [PASS/FAIL] POV consistency — details
- [PASS/FAIL] Voice distinction — details

### CLARITY & FLOW
- [PASS/FAIL] Opening clarity — details
- [PASS/FAIL] Context bridge (vs. previous chapter) — details
- [PASS/FAIL] Scene-state continuity — details
- [PASS/FAIL] Exposition/action balance — details
- [PASS/FAIL] Information pacing — details
- [PASS/FAIL] Dialogue clarity — details
- [PASS/FAIL] Closing hook — details

### READER COMPLAINT TRAPS
- [TRAP NAME] [Severity] — Line N: description + fix

### PROSE REPETITION
- [REPETITION TYPE] [Severity] — Line N: description

### SUMMARY
- Total issues found: X (Critical: Y, High: Z, Medium: W, Low: V)
- Overall verdict: PASS / CONDITIONAL PASS / FAIL
- Recommended action: proceed to user review / fix before review / rewrite
```

23. **If any CRITICAL issues exist, stop and present them first.** The user needs to fix those before anything else.

24. **If CONDITIONAL PASS, list the fixes needed and apply them with `patch`** — but only for mechanical issues (duplicate content, knowledge bleed, unattributed dialogue). For prose-level issues (pacing, emotional beats, flow), list them for the user to decide.

25. **If FAIL, explain why and provide a prioritized fix list.** Do not attempt to rewrite — the author's voice matters.

## Pitfalls

### Over-interpreting creative choices as errors

Just because a scene feels different from prior chapters doesn't mean it's wrong. Only flag issues that are objective contradictions (timeline, name, relationship, knowledge), not subjective preferences. When unsure, flag it as MEDIUM and let the user decide.

### Fixing prose when only structural review is requested

This skill is a structural/consistency gate, NOT a prose edit. Do not rewrite sentences, suggest better word choices, or restructure paragraphs unless the user specifically asks for a prose pass afterward. The output should be diagnostic, not editorial.

### Forgetting the previous chapter

Reader complaint trap #1 (disorienting scene jump) and #6 (duplicate beat) REQUIRE reading the previous chapter. If only one chapter is provided, note that the cross-chapter checks cannot run and limit the report to single-chapter checks.

### Missing the series bible

Many continuity checks (character facts, lore mechanics, timeline) require the series bible. If the bible is not available, state explicitly which checks were skipped and why.

### Ignoring the chapter beat sheet

If a beat sheet exists, compare the chapter against it. The chapter should hit every planned beat. If a beat is missing entirely, flag it as a HIGH severity issue. If a beat was added that wasn't planned, flag it as MEDIUM (may be fine, but should be intentional).

### Not distinguishing between fixable and subjective issues

Mechanical issues (knowledge bleed, duplicate content, unattributed dialogue) should be fixed automatically with `patch`. Subjective issues (pacing feel, emotional resonance, prose rhythm) should be listed for the user's review — don't auto-patch those.

### Confusing this with concept-stress-test

`concept-stress-test` evaluates a creative concept against genre complaint patterns BEFORE drafting. This skill evaluates a finished chapter against the series bible, continuity, and reader traps AFTER drafting. They serve different phases.

## Verification

- After fixing all identified issues, re-run the stress test on the corrected chapter.
- Confirm each flagged issue now shows [PASS] in the report.
- Report the updated counts (should be zero critical, reduced high/medium).
- Once the report shows all PASS except LOW (polish) items, the chapter is cleared.
