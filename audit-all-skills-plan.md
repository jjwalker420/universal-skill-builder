# Parallel Skill Audit & Fix Plan

## Context
Run the universal-skill-builder's architectural audit against all ~159 installed skills using parallel subagents, collect results, get approval on fixes, then apply fixes in parallel.

## Inventory
- **62 top-level skills** in `/Users/jjwalker/.claude/skills/` (excluding universal-skill-builder + template-skill)
- **4 document-skills** (docx, pdf, pptx, xlsx)
- **93 GWS sub-skills** (core services, personas, recipes)

---

## Phase 1: Audit (4 waves of parallel subagents, ~12 min)

Each subagent gets the full audit methodology (`references/auditing.md` + `references/skill-development-principles.md`) embedded directly in its prompt.

### Wave 1 — 10 subagents: Complex skills (over 300 lines)
One dedicated subagent per skill. Score against all 34 principles.

| Subagent | Skill | Lines |
|----------|-------|-------|
| A1 | writing-skills | 655 |
| A2 | slack-gif-creator | 646 |
| A3 | personal-finance | 578 |
| A4 | content-research-writer | 538 |
| A5 | langsmith-fetch | 485 |
| A6 | document-skills/pptx | 483 |
| A7 | invoice-organizer | 446 |
| A8 | file-organizer | 433 |
| A9 | test-driven-development | 371 |
| A10 | tailored-resume-generator | 345 |

### Wave 2 — 10 subagents: Standard/borderline skills (180-332 lines)
Batch 2-3 per subagent. Score 24 principles each.

| Subagent | Skills |
|----------|--------|
| B1 | mcp-builder (328) |
| B2 | meeting-insights-analyzer (327), twitter-algorithm-optimizer (326) |
| B3 | developer-growth-analysis (322), systematic-debugging (296) |
| B4 | competitive-ads-extractor (293), subagent-driven-development (277) |
| B5 | negotiation-advisor (226) |
| B6 | using-git-worktrees (218), receiving-code-review (213) |
| B7 | domain-name-brainstormer (212), skill-creator (209) |
| B8 | finishing-a-development-branch (200), lead-research-assistant (199) |
| B9 | eod-sync (193), dispatching-parallel-agents (182) |
| B10 | brainstorming (164), writing-plans (152), document-skills/docx (196), document-skills/pdf (294), document-skills/xlsx (288) |

### Wave 3 — 8 subagents: Simple/Standard top-level skills (32-164 lines)
Batch 4-6 per subagent.

| Subagent | Skills |
|----------|--------|
| C1 | raffle-winner-picker (159), connect (156), verification-before-completion (139), morning-briefing (136) |
| C2 | canvas-design (129), notebooklm (127), using-superpowers (117), wrapup (108) |
| C3 | requesting-code-review (105), changelog-generator (104), image-enhancer (99), video-downloader (98) |
| C4 | github-security-audit (98), webapp-testing (95), weekly-status (88), scenario-simulation (88) |
| C5 | meeting-review (81), skill-share (80), outreach-prep (80), connect-apps (80) |
| C6 | decision-filter (75), artifacts-builder (73), brand-guidelines (73), executing-plans (70) |
| C7 | All firecrawl variants (firecrawl, firecrawl-download, firecrawl-scrape, firecrawl-search, firecrawl-crawl, firecrawl-map, firecrawl-agent, firecrawl-instruct) |
| C8 | theme-factory (59), linkedin-post (59), internal-comms (32) |

### Wave 4 — 10 subagents: GWS sub-skills (~9-10 per subagent)
Compressed output format. Most are Simple tier (25-110 lines).

| Subagent | Group |
|----------|-------|
| D1 | GWS core services (gws-drive, gws-calendar, gws-chat, gws-docs, etc.) |
| D2 | Gmail family (gws-gmail-*) + gws-drive-upload |
| D3 | Remaining GWS services (gws-forms, gws-keep, gws-meet, gws-sheets-*, etc.) |
| D4 | gws-workflow-* + first 5 personas |
| D5 | Remaining personas + early recipes |
| D6-D10 | Recipes batched ~10 per subagent |

---

## Phase 2: Review (user approval gate)

After all waves complete, compile:
1. **Summary dashboard** — total scores, critical findings, skills recommended for splitting
2. **All HIGH priority fixes** aggregated across all skills
3. **Full scorecards** available for deep-dive

User approves: all HIGH, all HIGH+MEDIUM, or cherry-pick specific fixes.

---

## Phase 3: Fix (3 waves of parallel subagents, ~9 min)

### Fix Wave 1 — 10 subagents: One per oversized skill
Compression + restructuring. Target: under 300 lines each.

### Fix Wave 2 — 8 subagents: 2-4 standard skills each
Add missing sections (Step 0, guardrails, feedback loops).

### Fix Wave 3 — 5 subagents: 15-20 GWS recipes each
Minimal fixes expected for these small skills.

Each fix subagent gets: approved fix list, original scorecard, and methodology. Applies fixes, re-scores changed principles, reports before/after line counts.

---

## Subagent Prompt Template

Each audit subagent receives:

1. **Methodology** — full text of `auditing.md` + `skill-development-principles.md` (163 lines total, embedded directly)
2. **Assignment** — list of skills to audit with paths
3. **Output format:**

```
## [skill-name]
**Tier:** [Simple|Standard|Complex] — triggered by: [signals]
**Lines:** SKILL.md=[N], total=[N]
**Over 300-line ceiling:** [Yes/No]

### Scorecard
| # | Principle | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Single file, single job | COVERED/PARTIAL/MISSING | [cite] |
...

**Summary:** [N] COVERED, [N] PARTIAL, [N] MISSING out of [N] scored

### Ranked Fixes
1. **HIGH** — [specific actionable fix]
2. **MEDIUM** — [specific actionable fix]
3. **LOW** — [specific actionable fix]

### Scope Analysis
[Should this skill be split?]
```

For GWS batch subagents, use compressed format:
```
## [recipe-name] (Simple, [N] lines)
COVERED: [principle numbers]
PARTIAL: [#]: [gap]
MISSING: [#]: [what's needed]
Fixes: [only HIGH or MEDIUM]
```

---

## How to Run

Tell Claude: "Run the audit-all-skills-plan from my skill builder folder" or paste:

```
Using /dispatching-parallel-agents and /universal-skill-builder, execute 
audit-all-skills-plan.md from the universal-skill-builder folder. Start 
with Wave 1 (10 Complex skill audits in parallel).
```

---

## Estimated Timeline
- Phase 1 (Audit): ~12 min wall-clock
- Phase 2 (Review): depends on you
- Phase 3 (Fix): ~9 min wall-clock
- **Total: ~20 min + review time**
