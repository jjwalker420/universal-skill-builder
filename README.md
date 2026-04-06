# Universal Skill Builder

A multi-agent skill for Claude Code and Claude.ai that handles the full lifecycle
of building, testing, improving, auditing, and packaging Claude skills.

---

## What it does

| Mode | Trigger | What happens |
|------|---------|--------------|
| Create | "build a skill", "turn this into a skill" | Interview → write SKILL.md → generate evals → README |
| Evaluate | "test this skill", "run evals" | Spawn with-skill + baseline runs → eval viewer → feedback |
| Improve | "improve this skill", "iterate" | Apply feedback → rerun evals → confirm no regression |
| Optimize | "optimize this skill" | Compression pass → quality gate → cross-environment check |
| Audit | "audit this skill", "review this skill" | Score against 34 architectural principles → ranked fix list |
| Script Engineer | "add scripts to this skill" | Classify skill type → design scripts → token budget analysis |
| Package | "package this skill" | Validate → bundle into .skill file |

---

## What's included

```
universal-skill-builder/
├── SKILL.md                          — Main orchestrator
├── README.md                         — This file
├── agents/
│   ├── grader.md                     — Eval assertion grader
│   ├── comparator.md                 — Blind A/B comparison
│   ├── analyzer.md                   — Benchmark analysis
│   └── script-engineer.md            — Skill type classifier + script design
├── references/
│   ├── writing-guide.md              — Skill anatomy and writing patterns
│   ├── auditing.md                   — Architectural + post-ship audit framework
│   ├── skill-development-principles.md — 34 principles for skill quality
│   ├── script-patterns.md            — 8 token-efficiency patterns for scripts
│   ├── schemas.md                    — JSON schemas for evals, benchmarks, grading
│   ├── feedback-loop.md              — Post-deployment logging pattern
│   ├── env-adapters.md               — Claude Code vs Claude.ai adaptations
│   └── readme-template.md            — README template for generated skills
├── scripts/
│   ├── improve_description.py        — Description optimization loop
│   ├── run_loop.py                   — Eval iteration runner
│   ├── run_eval.py                   — Single eval runner
│   ├── aggregate_benchmark.py        — Benchmark aggregator
│   ├── generate_report.py            — Report generator
│   ├── package_skill.py              — Skill packager
│   ├── quick_validate.py             — Fast validation check
│   └── skill-templates/              — Reusable script templates
│       ├── web_scraper_optimized.py  — Filtered HTML extraction
│       ├── batch_api_caller.py       — Parallel batch execution
│       ├── incremental_runner.py     — Incremental run state tracking
│       └── structured_output.py     — JSON schema enforcement
├── assets/
│   └── eval_review.html             — Interactive eval review UI
└── eval-viewer/
    ├── generate_review.py            — Eval viewer server
    └── viewer.html                   — Eval viewer UI
```

---

## Requirements

- Claude Code (primary environment)
- Python 3.10+
- `pip3 install pyyaml` (required for packaging)
- `pip3 install beautifulsoup4 requests` (required for web scraper templates)

Also works in Claude.ai with reduced functionality (no script execution, no eval runner).
See `references/env-adapters.md` for environment-specific guidance.

---

## Quick start

**In Claude Code:**
```
build a skill that [describe what you want]
```

**To audit an existing skill:**
```
audit the [skill-name] skill
```

**To add script optimization to a data-heavy skill:**
```
add scripts to the [skill-name] skill
```

---

## The Script Engineer

Skills that retrieve external data (APIs, web pages, MCP sources) often burn far more
tokens than necessary. The Script Engineer agent classifies your skill into one of four
types and — for data-heavy skills — designs efficient scripts that move heavy lifting
out of the model and into code.

See `references/script-patterns.md` for the eight patterns it applies.

---

## The eval framework

USB includes a full evaluation framework: write test cases, spawn parallel with-skill
and baseline runs, grade assertions, view results in an interactive browser UI, and
track improvement across iterations. See `references/schemas.md` for data formats.

---

## License

MIT — use freely, modify, share, build on top of it.
If you improve it, consider sharing back.
