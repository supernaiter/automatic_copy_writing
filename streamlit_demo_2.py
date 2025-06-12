#!/usr/bin/env python3
"""
コピージェネレーター
"""

import streamlit as st
import openai
import pandas as pd
from typing import List, Dict, Tuple
import os

# 固定APIキー設定（環境変数から取得、なければデフォルト値）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-proj-your-api-key-here")

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
            selected_model = "o3-mini" if "o3-mini" in available_models else available_models[0]
            model_info = "💰 最新推論モデル（高性能・低コスト・推奨）"
            st.session_state.selected_model = selected_model
            st.session_state.model_info = model_info
    
    else:
        # 全モデル一覧選択
        selected_model = st.sidebar.selectbox(
            "使用するモデルを選択",
            available_models,
            index=0 if "o3-mini" in available_models else 0
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

def generate_copy_ideas(orientation: str, csv_file: str = None, num_ideas: int = 5, model: str = "gpt-4o") -> str:
    """オリエンテーション + 会話履歴ベースのコピー生成"""
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
                temperature=0.9
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
    page_title="コピージェネレーター",
    page_icon="✏️",
    layout="wide"
)

st.markdown("---")

# モデル選択
selected_model, model_info = display_model_selector()

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

# メインエリア
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 オリエンテーション入力")
    
    # オリエンテーション入力エリア
    orientation = st.text_area(
        "企業情報・課題・ターゲット等を入力してください",
        placeholder="""例：
課題のポイント
今回、募集する作品に期待すること
当社はゴム素材を用いて、真に価値ある製品を提供する会社でありたいと考えています。

市場・ターゲットの動向
「好きなことを仕事にしたい」「やりがいや達成感を大切にしたい」と考えている就職・転職を考えている若年層がターゲットです。

課題商品・サービスの訴求したいポイント
ゴムは代替不可能な唯一の素材で、未来を創造する大きな可能性があることを表現してもらいたいです。""",
        height=200
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
                result = generate_copy_ideas(orientation, csv_file, 5, selected_model)
                
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
    
    if st.sidebar.button("サンプルデータ表示"):
        st.sidebar.json({
            "total_generations": 42,
            "avg_generation_time": "3.2秒",
            "current_model": selected_model,
            "available_models_count": len(available_models)
        })
        
    # API設定確認
    if OPENAI_API_KEY == "sk-proj-your-api-key-here":
        st.sidebar.warning("⚠️ デフォルトAPIキーが設定されています")
    else:
        st.sidebar.success("✅ APIキーが設定済み") 