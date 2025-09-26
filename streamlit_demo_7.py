#!/usr/bin/env python3
"""
コピージェネレーター - v6（demo_5のUI + demo_3の高品質プロンプト）
demo_5の優れたUI機能とdemo_3の実績のある高品質なプロンプトを組み合わせたバージョン
"""

import streamlit as st
import openai
import pandas as pd
from typing import List, Dict, Tuple
import os
import json
import time

# APIキー設定（Streamlit Secrets対応）
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except:
    # ローカル開発時は環境変数から取得
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-proj-your-api-key-here")


def log_console(label: str, message: str) -> None:
    formatted = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [{label}] {message}"
    print(formatted)
    if 'execution_log' not in st.session_state:
        st.session_state.execution_log = []
    st.session_state.execution_log.append(formatted)
    st.session_state.execution_log = st.session_state.execution_log[-100:]

# 段階的生成用のプロンプト定義（demo_3のシンプルで高品質なプロンプト）
STAGED_PROMPTS = [
    {
        "stage": 1,
        "title": "🎯 構造化生成",
        "prompt": "生活者にとって新しい価値を発見できるwhat to say を２０案考えて、その上で二十個のコピーを作成せよ。\n\n※「what to say」とは「メッセージは何か」あるいは、その企画を通して「何を残すのか」「何を持ち帰ってもらうのか」という意味です。",
        "description": "20個のwhat to sayと20個のコピーを作成"
    },
    {
        "stage": 2,
        "title": "⚡ 強化・改善",
        "prompt": "どれも広告的で心が動かない、もっと強いメッセージが必要。使い古された言い回しを使わずに、定型的な構文は避けて。二十個のコピーを考えて",
        "description": "より強いメッセージに改善します"
    },
    {
        "stage": 3,
        "title": "✨ 最終洗練",
        "prompt": "最終的な二十個の案をそれぞれ意味が凝縮するように、短い言葉にリフレーズして",
        "description": "意味を凝縮した短いフレーズに最終調整"
    }
]

# 各段階をブロック形式に変換（demo_5のUIとの互換性のため）
COPY_BLOCKS = [
    {
        "id": f"stage_{prompt['stage']}",
        "title": prompt['title'],
        "prompt": prompt['prompt']
    } for prompt in STAGED_PROMPTS
]

# HOW TO SAY 型定義
HOW_TO_SAY_TYPES = [
    {
        "type": 1,
        "name": "意外なファクトに基づいて発見を与える",
        "examples": ["落書きをやめると、成績は下がる。", "セックスにもソックスを。足元を暖めると、オルガズムに達しやすくなる。", "日本語では、事故で亡くなる。海外ではkillという。"]
    },
    {
        "type": 2,
        "name": "建前を放棄して本音を語る",
        "examples": ["また売れなかったらどうしよう", "広告規制により、サンマを持たされています"]
    },
    {
        "type": 3,
        "name": "商品価値を最大化して、社会における意味を語る",
        "examples": ["ロケットも、文房具から生まれた。", "英語を話せると、10億人と話せる", "地図に残る仕事。（建設会社のコピー）"]
    },
    {
        "type": 4,
        "name": "数え方を工夫してみる",
        "examples": ["日本で４７番目に有名な県", "四十歳は２度目のハタチ。", "１億使っても、まだ２億。"]
    },
    {
        "type": 5,
        "name": "物事を捉える視点を変えてみる",
        "examples": ["ぼくのお父さんは、桃太郎というやつに殺されました。（鬼視点）", "おしりだって洗ってほしい（身体視点）", "太陽から見れば、日本には広大な空き地が広がっている（太陽視点）"]
    },
    {
        "type": 6,
        "name": "新しい二項対立を作ってみる",
        "examples": ["ゴリマッチョ。細マッチョ。", "ひたパン、つけパン", "権力より、愛だね"]
    },
    {
        "type": 7,
        "name": "商品がないことによる不便を描く",
        "examples": ["部長の山本はまもなく戻りますので、そこに座ってろ。（英会話のコピー）", "今、この男のカバンの中では、 水筒のお茶がめちゃくちゃ漏れている。"]
    },
    {
        "type": 8,
        "name": "ほっこりするシーンを切り取る",
        "examples": ["金魚の便秘なおる。（水族館のコピー）", "もう一回またがってから寝よ。（バイクのコピー）", "スキップしちゃった。（コージーコーナーのコピー）"]
    },
    {
        "type": 9,
        "name": "企業名を人の名前のように使う",
        "examples": ["なぜつばさを使わないんだ。あなたの資産もそうです。つばさ証券", "楽天カードマン", "新しい英雄、始まる。au"]
    },
    {
        "type": 10,
        "name": "その時代ならではの社会課題を語る",
        "examples": ["同性を好きになるのは、じつは左利きと同じくらいいる。", "年をとるだけで、劣化と呼ばれる時代を生きている。", "日本初の女性総理は、きっともう、この世にいる。"]
    },
    {
        "type": 11,
        "name": "納得できる世の中の法則を伝える",
        "examples": ["お母さんを育てるのは、赤ちゃんです。", "花を育てるようになると雨が好きになる", "試着室で思い出したら、本気の恋だと思う。", "着物を着ている日は、すこし丁寧に生きている。"]
    },
    {
        "type": 12,
        "name": "心の声やつぶやきをコピーにする",
        "examples": ["私だけ、美人だったら、いいのに。", "そうだ　京都、いこう。", "つまらん！"]
    },
    {
        "type": 13,
        "name": "ターゲットが共感できる想いを代弁してあげる",
        "examples": ["知名度だけが一流の会社で働くより、知名度だけが二流の会社で働きたい。", "結婚しなくても幸せになれるこの時代に　私は、あなたと結婚したいのです。", "１年が過ぎるのは早いが、１日はなかなか終わらない。"]
    },
    {
        "type": 14,
        "name": "自虐的に自分自身を語る",
        "examples": ["ここは、日本一心の距離が遠いサファリパーク", "スイてます嵐山", "その程度の機能ならドンキで十分だ！"]
    },
    {
        "type": 15,
        "name": "ダジャレにしてみる",
        "examples": ["バザールでござーる", "でっかいどお。北海道", "ナイフのようなナイーブ。", "あしたのもと 味の素", "カラダにピース。カルピス"]
    },
    {
        "type": 16,
        "name": "成分のように表現してみる",
        "examples": ["バファリンの半分はやさしさでできてます。", "おいしいものは、脂肪と糖でできている", "世界は誰かの仕事でできている"]
    },
    {
        "type": 17,
        "name": "価値を再定義する",
        "examples": ["年賀状は、贈り物だと思う。", "戦争を４度も経験したジーンズ（古着のコピー）", "チョコが義理なら、アメは人情。", "映画は、本当のことを言う嘘だ。"]
    },
    {
        "type": 18,
        "name": "効果を伝える",
        "examples": ["倒れるだけで腹筋", "吸引力が変わらないただ一つの掃除機", "ある日、日経は顔に出る"]
    },
    {
        "type": 19,
        "name": "ライバルに喧嘩を売る",
        "examples": ["マヨネーズよ。真似すんなよ。（ケチャップのコピー）", "現金って、奇妙なモノを持ち歩いているもんだ（クレジットカードのコピー）"]
    },
    {
        "type": 20,
        "name": "常識をひっくり返してみる",
        "examples": ["地味ハロウィン", "抽選で１名をハズレとする", "健康がブームになるなんて、異常だ。"]
    }
]

def get_available_models() -> List[str]:
    """利用可能なOpenAIモデル一覧を取得"""
    try:
        openai.api_key = OPENAI_API_KEY
        models = openai.models.list()
        # GPTモデルのみをフィルタリング（チャット用）
        gpt_models = []
        for model in models.data:
            model_id = model.id
            if any(prefix in model_id.lower() for prefix in ['gpt-', 'o1-', 'o3-']):
                gpt_models.append(model_id)
        
        # ソートして返す
        return sorted(gpt_models, reverse=True)
    except Exception as e:
        st.sidebar.error(f"モデル取得エラー: {str(e)}")
        # デフォルトモデルリストを返す
        return get_default_models()

def get_default_models() -> List[str]:
    """デフォルトモデルリスト"""
    return [
        "gpt-5",
        "gpt-5-chat-latest",
        "gpt-5-mini"
    ]

def get_model_categories() -> Dict[str, Dict]:
    """モデル情報をカテゴリ別に整理"""
    return {
        "🔥 次世代GPT-5モデル（推奨）": {
            "gpt-5": {
                "price": "価格未公開",
                "description": "🔥 最新GPT-5（最高品質・多用途）",
                "use_case": "最高品質のコピー生成",
                "recommended": True,
                "note": "✅ Chat Completions API対応 (高精度)"
            },
            "gpt-5-chat-latest": {
                "price": "価格未公開",
                "description": "🆕 GPT-5 Chat最新版（継続アップデート）",
                "use_case": "最新機能・迅速な改善反映",
                "recommended": True,
                "note": "✅ 常に最新の安定チャットモデル"
            },
            "gpt-5-mini": {
                "price": "$1.00/$4.00",
                "description": "⚡ GPT-5軽量版（高速・低コスト）",
                "use_case": "大量処理やアイデアブレスト",
                "recommended": True,
                "note": "✅ Chat Completions API対応 (コスト効率重視)"
            },
            "gpt-5-nano": {
                "price": "$0.35/$1.40",
                "description": "💨 GPT-5ナノ版（超高速・バッチ処理向け）",
                "use_case": "プロトタイピング、A/Bテスト",
                "recommended": False,
                "note": "ℹ️ 軽量版・最小コスト"
            }
        },
        "🎯 GPT-4シリーズ": {
            "gpt-4o": {
                "price": "$2.50/$10",
                "description": "🎯 最新GPT-4（バランス型・安定）",
                "use_case": "一般的なコピー生成",
                "recommended": True,
                "note": "✅ Chat Completions API対応 (全パラメータ)"
            },
            "gpt-4o-mini": {
                "price": "$0.15/$0.60",
                "description": "💨 軽量版GPT-4（高速・低コスト）",
                "use_case": "大量処理、高速生成",
                "recommended": True,
                "note": "✅ Chat Completions API対応 (全パラメータ)"
            },
            "gpt-4.1": {
                "price": "価格未公開",
                "description": "🆕 次世代GPT（ベータ版）",
                "use_case": "最新機能のテスト",
                "recommended": False,
                "note": "⚠️ ベータ版・要検証"
            }
        }
    }

def display_model_selector() -> Tuple[str, str]:
    """モデル選択UIを表示"""
    st.sidebar.header("🤖 AIモデル設定")
    
    # 利用可能なモデルを取得
    available_models = get_available_models()
    model_categories = get_model_categories()
    
    # モデル選択方式を選ぶ
    selection_mode = st.sidebar.radio(
        "選択方式",
        ["カテゴリ別選択", "全モデル一覧"],
        help="推奨はカテゴリ別選択です"
    )
    
    selected_model = None
    model_info = ""
    
    if selection_mode == "カテゴリ別選択":
        # カテゴリ別選択
        st.sidebar.markdown("### 📋 モデルカテゴリ")
        
        for category, models in model_categories.items():
            with st.sidebar.expander(category, expanded=True):
                for model_id, model_data in models.items():
                    if model_id in available_models:
                        # 推奨マークを追加
                        display_name = f"⭐ {model_id}" if model_data.get('recommended') else model_id
                        
                        if st.button(
                            f"{display_name}",
                            key=f"select_{model_id}",
                            help=f"{model_data['description']}\n価格: {model_data['price']}\n用途: {model_data['use_case']}"
                        ):
                            selected_model = model_id
                            model_info = model_data['description']
                            st.session_state.selected_model = model_id
                            st.session_state.model_info = model_info
        
        # セッション状態から現在のモデルを取得
        if 'selected_model' in st.session_state:
            selected_model = st.session_state.selected_model
            model_info = st.session_state.get('model_info', '')
        else:
            # デフォルト選択
            if "gpt-5" in available_models:
                selected_model = "gpt-5"
                model_info = "🔥 最新GPT-5（最高品質・多用途）"
            elif "gpt-5-chat-latest" in available_models:
                selected_model = "gpt-5-chat-latest"
                model_info = "🆕 GPT-5 Chat最新版（継続アップデート）"
            elif "gpt-5-mini" in available_models:
                model_info = "⚡ GPT-5軽量版（高速・低コスト）"
                selected_model = "gpt-5-mini"
            elif "gpt-4.1" in available_models:
                selected_model = "gpt-4.1"
                model_info = "🆕 次世代GPT（ベータ版）"
            elif "gpt-4o" in available_models:
                selected_model = "gpt-4o"
                model_info = "🎯 最新GPT-4（バランス型・安定）"
            elif "gpt-4o-mini" in available_models:
                selected_model = "gpt-4o-mini"
                model_info = "💨 軽量版GPT-4（高速・低コスト）"
            else:
                selected_model = available_models[0]
                model_info = "選択されたモデルの詳細情報"
            st.session_state.selected_model = selected_model
            st.session_state.model_info = model_info
    
    else:
        # 全モデル一覧選択
        # デフォルトのインデックスを決定
        default_index = 0
        if "gpt-5" in available_models:
            default_index = available_models.index("gpt-5")
        elif "gpt-5-chat-latest" in available_models:
            default_index = available_models.index("gpt-5-chat-latest")
        elif "gpt-5-mini" in available_models:
            default_index = available_models.index("gpt-5-mini")
        elif "gpt-4.1" in available_models:
            default_index = available_models.index("gpt-4.1")
        elif "gpt-4o" in available_models:
            default_index = available_models.index("gpt-4o")
        elif "gpt-4o-mini" in available_models:
            default_index = available_models.index("gpt-4o-mini")
        
        selected_model = st.sidebar.selectbox(
            "使用するモデルを選択",
            available_models,
            index=default_index
        )
        
        # 選択されたモデルの情報を検索
        for category, models in model_categories.items():
            if selected_model in models:
                model_info = models[selected_model]['description']
                break
        else:
            model_info = "選択されたモデルの詳細情報"
    
    # 現在選択されているモデル情報を表示
    if selected_model:
        st.sidebar.success(f"✅ 選択中: **{selected_model}**")
        st.sidebar.info(model_info)
        
        # 価格情報を表示
        for category, models in model_categories.items():
            if selected_model in models:
                price_info = models[selected_model]['price']
                use_case = models[selected_model]['use_case']
                note_info = models[selected_model].get('note', '')
                st.sidebar.markdown(f"💰 **価格**: {price_info}")
                st.sidebar.markdown(f"🎯 **適用例**: {use_case}")
                if note_info:
                    st.sidebar.markdown(f"ℹ️ **状態**: {note_info}")
                break
    
    return selected_model, model_info

def load_conversation_history(csv_file: str = None) -> List[Dict[str, str]]:
    """CSVから会話履歴を読み込み、OpenAI API形式に変換"""
    if not csv_file:
        return []
        
    try:
        df = pd.read_csv(csv_file)
        # NaN値を削除
        df = df.dropna()
        messages = []
        
        for _, row in df.iterrows():
            role = "user" if row['side'] == 'human' else "assistant"
            content = str(row['prompt']).strip()
            
            # 空文字列やNaNをスキップ
            if content and content != 'nan':
                messages.append({"role": role, "content": content})
        
        return messages
    except FileNotFoundError:
        st.warning(f"{csv_file} が見つかりません。履歴なしで続行します。")
        return []
    except Exception as e:
        st.error(f"履歴読み込みエラー: {str(e)}")
        return []

def parse_json_response(response_text: str) -> Dict:
    """JSON形式のレスポンスをパースし、エラーハンドリングを行う"""
    raw_text = response_text or ""
    cleaned_text = raw_text.strip()

    if not cleaned_text:
        return {
            "copies": [],
            "raw_text": raw_text,
            "error": "empty_response"
        }

    json_text = cleaned_text

    if "```json" in cleaned_text:
        json_start = cleaned_text.find("```json") + 7
        json_end = cleaned_text.find("```", json_start)
        json_text = cleaned_text[json_start:json_end].strip()
    elif "{" in cleaned_text and "}" in cleaned_text:
        json_start = cleaned_text.find("{")
        json_end = cleaned_text.rfind("}") + 1
        json_text = cleaned_text[json_start:json_end]

    try:
        parsed_data = json.loads(json_text)
        if isinstance(parsed_data, dict):
            parsed_data.setdefault("raw_text", raw_text)
        return parsed_data
    except json.JSONDecodeError:
        fallback_copies = [cleaned_text] if cleaned_text else []
        return {
            "copies": fallback_copies,
            "raw_text": raw_text,
            "error": "json_decode_failure"
        }

def format_copies_display(parsed_json: Dict) -> str:
    """パースされたJSONからコピーのみを抽出して表示用にフォーマット"""
    copies: List[str] = []
    raw_text = ""
    error_flag = False

    if isinstance(parsed_json, dict):
        raw_text = parsed_json.get("raw_text", "")
        error_flag = bool(parsed_json.get("error"))
        if "copies" in parsed_json:
            value = parsed_json.get("copies")
            if isinstance(value, list):
                copies = [str(item) for item in value if item]
            elif isinstance(value, str):
                copies = [value]
        elif "results" in parsed_json:
            value = parsed_json.get("results")
            if isinstance(value, list):
                copies = [str(item) for item in value if item]
            elif isinstance(value, str):
                copies = [value]
        elif "what_to_say" in parsed_json and "copies" in parsed_json:
            what_to_say = parsed_json.get("what_to_say") or []
            copy_list = parsed_json.get("copies") or []
            formatted = "【What to Say（20案）】\n"
            for i, wts in enumerate(what_to_say[:20], 1):
                formatted += f"{i}. {wts}\n"
            formatted += "\n【コピー（20案）】\n"
            for i, copy in enumerate(copy_list[:20], 1):
                formatted += f"{i}. {copy}\n"
            return formatted.strip()
        elif "refinements" in parsed_json:
            refinements = parsed_json.get("refinements") or []
            copies = []
            for refinement in refinements:
                copy = refinement.get("copy")
                if copy:
                    copies.append(str(copy))

    if not copies and raw_text:
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        copies = lines[:20]

    if error_flag:
        if copies:
            print("[streamlit_demo_7] JSON parsing fallback succeeded; displaying fallback copies.")
        else:
            print("[streamlit_demo_7] JSON parsing failed; displaying raw response text.")
            return raw_text or "エラーが発生しました"

    if len(copies) > 1:
        return "\n".join([f"{i}. {copy}" for i, copy in enumerate(copies, 1)])
    elif copies:
        return copies[0]
    else:
        if raw_text:
            return raw_text
        print("[streamlit_demo_7] No copies generated; returning fallback text.")
        return "コピーが生成されませんでした"

def extract_copies_list(parsed_json: Dict) -> List[str]:
    """パースされたJSONからコピーのリストを抽出"""
    copies = []
    
    if "error" in parsed_json:
        return []
    
    # 様々なJSON構造に対応
    if "copies" in parsed_json:
        if isinstance(parsed_json["copies"], list):
            copies = parsed_json["copies"]
        else:
            copies = [str(parsed_json["copies"])]
    elif "results" in parsed_json:
        if isinstance(parsed_json["results"], list):
            copies = parsed_json["results"]
        else:
            copies = [str(parsed_json["results"])]
    elif "what_to_say" in parsed_json and "copies" in parsed_json:
        # 段階1の構造化生成用 - copiesのみ抽出
        copy_list = parsed_json.get("copies", [])
        copies = copy_list
    elif "refinements" in parsed_json:
        # How to Say洗練用 - 洗練後のコピーのみ抽出
        refinements = parsed_json["refinements"]
        for refinement in refinements:
            copy = refinement.get("copy", "")
            if copy:
                copies.append(copy)
    else:
        # その他の構造の場合、全体を文字列として扱う
        copies = [str(parsed_json)]
    
    return copies


def append_execution_log(message: str) -> None:
    """実行ログをセッションに追記"""
    timestamp = time.strftime("%H:%M:%S")
    log_entry = {"time": timestamp, "message": message}
    if 'execution_log' not in st.session_state:
        st.session_state.execution_log = []
    st.session_state.execution_log.append(log_entry)
    # 最新50件に制限
    st.session_state.execution_log = st.session_state.execution_log[-50:]

def generate_feedback_based_copy(orientation: str, good_copies: List[str], bad_copies: List[str], conversation_messages: List[Dict], model: str = "gpt-5", temperature: float = 0.9) -> str:
    """ユーザーフィードバックを基にした自省的コピー生成"""
    openai.api_key = OPENAI_API_KEY
    
    # モデル種別を判定
    is_o1_pro = "o1-pro" in model.lower()
    is_o3_or_o1_other = any(prefix in model.lower() for prefix in ['o1-', 'o3-']) and not is_o1_pro
    use_json_mode = supports_json_mode(model)

    temperature = normalize_temperature(model, temperature)
    
    # 自省プロンプトを構築
    good_copies_text = "\n".join([f"✅ {copy}" for copy in good_copies])
    bad_copies_text = "\n".join([f"❌ {copy}" for copy in bad_copies])
    
    self_reflection_prompt = f"""
【ユーザーフィードバック分析】

以下のコピーについて、ユーザーが選択した良いコピーと選択しなかった悪いコピーを分析してください：

【良いコピー（ユーザーが選択）】
{good_copies_text}

【悪いコピー（ユーザーが選択しなかった）】
{bad_copies_text}

【分析タスク】
1. 良いコピーと悪いコピーの違いを詳細に分析してください
2. ユーザーが評価した要素（表現、響き、印象、効果など）を特定してください
3. その分析結果を踏まえて、より良いコピーを20個新たに生成してください

【分析観点】
- 言葉の選び方
- 感情的インパクト
- ターゲットへの響き方
- 記憶に残りやすさ
- 独創性
- 説得力
- 簡潔さ

分析結果を活用して、ユーザーの好みに合致する新しいコピーを作成してください。
"""
    
    json_instruction = """

回答は必ずJSON形式で出力してください。以下の形式に従ってください：

{
  "analysis": "良いコピーと悪いコピーの違いの分析結果",
  "insights": [
    "洞察1",
    "洞察2",
    ...
  ],
  "copies": [
    "改善されたコピー1",
    "改善されたコピー2",
    ...（20個）
  ]
}

JSON以外の説明や前置きは一切含めず、純粋なJSONのみを出力してください。"""
    
    try:
        if is_o1_pro:
            if conversation_messages:
                conversation_text = "\n\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_messages])
                user_message = f"{orientation}\n\n過去の会話:\n{conversation_text}\n\n{self_reflection_prompt}{json_instruction}"
            else:
                user_message = f"{orientation}\n\n{self_reflection_prompt}{json_instruction}"
            
            response = openai.responses.create(
                model=model,
                input=user_message,
                reasoning={"effort": "high"}
            )
            response_text = response.choices[0].message.content
            
        elif is_o3_or_o1_other:
            if conversation_messages:
                conversation_text = "\n\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_messages])
                user_message = f"{orientation}\n\n過去の会話:\n{conversation_text}\n\n{self_reflection_prompt}{json_instruction}"
            else:
                user_message = f"{orientation}\n\n{self_reflection_prompt}{json_instruction}"
            
            messages = [{"role": "user", "content": user_message}]
            
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_completion_tokens=3000
            )
            response_text = response.choices[0].message.content
        
        else:
            temperature = normalize_temperature(model, temperature)

            system_message = {
                "role": "system", 
                "content": f"""あなたは優秀なコピーライターです。
ユーザーのフィードバックを詳細に分析し、その洞察を活用してより良いコピーを生成してください。
良いコピーと悪いコピーの違いを深く理解し、ユーザーの好みに合致する改善されたコピーを作成してください。

重要：生成するコピーは純粋なコピー文言のみを出力してください。説明文、分析、型番号、型名などの余計な情報は一切含めないでください。コピーは完成品として、そのまま広告として使えるものにしてください。{json_instruction}"""
            }
            
            new_user_message = {
                "role": "user", 
                "content": f"{orientation}\n\n{self_reflection_prompt}"
            }
            
            messages = [system_message] + conversation_messages + [new_user_message]
            
            if use_json_mode:
                response = openai.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_completion_tokens=3000,
                    temperature=temperature,
                    response_format={"type": "json_object"}
                )
            else:
                response = openai.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_completion_tokens=3000,
                    temperature=temperature
                )
                
            response_text = response.choices[0].message.content
        
        # demo_3アプローチ：プレーンテキストをそのまに返す
        return response_text
            
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

def supports_json_mode(model: str) -> bool:
    """モデルがJSON Modeをサポートしているかチェック"""
    # o1系、o3系の推論モデルはJSON Modeをサポートしていない
    unsupported_prefixes = ['o1-', 'o3-']
    return not any(prefix in model.lower() for prefix in unsupported_prefixes)

def normalize_temperature(model: str, temperature: float) -> float:
    """モデル制約に応じてTemperatureを調整"""
    if model and model.lower().startswith("gpt-5"):
        return 1.0
    return temperature

def generate_staged_copy(orientation: str, stage_prompt: str, conversation_messages: List[Dict], model: str = "gpt-5", temperature: float = 0.9, stream_output: bool = False, stream_placeholder=None) -> Tuple[str, Dict]:
    """段階的コピー生成（JSON出力対応）"""
    openai.api_key = OPENAI_API_KEY
    
    # モデル種別を判定
    is_o1_pro = "o1-pro" in model.lower()
    is_o3_or_o1_other = any(prefix in model.lower() for prefix in ['o1-', 'o3-']) and not is_o1_pro
    use_json_mode = supports_json_mode(model)
    
    # ストリーム出力を要求された場合は JSON Mode を強制オフ
    if stream_output:
        use_json_mode = False
    
    temperature = normalize_temperature(model, temperature)

    # JSON出力用のプロンプト拡張
    json_instruction = """
回答は必ずJSON形式で出力してください。以下の形式に従ってください：

{
  "copies": [
    "コピー1",
    "コピー2", 
    ...（20個）
  ]
}

what to sayは思考の過程として重要ですが、最終的なJSONには含めず、コピーのみを出力してください。
JSON以外の説明や前置きは一切含めず、純粋なJSONのみを出力してください。"""

    base_system_message = {
        "role": "system",
        "content": """あなたは優秀なコピーライターです。\n段階的にコピーを改善していきます。これまでの会話履歴を踏まえて、指示に従ってコピーを作成・改善してください。重要：生成するコピーは純粋なコピー文言のみを出力してください。説明文、分析、型番号、型名などの余計な情報は一切含めないでください。コピーは完成品として、そのまま広告として使えるものにしてください。""",
    }

    strict_json_system_message = {
        "role": "system",
        "content": json_instruction,
    }
    
    try:
        if is_o1_pro:
            # o1-proはResponses APIのみ対応
            if conversation_messages:
                conversation_text = "\n\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_messages])
                user_message = f"{orientation}\n\n過去の会話:\n{conversation_text}\n\n{stage_prompt}{json_instruction}"
            else:
                user_message = f"{orientation}\n\n{stage_prompt}{json_instruction}"
            
            response = openai.responses.create(
                model=model,
                input=user_message,
                reasoning={"effort": "high"}
            )
            response_text = response.choices[0].message.content
            
        elif is_o3_or_o1_other:
            # その他の推論モデル用の処理
            if conversation_messages:
                conversation_text = "\n\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_messages])
                user_message = f"{orientation}\n\n過去の会話:\n{conversation_text}\n\n{stage_prompt}{json_instruction}"
            else:
                user_message = f"{orientation}\n\n{stage_prompt}{json_instruction}"
            
            messages = [{"role": "user", "content": user_message}]
            
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_completion_tokens=3000
            )
            response_text = response.choices[0].message.content
        
        else:
            # 標準GPTモデル用の処理
            system_messages: List[Dict[str, str]]
            if model.lower().startswith("gpt-5"):
                system_messages = [base_system_message, strict_json_system_message]
            else:
                system_messages = [{
                    "role": "system",
                    "content": base_system_message["content"] + "\n\n" + json_instruction
                }]

            new_user_message = {"role": "user", "content": f"{orientation}\n\n{stage_prompt}"}
            messages = system_messages + conversation_messages + [new_user_message]
            
            # ストリーミング表示が必要かどうか
            if stream_output and not use_json_mode:
                streamed_text = ""
                char_goal = 1800  # 粗い目安（20コピーで約1800文字）
                start_time = time.time()
                progress_bar = st.progress(0.0)
                eta_placeholder = st.empty()

                stream = openai.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_completion_tokens=3000,
                    temperature=temperature,
                    stream=True
                )
                for chunk in stream:
                    delta = chunk.choices[0].delta.content or ""
                    if not delta:
                        continue
                    streamed_text += delta

                    # タイプライター表示（末尾カーソル付き）
                    if stream_placeholder is not None:
                        typing_html = (
                            f'<div class="copy-display" style="max-height:400px;overflow-y:auto;white-space:pre-wrap;">'
                            f'{streamed_text}<span style="color:#f87171">▋</span></div>'
                        )
                        stream_placeholder.markdown(typing_html, unsafe_allow_html=True)

                    # 進捗計算
                    progress = min(0.99, len(streamed_text) / char_goal)
                    progress_bar.progress(progress)

                    # ETA 更新
                    if progress > 0:
                        elapsed = time.time() - start_time
                        eta = max(0, (elapsed / progress) - elapsed)
                        eta_placeholder.text(f"ETA: {eta:4.1f}s")

                # 完了処理
                progress_bar.progress(1.0)
                eta_placeholder.text("Done ✔")

                # 最終描画（カーソル除去）
                if stream_placeholder is not None:
                    stream_placeholder.markdown(
                        f'<div class="copy-display" style="max-height:400px;overflow-y:auto;white-space:pre-wrap;">{streamed_text}</div>',
                        unsafe_allow_html=True
                    )

                response_text = streamed_text
            else:
                if use_json_mode:
                    response = openai.chat.completions.create(
                        model=model,
                        messages=messages,
                        max_completion_tokens=3000,
                        temperature=temperature,
                        response_format={"type": "json_object"}
                    )
                else:
                    response = openai.chat.completions.create(
                        model=model,
                        messages=messages,
                        max_completion_tokens=3000,
                        temperature=temperature
                    )
                response_text = response.choices[0].message.content

        # Raw response logging for debugging
        log_console("api", f"RAW RESPONSE (first 500 chars): {response_text[:500] if response_text else 'EMPTY RESPONSE'}")

        # ストリーム時はプレーンテキストを返す（JSON解析スキップ）
        if stream_output:
            return response_text, {}
        else:
            parsed_json = parse_json_response(response_text)
            formatted_result = format_copies_display(parsed_json)
            return formatted_result, parsed_json
            
    except Exception as e:
        error_msg = str(e)
        return f"エラーが発生しました: {error_msg}", {}

def generate_how_to_say_refinement(copies: str, orientation: str, model: str = "gpt-5", temperature: float = 0.9) -> str:
    """HOW TO SAY型を使ってコピーを洗練（JSON出力対応）"""
    openai.api_key = OPENAI_API_KEY
    
    # HOW TO SAY型の詳細を文字列で構築
    how_to_say_details = ""
    for i, type_info in enumerate(HOW_TO_SAY_TYPES, 1):
        examples_str = "、".join([f'「{ex}」' for ex in type_info['examples']])
        how_to_say_details += f"{i}：{type_info['name']}\n例：{examples_str}\n\n"
    
    # モデル種別を判定
    is_o1_pro = "o1-pro" in model.lower()
    is_o3_or_o1_other = any(prefix in model.lower() for prefix in ['o1-', 'o3-']) and not is_o1_pro
    use_json_mode = supports_json_mode(model)
    
    json_instruction = """

回答は必ずJSON形式で出力してください。以下の形式に従ってください：

{
  "refinements": [
    {
      "original": "元のコピー",
      "type": "型X：型名",
      "copy": "洗練されたコピー",
      "reason": "この型を選んだ理由"
    },
    ...
  ]
}

JSON以外の説明や前置きは一切含めず、純粋なJSONのみを出力してください。"""

    prompt = f"""
以下の20個のコピーを分析し、それぞれに最も適した「How to Say」の型を選んで、その型に当てはめて洗練してください。

【オリエンテーション情報】
{orientation}

【生成されたコピー】
{copies}

【How to Say型一覧】
{how_to_say_details}

【重要な指示】
1. 各コピーを分析し、最も適した型（1-20）を判定してください
2. その型の特徴を活かして、コピーをより効果的に洗練してください
3. 洗練されたコピーは純粋なコピー文言のみを出力してください
4. 型番号や型名、説明などの余計な情報は一切含めないでください
5. 洗練されたコピーは完成品として、そのまま広告として使えるものにしてください

{json_instruction}
"""
    
    try:
        if is_o1_pro:
            response = openai.responses.create(
                model=model,
                input=prompt,
                reasoning={"effort": "high"}
            )
            response_text = response.choices[0].message.content
            
        elif is_o3_or_o1_other:
            messages = [{"role": "user", "content": prompt}]
            
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_completion_tokens=3000
            )
            response_text = response.choices[0].message.content
        
        else:
            temperature = normalize_temperature(model, temperature)

            system_message = {
                "role": "system", 
                "content": f"""あなたは優秀なコピーライターです。
与えられたコピーを20種類の「How to Say」型に当てはめて、より効果的に洗練してください。
各型の特徴を理解し、コピーの本質を保ちながら、より印象的で記憶に残る表現に変換してください。

重要：洗練されたコピーは純粋なコピー文言のみを出力してください。型番号や型名、説明などの余計な情報は一切含めないでください。洗練されたコピーは完成品として、そのまま広告として使えるものにしてください。{json_instruction}"""
            }
            
            messages = [system_message, {"role": "user", "content": prompt}]
            
            if use_json_mode:
                response = openai.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_completion_tokens=3000,
                    temperature=temperature,
                    response_format={"type": "json_object"}
                )
            else:
                response = openai.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_completion_tokens=3000,
                    temperature=temperature
                )
            
            response_text = response.choices[0].message.content
        
        # demo_3アプローチ：プレーンテキストをそのまに返す
        return response_text
            
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

def generate_custom_copy(orientation: str, custom_prompt: str, conversation_messages: List[Dict], model: str = "gpt-5", temperature: float = 0.9) -> Tuple[str, Dict]:
    """カスタムプロンプトによるコピー生成（JSON出力対応）"""
    openai.api_key = OPENAI_API_KEY
    
    # モデル種別を判定
    is_o1_pro = "o1-pro" in model.lower()
    is_o3_or_o1_other = any(prefix in model.lower() for prefix in ['o1-', 'o3-']) and not is_o1_pro
    use_json_mode = supports_json_mode(model)
    
    json_instruction = """

回答は必ずJSON形式で出力してください。以下の形式に従ってください：

{
  "copies": [
    "改善されたコピー1",
    "改善されたコピー2",
    ...（20個程度）
  ]
}

JSON以外の説明や前置きは一切含めず、純粋なJSONのみを出力してください。"""
    
    try:
        if is_o1_pro:
            if conversation_messages:
                conversation_text = "\n\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_messages])
                user_message = f"{orientation}\n\n過去の会話:\n{conversation_text}\n\n{custom_prompt}{json_instruction}"
            else:
                user_message = f"{orientation}\n\n{custom_prompt}{json_instruction}"
            
            response = openai.responses.create(
                model=model,
                input=user_message,
                reasoning={"effort": "high"}
            )
            response_text = response.choices[0].message.content
            
        elif is_o3_or_o1_other:
            if conversation_messages:
                conversation_text = "\n\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_messages])
                user_message = f"{orientation}\n\n過去の会話:\n{conversation_text}\n\n{custom_prompt}{json_instruction}"
            else:
                user_message = f"{orientation}\n\n{custom_prompt}{json_instruction}"
            
            messages = [{"role": "user", "content": user_message}]
            
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_completion_tokens=3000
            )
            response_text = response.choices[0].message.content
        
        else:
            temperature = normalize_temperature(model, temperature)

            system_message = {
                "role": "system", 
                "content": f"""あなたは優秀なコピーライターです。
これまでの会話履歴を踏まえて、カスタムフィードバックに基づいてコピーを改善・生成してください。

重要：生成するコピーは純粋なコピー文言のみを出力してください。説明文、分析、型番号、型名などの余計な情報は一切含めないでください。コピーは完成品として、そのまま広告として使えるものにしてください。{json_instruction}"""
            }
            
            new_user_message = {
                "role": "user", 
                "content": f"{orientation}\n\n{custom_prompt}"
            }
            
            messages = [system_message] + conversation_messages + [new_user_message]
            
            if use_json_mode:
                response = openai.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_completion_tokens=3000,
                    temperature=temperature,
                    response_format={"type": "json_object"}
                )
            else:
                response = openai.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_completion_tokens=3000,
                    temperature=temperature
                )
            
            response_text = response.choices[0].message.content
        
        # JSONをパースして表示用にフォーマット
        parsed_json = parse_json_response(response_text)
        formatted_result = format_copies_display(parsed_json)
        return formatted_result, parsed_json
            
    except Exception as e:
        error_msg = str(e)
        return f"エラーが発生しました: {error_msg}", {}

def generate_copy_ideas(orientation: str, csv_file: str = None, num_ideas: int = 5, model: str = "gpt-5", temperature: float = 0.9) -> str:
    """オリエンテーション + 会話履歴ベースのコピー生成（demo_3のシンプルアプローチ）"""
    openai.api_key = OPENAI_API_KEY
    
    # 会話履歴を読み込み
    conversation_history = load_conversation_history(csv_file)
    
    # モデル種別を判定
    is_o1_pro = "o1-pro" in model.lower()
    is_o3_or_o1_other = any(prefix in model.lower() for prefix in ['o1-', 'o3-']) and not is_o1_pro
    
    try:
        if is_o1_pro:
            user_message = f"{orientation}\n\n上記の情報を基に、効果的なキャッチコピーを{num_ideas}個作成してください。"
            
            response = openai.responses.create(
                model=model,
                input=user_message,
                reasoning={"effort": "high"}
            )
            return response.choices[0].message.content
            
        elif is_o3_or_o1_other:
            user_message = f"{orientation}\n\n上記の情報を基に、効果的なキャッチコピーを{num_ideas}個作成してください。"
            
            messages = [{"role": "user", "content": user_message}]
            
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_completion_tokens=1200,
                temperature=temperature
            )
            return response.choices[0].message.content
        
        else:
            system_message = {
                "role": "system", 
                "content": f"""あなたは優秀なコピーライターです。
これまでの会話履歴を踏まえて、与えられたオリエンテーション情報を活用し、効果的なキャッチコピーを作成してください。

出力は簡潔で、インパクトがあり、ターゲットに刺さるものを{num_ideas}個厳選してください。
コピーのみを出力してください。"""
            }
            
            new_user_message = {
                "role": "user", 
                "content": f"{orientation}\n\n最終的に{num_ideas}個の厳選されたキャッチコピーを出力してください。"
            }
            
            messages = [system_message] + conversation_history + [new_user_message]
                
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_completion_tokens=1200,
                temperature=temperature
            )
                
            return response.choices[0].message.content
            
    except Exception as e:
        error_msg = str(e)
        return f"エラーが発生しました: {error_msg}"

# Streamlit UI
st.set_page_config(
    page_title="クリエイティブ・ディレクターになろう",
    page_icon="👨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("クリエイティブ・ディレクターになろう👨 v6")

# A1明朝フォントの設定
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap');

.copy-display {
    font-family: 'Noto Serif JP', 'A1明朝', 'ヒラギノ明朝 ProN', 'Hiragino Mincho ProN', '游明朝体', 'Yu Mincho', YuMincho, 'HG明朝E', 'MS P明朝', 'MS PMincho', serif !important;
    font-size: 16px !important;
    line-height: 1.8 !important;
    padding: 10px !important;
    background-color: transparent !important;
    border-radius: 5px !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    color: #ffffff !important;
    white-space: pre-wrap !important;
    max-height: 240px !important;
    overflow-y: auto !important;
}

/* Streamlit特有のセレクター */
.stCheckbox > label > div[data-testid="stMarkdownContainer"] > p {
    font-family: 'Noto Serif JP', 'A1明朝', 'ヒラギノ明朝 ProN', 'Hiragino Mincho ProN', '游明朝体', 'Yu Mincho', YuMincho, 'HG明朝E', 'MS P明朝', 'MS PMincho', serif !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
}

/* チェックボックス全体のラベル */
.stCheckbox label {
    font-family: 'Noto Serif JP', 'A1明朝', 'ヒラギノ明朝 ProN', 'Hiragino Mincho ProN', '游明朝体', 'Yu Mincho', YuMincho, 'HG明朝E', 'MS P明朝', 'MS PMincho', serif !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
}

/* textareaの中身も明朝に */
.stTextArea textarea {
    font-family: 'Noto Serif JP', 'A1明朝', 'ヒラギノ明朝 ProN', 'Hiragino Mincho ProN', '游明朝体', 'Yu Mincho', YuMincho, 'HG明朝E', 'MS P明朝', 'MS PMincho', serif !important;
}

/* より具体的なStreamlitセレクター */
div[data-testid="stMarkdownContainer"] p {
    font-family: 'Noto Serif JP', 'A1明朝', 'ヒラギノ明朝 ProN', 'Hiragino Mincho ProN', '游明朝体', 'Yu Mincho', YuMincho, 'HG明朝E', 'MS P明朝', 'MS PMincho', serif !important;
}

/* 全体的なテキスト要素への適用 */
.element-container div[data-testid="stMarkdownContainer"] {
    font-family: 'Noto Serif JP', 'A1明朝', 'ヒラギノ明朝 ProN', 'Hiragino Mincho ProN', '游明朝体', 'Yu Mincho', YuMincho, 'HG明朝E', 'MS P明朝', 'MS PMincho', serif !important;
}
</style>
""", unsafe_allow_html=True)

# 追加CSS: Skeletonカードとパーティクル背景
st.markdown(
    """
    <style>
    /* Skeleton */
    .skeleton {
        width: 100%;
        height: 36px;
        background: #262626;
        border-radius: 6px;
        margin-bottom: 12px;
        animation: pulse 1.6s ease-in-out infinite;
    }
    @keyframes pulse {
        0%   { opacity: 0.6; }
        50%  { opacity: 0.35; }
        100% { opacity: 0.6; }
    }

    /* パーティクル風背景 */
    .stApp::before{
        content:"";
        position:fixed;inset:0;
        z-index:-1;
        background:radial-gradient(circle at 25% 25%,#ff6b9d22,transparent 40%),
                  radial-gradient(circle at 75% 75%,#8b5cf622,transparent 40%);
        animation:bgmove 12s linear infinite alternate;
    }
    @keyframes bgmove{to{background-position:30% 70%,70% 30%;}}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# モデル選択
selected_model, model_info = display_model_selector()

st.sidebar.markdown("---")

# サイドバー - Temperature設定
st.sidebar.header("🌡️ 創造性設定")
temperature = st.sidebar.slider(
    "Temperature（創造性レベル）",
    min_value=0.0,
    max_value=1.5,
    value=1.2,
    step=0.1
)



st.sidebar.markdown("---")

# 生成モード選択
st.sidebar.header("🎛️ 生成モード")
generation_mode = st.sidebar.radio(
    "モードを選択",
    ["一括生成", "段階的生成"],
    help="一括生成：3段階を連続実行\n段階的生成：各段階を個別実行"
)

# メインエリア
if generation_mode == "段階的生成":
    # 段階的生成モード
    
    # セッション状態の初期化
    if 'execution_results' not in st.session_state:
        st.session_state.execution_results = []  # 実行順にブロック結果を格納
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'current_orientation' not in st.session_state:
        st.session_state.current_orientation = ""
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # デフォルトのオリエンテーション
        default_orientation = """【課題商品・サービスの訴求したいポイント】
ルイボスとグリーンルイボスの2種の茶葉をブレンドし、ルイボスティーらしい豊かな香り立ちがありながら、すっきりとした飲みやすさを実現。クセのあるイメージのルイボスティーですが、すっきりゴクゴク飲める味わいです。アレルギー特定原材料等28品目不使用、カフェインゼロなのに、ルイボスティーの豊かな香りですっきりリフレッシュ。仕事中、食中食後、喉が渇いたときなどさまざまなシーンでおすすめです。

【今回、募集する作品に期待すること】
「GREEN DA・KA・RA」は"やさしさ"を大事にした心とカラダにやさしいブランドです。数あるルイボスティーの中でも、「GREEN DA・KA・RA やさしいルイボス」を選びたくなる、やさしさのつまった表現アイディアを期待しています。

【制作にあたっての注意事項】
「GREEN DA・KA・RAブランドの愛嬌を大切にしながら表現を検討してください。「GREEN DA・KA・RA」は"やさしさ"を大事にした心とカラダにやさしいブランドです。数あるルイボスティーの中でも、「GREEN DA・KA・RA やさしいルイボス」を選びたくなる、やさしさのつまった表現アイディアを期待しています。今回のお題では、さまざまな生活シーンで水分補給をする20~30代男女をターゲットにします。ルイボスとグリーンルイボスの2種の茶葉をブレンドし、ルイボスティーらしい豊かな香り立ちがありながら、すっきりとした飲みやすさを実現。クセのあるイメージのルイボスティーですが、すっきりゴクゴク飲める味わいです。アレルギー特定原材料等28品目不使用、カフェインゼロなのに、ルイボスティーの豊かな香りですっきりリフレッシュ。仕事中、食中食後、喉が渇いたときなどさまざまなシーンでおすすめです。「GREEN DA・KA・RA」ブランドの愛嬌を大切にしながら表現を検討してください。"""
        
        # オリエンテーション入力エリア
        orientation = st.text_area(
            "企業情報・課題・ターゲット等を入力してください",
            value=st.session_state.get('staged_orientation', default_orientation),
            height=300
        )
        
        st.markdown("---")
        
        # 各ブロックを独立実行可能に表示
        for i, block_info in enumerate(COPY_BLOCKS):
            block_id = block_info['id']
            
            # ブロック表示
            with st.container():
                col_btn = st.columns([1])[0]
                
                with col_btn:
                    if st.button(
                        f"▶️ {block_info['title']}",
                        key=f"block_{block_id}",
                        type="primary",
                        use_container_width=True
                    ):
                        if not orientation:
                            st.error("オリエンテーションを入力してください")
                        else:
                            # オリエンテーションを保存
                            st.session_state.current_orientation = orientation
                            
                            # 選択されたコピーがある場合、プロンプトに追加
                            enhanced_prompt = block_info['prompt']
                            if ('unified_selected_copies' in st.session_state and 
                                st.session_state.unified_selected_copies and 
                                'accumulated_copies' in st.session_state):
                                
                                selected_copies = []
                                for idx in st.session_state.unified_selected_copies:
                                    if idx < len(st.session_state.accumulated_copies):
                                        selected_copies.append(st.session_state.accumulated_copies[idx]['copy'])
                                
                                if selected_copies:
                                    selected_copies_text = '\n'.join([f"• {copy}" for copy in selected_copies])
                                    enhanced_prompt += f"\n\n【参考】ユーザーが特に気に入っていたコピー：\n{selected_copies_text}\n\nこれらの方向性や表現スタイルも参考にしながら、新しいコピーを生成してください。"
                            
                            if 'main_display' not in st.session_state:
                                st.session_state.main_display = st.empty()
                            result_placeholder = st.session_state.main_display
                            result_placeholder.empty()
                            result_placeholder.markdown("""<div class='skeleton'></div>""", unsafe_allow_html=True)
                            with st.spinner(f"生成中... (使用モデル: {selected_model})"):
                                result, parsed_json = generate_staged_copy(
                                    orientation,
                                    enhanced_prompt,
                                    st.session_state.conversation_history,
                                    selected_model,
                                    temperature,
                                    stream_output=False,
                                    stream_placeholder=result_placeholder
                                )

                                # GPT-5が空レスポンスを返した場合、GPT-4oでフォールバック
                                if selected_model.lower().startswith("gpt-5") and (not result or "エラーが発生しました" in result or len(result.strip()) < 50):
                                    log_console("warning", f"GPT-5 failed with empty response, falling back to GPT-4o")
                                    result, parsed_json = generate_staged_copy(
                                        orientation,
                                        enhanced_prompt,
                                        st.session_state.conversation_history,
                                        "gpt-4o",
                                        temperature,
                                        stream_output=False,
                                        stream_placeholder=result_placeholder
                                    )
                                
                            # 実行結果を順番に追加
                            execution_result = {
                                'id': block_id,
                                'title': block_info['title'],
                                'prompt': enhanced_prompt,
                                'result': result,
                                'raw_json': parsed_json,
                                'timestamp': time.time()
                            }
                            st.session_state.execution_results.append(execution_result)
                            
                            # 会話履歴に追加（シンプル）
                            st.session_state.conversation_history.append({
                                "role": "user", 
                                "content": enhanced_prompt
                            })
                            st.session_state.conversation_history.append({
                                "role": "assistant", 
                                "content": result
                            })
                            total_runs = len(st.session_state.execution_results)
                            append_execution_log(f"{block_info['title']} を実行しました（合計 {total_runs} 件）")
                            st.session_state.main_display.empty()
                            st.session_state.main_display.info(f"{block_info['title']} の結果を更新しました（合計 {total_runs} 件）")
                            st.rerun()
                

                
                st.markdown("---")
        

        
        # カスタムブロック
        with st.container():
            col_input_custom = st.columns([1])[0]
            
            with col_input_custom:
                custom_prompt = st.text_area(
                    "カスタムフィードバック・指示を入力",
                    height=100,
                    key="custom_prompt_input"
                )
                
                if st.button("カスタム実行", type="primary", use_container_width=True):
                    if not orientation:
                        st.error("オリエンテーションを入力してください")
                    elif not custom_prompt:
                        st.error("カスタムフィードバックを入力してください")
                    else:
                        # オリエンテーションを保存
                        st.session_state.current_orientation = orientation
                        
                        # 選択されたコピーがある場合、プロンプトに追加
                        enhanced_custom_prompt = custom_prompt
                        if ('unified_selected_copies' in st.session_state and 
                            st.session_state.unified_selected_copies and 
                            'accumulated_copies' in st.session_state):
                            
                            selected_copies = []
                            for idx in st.session_state.unified_selected_copies:
                                if idx < len(st.session_state.accumulated_copies):
                                    selected_copies.append(st.session_state.accumulated_copies[idx]['copy'])
                            
                            if selected_copies:
                                selected_copies_text = '\n'.join([f"• {copy}" for copy in selected_copies])
                                enhanced_custom_prompt += f"\n\n【参考】ユーザーが特に気に入っていたコピー：\n{selected_copies_text}\n\nこれらの方向性や表現スタイルも参考にしながら、新しいコピーを生成してください。"
                        
                        if 'main_display' not in st.session_state:
                            st.session_state.main_display = st.empty()
                        result_placeholder = st.session_state.main_display
                        result_placeholder.empty()
                        result_placeholder.markdown("""<div class='skeleton'></div>""", unsafe_allow_html=True)
                        with st.spinner(f"生成中... (使用モデル: {selected_model})"):
                            # カスタムは JSON モードでない前提でストリーム
                            result, parsed_json = generate_staged_copy(
                                orientation,
                                enhanced_custom_prompt,
                                st.session_state.conversation_history,
                                selected_model,
                                temperature,
                                stream_output=False,
                                stream_placeholder=result_placeholder
                            )
                            
                        # カスタム実行結果を追加
                        execution_result = {
                            'id': 'custom',
                            'title': 'カスタム実行',
                            'prompt': enhanced_custom_prompt,
                            'result': result,
                            'raw_json': parsed_json,
                            'timestamp': time.time()
                        }
                        st.session_state.execution_results.append(execution_result)
                        
                        # 会話履歴に追加
                        st.session_state.conversation_history.append({
                            "role": "user", 
                            "content": enhanced_custom_prompt
                        })
                        st.session_state.conversation_history.append({
                            "role": "assistant", 
                            "content": result
                        })
                        total_runs = len(st.session_state.execution_results)
                        st.info(f"実行結果を更新しました（合計 {total_runs} 件）")

                        st.rerun()
                

        
        st.markdown("---")
        
        # リセットボタン
        if len(st.session_state.execution_results) > 0:
            st.markdown("### リセット機能")
            col_reset, col_desc_reset = st.columns([1, 2])
            
            with col_reset:
                if st.button("全実行履歴をリセット", type="secondary", use_container_width=True):
                    st.session_state.execution_results = []
                    st.session_state.conversation_history = []
                    st.session_state.current_orientation = ""
                    # 新機能のセッション状態もクリア
                    if 'unified_selected_copies' in st.session_state:
                        del st.session_state.unified_selected_copies
                    if 'unified_feedback_result' in st.session_state:
                        del st.session_state.unified_feedback_result
                    # 蓄積されたコピーもクリア
                    if 'accumulated_copies' in st.session_state:
                        del st.session_state.accumulated_copies
                    st.rerun()
            

    
    with col2:
        if 'main_display' not in st.session_state:
            st.session_state.main_display = st.empty()
        
        if st.session_state.execution_results:
            if len(st.session_state.execution_results) > 0:
                st.markdown("---")
                st.markdown("## コピー選択")
                
                # すべてのコピーを蓄積する形で収集
                all_copies = []
                all_source_info = []
                
                # セッション状態に蓄積されたコピーを初期化（必要に応じて）
                if 'accumulated_copies' not in st.session_state:
                    st.session_state.accumulated_copies = []
                
                # 最新の実行結果からコピーを取得
                if st.session_state.execution_results:
                    latest_result = st.session_state.execution_results[-1]
                    raw_json = latest_result.get('raw_json', {})
                    
                    # JSONからコピーリストを抽出
                    copies_list = extract_copies_list(raw_json)

                    # 蓄積されたコピーリストに最新結果のコピーが含まれていない場合のみ追加
                    for copy in copies_list:
                        if copy not in [item['copy'] for item in st.session_state.accumulated_copies]:
                            st.session_state.accumulated_copies.append({
                                'copy': copy,
                                'source': latest_result['title'],
                                'execution_index': len(st.session_state.execution_results) - 1
                            })
                
                # フィードバック分析結果からコピーを追加
                if 'unified_feedback_result' in st.session_state:
                    feedback_text = st.session_state.unified_feedback_result
                    # フィードバック結果から「改善されたコピー」セクションを抽出
                    if "【✨ 改善されたコピー】" in feedback_text:
                        lines = feedback_text.split("\n")
                        in_copy_section = False
                        feedback_copies = []
                        for line in lines:
                            if "【✨ 改善されたコピー】" in line:
                                in_copy_section = True
                                continue
                            elif line.startswith("【") and in_copy_section:
                                break
                            elif in_copy_section and line.strip() and not line.startswith("【"):
                                # 番号付きの行を抽出
                                if ". " in line and any(char.isdigit() for char in line.split(". ")[0]):
                                    copy_text = ". ".join(line.split(". ")[1:]).strip()
                                    if copy_text:
                                        feedback_copies.append(copy_text)
                        
                        # フィードバックコピーを蓄積リストに追加（重複チェック）
                        for copy in feedback_copies:
                            if copy not in [item['copy'] for item in st.session_state.accumulated_copies]:
                                st.session_state.accumulated_copies.append({
                                    'copy': copy,
                                    'source': "フィードバック分析",
                                    'stage_num': 999  # フィードバック用の特別な番号
                                })
                
                # 蓄積されたコピーをall_copiesに追加（最新20個のみ表示）
                for item in st.session_state.accumulated_copies[-20:]:  # 最新20個のみ
                    all_copies.append(item['copy'])
                    all_source_info.append(item['source'])
                
                # セッション状態の初期化
                if 'unified_selected_copies' not in st.session_state:
                    st.session_state.unified_selected_copies = []
                
                # コピー選択UI
                if all_copies:
                    selected_indices = []
                    
                    for i, copy in enumerate(all_copies):
                        if st.checkbox(
                            f"{copy}",
                            key=f"unified_checkbox_{i}",
                            value=i in st.session_state.unified_selected_copies
                        ):
                            selected_indices.append(i)
                    
                    # 選択状態を更新
                    st.session_state.unified_selected_copies = selected_indices
                    
                    # フィードバック分析ボタン
                    if len(selected_indices) > 0 and len(selected_indices) < len(all_copies):
                        good_copies = [all_copies[i] for i in selected_indices]
                        bad_copies = [all_copies[i] for i in range(len(all_copies)) if i not in selected_indices]
                        
                        if st.button(
                            "改善コピーを生成",
                            key="unified_analyze_feedback",
                            type="primary"
                        ):
                            with st.spinner("フィードバック分析中..."):
                                feedback_result = generate_feedback_based_copy(
                                    st.session_state.current_orientation,
                                    good_copies,
                                    bad_copies,
                                    st.session_state.conversation_history,
                                    selected_model,
                                    temperature
                                )
                                
                                # フィードバック結果を保存
                                st.session_state.unified_feedback_result = feedback_result
                            
                            st.success("完了しました")
                            st.rerun()
                    

                
                if 'unified_feedback_result' in st.session_state:
                    st.download_button(
                        label="分析結果をダウンロード",
                        data=st.session_state.unified_feedback_result,
                        file_name="feedback_analysis_detailed.txt",
                        mime="text/plain",
                        key="download_unified_feedback"
                    )
                
                st.markdown("---")
                
                # 全実行結果の統合ダウンロード
                all_results = ""
                for i, execution in enumerate(st.session_state.execution_results):
                    all_results += f"=== 実行{i+1}: {execution['title']} ===\n"
                    all_results += f"実行時刻: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(execution['timestamp']))}\n"
                    all_results += f"プロンプト: {execution['prompt'][:100]}...\n\n"
                    all_results += f"{execution['result']}\n\n"
                    all_results += "=" * 50 + "\n\n"
                
                st.download_button(
                    label="全実行結果をダウンロード",
                    data=all_results,
                    file_name="copy_all_executions.txt",
                    mime="text/plain",
                    type="primary"
                )
                
                
        
        # 実行履歴の表示
        if st.session_state.execution_results:
            st.markdown("---")
            st.markdown("## 実行履歴")
            
            # 最新の実行結果を表示
            latest_execution = st.session_state.execution_results[-1]
            st.markdown(f"### 最新実行: {latest_execution['title']}")
            st.markdown(f'<div class="copy-display">{latest_execution["result"]}</div>', unsafe_allow_html=True)
            
            # 「もう一声」ボタンで最新結果をさらにブラッシュアップ
            if st.button("💡 もう一声", key="refine_latest_execution", type="primary"):
                # 参照するオリエンテーションを決定
                orientation_for_refine = st.session_state.get('current_orientation', orientation)
                base_copies_text = latest_execution["result"]
                with st.spinner("さらにコピーを磨いています..."):
                    stage2_prompt = "どれも広告的で心が動かない、もっと強いメッセージが必要。使い古された言い回しを使わずに、定型的な構文は避けて。二十個のコピーを考えて"
                    if 'main_display' not in st.session_state:
                        st.session_state.main_display = st.empty()
                    result_placeholder = st.session_state.main_display
                    result_placeholder.empty()
                    result_placeholder.markdown("""<div class='skeleton'></div>""", unsafe_allow_html=True)
                    formatted_refine, parsed_json_refine = generate_staged_copy(
                        orientation_for_refine,
                        stage2_prompt,
                        st.session_state.conversation_history,
                        selected_model,
                        temperature,
                        stream_output=False,
                        stream_placeholder=result_placeholder
                    )
                # 実行履歴へ追加
                refine_execution = {
                    'id': f"{latest_execution['id']}_refined",
                    'title': f"{latest_execution['title']} - もう一声",
                    'prompt': "Refine latest copies using How to Say self-reflection",
                    'result': formatted_refine,
                    'raw_json': parsed_json_refine,
                    'timestamp': time.time()
                }
                st.session_state.execution_results.append(refine_execution)
                # 会話履歴へ追加
                st.session_state.conversation_history.append({
                    "role": "user",
                    "content": "もう一声: 最新コピーをさらに磨いて"
                })
                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": formatted_refine
                })
                total_runs = len(st.session_state.execution_results)
                st.info(f"実行結果を更新しました（合計 {total_runs} 件）")
                st.rerun()
            
            # 実行履歴をリストで表示
            if len(st.session_state.execution_results) > 1:
                st.markdown("### 実行履歴一覧")
                for i, execution in enumerate(reversed(st.session_state.execution_results)):
                    with st.expander(f"実行{len(st.session_state.execution_results) - i}: {execution['title']} ({time.strftime('%H:%M:%S', time.localtime(execution['timestamp']))})"):
                        st.markdown(f'<div class="copy-display">{execution["result"]}</div>', unsafe_allow_html=True)
                        st.download_button(
                            label=f"ダウンロード - {execution['title']}",
                            data=execution['result'],
                            file_name=f"{execution['id']}_result.txt",
                            mime="text/plain",
                            key=f"download_{execution['timestamp']}"
                        )

else:
    # 一括生成モード（3段階連続実行）
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # デフォルトのオリエンテーション
        default_orientation_simple = """【課題商品・サービスの訴求したいポイント】
ルイボスとグリーンルイボスの2種の茶葉をブレンドし、ルイボスティーらしい豊かな香り立ちがありながら、すっきりとした飲みやすさを実現。クセのあるイメージのルイボスティーですが、すっきりゴクゴク飲める味わいです。アレルギー特定原材料等28品目不使用、カフェインゼロなのに、ルイボスティーの豊かな香りですっきりリフレッシュ。仕事中、食中食後、喉が渇いたときなどさまざまなシーンでおすすめです。

【今回、募集する作品に期待すること】
「GREEN DA・KA・RA」は"やさしさ"を大事にした心とカラダにやさしいブランドです。数あるルイボスティーの中でも、「GREEN DA・KA・RA やさしいルイボス」を選びたくなる、やさしさのつまった表現アイディアを期待しています。

【制作にあたっての注意事項】
「GREEN DA・KA・RAブランドの愛嬌を大切にしながら表現を検討してください。「GREEN DA・KA・RA」は"やさしさ"を大事にした心とカラダにやさしいブランドです。数あるルイボスティーの中でも、「GREEN DA・KA・RA やさしいルイボス」を選びたくなる、やさしさのつまった表現アイディアを期待しています。今回のお題では、さまざまな生活シーンで水分補給をする20~30代男女をターゲットにします。ルイボスとグリーンルイボスの2種の茶葉をブレンドし、ルイボスティーらしい豊かな香り立ちがありながら、すっきりとした飲みやすさを実現。クセのあるイメージのルイボスティーですが、すっきりゴクゴク飲める味わいです。アレルギー特定原材料等28品目不使用、カフェインゼロなのに、ルイボスティーの豊かな香りですっきりリフレッシュ。仕事中、食中食後、喉が渇いたときなどさまざまなシーンでおすすめです。「GREEN DA・KA・RA」ブランドの愛嬌を大切にしながら表現を検討してください。"""
        
        # オリエンテーション入力エリア
        orientation = st.text_area(
            "企業情報・課題・ターゲット等を入力してください",
            value=default_orientation_simple,
            height=300
        )
        
        generate_button = st.button("書いてみて", type="primary", use_container_width=True)

    with col2:
        # 単一のメイン表示プレースホルダー
        if 'main_display' not in st.session_state:
            st.session_state.main_display = st.empty()
            if 'main_display' not in st.session_state:
                st.session_state.main_display = st.empty()
            result_placeholder = st.session_state.main_display

        # 前回生成済みの結果がある場合は表示
        if st.session_state.get('last_batch_result'):
            result_placeholder.markdown(f'<div class="copy-display">{st.session_state.last_batch_result}</div>', unsafe_allow_html=True)

        if generate_button:
            if not orientation:
                st.error("オリエンテーションを入力してください")
            else:
                # 会話履歴をリセット
                st.session_state.batch_conversation_history = []
                st.session_state.batch_results = []
                
                # 3段階を連続実行
                for i, stage_info in enumerate(STAGED_PROMPTS, 1):
                    result_placeholder = st.session_state.main_display
                    result_placeholder.empty()
                    result_placeholder.markdown("""<div class='skeleton'></div>""", unsafe_allow_html=True)
                    with st.spinner(f"生成中... (使用モデル: {selected_model})"):
                        result, parsed_json = generate_staged_copy(
                            orientation,
                            stage_info['prompt'],
                            st.session_state.batch_conversation_history,
                            selected_model,
                            temperature,
                            stream_output=False,
                            stream_placeholder=result_placeholder
                        )

                        # GPT-5が空レスポンスを返した場合、GPT-4oでフォールバック
                        if selected_model.lower().startswith("gpt-5") and (not result or "エラーが発生しました" in result or len(result.strip()) < 50):
                            log_console("warning", f"GPT-5 failed with empty response in stage {i}, falling back to GPT-4o")
                            result, parsed_json = generate_staged_copy(
                                orientation,
                                stage_info['prompt'],
                                st.session_state.batch_conversation_history,
                                "gpt-4o",
                                temperature,
                                stream_output=False,
                                stream_placeholder=result_placeholder
                            )
                        
                        # 既存表示をリセットし Skeleton
                        result_placeholder.empty()
                        result_placeholder.markdown(f'<div class="copy-display">{result}</div>', unsafe_allow_html=True)
                        
                        # 会話履歴と結果は必要に応じて保持
                        st.session_state.batch_results = [{
                            'stage': i,
                            'title': stage_info['title'],
                            'prompt': stage_info['prompt'],
                            'result': result,
                            'raw_json': parsed_json
                        }]
                        st.session_state.batch_conversation_history.append({
                            "role": "user", 
                            "content": stage_info['prompt']
                        })
                        st.session_state.batch_conversation_history.append({
                            "role": "assistant", 
                            "content": result
                        })
                    total_runs = len(st.session_state.batch_results)
                    st.info(f"実行結果を更新しました（合計 {total_runs} 件）")
                    st.session_state.last_batch_result = result
                
                # 初回や未生成時の案内
                if not st.session_state.get('batch_results'):
                    st.info("「書いてみて」ボタンを押してコピーを生成してください")

        # --- 一括生成後のもう一声 ---
        if st.session_state.get('batch_results'):
            latest_batch = st.session_state.batch_results[-1]
            st.markdown("---")
            if st.button("💡 もう一声", key="batch_refine", type="primary"):
                orientation_for_refine = orientation  # batch mode orientation is local
                stage2_prompt = "どれも広告的で心が動かない、もっと強いメッセージが必要。使い古された言い回しを使わずに、定型的な構文は避けて。二十個のコピーを考えて"
                if 'main_display' not in st.session_state:
                    st.session_state.main_display = st.empty()
                result_placeholder = st.session_state.main_display
                result_placeholder.empty()
                result_placeholder.markdown("""<div class='skeleton'></div>""", unsafe_allow_html=True)
                with st.spinner("さらにコピーを磨いています..."):
                    formatted_refine, parsed_json_refine = generate_staged_copy(
                        orientation_for_refine,
                        stage2_prompt,
                        st.session_state.batch_conversation_history,
                        selected_model,
                        temperature,
                        stream_output=False,
                        stream_placeholder=result_placeholder
                    )
                    result_placeholder.markdown(f'<div class="copy-display">{formatted_refine}</div>', unsafe_allow_html=True)
                    st.session_state.last_batch_result = formatted_refine

                # 履歴更新
                refine_entry = {
                    'stage': latest_batch['stage'],
                    'title': f"{latest_batch['title']} - もう一声",
                    'prompt': stage2_prompt,
                    'result': formatted_refine,
                    'raw_json': parsed_json_refine
                }
                st.session_state.batch_results.append(refine_entry)
                # 会話履歴
                st.session_state.batch_conversation_history.append({
                    "role": "user",
                    "content": stage2_prompt
                })
                st.session_state.batch_conversation_history.append({
                    "role": "assistant",
                    "content": formatted_refine
                })
                total_runs = len(st.session_state.batch_results)
                st.info(f"実行結果を更新しました（合計 {total_runs} 件）")
                st.rerun()

st.sidebar.markdown("---")

# サイドバー - 管理者用機能のみ
st.sidebar.header("🔧 管理者機能")
if st.sidebar.checkbox("管理者モード", value=False):
    st.sidebar.markdown("---")
    st.sidebar.subheader("管理者設定")
    
    available_models = get_available_models()
    
    if st.sidebar.button("利用可能モデル一覧表示"):
        st.sidebar.write("📋 利用可能なモデル:")
        for model in available_models:
            st.sidebar.write(f"• {model}")
    
    if st.sidebar.button("モデル詳細情報表示"):
        model_categories = get_model_categories()
        for category, models in model_categories.items():
            st.sidebar.write(f"**{category}**")
            for model_id, model_data in models.items():
                if model_id in available_models:
                    st.sidebar.write(f"• {model_id}: {model_data['price']}")
    
    if st.sidebar.button("実行状態表示"):
        if generation_mode == "段階的生成":
            st.sidebar.json({
                "available_blocks": len(COPY_BLOCKS),
                "completed_executions": len(st.session_state.get('execution_results', [])),
                "conversation_length": len(st.session_state.get('conversation_history', [])),
                "independent_execution": True,
                "selected_model": selected_model
            })
        else:
            st.sidebar.info("段階的生成モードではありません")
        
    # API設定確認
    if OPENAI_API_KEY == "sk-proj-your-api-key-here":
        st.sidebar.warning("⚠️ デフォルトAPIキーが設定されています")
    else:
        st.sidebar.success("✅ APIキーが設定済み") 