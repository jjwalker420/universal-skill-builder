"""
Template: batch_api_caller.py
Pattern: Parallel Batch Execution (Pattern 7) + Strict Output Schema (Pattern 4)
Customize: TASKS list, fetch_one() function, OUTPUT_PATH
"""

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Any

# --- CUSTOMIZE THESE ---
OUTPUT_PATH = os.path.expanduser("~/.claude/skill-cache/batch_output.json")
MAX_WORKERS = 5
MAX_CALLS   = 10

# Define your tasks — each dict is passed to fetch_one()
TASKS: list[dict] = [
    {"source": "source_a", "params": {}},
    {"source": "source_b", "params": {}},
    {"source": "source_c", "params": {}},
]
# --- END CUSTOMIZE ---


def fetch_one(task: dict) -> dict:
    """Replace this with your actual API call logic."""
    source = task["source"]
    # params = task["params"]
    # result = your_api_client.call(source, **params)
    # return {"source": source, "data": result, "ok": True}
    raise NotImplementedError(f"fetch_one not implemented for source: {source}")


def run_batch(tasks: list[dict]) -> list[dict]:
    results: list[dict] = []
    capped = tasks[:MAX_CALLS]
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_one, t): t for t in capped}
        for future in as_completed(futures):
            task = futures[future]
            try:
                results.append(future.result())
            except Exception as e:
                results.append({
                    "source": task.get("source", "unknown"),
                    "ok":     False,
                    "error":  str(e),
                })
    return results


def build_output(results: list[dict]) -> dict:
    succeeded = [r for r in results if r.get("ok", False)]
    failed    = [r for r in results if not r.get("ok", True)]
    return {
        "fetched_at":    datetime.now().isoformat(),
        "total_tasks":   len(results),
        "succeeded":     len(succeeded),
        "failed":        len(failed),
        "results":       results,
        "failed_sources": [r.get("source") for r in failed],
    }


def main():
    if not TASKS:
        print(json.dumps({"error": "no tasks defined"}))
        sys.exit(1)

    results = run_batch(TASKS)
    output  = build_output(results)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
