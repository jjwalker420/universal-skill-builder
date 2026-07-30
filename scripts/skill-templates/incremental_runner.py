"""
Template: incremental_runner.py
Pattern: Incremental Runs (Pattern 6) + Stop Conditions (Pattern 5)
Customize: SKILL_NAME, STATE_FILE, MAX_NEW_ITEMS, fetch_new_items()
"""

import json
import os
import sys
from datetime import datetime
from typing import Optional

# --- CUSTOMIZE THESE ---
SKILL_NAME    = "my-skill"          # used in state file path
MAX_NEW_ITEMS = 50                  # hard ceiling on items processed per run
# --- END CUSTOMIZE ---

STATE_DIR  = os.path.expanduser("~/.claude/skill-state")
STATE_FILE = os.path.join(STATE_DIR, f"{SKILL_NAME}.json")


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "last_run":      None,
        "last_id":       None,
        "total_fetched": 0,
    }


def save_state(state: dict):
    os.makedirs(STATE_DIR, exist_ok=True)
    state["last_run"] = datetime.now().isoformat()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def fetch_new_items(since_id: Optional[str]) -> list[dict]:
    """
    Replace with your actual fetch logic.
    Should return only items newer than since_id.
    Items must each have an 'id' field for state tracking.
    """
    raise NotImplementedError("fetch_new_items not implemented")


def build_output(new_items: list[dict], state: dict, truncated: bool) -> dict:
    return {
        "skill":         SKILL_NAME,
        "run_at":        datetime.now().isoformat(),
        "previous_run":  state.get("last_run"),
        "new_items":     new_items,
        "new_count":     len(new_items),
        "total_fetched": state.get("total_fetched", 0) + len(new_items),
        "truncated":     truncated,
    }


def main():
    state     = load_state()
    since_id  = state.get("last_id")

    raw_items = fetch_new_items(since_id)

    truncated = len(raw_items) > MAX_NEW_ITEMS
    new_items = raw_items[:MAX_NEW_ITEMS]

    output = build_output(new_items, state, truncated)

    if new_items:
        state["last_id"]       = new_items[0].get("id")
        state["total_fetched"] = output["total_fetched"]
        save_state(state)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
