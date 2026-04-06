"""
Template: structured_output.py
Pattern: Strict Output Schema (Pattern 4)
Use this as a mixin/base for any script that needs schema enforcement.
Customize: define your own dataclasses, call validate_and_emit().
"""

import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class BaseOutput:
    """Extend this in your script. All script outputs must inherit from BaseOutput."""
    skill:      str
    fetched_at: str = field(default_factory=lambda: datetime.now().isoformat())
    ok:         bool = True
    error:      Optional[str] = None
    truncated:  bool = False


@dataclass
class ItemOutput(BaseOutput):
    """Example extension — replace 'items' with your actual fields."""
    items:       list[dict] = field(default_factory=list)
    total_items: int = 0


def validate_and_emit(output: BaseOutput) -> str:
    """
    Validate that required fields are present, then serialize to JSON.
    Call this at the end of every script's main() instead of print(json.dumps(...)).
    """
    data = asdict(output)

    required = ["skill", "fetched_at", "ok"]
    missing  = [k for k in required if k not in data or data[k] is None]
    if missing:
        error_output = {
            "skill":      getattr(output, "skill", "unknown"),
            "fetched_at": datetime.now().isoformat(),
            "ok":         False,
            "error":      f"Missing required fields: {missing}",
        }
        print(json.dumps(error_output, indent=2))
        sys.exit(1)

    serialized = json.dumps(data, indent=2, default=str)
    print(serialized)
    return serialized


def emit_error(skill: str, message: str):
    """Emit a well-formed error output and exit. Call when a script fails."""
    output = {
        "skill":      skill,
        "fetched_at": datetime.now().isoformat(),
        "ok":         False,
        "error":      message,
    }
    print(json.dumps(output, indent=2))
    sys.exit(1)


# --- EXAMPLE USAGE (remove in production scripts) ---
if __name__ == "__main__":
    result = ItemOutput(
        skill       = "example-skill",
        items       = [{"title": "Test item", "url": "https://example.com"}],
        total_items = 1,
    )
    validate_and_emit(result)
