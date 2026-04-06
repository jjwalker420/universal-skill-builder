# Script Engineer Agent

Called by USB during Create and Audit modes when a skill involves data retrieval,
API calls, or periodic execution. Two phases: classify, then design.

---

## Phase 1: Skill Type Classification

Classify the skill being built or audited into one of four types.
Read the skill description and intended modes before classifying.

| Type | Label | Signal | Script need |
|------|-------|--------|-------------|
| A | Data / API | Retrieves external data, calls APIs, scrapes, polls sources | Required |
| B | Reasoning / Advisory | Analyzes, recommends, drafts based on provided context | Rarely needed |
| C | Creative / Output | Generates text, posts, messages, documents | Sometimes useful |
| D | Infrastructure / Meta | Manages other skills, installs, audits, orchestrates | Core |

**Classification rules:**
- If the skill calls MCPs (Notion, Slack, Gmail, Calendar, etc.) to retrieve data → Type A
- If the skill fetches web pages or scrapes → Type A
- If the skill runs on a schedule or daily → Type A
- If the skill builds or audits other skills → Type D
- If the skill is purely advisory with no external data pull → Type B
- If the skill generates text output (posts, emails, pitches) → Type C

**Examples:**
- Type A: morning briefings, daily syncs, data monitors, meeting review, security audits
- Type B: advisors, decision filters, pitch refiners, scenario simulators
- Type C: post writers, outreach drafters, content generators
- Type D: skill installers, skill builders, orchestrators

**After classifying:**
- Type A or D → proceed to Phase 2
- Type B or C → report the type to USB and stop. No script design needed unless the
  user explicitly requests it.

---

## Phase 2: Script Design

Run this phase only for Type A and D skills.

### 2a. Token Budget Analysis

For each data source the skill touches, ask:
- What does the model actually need from this source?
- What should be filtered OUT before it reaches the model?
- Can the output be structured as JSON or markdown rather than raw text?
- What is the maximum acceptable token return per call?

Target budgets (these are ceilings, not goals):
- Single API response: 2,000 tokens
- Batch of 3-5 API responses combined: 5,000 tokens
- Full skill run context overhead: 10,000 tokens

If current approach would exceed these, a script is required.

### 2b. Identify What Moves to Code

For each task the skill performs, classify it:

| Task type | Stays in model | Moves to script |
|-----------|---------------|-----------------|
| Deciding what to fetch | Yes | No |
| Fetching data | No | Yes |
| Filtering HTML/markup | No | Yes |
| Parsing page structure | No (after first run) | Yes |
| Formatting output as JSON | No | Yes |
| Making multiple API calls | No (if >2) | Yes |
| Deciding what to do with data | Yes | No |
| Writing final output | Yes | No |

The model orchestrates. Scripts execute. Keep decision logic in the model;
keep data retrieval, filtering, and formatting in scripts.

### 2c. Check Available Templates

Before writing new scripts, check if a template in
`scripts/skill-templates/` applies:

- `web_scraper_optimized.py` — filtered HTML extraction, 90%+ token reduction
- `batch_api_caller.py` — parallel API calls with threading, structured JSON output
- `incremental_runner.py` — check-last-run state, only process new items
- `structured_output.py` — enforce a strict JSON schema on any script output

If a template fits, specify which one and what parameters to customize.
If no template fits, specify the script to write from scratch.

### 2d. Output Schema Design

Every script must return one of:
- JSON with a defined schema (preferred for structured data)
- Markdown with a defined structure (acceptable for narrative summaries)
- Never raw HTML, never unfiltered API responses

Define the output schema before writing the script. Example:

```json
{
  "source": "string",
  "fetched_at": "ISO timestamp",
  "items": [
    {
      "title": "string",
      "url": "string",
      "summary": "string (max 200 chars)"
    }
  ],
  "total_items": "integer",
  "truncated": "boolean"
}
```

### 2e. Parallel and Incremental Opportunities

Check for:
- **Parallel**: Does the skill call 3+ sources or run 3+ searches? If yes, use threading.
  Multiple sequential calls each add full conversation context. Batch them.
- **Incremental**: Does the skill run repeatedly on the same source? If yes, implement
  state tracking. Script checks what was last processed; only fetches new items.
- **Stop conditions**: Does the skill paginate or loop? Define a hard max (page limit,
  item limit, call limit) directly in the script. Never leave it open-ended.

### 2f. Deliverable

Produce a script design spec with:
1. Type classification with reasoning
2. Token budget analysis (current vs target)
3. Task breakdown (model vs script)
4. Template recommendation or from-scratch spec
5. Output schema (JSON or markdown structure)
6. Parallel / incremental flags
7. Any hard-coded configuration to bake in (URLs, category names, field selectors)

Present the spec to the user before writing any code. Confirm before proceeding.
