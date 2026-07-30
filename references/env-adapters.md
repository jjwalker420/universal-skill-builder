# Environment Adapters

## Tool Priority (all environments)

When multiple paths exist to accomplish something, prefer the most reliable: **dedicated tool/MCP first → computer use second → manual/ask user third.** For example: read a file with the Read tool, not by screenshotting it. Search the web with web search, not by navigating Chrome. Use computer use only for things like opening the eval viewer HTML or interacting with native apps.

## Data Sources by Environment

| Data | Claude Code | Cowork | Claude.ai |
|---|---|---|---|
| Skill files | Local filesystem | Mounted folder | User uploads |
| Eval results | Local workspace | Mounted workspace | Filesystem (VM) |
| Web research | Web search tool | Web search tool | Web search tool |
| MCP data | Local stdio/HTTP servers | Cloud MCP connectors | Cloud MCP connectors |
| User feedback | feedback.json (local) | feedback.json (download) | Inline conversation |

If a data source isn't available in the current environment, design the fallback (upload, MCP pull, or "not available here").

---

## Cowork

**What works:** Subagents, parallel test runs, grading, aggregation — the full workflow applies. If timeouts are severe, run test prompts in series.

**No display:** Use `--static <output_path>` with the eval viewer to write standalone HTML. Proffer a link for the user to open it. Do NOT write custom HTML — use `generate_review.py`.

**Computer use:** Cowork has computer-use access. Use it to open eval viewer HTML files, take screenshots of outputs for comparison, or interact with apps the skill-under-test needs.

**Feedback collection:** The viewer's "Submit All Reviews" downloads `feedback.json` as a file. You may need to request file access.

**Description optimization:** `run_loop.py` / `run_eval.py` work (uses `claude -p` via subprocess). Save until the skill is fully finished.

**Updating an existing skill:** Preserve the original name. Copy to `/tmp/skill-name/` before editing — installed paths may be read-only.

---

## Claude.ai

No subagents — mechanics change:

**Running test cases:** Execute each test prompt yourself, one at a time. Skip baseline runs. Less rigorous (you wrote and run the skill), but the human review step compensates.

**Reviewing results:** Present results directly in conversation — show prompt + output per test case. For file outputs (.docx, .xlsx), save to filesystem and tell the user where to download. Ask for feedback inline.

**Benchmarking:** Skip quantitative benchmarking — no meaningful baselines without subagents. Focus on qualitative feedback.

**Description optimization:** Requires `claude -p` (Claude Code only). Skip on Claude.ai.

**Blind comparison:** Requires subagents. Skip.

**Updating an existing skill:** Preserve the original name and `name` frontmatter field. Copy to `/tmp/skill-name/` before editing. Stage in `/tmp/` first, then copy to output directory.
