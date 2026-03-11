#!/usr/bin/env python3
"""Inject resume context for unfinished ralplan sessions."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

PROJECT_DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
STATE_PATH = PROJECT_DIR / ".claude" / "ralplan" / "state.json"

NEXT_STEP_BY_STAGE = {
    "init": "Initialize missing flags and then continue into Planner.",
    "awaiting-flags": "Ask the user for any missing interactive/deliberate flags before continuing.",
    "planner": "Continue with the Planner stage and produce the draft plan.",
    "interactive-draft-gate": "Resume the draft review checkpoint and resolve the user's choice.",
    "architect": "Resume with the Architect review, then proceed to Critic.",
    "critic": "Resume with the Critic review and determine whether iteration is required.",
    "revision-loop": "Resume the revision loop: update the plan, rerun Architect, then rerun Critic.",
    "interactive-final-gate": "Resume the final approval checkpoint and collect the user's execution choice.",
    "final-output": "Deliver the final plan or handoff and then mark the workflow completed.",
}


def emit(payload: dict) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))


if not STATE_PATH.exists():
    emit({})
    raise SystemExit(0)

try:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
except Exception as exc:  # pragma: no cover
    emit({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": f"ralplan state exists but could not be read: {exc}"}})
    raise SystemExit(0)

if state.get("active") is not True:
    emit({})
    raise SystemExit(0)

stage = state.get("stage") or "unknown"
summary = state.get("task_summary") or "(no task summary)"
iteration = state.get("iteration", 0)
next_step = NEXT_STEP_BY_STAGE.get(stage, "Resume the remaining ralplan steps until the state reaches completed.")

emit({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": (
            "Unfinished ralplan workflow detected. "
            f"Task: {summary}. Current stage: {stage}. Iteration: {iteration}. "
            f"Next required step: {next_step}"
        ),
    }
})
raise SystemExit(0)
