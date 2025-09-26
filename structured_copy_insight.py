#!/usr/bin/env python3
"""Generate a top copy insight from a monologue with progress streaming."""

from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from openai import OpenAI


RESULT_SCHEMA: Dict[str, Any] = {
    "type": "json_schema",
    "name": "CopyTopline",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "top_copy": {"type": "string"},
        },
        "required": ["top_copy"],
        "additionalProperties": False,
    },
}


PROMPT_TEMPLATE = textwrap.dedent(
    '''
    あなたは独白から未言語化の洞察を抽出し、核心を突くコピーを作るコピーライターである。
    以下を内部で思考し、最終的には top_copy に最適な1案のみを JSON で返すこと。

    - 5 Whys で根本課題を掘り下げる。
    - JTBD仮説を10案検討し、価値の焦点を見極める。
    - ラダリングで価値階層を確認し、候補コピーを磨く。
    - 最終的に、最も刺さる1案を top_copy に格納する。

    返答は JSON オブジェクト以外出力しないこと。

    独白:
    """{monologue}"""
    '''
).strip()


PROGRESS_PROMPT_TEMPLATE = textwrap.dedent(
    '''
    あなたはメインモデルと同じコピー洞察タスクを進める `gpt-5-mini` です。
    実況はすべてユーザー向けの外向き説明として書き、内部独白は禁止です。
    5 Whys、JTBD仮説10案、ラダリング、最終案選定を行いながら、思いつきや気づきを短い文で次々に書き出してください。

    出力スタイル指示:
    - 謝罪・ポリシー言及・「出せません」といった断り文句は書かない。必ずブレインストームのメモを書き続ける。
    - 「ユーザーは」「なぜ1」などの機械的ラベルや説明調の書き方を避け、自分の頭の中で転がしている言葉として自然に語る。
    - 箇条書き、行頭記号、または「案A」「ん？」「これだと…」のような人間らしい書き出しを用いる。
    - 各行は1～2文を書いたらすぐ改行して次に進み、テンポ良く書き進める。
    - 最低50行以上のメモを書き、同じ語尾やフレーズをできるだけ避ける。
    - 途中で思考が揺れたり矛盾したりしてもよい。推敲せず、そのまま書く。
    - 最終コピーやJSONなど結論そのものは出力しない。
    - 思考を終えたら最後に「（ブレインストーミング終了）」とだけ記す。

    独白:
    """{monologue}"""
    '''
).strip()


def ensure_api_key() -> None:
    if os.getenv("OPENAI_API_KEY"):
        return
    print("[ERROR] OPENAI_API_KEY が環境変数で設定されていません。", file=sys.stderr)
    sys.exit(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Structured copy insight generator")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose モードでプロンプトやレスポンスを表示",
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="進行状況ストリーミングを無効化",
    )
    return parser


def read_monologue(verbose: bool) -> str:
    if verbose:
        print("[DEBUG] 独白入力待ち", flush=True)
    print("独白を入力してください。入力終了時は空行で確定します。", flush=True)
    lines: List[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line.strip() and lines:
            break
        if not line.strip() and not lines:
            continue
        lines.append(line)
    monologue = "\n".join(lines).strip()
    if verbose:
        print("[DEBUG] 入力された独白:\n" + monologue)
    if not monologue:
        print("[ERROR] 独白が入力されませんでした。", file=sys.stderr)
        sys.exit(1)
    return monologue


def extract_json_from_response(response: Any, verbose: bool) -> Dict[str, Any]:
    if verbose:
        print("[DEBUG] レスポンスオブジェクト:")
        print(response)
    payload: str = ""
    for output in response.output or []:
        content_list = getattr(output, "content", None) or []
        for content in content_list:
            if getattr(content, "type", None) == "output_text":
                payload += content.text
    payload = payload.strip()
    if verbose:
        print("[DEBUG] モデルからの生テキスト:\n" + payload)
    if not payload:
        raise RuntimeError("モデルからテキスト出力を取得できませんでした。")
    return json.loads(payload)


def stream_progress(monologue: str, verbose: bool) -> None:
    client = OpenAI()
    prompt = PROGRESS_PROMPT_TEMPLATE.format(monologue=monologue)
    if verbose:
        print("[DEBUG] 進捗ストリーム開始")
    try:
        with client.responses.stream(
            model="gpt-5-mini",
            input=prompt,
        ) as stream:
            for event in stream:
                if event.type == "response.output_text.delta":
                    print(event.delta, end="", flush=True)
    except Exception as exc:  # pragma: no cover
        if verbose:
            print(f"\n[DEBUG] 進捗ストリームエラー: {exc}", file=sys.stderr)
    finally:
        print()
        if verbose:
            print("[DEBUG] 進捗ストリーム終了")


def build_markdown(data: Dict[str, Any]) -> str:
    top_copy = data.get("top_copy", "")
    lines: List[str] = ["# Copy Insight Report", "", "## Top Copy", top_copy]
    return "\n".join(lines).strip() + "\n"


def save_markdown(content: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = Path(f"copy_insight_{timestamp}.md")
    path.write_text(content, encoding="utf-8")
    return path


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    verbose = bool(args.verbose)
    enable_progress = not bool(args.no_progress)

    ensure_api_key()
    monologue = read_monologue(verbose)

    client = OpenAI()
    prompt = PROMPT_TEMPLATE.format(monologue=monologue)

    if verbose:
        print("[DEBUG] 最終プロンプト:\n" + prompt)

    progress_thread: threading.Thread | None = None
    if enable_progress:
        progress_thread = threading.Thread(
            target=stream_progress,
            args=(monologue, verbose),
            daemon=True,
        )
        progress_thread.start()

    response = client.responses.create(
        model="gpt-5",
        input=prompt,
        text={"format": RESULT_SCHEMA},
    )

    if progress_thread is not None:
        progress_thread.join()

    parsed = extract_json_from_response(response, verbose)
    markdown = build_markdown(parsed)
    output_path = save_markdown(markdown)

    print("=== JSON ===")
    print(json.dumps(parsed, ensure_ascii=False, indent=2))
    print("\n=== Markdown Preview ===")
    print(markdown)
    print(f"[OK] Markdown saved to {output_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] 中断されました。", file=sys.stderr)
        sys.exit(130)

