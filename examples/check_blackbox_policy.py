#!/usr/bin/env python3
"""Example policy gate for an Agent Blackbox run.json artifact.

Usage:
    python3 examples/check_blackbox_policy.py .agent-blackbox/latest/run.json

Exit codes are intentionally simple for CI experiments:
    0 = allow
    1 = review needed
    2 = block
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Keep the example runnable from a source checkout without installation.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent_blackbox.policy import decide_policy_file  # noqa: E402

EXIT_CODES = {"allow": 0, "review": 1, "block": 2}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 1:
        print("usage: check_blackbox_policy.py <path-to-run.json>", file=sys.stderr)
        return 2

    decision = decide_policy_file(argv[0])
    print(json.dumps(decision, indent=2))
    return EXIT_CODES[decision["decision"]]


if __name__ == "__main__":
    raise SystemExit(main())
