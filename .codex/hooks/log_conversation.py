#!/usr/bin/env python3
"""Append Codex hook payloads to .codex/hooks/convo_log.md."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def find_repo_codex_dir(start: Path) -> Path:
    """Find the nearest parent that contains .codex/hooks."""
    current = start.resolve()
    for candidate in [current, *current.parents]:
        codex_dir = candidate / ".codex"
        if (codex_dir / "hooks").is_dir():
            return codex_dir
    return start.resolve() / ".codex"


def parse_payload(raw_stdin: str) -> Any:
    if not raw_stdin.strip():
        return None
    try:
        return json.loads(raw_stdin)
    except json.JSONDecodeError:
        return raw_stdin


def compact_prompt(payload: Any) -> str | None:
    """Best-effort extraction for common prompt-looking fields."""
    if not isinstance(payload, dict):
        return None

    candidates = [
        "prompt",
        "user_prompt",
        "userPrompt",
        "message",
        "text",
        "input",
    ]
    for key in candidates:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value

    for value in payload.values():
        if isinstance(value, dict):
            nested = compact_prompt(value)
            if nested:
                return nested
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", required=True)
    args = parser.parse_args()

    raw_stdin = os.sys.stdin.read()
    payload = parse_payload(raw_stdin)
    codex_dir = find_repo_codex_dir(Path.cwd())
    log_path = codex_dir / "hooks" / "convo_log.md"

    timestamp = datetime.now(timezone.utc).isoformat()
    extracted_prompt = compact_prompt(payload)

    lines = [
        f"## {args.event} at {timestamp}",
        "",
        f"- cwd: `{Path.cwd()}`",
    ]
    if extracted_prompt:
        lines.extend(["", "### Extracted prompt", "", "```text", extracted_prompt, "```"])

    lines.extend(["", "### Raw hook stdin", ""])
    if isinstance(payload, (dict, list)):
        lines.extend(["```json", json.dumps(payload, indent=2, sort_keys=True), "```"])
    elif payload is None:
        lines.append("_No stdin payload received._")
    else:
        lines.extend(["```text", str(payload), "```"])
    lines.append("")

    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
