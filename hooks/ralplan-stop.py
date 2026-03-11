#!/usr/bin/env python3
"""Prevent ralplan from stopping before completion."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

PROJECT_DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
STATE_PATH = PROJECT_DIR / ".claude" / "ralplan" / "state.json"

NEXT_STEP_BY_STAGE = {
    "init": "ralplan has started and must initialize flags or move into planner.",
    "awaiting-flags": "ralplan is waiting for interactive/deliberate choices. Ask the user and continue.",
    "planner": "ralplan must finish the Planner draft before stopping.",
    "interactive-draft-gate": "ralplan must resolve the draft review checkpoint before stopping.",
    "architect": "ralplan must finish the Architect review before stopping.",
    "critic": "ralplan must finish the Critic review before stopping.",
    "revision-loop": "ralplan must run the next revision loop before stopping.",
    "interactive-final-gate": "ralplan must resolve the final approval checkpoint before stopping.",
    "final-output": "ralplan must deliver the final plan output and mark itself completed before stopping.",
}


def emit(payload: dict) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))


if not STATE_PATH.exists():
    emit({"decision": "approve", "reason": "ralplan state file not found"})
    raise SystemExit(0)

try:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
except Exception as exc:  # pragma: no cover
    emit({"decision": "approve", "reason": f"failed to read ralplan state: {exc}"})
    raise SystemExit(0)

if state.get("active") is not True:
    emit({"decision": "approve", "reason": "ralplan state is not active"})
    raise SystemExit(0)

stage = state.get("stage")
if stage == "completed":
    emit({"decision": "approve", "reason": "ralplan flow already completed"})
    raise SystemExit(0)

message = NEXT_STEP_BY_STAGE.get(stage, "ralplan is still active and must reach completed before stopping.")
emit({"decision": "block", "reason": f"ralplan is active at stage '{stage}'. {message}"})
raise SystemExit(0)
