"""Small, explainable policy decisions for Agent Blackbox run artifacts.

This is intentionally a review helper, not a sandbox or prevention engine.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BLOCKING_HINTS = {"secrets_hint", "destructive_hint"}
REVIEW_HINTS = {"file_write", "stderr_output", "network_hint"}


def decide_policy(run: dict[str, Any]) -> dict[str, Any]:
    """Return an allow/review/block decision for a run.json-like dict."""
    hints = set(run.get("risk_hints") or [])
    reasons: list[str] = []

    blocking = sorted(hints & BLOCKING_HINTS)
    if blocking:
        return {
            "decision": "block",
            "reasons": [f"blocking risk hint: {hint}" for hint in blocking],
        }

    review = sorted(hints & REVIEW_HINTS)
    reasons.extend(f"review risk hint: {hint}" for hint in review)

    if run.get("exit_code") not in (0, None):
        reasons.append(f"wrapped command exited with {run.get('exit_code')}")

    if reasons:
        return {"decision": "review", "reasons": reasons}

    return {"decision": "allow", "reasons": ["no configured risk hints and exit_code is 0"]}


def decide_policy_file(path: str | Path) -> dict[str, Any]:
    """Load an Agent Blackbox run.json file and decide allow/review/block."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    decision = decide_policy(data)
    return {
        "schema": "agent-blackbox.policy-decision.v1",
        "run_id": data.get("run_id"),
        "decision": decision["decision"],
        "reasons": decision["reasons"],
    }
