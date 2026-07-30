# universal-skill-builder

A Claude skill for building, testing, auditing, and shipping other Claude skills. It handles the full lifecycle — from capturing a workflow in conversation to packaging a production-ready `.skill` file.

## What It Does

Six modes covering the complete skill development lifecycle:

| Mode | What it does |
|---|---|
| **Create** | Interviews you (or captures a workflow from the current conversation) and writes a complete SKILL.md with evals and README |
| **Evaluate** | Runs test cases with-skill vs baseline using subagents, grades results, launches an interactive benchmark viewer |
| **Improve** | Reads eval feedback, applies targeted improvements, reruns evals to confirm progress |
| **Optimize** | Compression pass, redundancy scan, cross-environment test, quality gate check |
| **Audit** | Scores any skill against 34 architectural principles, checks if the skill should be split, produces a ranked fix list |
| **Package** | Bundles the skill into a `.skill` file for sharing or installation |

## Installation

Copy the `universal-skill-builder/` folder into your `.claude/skills/` directory.

```
cp -r universal-skill-builder/ ~/.claude/skills/universal-skill-builder/
```

**Requirements:**
- Python 3.10+ (for eval viewer, benchmarking, and packaging scripts)
- `pyyaml` (`pip install pyyaml`) — only needed for packaging

**Works in:** Claude Code, Cowork, and Claude.ai (with reduced functionality — no subagents or description optimization in Claude.ai).

## Usage

Just tell Claude what you need. The skill triggers on natural language:

- "Build a skill" / "Create a skill for X"
- "Turn this into a skill" / "Make a skill from what we just did"
- "Test this skill" / "Run evals"
- "Audit this skill" / "Is this skill doing too much?"
- "Optimize this description"
- "Package this skill"

### Creating from a conversation

If you've been working through a workflow with Claude and want to capture it as a reusable skill, just say "turn this into a skill." The skill-creator will scan the conversation, extract the repeatable pattern, and draft a skill based on what actually happened — then confirm with you before filling in any gaps.

### Auditing an existing skill

Point it at any installed skill and say "audit this skill." It scores all 34 development principles, checks whether the skill is trying to do too much, and gives you a ranked fix list. If you approve fixes, it runs the full improvement loop: Audit → Evaluate → Improve → Optimize → Package.

## File Structure

```
universal-skill-builder/
├── SKILL.md                          # Core engine — mode routing, steps, guardrails
├── README.md                         # This file
├── agents/
│   ├── grader.md                     # Subagent instructions for grading eval outputs
│   ├── comparator.md                 # Blind A/B comparison between skill versions
│   └── analyzer.md                   # Post-comparison analysis
├── scripts/
│   ├── quick_validate.py             # Fast validation check for skill structure
│   ├── aggregate_benchmark.py        # Aggregates eval runs into benchmark.json
│   ├── generate_report.py            # Generates benchmark reports
│   ├── improve_description.py        # AI-powered description optimization
│   ├── run_eval.py                   # Runs a single eval
│   ├── run_loop.py                   # Description optimization loop
│   ├── package_skill.py              # Packages skill into .skill file
│   └── utils.py                      # Shared utilities
├── assets/
│   └── eval_review.html              # Interactive eval review template
├── eval-viewer/
│   ├── generate_review.py            # Generates interactive HTML review pages
│   └── viewer.html                   # Benchmark viewer template
└── references/
    ├── writing-guide.md              # Skill anatomy, progressive disclosure, writing style
    ├── schemas.md                    # JSON schemas for evals, grading, benchmarks
    ├── env-adapters.md               # Environment-specific adaptations
    ├── feedback-loop.md              # Post-deployment logging pattern
    ├── readme-template.md            # README template for generated skills
    ├── auditing.md                   # Architectural + post-ship audit protocols
    └── skill-development-principles.md  # 34 principles used for scoring
```

## Design Principles

The skill is built on 34 development principles covering file architecture, conciseness, environment awareness, self-learning, automation, and build process. These same principles are used when auditing other skills. See `references/skill-development-principles.md` for the full list.

## License

MIT
