# coding: utf-8
"""Command-line pipeline runner for GPT-5 copy generation.

This script replaces the Streamlit interface with a deterministic
workflow that exercises the end-to-end functionality:

1. Lists available models and confirms GPT-5 access.
2. Runs the three staged generation prompts.
3. Performs feedback-based refinement on a sample split.
4. Applies How-to-Say refinement to the latest copies.
5. Executes a custom prompt and a lightweight idea generator.

The goal is to help quickly verify that the underlying logic works
without relying on manual UI operations.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import textwrap
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

import openai


DEFAULT_ORIENTATION = textwrap.dedent(
    """[課題商品・サービスの訴求したいポイント]\n"""
    "ルイボスとグリーンルイボスの2種の茶葉をブレンドし、ルイボスティーらしい豊かな香り立ちがありながら、すっきりとした飲みやすさを実現。クセのあるイメージのルイボスティーですが、すっきりゴクゴク飲める味わいです。アレルギー特定原材料等28品目不使用、カフェインゼロなのに、ルイボスティーの豊かな香りですっきりリフレッシュ。仕事中、食中食後、喉が渇いたときなどさまざまなシーンでおすすめです。\n\n"
    "[今回、募集する作品に期待すること]\n"
    "GREEN DA・KA・RA はやさしさを大事にした心とカラダにやさしいブランドです。数あるルイボスティーの中でも、GREEN DA・KA・RA やさしいルイボスを選びたくなる、やさしさのつまった表現アイディアを期待しています。\n\n"
    "[制作にあたっての注意事項]\n"
    "GREEN DA・KA・RA ブランドの愛嬌を大切にしながら表現を検討してください。今回のお題では、さまざまな生活シーンで水分補給をする20~30代男女をターゲットにします。ルイボスとグリーンルイボスの2種の茶葉をブレンドし、ルイボスティーらしい豊かな香り立ちがありながら、すっきりとした飲みやすさを実現。クセのあるイメージのルイボスティーですが、すっきりゴクゴク飲める味わいです。アレルギー特定原材料等28品目不使用、カフェインゼロなのに、ルイボスティーの豊かな香りですっきりリフレッシュ。仕事中、食中食後、喉が渇いたときなどさまざまなシーンでおすすめです。GREEN DA・KA・RAブランドの愛嬌を大切にしながら表現を検討してください。"
)


STAGED_PROMPTS: List[Dict[str, Any]] = [
    {
        "stage": 1,
        "title": "🎯 構造化生成",
        "prompt": "生活者にとって新しい価値を発見できるwhat to say を２０案考えて、その上で二十個のコピーを作成せよ。\n\n※「what to say」とは「メッセージは何か」あるいは、その企画を通して「何を残すのか」「何を持ち帰ってもらうのか」という意味です。",
    },
    {
        "stage": 2,
        "title": "⚡ 強化・改善",
        "prompt": "どれも広告的で心が動かない、もっと強いメッセージが必要。使い古された言い回しを使わずに、定型的な構文は避けて。二十個のコピーを考えて",
    },
    {
        "stage": 3,
        "title": "✨ 最終洗練",
        "prompt": "最終的な二十個の案をそれぞれ意味が凝縮するように、短い言葉にリフレーズして",
    },
]


HOW_TO_SAY_TYPES: List[Dict[str, Any]] = [
    {
        "type": 1,
        "name": "意外なファクトに基づいて発見を与える",
        "examples": [
            "落書きをやめると、成績は下がる。",
            "セックスにもソックスを。足元を暖めると、オルガズムに達しやすくなる。",
            "日本語では、事故で亡くなる。海外ではkillという。",
        ],
    },
    {
        "type": 2,
        "name": "建前を放棄して本音を語る",
        "examples": ["また売れなかったらどうしよう", "広告規制により、サンマを持たされています"],
    },
    {
        "type": 3,
        "name": "商品価値を最大化して、社会における意味を語る",
        "examples": [
            "ロケットも、文房具から生まれた。",
            "英語を話せると、10億人と話せる",
            "地図に残る仕事。（建設会社のコピー）",
        ],
    },
    {
        "type": 4,
        "name": "数え方を工夫してみる",
        "examples": ["日本で４７番目に有名な県", "四十歳は２度目のハタチ。", "１億使っても、まだ２億。"],
    },
    {
        "type": 5,
        "name": "物事を捉える視点を変えてみる",
        "examples": [
            "ぼくのお父さんは、桃太郎というやつに殺されました。（鬼視点）",
            "おしりだって洗ってほしい（身体視点）",
            "太陽から見れば、日本には広大な空き地が広がっている（太陽視点）",
        ],
    },
    {
        "type": 6,
        "name": "新しい二項対立を作ってみる",
        "examples": ["ゴリマッチョ。細マッチョ。", "ひたパン、つけパン", "権力より、愛だね"],
    },
    {
        "type": 7,
        "name": "商品がないことによる不便を描く",
        "examples": [
            "部長の山本はまもなく戻りますので、そこに座ってろ。（英会話のコピー）",
            "今、この男のカバンの中では、 水筒のお茶がめちゃくちゃ漏れている。",
        ],
    },
    {
        "type": 8,
        "name": "ほっこりするシーンを切り取る",
        "examples": ["金魚の便秘なおる。（水族館のコピー）", "もう一回またがってから寝よ。（バイクのコピー）", "スキップしちゃった。（コージーコーナーのコピー）"],
    },
    {
        "type": 9,
        "name": "企業名を人の名前のように使う",
        "examples": ["なぜつばさを使わないんだ。あなたの資産もそうです。つばさ証券", "楽天カードマン", "新しい英雄、始まる。au"],
    },
    {
        "type": 10,
        "name": "その時代ならではの社会課題を語る",
        "examples": [
            "同性を好きになるのは、じつは左利きと同じくらいいる。",
            "年をとるだけで、劣化と呼ばれる時代を生きている。",
            "日本初の女性総理は、きっともう、この世にいる。",
        ],
    },
    {
        "type": 11,
        "name": "納得できる世の中の法則を伝える",
        "examples": [
            "お母さんを育てるのは、赤ちゃんです。",
            "花を育てるようになると雨が好きになる",
            "試着室で思い出したら、本気の恋だと思う。",
            "着物を着ている日は、すこし丁寧に生きている。",
        ],
    },
    {
        "type": 12,
        "name": "心の声やつぶやきをコピーにする",
        "examples": ["私だけ、美人だったら、いいのに。", "そうだ 京都、いこう。", "つまらん！"],
    },
    {
        "type": 13,
        "name": "ターゲットが共感できる想いを代弁してあげる",
        "examples": [
            "知名度だけが一流の会社で働くより、知名度だけが二流の会社で働きたい。",
            "結婚しなくても幸せになれるこの時代に 私は、あなたと結婚したいのです。",
            "１年が過ぎるのは早いが、１日はなかなか終わらない。",
        ],
    },
    {
        "type": 14,
        "name": "自虐的に自分自身を語る",
        "examples": ["ここは、日本一心の距離が遠いサファリパーク", "スイてます嵐山", "その程度の機能ならドンキで十分だ！"],
    },
    {
        "type": 15,
        "name": "ダジャレにしてみる",
        "examples": ["バザールでござーる", "でっかいどお。北海道", "ナイフのようなナイーブ。", "あしたのもと 味の素", "カラダにピース。カルピス"],
    },
    {
        "type": 16,
        "name": "成分のように表現してみる",
        "examples": ["バファリンの半分はやさしさでできてます。", "おいしいものは、脂肪と糖でできている", "世界は誰かの仕事でできている"],
    },
    {
        "type": 17,
        "name": "価値を再定義する",
        "examples": [
            "年賀状は、贈り物だと思う。",
            "戦争を４度も経験したジーンズ（古着のコピー）",
            "チョコが義理なら、アメは人情。",
            "映画は、本当のことを言う嘘だ。",
        ],
    },
    {
        "type": 18,
        "name": "効果を伝える",
        "examples": ["倒れるだけで腹筋", "吸引力が変わらないただ一つの掃除機", "ある日、日経は顔に出る"],
    },
    {
        "type": 19,
        "name": "ライバルに喧嘩を売る",
        "examples": ["マヨネーズよ。真似すんなよ。（ケチャップのコピー）", "現金って、奇妙なモノを持ち歩いているもんだ（クレジットカードのコピー）"],
    },
    {
        "type": 20,
        "name": "常識をひっくり返してみる",
        "examples": ["地味ハロウィン", "抽選で１名をハズレとする", "健康がブームになるなんて、異常だ。"],
    },
]


def ensure_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Export it before running this script.")
    return api_key


def supports_json_mode(model: str) -> bool:
    lower = model.lower()
    return not (lower.startswith("o1-") or lower.startswith("o3-"))


def normalize_temperature(model: str, temperature: float) -> float:
    if model.lower().startswith("gpt-5"):
        return 1.0
    return temperature


def parse_json_response(response_text: str) -> Dict[str, Any]:
    try:
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            json_text = response_text[start:end].strip()
        elif "{" in response_text and "}" in response_text:
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            json_text = response_text[start:end]
        else:
            json_text = response_text
        return json.loads(json_text)
    except json.JSONDecodeError:
        return {"copies": [response_text], "error": "json_decode_failure"}


def extract_copies_list(parsed: Dict[str, Any]) -> List[str]:
    copies: List[str] = []
    if not isinstance(parsed, dict):
        return copies
    if "error" in parsed:
        return copies
    if "copies" in parsed:
        value = parsed["copies"]
        if isinstance(value, list):
            copies = [str(item) for item in value]
        else:
            copies = [str(value)]
    elif "results" in parsed:
        value = parsed["results"]
        if isinstance(value, list):
            copies = [str(item) for item in value]
        else:
            copies = [str(value)]
    elif "refinements" in parsed:
        refinements = parsed["refinements"]
        for item in refinements:
            copy = item.get("copy")
            if copy:
                copies.append(str(copy))
    return copies


def format_numbered(items: Sequence[str]) -> str:
    return "\n".join(f"{idx+1}. {text}" for idx, text in enumerate(items))


def load_conversation_history(path: Optional[str]) -> List[Dict[str, str]]:
    if not path:
        return []
    if not os.path.exists(path):
        raise FileNotFoundError(f"Conversation history CSV '{path}' not found.")
    messages: List[Dict[str, str]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            side = row.get("side", "")
            prompt = (row.get("prompt") or "").strip()
            if not prompt:
                continue
            role = "user" if side == "human" else "assistant"
            messages.append({"role": role, "content": prompt})
    return messages


@dataclass
class CopyPipelineRunner:
    orientation: str
    model: str = "gpt-5"
    temperature: float = 0.9
    history_csv: Optional[str] = None
    client: Any = field(init=False)
    conversation_history: List[Dict[str, str]] = field(init=False)

    def __post_init__(self) -> None:
        api_key = ensure_api_key()
        openai.api_key = api_key
        self.client = openai
        self.conversation_history = load_conversation_history(self.history_csv)
        self.temperature = normalize_temperature(self.model, self.temperature)

    # ---- API wrappers -------------------------------------------------

    def get_available_models(self) -> List[str]:
        models = self.client.models.list()
        model_ids = [item.id for item in models.data]
        return sorted(model_ids, reverse=True)

    def run_chat_completion(
        self,
        messages: List[Dict[str, str]],
        *,
        max_tokens: int = 3000,
        response_format: Optional[Dict[str, str]] = None,
    ) -> str:
        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "max_completion_tokens": max_tokens,
            "temperature": self.temperature,
        }
        if response_format:
            kwargs["response_format"] = response_format
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content

    def run_response_api(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            reasoning={"effort": "high"},
        )
        return response.choices[0].message.content

    # ---- Generation steps --------------------------------------------

    def run_stage(self, stage_prompt: str) -> Tuple[str, Dict[str, Any]]:
        base_system_message = {
            "role": "system",
            "content": textwrap.dedent(
                """You are a senior copywriter.
Review the prior conversation and generate the requested copy.
Respond in Japanese.
"""
            ),
        }

        strict_json_instruction = {
            "role": "system",
            "content": textwrap.dedent(
                """Return exactly 20 Japanese advertising copy lines.
Output pure JSON only in this schema:
{
  "copies": ["copy1", "copy2", ..., "copy20"]
}
No prose, no explanations, no extra keys.
"""
            ),
        }

        user_message = {
            "role": "user",
            "content": f"{self.orientation}\n\n{stage_prompt}",
        }

        messages = [base_system_message]
        if self.model.lower().startswith("gpt-5"):
            messages.append(strict_json_instruction)
        messages.extend(self.conversation_history)
        messages.append(user_message)
        try:
            content = self.run_chat_completion(
                messages,
                response_format={"type": "json_object"},
            )
        except Exception as e:
            print(f"API Error in run_stage: {e}")
            content = self.run_chat_completion(messages)

        # Raw response logging for debugging
        print(f"--- RAW RESPONSE (first 500 chars) ---")
        print(content[:500] if content else "EMPTY RESPONSE")
        print("--- END RAW RESPONSE ---")

        parsed = parse_json_response(content)
        copies = extract_copies_list(parsed)

        if not copies:
            # GPT-5が失敗した場合、GPT-4oでフォールバック
            if self.model.lower().startswith("gpt-5"):
                print("GPT-5 failed with empty response, falling back to GPT-4o")
                fallback_model = "gpt-4o"
                fallback_temperature = normalize_temperature(fallback_model, self.temperature)
                try:
                    content = self.client.chat.completions.create(
                        model=fallback_model,
                        messages=messages,
                        max_completion_tokens=3000,
                        temperature=fallback_temperature,
                        response_format={"type": "json_object"},
                    ).choices[0].message.content
                except Exception:
                    content = self.client.chat.completions.create(
                        model=fallback_model,
                        messages=messages,
                        max_completion_tokens=3000,
                        temperature=fallback_temperature,
                    ).choices[0].message.content

                # Raw response logging for debugging
                print(f"--- RAW RESPONSE (GPT-4o fallback, first 500 chars) ---")
                print(content[:500] if content else "EMPTY RESPONSE")
                print("--- END RAW RESPONSE ---")

                parsed = parse_json_response(content)
                copies = extract_copies_list(parsed)

            if not copies:
                fallback = []
                for line in content.splitlines():
                    cleaned = line.strip().lstrip("-•1234567890. ")
                    if cleaned:
                        fallback.append(cleaned)
                copies = fallback[:20]
                parsed = {"copies": copies, "raw_text": content}
            else:
                parsed["raw_text"] = content
        else:
            parsed["raw_text"] = content

        if len(copies) < 1:
            print("Warning: Stage generation returned no copies; continuing with raw output.")

        return format_numbered(copies), parsed

    def run_feedback(self, good: List[str], bad: List[str]) -> Dict[str, Any]:
        prompt_lines: List[str] = [
            "【ユーザーフィードバック分析】",
            "",
            "良いコピー:",
        ]
        prompt_lines.extend(f"✅ {c}" for c in good)
        prompt_lines.append("")
        prompt_lines.append("悪いコピー:")
        prompt_lines.extend(f"❌ {c}" for c in bad)
        prompt_lines.append("")
        prompt_lines.append("上記を分析し、JSONで分析と20件の改善コピーを返してください。")
        prompt = "\n".join(prompt_lines)
        system_message = {
            "role": "system",
            "content": textwrap.dedent(
                "You are a senior copywriter.\n"
                "Analyze the provided feedback, identify what the user values, and generate 20 improved copies.\n"
                "Return strictly in JSON using this schema:\n"
                "{\n"
                "  \"analysis\": \"...\",\n"
                "  \"insights\": [\"...\"],\n"
                "  \"copies\": [\"...\"]\n"
                "}\n"
            ),
        }
        user_message = {"role": "user", "content": prompt}
        messages = [system_message] + self.conversation_history + [user_message]
        try:
            content = self.run_chat_completion(messages, response_format={"type": "json_object"})
        except Exception:
            content = self.run_chat_completion(messages)
        parsed = parse_json_response(content)
        copies = extract_copies_list(parsed)

        if len(copies) < 3:
            try:
                raw = json.loads(content)
                copies = extract_copies_list(raw)
                parsed = raw
            except json.JSONDecodeError:
                fallback = []
                for line in content.splitlines():
                    cleaned = line.strip().lstrip("-•1234567890. ")
                    if cleaned:
                        fallback.append(cleaned)
                copies = fallback[:20]
                parsed = {"copies": copies, "raw_text": content}
        else:
            parsed["raw_text"] = content

        if len(copies) < 1:
            print("Warning: Feedback refinement returned no copies; continuing with raw output.")
        return parsed

    def run_how_to_say(self, copies: List[str]) -> Dict[str, Any]:
        detail_lines: List[str] = []
        for item in HOW_TO_SAY_TYPES:
            detail_lines.append(f"Type {item['type']}: {item['name']}")
            example_line = ", ".join(item["examples"])
            detail_lines.append(f"Examples: {example_line}")
            detail_lines.append("")
        how_to_say_details = "\n".join(detail_lines).strip()
        prompt_lines = [
            "Analyze the following copies and refine each using the most suitable How to Say pattern.",
            "",
            "[Orientation]",
            self.orientation,
            "",
            "[Copies]",
            format_numbered(copies),
            "",
            "[How to Say Patterns]",
            how_to_say_details,
            "",
            "Return JSON only.",
        ]
        prompt = "\n".join(prompt_lines)
        system_message = {
            "role": "system",
            "content": (
                "You are a senior copywriter.\n"
                "Refine each copy using the best-fitting How to Say pattern.\n"
                "Output JSON with this structure:\n"
                "{\n"
                "  \"refinements\": [\n"
                "    {\n"
                "      \"original\": \"...\",\n"
                "      \"type\": \"Pattern Name\",\n"
                "      \"copy\": \"Refined Copy\",\n"
                "      \"reason\": \"Why this pattern fits\"\n"
                "    }\n"
                "  ]\n"
                "}\n"
            ),
        }
        messages = [system_message, {"role": "user", "content": prompt}]
        try:
            content = self.run_chat_completion(messages, response_format={"type": "json_object"})
        except Exception:
            content = self.run_chat_completion(messages)
        parsed = parse_json_response(content)
        copies_out = extract_copies_list(parsed)

        if len(copies_out) < 3:
            try:
                raw = json.loads(content)
                copies_out = extract_copies_list(raw)
                parsed = raw
            except json.JSONDecodeError:
                fallback = []
                for line in content.splitlines():
                    cleaned = line.strip().lstrip("-•1234567890. ")
                    if cleaned:
                        fallback.append(cleaned)
                copies_out = fallback[:20]
                parsed = {"copies": copies_out, "raw_text": content}
        else:
            parsed["raw_text"] = content

        if len(copies_out) < 1:
            print("Warning: How-to-Say refinement returned no copies; continuing with raw output.")
        return parsed

    def run_custom(self, custom_prompt: str) -> Dict[str, Any]:
        system_message = {
            "role": "system",
            "content": (
                "You are a senior copywriter.\n"
                "Follow the custom instructions and return copies only.\n"
                "Respond using JSON with a top-level \"copies\" array."
            ),
        }
        user_message = {
            "role": "user",
            "content": f"{self.orientation}\n\n{custom_prompt}\n\nJSON以外の情報は不要です。",
        }
        messages = [system_message] + self.conversation_history + [user_message]
        content = self.run_chat_completion(messages, response_format={"type": "json_object"})
        parsed = parse_json_response(content)
        copies = extract_copies_list(parsed)
        if not copies:
            raise RuntimeError("Custom prompt returned no copies.")
        return parsed

    def run_copy_ideas(self, num_ideas: int = 5) -> str:
        system_message = {
            "role": "system",
            "content": (
                "You are a senior copywriter.\n"
                "Produce impactful, memorable copies using the provided orientation.\n"
                "Return exactly the requested number of copy lines."
            ),
        }
        user_message = {
            "role": "user",
            "content": f"{self.orientation}\n\n最終的に{num_ideas}個の厳選されたキャッチコピーを出力してください。",
        }
        messages = [system_message] + self.conversation_history + [user_message]
        content = self.run_chat_completion(messages, max_tokens=1200)
        return content.strip()

    # ---- Composite flows ---------------------------------------------

    def run_full_check(self) -> None:
        print("[1/7] Listing available models ...", flush=True)
        models = self.get_available_models()
        if self.model not in models:
            raise RuntimeError(f"Model '{self.model}' is not available. Found {len(models)} models.")
        print(f"        Found {len(models)} models. Using: {self.model}")

        stage_results: List[Dict[str, Any]] = []
        for stage in STAGED_PROMPTS:
            print(f"[{stage['stage']+1}/7] Running stage {stage['stage']} - {stage['title']} ...", flush=True)
            formatted, parsed = self.run_stage(stage["prompt"])
            copies = extract_copies_list(parsed)
            if copies:
                print("        Sample copy:", copies[0])
            else:
                print("        (No copies returned; see raw output)")
            stage_results.append(parsed)

        latest_copies = extract_copies_list(stage_results[-1])
        good = latest_copies[:min(5, len(latest_copies)//2 or 5)]
        bad = latest_copies[-min(5, len(latest_copies)//2 or 5):]

        print("[5/7] Running feedback refinement ...", flush=True)
        feedback_parsed = self.run_feedback(good, bad)
        print("        Feedback insights count:", len(feedback_parsed.get("insights", [])))

        print("[6/7] Running How-to-Say refinement ...", flush=True)
        how_to_say_parsed = self.run_how_to_say(latest_copies)
        print("        Refinements generated:", len(how_to_say_parsed.get("refinements", [])))

        print("[7/7] Running custom prompt + copy ideas ...", flush=True)
        custom_parsed = self.run_custom("ブランドのやさしさを働く30代に向けて表現してください。")
        print("        Custom copies count:", len(extract_copies_list(custom_parsed)))

        ideas_text = self.run_copy_ideas()
        idea_lines = [line for line in ideas_text.splitlines() if line.strip()]
        print("        Idea lines:", len(idea_lines))

        print("\nAll checks completed successfully.")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run GPT-5 copy generation pipeline checks.")
    parser.add_argument("--orientation-file", help="Path to a text file containing the orientation text.")
    parser.add_argument("--model", default="gpt-5", help="Model ID to use. Default: gpt-5")
    parser.add_argument("--temperature", type=float, default=0.9, help="Sampling temperature (will be clamped for GPT-5)")
    parser.add_argument("--history-csv", help="Optional CSV with previous conversation history (columns: side,prompt)")
    return parser.parse_args(argv)


def load_orientation(path: Optional[str]) -> str:
    if not path:
        return DEFAULT_ORIENTATION
    if not os.path.exists(path):
        raise FileNotFoundError(f"Orientation file '{path}' not found.")
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def main(argv: Sequence[str]) -> None:
    args = parse_args(argv)
    orientation = load_orientation(args.orientation_file)
    runner = CopyPipelineRunner(
        orientation=orientation,
        model=args.model,
        temperature=args.temperature,
        history_csv=args.history_csv,
    )
    runner.run_full_check()


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

