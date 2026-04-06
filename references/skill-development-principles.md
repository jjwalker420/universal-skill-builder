# Skill Development Principles
*34 principles for building high-quality Claude skills. Use as a scoring rubric and design checklist.*

Tier tags: `[ALL]` = applies to all skills. `[STD+]` = Standard and Complex only. `[CPLX]` = Complex only. See `references/auditing.md` Step 0 for tier classification.

---

## File Architecture

1. **Single file, single job.** `[ALL]` Every .md has one purpose. If you're tempted to put two things in one file, you need two files.
2. **Five-file max for v1.** `[STD+]` SKILL.md (engine), one frameworks/rules file, one tool-references file, one output-templates file, one data/state file. Add files only when a clear single-responsibility demands it.
3. **SKILL.md is the engine.** `[STD+]` It contains modes, steps, and routing. It references other files — it never duplicates their content.
4. **Static reference vs temporal state.** `[STD+]` Frameworks, guardrails, and tool docs are static (change rarely). Snapshots, logs, and dashboards are temporal (change often). Never mix them in the same file.
5. **Zero cross-file redundancy.** `[STD+]` If data exists in one file, other files point to it. Duplicated tables across files are a maintenance liability and a token cost.

## Conciseness

6. **Every line loads every message.** `[ALL]` Project instructions, CLAUDE.md, and skill files consume context on every interaction. A 300-line file that could be 80 lines wastes 220 lines of tokens on every single message.
7. **Draft → compress → compress again.** `[ALL]` First draft captures all ideas. Second pass cuts duplication and obvious-to-Claude instructions. Third pass asks "does this line change Claude's behavior?" If no, cut it.
8. **Don't instruct Claude on default behavior.** `[ALL]` "Summarize concisely" in upload handling, "use proper formatting" — Claude does this. Only instruct on behavior that deviates from defaults.
9. **Tables over prose for structured routing.** `[STD+]` A routing table (user says X → do Y) orients Claude in 2 seconds. The same info as paragraphs takes 20 seconds.
10. **No stale data in instructions.** `[ALL]` Financial figures, account balances, project status — anything that changes monthly or faster does NOT belong in project instructions. Use a pull-on-demand protocol: Claude asks for the file or pulls from MCP.

## Environment Awareness

11. **Three environments, different capabilities.** `[STD+]` Chat (claude.ai): MCP connectors + web search, no local files, artifacts render inline. Cowork: local file access + MCP connectors + computer use, best for operational runs. Claude Code: local files + local MCP servers (stdio/HTTP), best for dev tooling.
12. **Design data flows per environment.** `[CPLX]` Before building any feature, answer: where does the input come from in each environment? If Chat can't access a data source, design the fallback (upload protocol, MCP pull, or "not available in Chat").
13. **Build in one environment, test in another.** `[CPLX]` Design and edit skill files in Chat → test operationally in Cowork/Code → bring feedback back to Chat for patches.
14. **Cross-environment prompts need verification steps.** `[CPLX]` When one environment generates a prompt for another, always include 2-3 verification checks so the user can confirm changes landed correctly.

## Self-Learning

15. **Every skill should ship with a feedback loop.** `[STD+]` At minimum: a log file that records what the skill recommended and what actually happened, and a periodic self-audit step that reviews outcomes and proposes improvements.
16. **The loop: recommend → log → outcome → audit → propose → approve.** `[STD+]` The skill proposes changes. The user approves or rejects. Never auto-apply structural changes.
17. **Override patterns are signal.** `[CPLX]` If the user overrides the same recommendation type 3+ times, the threshold is wrong. The skill should detect this and suggest recalibration.

## Automation

18. **Default to "set it and forget it."** `[STD+]` Every feature evaluated: can this run on a schedule without the user touching it? If yes, that's the default design.
19. **Computer use expands Cowork's reach.** `[CPLX]` Cowork can start local servers, open apps, navigate UIs. Always consider this when designing workflows that previously required Claude Code.
20. **MCP first, computer use second, manual third.** `[STD+]` When multiple paths exist, always prefer the most reliable automated path.

## Skill Design Patterns

21. **Modes are the top-level routing unit.** `[STD+]` Each mode handles one category of user intent. Modes have sequential steps. Steps reference framework files for heavy logic.
22. **Step 0 loads context. Always.** `[ALL]` Every skill run starts by loading the minimum required files. Use conditional loading — don't read everything every time.
23. **Output templates live in their own file.** `[STD+]` Separating templates from logic lets you iterate on presentation without touching the engine.
24. **Guardrails are non-negotiable rules.** `[ALL]` They live in SKILL.md as a standalone section, enforced across all modes regardless of context window state. They're the one acceptable duplication — also kept in project instructions as a fallback.
25. **Watchlist/feedback patterns.** `[CPLX]` When one mode produces research or recommendations, other modes should read that output. This creates compounding value across modes.

## Project Structure

26. **R&D folder in Chat, operational in Cowork.** `[CPLX]` Every skill project gets a Chat project for design work and a Cowork project (or the same project accessed via Cowork) for live runs.
27. **CLAUDE.md is the router.** `[CPLX]` Minimal — routing logic, file update rules, data priority table. It tells Claude where to look, not what to do.
28. **Project instructions are the cold-start context.** `[CPLX]` They load every message, so they must be lean. They orient Claude on role, routing, tone, and the minimum reference data needed for the current environment.
29. **README.md for the human.** `[STD+]` Prompts, guidelines, troubleshooting, and roadmap. This is for the user, not for Claude's runtime. Don't put it in project instructions.
30. **Handoff docs for session continuity.** `[CPLX]` At the end of a major build session, produce a handoff .md capturing: what was built, what files changed, known issues, and how to continue. Upload it to start the next session cold.

## Build Process

31. **Phase-based development.** `[STD+]` Infrastructure → data → skill logic → optimization audit → visual layer. Each phase has clear completion criteria before moving on.
32. **Test with live data before shipping.** `[ALL]` Run a full end-to-end test with real data before calling a skill production-ready. No skill ships without this.
33. **Optimization is a dedicated phase, not an afterthought.** `[STD+]` A proper optimization audit routinely cuts SKILL.md line count by 30-50% while maintaining or adding functionality. Schedule this explicitly.
34. **v1 should be minimal and correct, not feature-complete.** `[ALL]` Ship the core modes, prove they work, then iterate. The roadmap exists because v1 shipped without trying to do everything.
