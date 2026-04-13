---
name: universal-skill-builder
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, capture a workflow from the current conversation and turn it into a skill, edit or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, audit an existing skill against architectural principles, check if a skill is doing too much and should be split, or optimize a skill's description for better triggering accuracy. ALWAYS trigger when the user says "build a skill", "turn this into a skill", "audit this skill", "review this skill", "is this skill doing too much", "optimize this description", "package this skill", "make a skill from what we just did", "save this workflow", "can we automate this", or any variation.
---

# Skill Creator

## Mode Routing

| User says... | Mode | Key files to read |
|---|---|---|
| Create/build a skill | Create | references/writing-guide.md, references/schemas.md |
| Test/evaluate a skill | Evaluate | agents/grader.md, agents/comparator.md |
| Improve/iterate a skill | Improve | agents/analyzer.md, previous eval results |
| Optimize description | Optimize | scripts/improve_description.py |
| Package a skill | Package | scripts/package_skill.py |
| Audit/review/optimize a skill | Audit | references/auditing.md, references/skill-development-principles.md |
| Add/audit scripts for a skill | Script Engineer | agents/script-engineer.md, references/script-patterns.md |

## Guardrails (enforce on every run)

- Never use `/skill-test` or any other testing skill to run evals
- ALWAYS generate the eval viewer (`generate_review.py`) BEFORE evaluating outputs yourself — get results in front of the human first
- In `grading.json`, use field names `text`, `passed`, `evidence` — not `name`/`met`/`details`
- In `benchmark.json`, put `with_skill` runs before baseline counterparts; nest `pass_rate` under `result`
- Never delete content from skills — only move to reference files or compress
- At end of any multi-turn build session, generate a handoff.md: iteration count, current state, known issues, next steps

### Quality gate (before delivering any generated SKILL.md)

Assess the generated skill's complexity tier per `references/auditing.md` Step 0. Apply checks for that tier and above.

All tiers:
- Step 0 context loading? (principle 22)
- Guardrails section? (principle 24)
- SKILL.md under 300 lines? Target 300, hard ceiling 350. Compress if over. (principles 6, 7)
- No instructions for default Claude behavior? (principle 8)
- v1 scope: core modes only, prove they work before adding features? (principle 34)
- If skill retrieves data or calls APIs (Type A/D): does it use scripts for heavy lifting rather than model logic? (references/script-patterns.md — load script-engineer.md if not)

Standard and Complex only:
- Mode routing table at top? (principles 9, 21)
- Output templates separated if >3? (principle 23)
- Feedback/logging mechanism included? (principle 15)
- Automation evaluation included? (principle 18)

If any applicable check fails, fix before showing to user.

## Mode Data Flow

| Mode | Reads | Produces |
|---|---|---|
| Create | user interview | SKILL.md, evals.json, README.md |
| Evaluate | evals.json, SKILL.md | benchmark.json, feedback.json, eval outputs |
| Improve | feedback.json, benchmark.json, transcripts | revised SKILL.md |
| Optimize | SKILL.md, benchmark.json | compressed SKILL.md |
| Package | final SKILL.md + all skill files | .skill file |
| Audit | SKILL.md, feedback-log.md (if present), principles | scorecard, ranked fix list |

## Step 0: Load Context

1. Read this file for routing and workflow
2. Based on mode, read the files listed in the routing table
3. If in Cowork or Claude.ai: read the relevant section of `references/env-adapters.md`
4. Verify Python 3.10+ is available (`python3 --version`). The eval viewer and packaging scripts require it.

---

## Creating a Skill

### Capture Intent

Determine where the user is — starting fresh, have a draft already, or want to capture a workflow from the current conversation.

**Capturing from a conversation:** When the user says "turn this into a skill" or similar, extract the workflow before asking questions:
1. Scan the conversation for tools used, steps taken, and corrections the user made
2. Identify the repeatable pattern — what stays the same every time vs what changes per use
3. Extract inputs (what the user provides), outputs (what gets produced), and decision points (where judgment is needed)
4. Draft the skill based on the observed workflow, then confirm: "Here's what I captured — does this match what you'd want every time?"
5. Only ask interview questions to fill gaps the conversation didn't cover

**Starting fresh or from a draft:** Gather these before writing:
1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Do we need test cases? Skills with verifiable outputs benefit from them; subjective skills often don't. Suggest the default, let the user decide.

### Interview and Research

Ask about edge cases, input/output formats, example files, success criteria, and dependencies before writing test prompts. Use available MCPs to research in parallel if useful.

### Write the SKILL.md

Fill in these components:

- **name**: Gerund form (e.g., `analyzing-data`, `creating-reports`). Lowercase, hyphens only. No platform names (claude, anthropic). Max 64 chars.
- **description**: Write this LAST. Third person. Max 1024 characters. See "Writing the Description" below.
- **compatibility**: Required tools/dependencies (optional)
- **skill body**: modes, steps, routing

Read `references/writing-guide.md` for skill anatomy, progressive disclosure, writing patterns, and style guidance.

Every generated skill must include: a feedback/logging mechanism (see `references/feedback-loop.md`), a self-audit hook in any periodic mode, and an automation evaluation (can any output be scheduled).

### Writing Standards (apply when authoring any skill body)

**Degrees of Freedom** — match instruction format to how much judgment Claude should apply:
- **Bullet points** → high freedom (heuristics, "use best judgment")
- **Code block templates** → medium freedom (fill in this structured form)
- **Exact bash commands** → low freedom (fragile ops, do not improvise)

**Structure rules:**
- Use `/` for all file paths, never `\`
- Progressive disclosure goes one level deep only — link to a secondary file, never chain links further
- Complex skills (3+ steps with state) must include a copy-pasteable markdown checklist Claude can update to track progress
- For any multi-step workflow that modifies state: **Plan → Validate → Execute** — check preconditions before applying changes
- Scripts are black boxes: if Claude is unsure how a script behaves, run `--help`, not guesswork

### Writing the Description

The description is how Claude decides whether to use the skill — it's the most important line in the file. Write it after the skill is complete, not before.

1. **Write in third person.** Lead with what it does in one sentence. Then list specific trigger contexts.
2. **Include trigger phrases** the user would actually say — both explicit ("audit this skill") and implicit ("is this skill doing too much?").
3. **Be pushy.** Claude undertriggers by default. Add "ALWAYS trigger when..." with concrete examples. Include near-miss phrases the user might say.
4. **Stay under 1024 characters.** This is a hard system limit. Every character counts — cut filler words.
5. **Don't duplicate the body.** The description says *when* to use the skill. The body says *how*.

Before delivering, run the quality gate in the Guardrails section above.

### Test Cases

Write 2-3 realistic test prompts. Share with user for approval. Save to `evals/evals.json` — see `references/schemas.md` for the schema.

### Generate README

After the skill passes evals, generate a README.md using the template in `references/readme-template.md`. Fill in all sections from the skill's modes, trigger phrases, and environment requirements. Save alongside the skill's SKILL.md.

---

## Running and Evaluating Test Cases

One continuous sequence — don't stop partway. Put results in `<skill-name>-workspace/`, organized by `iteration-<N>/eval-<name>/`.

### Step 1: Spawn all runs in the same turn

For each test case, spawn two subagents simultaneously — one with-skill, one baseline. Do not spawn with-skill first and come back for baselines later.

**With-skill run:**
```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <files or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<name>/with_skill/outputs/
- Outputs to save: <what the user cares about>
```

**Baseline run** (same prompt):
- New skill: no skill path, save to `without_skill/outputs/`
- Improving existing: snapshot first (`cp -r <skill-path> <workspace>/skill-snapshot/`), point baseline at snapshot, save to `old_skill/outputs/`

Write `eval_metadata.json` per eval directory (see `references/schemas.md` for format).

**Directory structure:** Each config directory must contain `run-N/` subdirectories (e.g., `eval-tip-calc/with_skill/run-1/`) with `grading.json`, `timing.json`, and `outputs/` inside. The aggregator expects this nesting — flat directories produce empty benchmarks.

### Step 2: While runs are in progress, draft assertions

Draft quantitative assertions for each test case. Good assertions are objectively verifiable and have descriptive names — they should read clearly in the benchmark viewer. Subjective skills are better evaluated qualitatively. Update `eval_metadata.json` and `evals/evals.json` with finalized assertions.

### Step 3: Capture timing data

When each subagent completes, save `total_tokens` and `duration_ms` immediately to `timing.json` in the run directory — this data is only available at notification time and cannot be recovered later. See `references/schemas.md` for format.

### Step 4: Grade, aggregate, launch viewer

1. **Grade** — spawn a grader subagent using `agents/grader.md`. Save to `grading.json`. Use `text`, `passed`, `evidence` fields. For assertions checkable programmatically, write and run a script rather than eyeballing.

2. **Aggregate:**
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
   See `references/schemas.md` for the exact benchmark.json schema the viewer expects.

3. **Analyze** — read the "Analyzing Benchmark Results" section in `agents/analyzer.md`. Surface: non-discriminating assertions (always pass regardless of skill), high-variance evals (possibly flaky), time/token tradeoffs.

4. **Launch viewer:**
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   For iteration 2+: add `--previous-workspace <workspace>/iteration-<N-1>`.
   In headless/Cowork: use `--static <output_path>` instead.

5. Tell the user: "I've opened the results in your browser. The Outputs tab lets you review test cases and leave feedback; the Benchmark tab shows the stats. Click 'Submit All Reviews' when done."

### Step 5: Read the feedback

When done, read `feedback.json`. Empty feedback = user was satisfied. Focus improvements on cases with specific complaints. Kill the viewer: `kill $VIEWER_PID 2>/dev/null`.

---

## Improving the Skill

### How to think about improvements

1. **Generalize from feedback.** These skills run at scale across many different prompts. Avoid fiddly overfit changes — if something is stubborn, try different metaphors or patterns.
2. **Keep the prompt lean.** Remove things that aren't pulling their weight. Read transcripts to spot wasted motion, then cut the instructions causing it.
3. **Explain the why.** LLMs follow reasoning better than rigid rules. If you're writing ALWAYS/NEVER in all caps, reframe and explain the reason instead.
4. **Bundle repeated work.** If multiple test runs independently wrote the same helper script, put it in `scripts/` and tell the skill to use it.

### Iteration loop

1. Apply improvements to the skill
2. Rerun all test cases into `iteration-<N+1>/` — with-skill + baseline
3. Launch viewer with `--previous-workspace` pointing at previous iteration
4. Wait for user review → read feedback → improve → repeat

Stop when: user is satisfied, all feedback is empty, or no meaningful progress is being made.

When iteration stops, proceed to the Optimize phase before packaging.

---

## Phase: Optimize

After the skill works and evals pass, run a full optimization audit. Do NOT skip — this runs before every packaging.

1. **Quality gate:** Run the checklist from the Guardrails section. Fix any failures.
2. **Redundancy scan:** Check every file for duplicated content. Keep in one place, point from others.
3. **Compression pass:** For each remaining line, ask "does removing this change Claude's output?" If no, cut it. Target 300 lines, hard ceiling 350 for complex multi-mode skills.
4. **Environment check:** Does the skill specify which environments it works in and what differs? If not, add it.
5. **Cross-environment test:** Confirm the skill works in at least one environment other than the one it was built in. Verify: (a) `quick_validate.py` passes, (b) all file paths in SKILL.md are relative — no absolute paths tied to one machine, (c) Step 0 loads correctly in the target environment (files exist and are readable).
6. **Re-run evals** to verify no regression.

---

## Advanced: Blind Comparison

For rigorous A/B comparison between two versions, read `agents/comparator.md` and `agents/analyzer.md`. Give two outputs to an independent agent without revealing which is which, then analyze why the winner won. Optional — most users won't need it.

---

## Description Optimization

The `description` frontmatter is the primary trigger mechanism. After creating or improving a skill, offer to optimize it.

**Step 1:** Create 20 eval queries — mix of should-trigger and should-not-trigger — as `{"query": "...", "should_trigger": true/false}` JSON. Queries must be realistic (file paths, company names, casual phrasing, typos). Should-not-trigger: near-misses sharing keywords but needing something different. Must be substantive enough that Claude would benefit from a skill.

**Step 2:** Review with user. Read `assets/eval_review.html`, replace `__EVAL_DATA_PLACEHOLDER__`, `__SKILL_NAME_PLACEHOLDER__`, `__SKILL_DESCRIPTION_PLACEHOLDER__`. Write to `/tmp/eval_review_<skill-name>.html` and open it. User exports to `~/Downloads/eval_set.json`.

**Step 3:** Run the optimization loop:
```bash
python -m scripts.run_loop \
  --eval-set <path> --skill-path <path> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 --verbose
```
Splits evals 60/40 train/test, evaluates 3 runs per query, proposes improvements, selects best by test score (not train, to avoid overfitting).

**Step 4:** Take `best_description` from JSON output, update SKILL.md frontmatter, show user before/after with scores.

---

## Package and Present

Before packaging, run at least one eval with a real file or real use case the user provides — not just synthetic prompts. Synthetic evals catch structural issues; real data catches the gaps that matter.

Only if the `present_files` tool is available:

Requires `pyyaml` (`pip3 install pyyaml` if not installed).

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

Point the user to the resulting `.skill` file path.

---

## Auditing a Skill

Read `references/auditing.md` for both audit types:
- **Architectural Audit** (any skill, any time): Assess complexity tier (Simple/Standard/Complex), then score applicable principles. Produce scorecard and ranked fix list.
- **Post-Ship Audit** (deployed skills): Analyze feedback-log for override patterns, stale outcomes, unused modes.

### Post-Audit Improvement Flow

The audit produces the diagnosis. The treatment follows the existing loop:

1. **Audit** → scorecard + ranked fix list → user approves fixes
2. **Evaluate** → run evals on the current (pre-fix) version to establish a baseline
3. **Improve** → apply approved fixes, rerun evals, confirm no regression
4. **Optimize** → compression pass, cross-environment test, quality gate
5. **Package** → repackage the improved skill

Don't skip steps 2–4. Without a baseline eval before fixing, you can't prove the fixes helped and didn't break something else.

---

## Self-Learning

This skill should practice what it preaches. After each skill build session, append to `skill-creator-log.md` in the workspace:

```
## [Date] — [Skill Name] — [Mode Used]
What worked: [brief]
What broke: [brief]
User overrides: [any instructions the user rejected or changed]
```

Periodically review the log for patterns — if the same issue recurs across builds, the skill-creator's own instructions need updating.

---

## Reference Files

- `agents/grader.md` — Evaluating assertions against outputs
- `agents/comparator.md` — Blind A/B comparison
- `agents/analyzer.md` — Analyzing why one version beat another
- `references/schemas.md` — JSON schemas for evals.json, grading.json, benchmark.json, etc.
- `references/writing-guide.md` — Skill anatomy, progressive disclosure, writing patterns
- `references/env-adapters.md` — Environment-specific adaptations (Cowork, Claude.ai)
- `references/feedback-loop.md` — Post-deployment logging pattern for generated skills
- `references/readme-template.md` — README.md template to fill in per skill
- `references/auditing.md` — Architectural audit + post-ship performance audit
- `references/skill-development-principles.md` — 34 architectural principles for skill quality
- `agents/script-engineer.md` — Skill type classification + script design phase
- `references/script-patterns.md` — Eight token-efficiency patterns for skill scripts