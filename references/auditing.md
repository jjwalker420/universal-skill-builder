# Skill Auditing

Two audit types. Both end with: proposed fixes → user approval → apply → re-verify.

---

## Architectural Audit (any skill, any time)

**0. Assess complexity tier.** Read the target skill — SKILL.md + all referenced files. Count lines, modes, files, and reference files. Classify:

| Signal | Simple | Standard | Complex |
|--------|--------|----------|---------|
| Modes | 1 | 2-3 | 4+ |
| Total files | 1 | 2-4 | 5+ |
| SKILL.md lines | <150 | 150-300 | 300+ |
| Reference files | 0 | 1-3 | 4+ |
| Cross-mode data flow | None | Minimal | Yes |

**Highest tier triggered by any single signal wins.** State the tier and which signals triggered it.

Tier determines which principles to score:

**Simple (9 principles):** 1, 6, 7, 8, 10, 22, 24, 32, 34
**Standard (24 principles):** Simple + 2, 3, 4, 5, 9, 11, 15, 16, 18, 20, 21, 23, 29, 31, 33
**Complex (34 principles):** Standard + 12, 13, 14, 17, 19, 25, 26, 27, 28, 30

Escape hatch: if a principle is relevant despite tier exclusion, include it with justification. The tier is a default filter, not a ceiling.

**1. Read the target skill.** SKILL.md + all referenced files. Count lines per file — flag anything over 300.

**2. Score applicable principles.** For each principle in the tier: ✅ COVERED / ⚠️ PARTIAL / ❌ MISSING. Cite evidence (line numbers, file names). PARTIAL: explain the gap. MISSING: state exactly what's needed.

**3. Check tier-relevant specifics:**

All tiers:
- SKILL.md line count (principle 6)
- Default-behavior instructions that should be cut (principle 8)
- Step 0 context loading (principle 22)
- Guardrails consolidated, not scattered (principle 24)

Standard+:
- Cross-file redundancy (principle 5)
- Mode routing table at top (principles 9, 21)
- Feedback/self-learning loop (principles 15, 16)
- Output templates separated from engine (principle 23)
- Static vs temporal separation (principle 4)
- Environment awareness (principle 11)
- Automation evaluation (principle 18)
- README.md present (principle 29)

Complex only:
- Data flows per environment (principle 12)
- Cross-environment verification (principle 14)
- Override pattern detection (principle 17)
- Watchlist/cross-mode patterns (principle 25)

**4. Scope analysis — is this skill doing too much?** A skill should be one job with multiple entry points (modes). Signs it should be split:
- Modes that don't share reference files, scripts, or domain knowledge
- Modes that serve completely different user needs at different times
- The skill needs more than 5-6 reference files to cover everything
- Two modes would never be needed in the same session
- The description is hard to write because the skill does unrelated things

If splitting is warranted, recommend which modes become separate skills and provide a starter prompt for each new skill the user can paste into a new chat:
```
"I want to build a skill called [name]. It should [1-sentence purpose].
Key modes: [list]. It was split from [original skill] because [reason]."
```

**5. Scorecard.** Report: tier assessed, principles scored (N of 34), covered/partial/missing counts by category.

**6. Ranked fix list.** HIGH / MEDIUM / LOW. Each fix specific and actionable.

**7. Get approval.** Present scorecard and fixes. Do NOT auto-apply.

**8. Apply and re-score.** Apply approved fixes. Re-run scoring on changed sections.

---

## Post-Ship Performance Audit (deployed skills only)

Run when: user requests a review, monthly maintenance, or feedback-log shows patterns.

**1. Gather data.** Read the skill's feedback-log.md (or decisions-log.md). Count triggers, recommendations followed vs overridden, outcomes logged.

**2. Pattern analysis:**
- Override rate by mode: >40% overridden → needs recalibration
- Outcome quality: % of followed recommendations with positive outcomes
- Stale thresholds: hardcoded values still accurate?
- Unused modes: 0 triggers → candidate for removal or trigger improvement

**3. Compression check.** Re-count SKILL.md lines. Cut reactive additions that could be generalized.

**4. Propose 1-3 improvements.** Ranked by impact. Do NOT auto-apply.

**5. Re-run evals** to verify no regression.
