
#!/usr/bin/env python3
"""Copy Experiment Lab - interactive prompt-driven copy generator."""
import json
import os
import textwrap
import time
from typing import Any, Dict, List, Sequence

import openai
import streamlit as st


try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except Exception:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY is not set. Set it in Streamlit secrets or environment variables.")
    st.stop()

openai.api_key = OPENAI_API_KEY


DEFAULT_ORIENTATION = textwrap.dedent(
    """
    【課題商品・サービスの訴求したいポイント】
    ルイボスとグリーンルイボスの2種の茶葉をブレンドし、ルイボスティーらしい豊かな香り立ちがありながら、すっきりとした飲みやすさを実現。クセのあるイメージのルイボスティーですが、すっきりゴクゴク飲める味わいです。アレルギー特定原材料等28品目不使用、カフェインゼロなのに、ルイボスティーの豊かな香りですっきりリフレッシュ。仕事中、食中食後、喉が渇いたときなどさまざまなシーンでおすすめです。

    【今回、募集する作品に期待すること】
    GREEN DA・KA・RA はやさしさを大事にした心とカラダにやさしいブランドです。数あるルイボスティーの中でも、GREEN DA・KA・RA やさしいルイボスを選びたくなる、やさしさのつまった表現アイディアを期待しています。

    【制作にあたっての注意事項】
    GREEN DA・KA・RA ブランドの愛嬌を大切にしながら表現を検討してください。今回のお題では、さまざまな生活シーンで水分補給をする20~30代男女をターゲットにします。ルイボスとグリーンルイボスの2種の茶葉をブレンドし、ルイボスティーらしい豊かな香り立ちがありながら、すっきりとした飲みやすさを実現。クセのあるイメージのルイボスティーですが、すっきりゴクゴク飲める味わいです。アレルギー特定原材料等28品目不使用、カフェインゼロなのに、ルイボスティーの豊かな香りですっきりリフレッシュ。仕事中、食中食後、喉が渇いたときなどさまざまなシーンでおすすめです。
    """
).strip()


PRESET_PROMPTS: Sequence[Dict[str, str]] = (
    {
        "label": "🎯 構造化生成",
        "prompt": textwrap.dedent(
            """
            生活者にとって新しい価値を発見できるwhat to say を２０案考えて、その上で二十個のコピーを作成せよ。

            ※『what to say』とは『メッセージは何か』あるいは、その企画を通して『何を残すのか』『何を持ち帰ってもらうのか』という意味です。
            """
        ).strip(),
    },
    {
        "label": "⚡ 強化・改善",
        "prompt": textwrap.dedent(
            """
            どれも広告的で心が動かない、もっと強いメッセージが必要。使い古された言い回しを使わずに、定型的な構文は避けて。二十個のコピーを考えて。
            """
        ).strip(),
    },
    {
        "label": "✨ 最終洗練",
        "prompt": textwrap.dedent(
            """
            最終的な二十個の案をそれぞれ意味が凝縮するように、短い言葉にリフレーズして。
            """
        ).strip(),
    },
    {
        "label": "🧠 インサイト抽出",
        "prompt": textwrap.dedent(
            """
            以下のコピー群から共通する洞察と改善すべきポイントを洗い出し、強みを活かした20個の新コピーを生成せよ。
            """
        ).strip(),
    },
)

DEFAULT_MODELS: Sequence[str] = (
    "gpt-5",
    "gpt-5-chat-latest",
    "gpt-5-mini",
    "gpt-4o",
    "gpt-4.1",
)


def log_console(label: str, message: str) -> None:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [{label}] {message}"
    print(formatted)
    st.session_state.execution_log.append(formatted)
    st.session_state.execution_log = st.session_state.execution_log[-200:]


def supports_json_mode(model: str) -> bool:
    lower = model.lower()
    return not (lower.startswith("o1-") or lower.startswith("o3-"))


def normalize_temperature(model: str, temperature: float) -> float:
    if model.lower().startswith("gpt-5"):
        return 1.0
    return temperature


def parse_json_response(response_text: str) -> Dict[str, Any]:
    if not isinstance(response_text, str):
        return {"copies": [], "error": "non_string_response"}
    try:
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            snippet = response_text[start:end].strip()
            return json.loads(snippet)
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {"copies": [], "error": "json_decode_failure", "raw_text": response_text}


def extract_copies_list(parsed: Dict[str, Any]) -> List[str]:
    copies: List[str] = []
    if not isinstance(parsed, dict):
        return copies
    value = parsed.get("copies")
    if isinstance(value, list):
        copies = [str(item) for item in value if str(item).strip()]
    elif isinstance(value, str):
        copies = [value]
    elif "results" in parsed and isinstance(parsed["results"], list):
        copies = [str(item) for item in parsed["results"] if str(item).strip()]
    return copies


def fallback_lines(text: str, copy_count: int) -> List[str]:
    lines: List[str] = []
    for line in text.splitlines():
        cleaned = line.strip().lstrip("-•0123456789. ")
        if cleaned:
            lines.append(cleaned)
    return lines[:copy_count]


BASE_SYSTEM_MESSAGE = textwrap.dedent(
    """You are a senior Japanese copywriter. Review the given context and craft memorable advertising copy.
    Write outputs in Japanese and focus on clarity, freshness, and brand fit."""
).strip()

STRICT_SCHEMA_TEMPLATE = textwrap.dedent(
    """Return exactly {copy_count} Japanese advertising copy lines.
    Output pure JSON only using this schema:
    {{
      "copies": ["copy1", ..., "copy{copy_count}"]
    }}
    No explanations, no additional keys."""
).strip()


def build_messages(orientation: str, prompt: str, copy_count: int) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": BASE_SYSTEM_MESSAGE},
        {"role": "system", "content": STRICT_SCHEMA_TEMPLATE.format(copy_count=copy_count)},
    ]
    sections: List[str] = []
    orientation = orientation.strip()
    prompt = prompt.strip()
    if orientation:
        sections.append(f"[Orientation]\n{orientation}")
    if prompt:
        sections.append(f"[Prompt]\n{prompt}")
    sections.append(
        f"[Output Requirement]\n日本語で{copy_count}件のキャッチコピーのみを生成し、JSON以外は出力しないこと。"
    )
    user_content = "\n\n".join(sections)
    messages.append({"role": "user", "content": user_content})
    return messages


def call_chat_completion(
    messages: List[Dict[str, str]],
    model: str,
    temperature: float,
    max_completion_tokens: int,
) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": normalize_temperature(model, temperature),
        "max_completion_tokens": max_completion_tokens,
    }
    if supports_json_mode(model):
        kwargs["response_format"] = {"type": "json_object"}
    response = openai.chat.completions.create(**kwargs)
    choice = response.choices[0]
    content = choice.message.content or ""
    used_model = getattr(response, "model", model)
    if not content.strip() and "response_format" in kwargs:
        log_console("retry", "Empty response with JSON mode. Retrying without response_format.")
        kwargs.pop("response_format", None)
        response = openai.chat.completions.create(**kwargs)
        choice = response.choices[0]
        content = choice.message.content or ""
        used_model = getattr(response, "model", model)
    return {"content": content, "used_model": used_model, "choice": choice}


def generate_copies(
    orientation: str,
    prompt: str,
    model: str,
    temperature: float,
    copy_count: int,
    max_completion_tokens: int,
) -> Dict[str, Any]:
    messages = build_messages(orientation, prompt, copy_count)
    log_console("prompt", f"Dispatching request to {model} (copy_count={copy_count})")
    result = call_chat_completion(messages, model, temperature, max_completion_tokens)
    content = result["content"]
    used_model = result["used_model"]

    if not content.strip() and model.lower().startswith("gpt-5"):
        log_console("warning", "GPT-5 returned an empty response. Falling back to gpt-4o.")
        fallback_result = call_chat_completion(messages, "gpt-4o", temperature, max_completion_tokens)
        content = fallback_result["content"]
        used_model = fallback_result["used_model"]

    parsed = parse_json_response(content)
    copies = extract_copies_list(parsed)
    if not copies:
        copies = fallback_lines(content, copy_count)
        parsed.setdefault("raw_text", content)
    else:
        parsed["raw_text"] = content

    return {
        "copies": copies,
        "raw_text": content,
        "parsed": parsed,
        "used_model": used_model,
        "messages": messages,
    }


def render_history(history: Sequence[Dict[str, Any]]) -> None:
    if not history:
        return
    st.subheader("履歴")
    for entry in reversed(history):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(entry["timestamp"]))
        header = f"{timestamp} / {entry['used_model']} / {len(entry['copies'])}本"
        with st.expander(header):
            st.markdown("#### Orientation")
            st.write(entry["orientation"] or "(なし)")
            st.markdown("#### Prompt")
            st.write(entry["prompt"] or "(なし)")
            st.markdown("#### Copies")
            if entry["copies"]:
                for idx, copy in enumerate(entry["copies"], start=1):
                    st.markdown(f"{idx}. {copy}")
            else:
                st.info("コピーが抽出できませんでした。RAWレスポンスを参照してください。")
            with st.expander("RAW Response"):
                st.code(entry["raw_text"] or "(empty)")


def main() -> None:
    st.set_page_config(page_title="Copy Experiment Lab", layout="wide")
    st.title("Copy Experiment Lab")
    st.caption("GPT-5を中心にプロンプトを試行錯誤するための実験用インターフェース")

    if "execution_log" not in st.session_state:
        st.session_state.execution_log = []
    if "prompt_area" not in st.session_state:
        st.session_state.prompt_area = PRESET_PROMPTS[0]["prompt"]
    if "orientation_area" not in st.session_state:
        st.session_state.orientation_area = DEFAULT_ORIENTATION
    if "history" not in st.session_state:
        st.session_state.history = []

    with st.sidebar:
        st.header("設定")
        model = st.selectbox("モデル", DEFAULT_MODELS, index=0)
        temperature = st.slider("Temperature", 0.0, 1.2, 1.0, 0.1)
        copy_count = st.slider("コピー数", 5, 30, 20, 1)
        max_completion_tokens = st.slider("max_completion_tokens", 500, 4000, 3000, 100)
        show_logs = st.checkbox("ログを表示", value=True)
        st.markdown("---")
        st.markdown("### プロンプトテンプレート")
        cols = st.columns(len(PRESET_PROMPTS))
        for col, preset in zip(cols, PRESET_PROMPTS):
            if col.button(preset["label"]):
                st.session_state.prompt_area = preset["prompt"]
                st.session_state["prompt_text_area"] = preset["prompt"]

    col_left, col_right = st.columns(2)
    with col_left:
        orientation = st.text_area(
            "オリエンテーション / 背景情報",
            value=st.session_state.orientation_area,
            key="orientation_text_area",
            height=260,
        )
        st.session_state.orientation_area = orientation
    with col_right:
        prompt_text = st.text_area(
            "プロンプト (テンプレートボタンで書き換え / 自由入力)",
            value=st.session_state.prompt_area,
            key="prompt_text_area",
            height=260,
        )
        st.session_state.prompt_area = prompt_text

    generate = st.button("コピーを生成", type="primary", use_container_width=True)

    if generate:
        if not prompt_text.strip():
            st.warning("プロンプトを入力してください。")
        else:
            with st.spinner("生成中..."):
                result = generate_copies(
                    orientation=orientation,
                    prompt=prompt_text,
                    model=model,
                    temperature=temperature,
                    copy_count=copy_count,
                    max_completion_tokens=max_completion_tokens,
                )
            copies = result["copies"]
            raw_text = result["raw_text"]
            used_model = result["used_model"]
            parsed = result["parsed"]

            if copies:
                st.success(f"{len(copies)}件のコピーを生成しました (使用モデル: {used_model})")
                st.markdown("### 生成結果")
                for idx, copy in enumerate(copies, start=1):
                    st.markdown(f"{idx}. {copy}")
            else:
                st.error("JSONからコピーを抽出できませんでした。RAWレスポンスを確認してください。")

            with st.expander("RAWレスポンス"):
                st.code(raw_text or "(empty)")

            st.download_button(
                label="結果をダウンロード",
                data="\n".join(copies) if copies else raw_text,
                file_name="copy_generation.txt",
                mime="text/plain",
            )

            st.session_state.history.append(
                {
                    "timestamp": time.time(),
                    "orientation": orientation,
                    "prompt": prompt_text,
                    "copies": copies,
                    "raw_text": raw_text,
                    "parsed": parsed,
                    "used_model": used_model,
                }
            )
            st.session_state.history = st.session_state.history[-20:]

    if show_logs and st.session_state.execution_log:
        with st.expander("ログ", expanded=False):
            st.code("\n".join(st.session_state.execution_log[-50:]))

    render_history(st.session_state.history)


if __name__ == "__main__":
    main()
