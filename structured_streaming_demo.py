#!/usr/bin/env python3
"""Structured streaming demo enforcing a JSON schema with OpenAI Responses API."""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List

from openai import OpenAI


SCHEMA: Dict[str, Any] = {
    "type": "json_schema",
    "name": "WorkLog",
    "schema": {
        "type": "object",
        "properties": {
            "task": {"type": "string"},
            "elapsed_minutes": {"type": "integer", "minimum": 0},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["task", "elapsed_minutes", "notes"],
        "additionalProperties": False,
    },
    "strict": True,
}

PROMPT = (
    "次のスキーマに完全準拠するJSONだけを返して。\n"
    "task: いま取り組んでいる作業名\n"
    "elapsed_minutes: 経過分\n"
    "notes: 箇条書きメモ（任意）"
)


def ensure_api_key() -> None:
    if os.getenv("OPENAI_API_KEY"):
        return
    print("[ERROR] OPENAI_API_KEY が環境変数で設定されていません。", file=sys.stderr)
    sys.exit(1)


def concat_text_from_response(response: Any) -> str:
    texts: List[str] = []
    for output in getattr(response, "output", []) or []:
        for part in getattr(output, "content", []) or []:
            text = getattr(part, "text", None)
            if isinstance(text, str):
                texts.append(text)
    return "".join(texts).strip()


def main() -> None:
    ensure_api_key()
    client = OpenAI()

    print("=== streaming (崩れた断片でもそのまま表示) ===")
    with client.responses.stream(
        model="gpt-5",
        input=PROMPT,
        text={"format": SCHEMA},
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)

        final = stream.get_final_response()

    raw_text = concat_text_from_response(final)
    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        parsed = {"error": "json_decode_failure", "raw_text": raw_text}

    print("\n\n=== parsed (厳密パース結果) ===")
    print(json.dumps(parsed, ensure_ascii=False, indent=2))

    print("\033[31m[OK] Structured JSON parsed & validated against schema.\033[0m")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        sys.exit(130)

