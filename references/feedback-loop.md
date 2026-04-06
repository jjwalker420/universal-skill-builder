# Post-Deployment Feedback Loop Pattern

Every skill that produces recommendations or decisions should include this pattern.

## What to build into generated skills

### Log file: `decisions-log.md` (or `feedback-log.md`)

After the skill produces a recommendation or output, append a log entry:

```
## [Date] — [Mode]: [Brief Description]
Output: [What the skill produced]
User action: [PENDING]
Outcome: [PENDING — updated at next review]
```

When the user reports what they actually did ("I used it" / "I ignored it" / "I did something different"), update `User action` and eventually `Outcome`.

### Periodic review step (monthly or user-triggered)

Scan the log for:

- **Override patterns**: user ignores the same recommendation type 3+ times → surface this and suggest threshold recalibration
- **Stale outcomes**: entries older than 30 days with `PENDING` status → prompt user to update
- **Outcome quality**: when outcomes are logged, assess whether the skill's recommendation was good — what % led to positive outcomes

### Self-audit hook

In any skill mode that runs periodically (daily briefing, monthly review, etc.), include a hook that:
1. Checks for entries with `PENDING` status older than the review window
2. Reports the override rate for each recommendation type
3. Flags any mode that has been consistently overridden

### Automation evaluation

When writing a new skill, ask: can any of this skill's outputs be scheduled or automated? If yes, document the scheduling path (e.g., cron via Claude Code, scheduled agent, etc.) in the skill's README.md.
