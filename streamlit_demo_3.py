#!/usr/bin/env python3
"""
コピージェネレーター - 段階的生成対応版
"""

import streamlit as st
import openai
import pandas as pd
from typing import List, Dict, Tuple
import os

# APIキー設定（Streamlit Secrets対応）
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except:
    # ローカル開発時は環境変数から取得
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-proj-your-api-key-here")

# 段階的生成用のプロンプト定義
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
        "gpt-4.1",
        "o3-mini",
        "o1-pro", 
        "o1-mini",
        "o1-preview",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4"
    ]

def get_model_categories() -> Dict[str, Dict]:
    """モデル情報をカテゴリ別に整理"""
    return {
        "🧠 推論特化モデル（推奨）": {
            "o3-mini": {
                "price": "$1.10/$4.40",
                "description": "💰 最新推論モデル（高性能・低コスト・推奨）",
                "use_case": "コピーライティング、複雑な推論",
                "recommended": True,
                "note": "✅ Chat Completions API対応 (temperature非対応)"
            },
            "o1-pro": {
                "price": "$150/$600",
                "description": "🧠 最高性能推論モデル（極めて高価）",
                "use_case": "最重要プロジェクト、最高品質要求",
                "recommended": False,
                "note": "⚠️ Responses APIのみ対応 (特別な実装)"
            },
            "o1-mini": {
                "price": "$3/$12",
                "description": "⚡ 高速推論モデル（バランス型）",
                "use_case": "一般的な推論タスク",
                "recommended": False,
                "note": "✅ Chat Completions API対応 (temperature非対応)"
            },
            "o1-preview": {
                "price": "$15/$60",
                "description": "🔬 プレビュー版推論モデル",
                "use_case": "テスト・実験用",
                "recommended": False,
                "note": "✅ Chat Completions API対応 (temperature非対応)"
            }
        },
        "🎯 標準GPTモデル": {
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
            "gpt-4-turbo": {
                "price": "$10/$30",
                "description": "🚀 GPT-4ターボ（高速版）",
                "use_case": "高速処理が必要な場合",
                "recommended": False,
                "note": "✅ Chat Completions API対応 (全パラメータ)"
            },
            "gpt-4": {
                "price": "$30/$60",
                "description": "🏆 標準GPT-4",
                "use_case": "基本的なタスク",
                "recommended": False,
                "note": "✅ Chat Completions API対応 (全パラメータ)"
            }
        },
        "🔮 最新実験モデル": {
            "o3-pro": {
                "price": "$20/$80",
                "description": "🔮 最上位推論モデル（実験版）",
                "use_case": "最高品質が必要な場合",
                "recommended": False,
                "note": "⚠️ 限定的対応・要検証"
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
            if "gpt-4.1" in available_models:
                selected_model = "gpt-4.1"
                model_info = "🆕 次世代GPT（ベータ版）"
            elif "gpt-4o" in available_models:
                selected_model = "gpt-4o"
                model_info = "🎯 最新GPT-4（バランス型・安定）"
            elif "o3-mini" in available_models:
                selected_model = "o3-mini"
                model_info = "💰 最新推論モデル（高性能・低コスト・推奨）"
            else:
                selected_model = available_models[0]
                model_info = "選択されたモデルの詳細情報"
            st.session_state.selected_model = selected_model
            st.session_state.model_info = model_info
    
    else:
        # 全モデル一覧選択
        # デフォルトのインデックスを決定
        default_index = 0
        if "gpt-4.1" in available_models:
            default_index = available_models.index("gpt-4.1")
        elif "gpt-4o" in available_models:
            default_index = available_models.index("gpt-4o")
        elif "o3-mini" in available_models:
            default_index = available_models.index("o3-mini")
        
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

def generate_staged_copy(orientation: str, stage_prompt: str, conversation_messages: List[Dict], model: str = "gpt-4o", temperature: float = 0.9) -> str:
    """段階的コピー生成"""
    openai.api_key = OPENAI_API_KEY
    
    # モデル種別を判定
    is_o1_pro = "o1-pro" in model.lower()
    is_o3_or_o1_other = any(prefix in model.lower() for prefix in ['o1-', 'o3-']) and not is_o1_pro
    
    try:
        if is_o1_pro:
            # o1-proはResponses APIのみ対応
            if conversation_messages:
                # 過去の会話があれば含める
                conversation_text = "\n\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_messages])
                user_message = f"""
{orientation}

過去の会話:
{conversation_text}

{stage_prompt}
"""
            else:
                user_message = f"""
{orientation}

{stage_prompt}
"""
            
            response = openai.responses.create(
                model=model,
                input=user_message,
                reasoning={"effort": "high"}
            )
            return response.choices[0].message.content
            
        elif is_o3_or_o1_other:
            # その他の推論モデル用の処理
            if conversation_messages:
                # 過去の会話があれば含める
                conversation_text = "\n\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_messages])
                user_message = f"""
{orientation}

過去の会話:
{conversation_text}

{stage_prompt}
"""
            else:
                user_message = f"""
{orientation}

{stage_prompt}
"""
            
            messages = [{"role": "user", "content": user_message}]
            
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_completion_tokens=1200
            )
            return response.choices[0].message.content
        
        else:
            # 標準GPTモデル用の処理
            system_message = {
                "role": "system", 
                "content": """あなたは優秀なコピーライターです。
段階的にコピーを改善していきます。これまでの会話履歴を踏まえて、指示に従ってコピーを作成・改善してください。"""
            }
            
            # 新しいユーザーメッセージを追加
            new_user_message = {
                "role": "user", 
                "content": f"""
{orientation}

{stage_prompt}
"""
            }
            
            # メッセージ配列を構築（システム + 過去の会話 + 新しいメッセージ）
            messages = [system_message] + conversation_messages + [new_user_message]
            
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=1200,
                temperature=temperature
            )
            return response.choices[0].message.content
            
    except Exception as e:
        error_msg = str(e)
        
        # エラー時のフォールバック処理
        if is_o1_pro:
            st.warning(f"⚠️ {model}でエラーが発生しました: {error_msg}")
            fallback_model = "o3-mini"
            st.info(f"🔄 {fallback_model}にフォールバックします。")
            return generate_staged_copy(orientation, stage_prompt, conversation_messages, fallback_model)
        
        elif is_o3_or_o1_other:
            st.warning(f"⚠️ {model}でエラーが発生しました: {error_msg}")
            fallback_model = "gpt-4o"
            st.info(f"🔄 {fallback_model}にフォールバックします。")
            return generate_staged_copy(orientation, stage_prompt, conversation_messages, fallback_model)
        
        else:
            return f"エラーが発生しました: {error_msg}"

def generate_copy_ideas(orientation: str, csv_file: str = None, num_ideas: int = 5, model: str = "gpt-4o", temperature: float = 0.9) -> str:
    """オリエンテーション + 会話履歴ベースのコピー生成（従来版）"""
    openai.api_key = OPENAI_API_KEY
    
    # 会話履歴を読み込み
    conversation_history = load_conversation_history(csv_file)
    
    # モデル種別を判定
    is_o1_pro = "o1-pro" in model.lower()
    is_o3_or_o1_other = any(prefix in model.lower() for prefix in ['o1-', 'o3-']) and not is_o1_pro
    
    try:
        if is_o1_pro:
            # o1-proはResponses APIのみ対応
            user_message = f"""
{orientation}

上記の情報を基に、効果的なキャッチコピーを{num_ideas}個作成してください。
"""
            
            response = openai.responses.create(
                model=model,
                input=user_message,
                reasoning={"effort": "high"}  # o1-pro用のパラメータ
            )
            # Responses APIの正しいレスポンス形式
            return response.choices[0].message.content
            
        elif is_o3_or_o1_other:
            # その他の推論モデル（o1、o3-mini等）用の処理
            user_message = f"""
{orientation}

上記の情報を基に、効果的なキャッチコピーを{num_ideas}個作成してください。
"""
            
            # 推論モデルは履歴を含めず、シンプルなメッセージのみ
            messages = [{"role": "user", "content": user_message}]
            
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_completion_tokens=1200
                # temperatureパラメータは推論モデルでサポートされていない
            )
            return response.choices[0].message.content
        
        else:
            # 標準GPTモデル用の処理
            system_message = {
                "role": "system", 
                "content": """あなたは優秀なコピーライターです。
これまでの会話履歴を踏まえて、与えられたオリエンテーション情報を活用し、効果的なキャッチコピーを作成してください。

出力は簡潔で、インパクトがあり、ターゲットに刺さるものを5個厳選してください。
コピーのみを出力してください。"""
            }
            
            # 新しいユーザーメッセージを追加
            new_user_message = {
                "role": "user", 
                "content": f"""
{orientation}

最終的に{num_ideas}個の厳選されたキャッチコピーを出力してください。
"""
            }
            
            # メッセージ配列を構築
            messages = [system_message] + conversation_history + [new_user_message]
            
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=1200,
                temperature=temperature
            )
            return response.choices[0].message.content
            
    except Exception as e:
        error_msg = str(e)
        
        # o1-proでエラーが発生した場合の特別な処理
        if is_o1_pro:
            st.warning(f"⚠️ {model}でエラーが発生しました。Responses API要求: {error_msg}")
            fallback_model = "o3-mini"
            st.info(f"🔄 {fallback_model}にフォールバックします。")
            return generate_copy_ideas(orientation, csv_file, num_ideas, fallback_model)
        
        # その他の推論モデルでエラーの場合
        elif is_o3_or_o1_other:
            st.warning(f"⚠️ {model}でエラーが発生しました: {error_msg}")
            fallback_model = "gpt-4o"
            st.info(f"🔄 {fallback_model}にフォールバックします。")
            return generate_copy_ideas(orientation, csv_file, num_ideas, fallback_model)
        
        else:
            return f"エラーが発生しました: {error_msg}"

# Streamlit UI
st.set_page_config(
    page_title="コピージェネレーター - 段階的生成",
    page_icon="✏️",
    layout="wide"
)

st.title("✏️ コピージェネレーター - 段階的生成")
st.markdown("段階的にコピーを改善していくシステムです。各段階の結果が蓄積されます。")

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
    step=0.1,
    help="0.0: 一貫性重視 ← → 1.5: 創造性重視（1.5以上は推奨しません）"
)

# Temperature説明
if temperature <= 0.3:
    temp_desc = "🔒 非常に一貫性重視（決定論的）"
    temp_color = "info"
elif temperature <= 0.6:
    temp_desc = "📋 やや保守的"
    temp_color = "info"
elif temperature <= 1.0:
    temp_desc = "⚖️ バランス型"
    temp_color = "success"
elif temperature <= 1.3:
    temp_desc = "🎨 創造性重視（推奨）"
    temp_color = "success"
else:
    temp_desc = "⚠️ 非常に創造的（実験的・不安定）"
    temp_color = "warning"

if temp_color == "warning":
    st.sidebar.warning(f"現在設定: **{temperature}** - {temp_desc}")
elif temp_color == "success":
    st.sidebar.success(f"現在設定: **{temperature}** - {temp_desc}")
else:
    st.sidebar.info(f"現在設定: **{temperature}** - {temp_desc}")

# 高いTemperatureの警告
if temperature > 1.4:
    st.sidebar.error("⚠️ **警告**: Temperature 1.4以上では意味不明な文字列が生成される可能性があります！")
    
# 推奨設定の案内
st.sidebar.markdown("**💡 推奨設定:**")
st.sidebar.markdown("• コピーライティング: 0.8 - 1.2")
st.sidebar.markdown("• 創造的作業: 1.0 - 1.3")
st.sidebar.markdown("• 一貫性重視: 0.3 - 0.7")

st.sidebar.markdown("---")

# サイドバー - 会話履歴設定
st.sidebar.header("📁 会話履歴設定")

# CSVファイル一覧を取得
csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
csv_options = ["履歴なし"] + csv_files

selected_csv = st.sidebar.selectbox(
    "会話履歴ファイルを選択",
    csv_options,
    index=1 if "interaction_copy_focused.csv" in csv_files else 0
)

# 生成モード選択
st.sidebar.markdown("---")
st.sidebar.header("🎛️ 生成モード")
generation_mode = st.sidebar.radio(
    "モードを選択",
    ["段階的生成", "一括生成"],
    help="段階的生成：4段階で改善\n一括生成：従来の一度で生成"
)

# メインエリア
if generation_mode == "段階的生成":
    # 段階的生成モード
    
    # セッション状態の初期化
    if 'staged_results' not in st.session_state:
        st.session_state.staged_results = {}
    if 'staged_conversation' not in st.session_state:
        st.session_state.staged_conversation = []
    if 'staged_orientation' not in st.session_state:
        st.session_state.staged_orientation = ""
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📋 オリエンテーション入力")
        
        # デフォルトのオリエンテーション
        default_orientation = """【課題商品・サービスの訴求したいポイント】
ルイボスとグリーンルイボスの2種の茶葉をブレンドし、ルイボスティーらしい豊かな香り立ちがありながら、すっきりとした飲みやすさを実現。クセのあるイメージのルイボスティーですが、すっきりゴクゴク飲める味わいです。アレルギー特定原材料等28品目不使用、カフェインゼロなのに、ルイボスティーの豊かな香りですっきりリフレッシュ。仕事中、食中食後、喉が渇いたときなどさまざまなシーンでおすすめです。

【今回、募集する作品に期待すること】
「GREEN DA・KA・RA」は"やさしさ"を大事にした心とカラダにやさしいブランドです。数あるルイボスティーの中でも、「GREEN DA・KA・RA やさしいルイボス」を選びたくなる、やさしさのつまった表現アイディアを期待しています。

【制作にあたっての注意事項】
「GREEN DA・KA・RAブランドの愛嬌を大切にしながら表現を検討してください。「GREEN DA・KA・RA」は"やさしさ"を大事にした心とカラダにやさしいブランドです。数あるルイボスティーの中でも、「GREEN DA・KA・RA やさしいルイボス」を選びたくなる、やさしさのつまった表現アイデアを期待しています。今回のお題では、さまざまな生活シーンで水分補給をする20~30代男女をターゲットにします。ルイボスとグリーンルイボスの2種の茶葉をブレンドし、ルイボスティーらしい豊かな香り立ちがありながら、すっきりとした飲みやすさを実現。クセのあるイメージのルイボスティーですが、すっきりゴクゴク飲める味わいです。アレルギー特定原材料等28品目不使用、カフェインゼロなのに、ルイボスティーの豊かな香りですっきりリフレッシュ。仕事中、食中食後、喉が渇いたときなどさまざまなシーンでおすすめです。「GREEN DA・KA・RA」ブランドの愛嬌を大切にしながら表現を検討してください。"""
        
        # オリエンテーション入力エリア
        orientation = st.text_area(
            "企業情報・課題・ターゲット等を入力してください",
            value=st.session_state.get('staged_orientation', default_orientation),
            height=300
        )
        
        # 段階的生成の進行状況
        st.markdown("### 🚀 段階的生成（並列実行可能）")
        
        # 完了状況を表示
        completed_stages = len(st.session_state.staged_results)
        total_stages = len(STAGED_PROMPTS)
        st.markdown(f"**完了状況**: {completed_stages}/{total_stages} 段階完了")
        
        # 各段階のボタン（すべていつでも実行可能）
        for i, stage_info in enumerate(STAGED_PROMPTS):
            stage_num = stage_info['stage']
            
            # ボタンの状態を決定（すべて実行可能）
            if stage_num in st.session_state.staged_results:
                # 既に実行済み
                button_label = f"🔄 {stage_info['title']} (再実行)"
                button_type = "secondary"
            else:
                # 未実行
                button_label = f"▶️ {stage_info['title']}"
                button_type = "primary"
            
            col_btn, col_desc = st.columns([1, 2])
            with col_btn:
                if st.button(
                    button_label,
                    key=f"stage_{stage_num}",
                    type=button_type
                ):
                    if not orientation:
                        st.error("オリエンテーションを入力してください")
                    else:
                        # オリエンテーションを保存
                        st.session_state.staged_orientation = orientation
                        
                        # 選択されたCSVファイルから初期履歴を読み込み（初回のみ）
                        if not st.session_state.staged_conversation:
                            csv_file = selected_csv if selected_csv != "履歴なし" else None
                            initial_history = load_conversation_history(csv_file)
                            st.session_state.staged_conversation = initial_history.copy()
                        
                        with st.spinner(f"{stage_info['title']}を生成中... (使用モデル: {selected_model})"):
                            result = generate_staged_copy(
                                orientation, 
                                stage_info['prompt'], 
                                st.session_state.staged_conversation,
                                selected_model,
                                temperature
                            )
                            
                        # 結果を保存
                        st.session_state.staged_results[stage_num] = result
                        
                        # 会話履歴に追加または更新
                        # 既存の同じプロンプトがあるかチェック
                        found_existing = False
                        for j, msg in enumerate(st.session_state.staged_conversation):
                            if (msg['role'] == 'user' and 
                                msg['content'] == stage_info['prompt']):
                                # 既存のプロンプト見つかった場合、次のassistant応答を更新
                                if j + 1 < len(st.session_state.staged_conversation):
                                    st.session_state.staged_conversation[j + 1]['content'] = result
                                else:
                                    st.session_state.staged_conversation.append({
                                        "role": "assistant", 
                                        "content": result
                                    })
                                found_existing = True
                                break
                        
                        if not found_existing:
                            # 新しいプロンプトの場合、追加
                            st.session_state.staged_conversation.append({
                                "role": "user", 
                                "content": stage_info['prompt']
                            })
                            st.session_state.staged_conversation.append({
                                "role": "assistant", 
                                "content": result
                            })
                        
                        st.rerun()
            
            with col_desc:
                st.markdown(f"*{stage_info['description']}*")
        
        # リセットボタン
        if len(st.session_state.staged_results) > 0:
            if st.button("🔄 段階的生成をリセット", type="secondary"):
                st.session_state.staged_results = {}
                st.session_state.staged_conversation = []
                st.session_state.staged_orientation = ""
                st.rerun()
    
    with col2:
        st.subheader("✨ 段階別生成結果")
        
        # 各段階の結果を表示
        if st.session_state.staged_results:
            for stage_num, result in st.session_state.staged_results.items():
                stage_info = STAGED_PROMPTS[stage_num - 1]
                
                with st.expander(f"{stage_info['title']} の結果", expanded=True):
                    st.markdown(f"**プロンプト**: {stage_info['prompt']}")
                    st.markdown("---")
                    st.text_area(
                        f"生成結果 - 段階 {stage_num}",
                        value=result,
                        height=300,
                        key=f"result_display_{stage_num}"
                    )
                    
                    # ボタンを横並びで配置
                    col_download, col_reflect = st.columns([1, 1])
                    
                    with col_download:
                        # 個別ダウンロードボタン
                        st.download_button(
                            label=f"📄 段階{stage_num}の結果をダウンロード",
                            data=result,
                            file_name=f"copy_stage_{stage_num}.txt",
                            mime="text/plain",
                            key=f"download_{stage_num}"
                        )
                    
                    with col_reflect:
                        # 自省再生成ボタン
                        if st.button(
                            f"🤔 段階{stage_num}を自省して再生成",
                            key=f"reflect_{stage_num}",
                            help="現在の結果を自省・改善してより良いコピーを生成します"
                        ):
                            # 自省プロンプトを作成
                            reflect_prompt = f"""
これまでの結果を自省してください：

{result}

上記の結果を客観的に分析し、以下の観点から改善してください：
1. より印象的で記憶に残るか
2. ターゲットに刺さる表現になっているか  
3. 独創性と説得力のバランスは適切か
4. 簡潔で力強いメッセージになっているか

自省の結果を踏まえ、改善されたコピーを生成してください。
"""
                            
                            with st.spinner(f"段階{stage_num}を自省して再生成中... (使用モデル: {selected_model})"):
                                # 自省による再生成
                                reflected_result = generate_staged_copy(
                                    st.session_state.staged_orientation,
                                    reflect_prompt,
                                    st.session_state.staged_conversation,
                                    selected_model,
                                    temperature
                                )
                                
                                # 結果を更新
                                st.session_state.staged_results[stage_num] = reflected_result
                                
                                # 会話履歴も更新（最新の結果で置き換え）
                                # 該当段階のassistant応答を探して更新
                                for i, msg in enumerate(st.session_state.staged_conversation):
                                    if (msg['role'] == 'assistant' and 
                                        i > 0 and 
                                        st.session_state.staged_conversation[i-1]['content'] == stage_info['prompt']):
                                        st.session_state.staged_conversation[i]['content'] = reflected_result
                                        break
                                
                                st.success(f"段階{stage_num}の自省再生成が完了しました！")
                                st.rerun()
            
            # 全結果の統合ダウンロード
            if len(st.session_state.staged_results) > 0:
                st.markdown("---")
                all_results = ""
                for stage_num in sorted(st.session_state.staged_results.keys()):
                    stage_info = STAGED_PROMPTS[stage_num - 1]
                    result = st.session_state.staged_results[stage_num]
                    all_results += f"=== {stage_info['title']} ===\n"
                    all_results += f"プロンプト: {stage_info['prompt']}\n\n"
                    all_results += f"{result}\n\n"
                    all_results += "=" * 50 + "\n\n"
                
                st.download_button(
                    label="📦 全段階の結果をダウンロード",
                    data=all_results,
                    file_name="copy_all_stages.txt",
                    mime="text/plain",
                    type="primary"
                )
        else:
            st.info("オリエンテーションを入力して、段階的生成を開始してください。")

else:
    # 一括生成モード（従来版）
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📋 オリエンテーション入力")
        
        # デフォルトのオリエンテーション
        default_orientation_simple = """【課題商品・サービスの訴求したいポイント】
ルイボスとグリーンルイボスの2種の茶葉をブレンドし、ルイボスティーらしい豊かな香り立ちがありながら、すっきりとした飲みやすさを実現。クセのあるイメージのルイボスティーですが、すっきりゴクゴク飲める味わいです。アレルギー特定原材料等28品目不使用、カフェインゼロなのに、ルイボスティーの豊かな香りですっきりリフレッシュ。仕事中、食中食後、喉が渇いたときなどさまざまなシーンでおすすめです。

【今回、募集する作品に期待すること】
「GREEN DA・KA・RA」は"やさしさ"を大事にした心とカラダにやさしいブランドです。数あるルイボスティーの中でも、「GREEN DA・KA・RA やさしいルイボス」を選びたくなる、やさしさのつまった表現アイディアを期待しています。

【制作にあたっての注意事項】
「GREEN DA・KA・RAブランドの愛嬌を大切にしながら表現を検討してください。「GREEN DA・KA・RA」は"やさしさ"を大事にした心とカラダにやさしいブランドです。数あるルイボスティーの中でも、「GREEN DA・KA・RA やさしいルイボス」を選びたくなる、やさしさのつまった表現アイデアを期待しています。今回のお題では、さまざまな生活シーンで水分補給をする20~30代男女をターゲットにします。ルイボスとグリーンルイボスの2種の茶葉をブレンドし、ルイボスティーらしい豊かな香り立ちがありながら、すっきりとした飲みやすさを実現。クセのあるイメージのルイボスティーですが、すっきりゴクゴク飲める味わいです。アレルギー特定原材料等28品目不使用、カフェインゼロなのに、ルイボスティーの豊かな香りですっきりリフレッシュ。仕事中、食中食後、喉が渇いたときなどさまざまなシーンでおすすめです。「GREEN DA・KA・RA」ブランドの愛嬌を大切にしながら表現を検討してください。"""
        
        # オリエンテーション入力エリア
        orientation = st.text_area(
            "企業情報・課題・ターゲット等を入力してください",
            value=default_orientation_simple,
            height=300
        )
        
        generate_button = st.button("🚀 コピー生成", type="primary")

    with col2:
        st.subheader("✨ 生成結果")
        
        if generate_button:
            if not orientation:
                st.error("オリエンテーションを入力してください")
            else:
                # 選択されたCSVファイルを使用
                csv_file = selected_csv if selected_csv != "履歴なし" else None
                
                with st.spinner(f"コピーを生成中... (使用モデル: {selected_model})"):
                    result = generate_copy_ideas(orientation, csv_file, 5, selected_model, temperature)
                    
                st.success("生成完了！")
                st.text_area("生成されたコピー", value=result, height=400)
                
                # ダウンロードボタン
                st.download_button(
                    label="📄 結果をダウンロード",
                    data=result,
                    file_name="copy_ideas.txt",
                    mime="text/plain"
                )

# 選択されたファイルの情報を表示
if selected_csv != "履歴なし":
    try:
        df = pd.read_csv(selected_csv)
        st.sidebar.info(f"📊 履歴: {len(df)}件のメッセージ")
    except:
        st.sidebar.error("ファイル読み込みエラー")

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
    
    if st.sidebar.button("段階的生成状態表示"):
        if generation_mode == "段階的生成":
            st.sidebar.json({
                "total_stages": len(STAGED_PROMPTS),
                "completed_stages": len(st.session_state.get('staged_results', {})),
                "conversation_length": len(st.session_state.get('staged_conversation', [])),
                "parallel_execution": True,
                "selected_model": selected_model
            })
        else:
            st.sidebar.info("段階的生成モードではありません")
        
    # API設定確認
    if OPENAI_API_KEY == "sk-proj-your-api-key-here":
        st.sidebar.warning("⚠️ デフォルトAPIキーが設定されています")
    else:
        st.sidebar.success("✅ APIキーが設定済み") 