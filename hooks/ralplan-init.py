#!/usr/bin/env python3
"""Initialize ralplan state when the skill is invoked."""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
STATE_DIR = PROJECT_DIR / ".claude" / "ralplan"
STATE_FILE = STATE_DIR / "state.json"
SKILL_PATTERN = re.compile(r"/(?:[A-Za-z0-9:_-]+:)?ralplan\b")
INTERACTIVE_PATTERN = re.compile(r"--interactive\b")
DELIBERATE_PATTERN = re.compile(r"--deliberate\b")


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_optional_flag(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "on"}:
            return True
        if lowered in {"0", "false", "no", "off"}:
            return False
    return None


def read_payload() -> dict[str, Any]:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def build_state(payload: dict[str, Any]) -> dict[str, Any] | None:
    prompt = payload.get("prompt") or payload.get("userPrompt") or ""
    if not isinstance(prompt, str) or not SKILL_PATTERN.search(prompt):
        return None

    interactive = normalize_optional_flag(os.environ.get("RALPLAN_INTERACTIVE"))
    deliberate = normalize_optional_flag(os.environ.get("RALPLAN_DELIBERATE"))

    if interactive is None and INTERACTIVE_PATTERN.search(prompt):
        interactive = True
    if deliberate is None and DELIBERATE_PATTERN.search(prompt):
        deliberate = True

    stage = os.environ.get("RALPLAN_STAGE")
    if not stage:
        stage = "init"

    iteration_raw = os.environ.get("RALPLAN_ITERATION")
    try:
        iteration = max(0, int(iteration_raw)) if iteration_raw is not None else 0
    except ValueError:
        iteration = 0

    session_id = str(payload.get("session_id") or payload.get("sessionId") or os.environ.get("CLAUDE_SESSION_ID") or "")

    return {
        "active": os.environ.get("RALPLAN_ACTIVE", "true").lower() == "true",
        "stage": stage,
        "interactive": interactive,
        "deliberate": deliberate,
        "iteration": iteration,
        "task_summary": prompt.strip(),
        "session_id": session_id,
        "updated_at": iso_now(),
    }


def main() -> int:
    payload = read_payload()
    state = build_state(payload)
    if state is None:
        json.dump({}, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    json.dump({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": f"Initialized ralplan state at {STATE_FILE}. Current stage: {state['stage']}."}}, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
