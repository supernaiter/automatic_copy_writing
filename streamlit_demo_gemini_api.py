#!/usr/bin/env python3
"""
コピージェネレーター - Gemini API版
Google Gemini APIを使用した段階的コピー生成システム
"""

import streamlit as st
import os
from google import genai
import pandas as pd
from typing import List, Dict, Tuple

# Gemini APIキー設定
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "your-gemini-api-key-here")

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
    """利用可能なGeminiモデル一覧を取得"""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        models_list = genai.list_models()
        gemini_models = []
        for model in models_list:
            model_name = model.name.replace('models/', '')
            if 'gemini' in model_name.lower():
                gemini_models.append(model_name)
        return sorted(gemini_models, reverse=True)
    except Exception as e:
        st.sidebar.error(f"モデル取得エラー: {str(e)}")
        return get_default_models()

def get_default_models() -> List[str]:
    """デフォルトモデルリスト"""
    return [
        "gemini-2.5-flash-preview-05-20",
        "gemini-2.5-pro-preview-06-05", 
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-1.5-flash",
        "gemini-1.5-flash-8b",
        "gemini-1.5-pro"
    ]

def get_model_categories() -> Dict[str, Dict]:
    """モデル情報をカテゴリ別に整理"""
    return {
        "🧠 最新Gemini 2.5モデル（推奨）": {
            "gemini-2.5-flash-preview-05-20": {
                "price": "価格情報未公開",
                "description": "💰 最新Flash（高性能・低コスト・推奨）",
                "use_case": "コピーライティング、複雑な推論",
                "recommended": True,
                "note": "✅ 思考機能付き"
            },
            "gemini-2.5-pro-preview-06-05": {
                "price": "価格情報未公開",
                "description": "🧠 最高性能思考モデル",
                "use_case": "最重要プロジェクト、最高品質要求",
                "recommended": False,
                "note": "⚡ 高性能思考・推論"
            }
        },
        "🎯 Gemini 2.0モデル": {
            "gemini-2.0-flash": {
                "price": "$0.10/$0.40",
                "description": "🎯 次世代Flash（バランス型・安定）",
                "use_case": "一般的なコピー生成",
                "recommended": True,
                "note": "✅ マルチモーダル対応"
            },
            "gemini-2.0-flash-lite": {
                "price": "価格情報未公開",
                "description": "💨 軽量版2.0Flash（高速・低コスト）",
                "use_case": "大量処理、高速生成",
                "recommended": True,
                "note": "✅ 効率性重視"
            }
        },
        "🔧 Gemini 1.5モデル": {
            "gemini-1.5-flash": {
                "price": "$0.075/$0.30",
                "description": "🚀 1.5Flash（高速版）",
                "use_case": "高速処理が必要な場合",
                "recommended": False,
                "note": "✅ 実績のある安定モデル"
            },
            "gemini-1.5-flash-8b": {
                "price": "$0.0375/$0.15",
                "description": "💨 軽量Flash（最低コスト）",
                "use_case": "シンプルなタスク",
                "recommended": False,
                "note": "✅ 最安値オプション"
            },
            "gemini-1.5-pro": {
                "price": "$0.125/$0.50",
                "description": "🏆 1.5Pro（高性能）",
                "use_case": "複雑な推論タスク",
                "recommended": False,
                "note": "✅ 長いコンテキスト"
            }
        }
    }

def display_model_selector() -> Tuple[str, str]:
    """モデル選択UIを表示"""
    st.sidebar.header("🤖 Gemini モデル設定")
    
    available_models = get_available_models()
    model_categories = get_model_categories()
    
    selection_mode = st.sidebar.radio(
        "選択方式",
        ["カテゴリ別選択", "全モデル一覧"],
        help="推奨はカテゴリ別選択です"
    )
    
    selected_model = None
    model_info = ""
    
    if selection_mode == "カテゴリ別選択":
        st.sidebar.markdown("### 📋 モデルカテゴリ")
        
        for category, models in model_categories.items():
            with st.sidebar.expander(category, expanded=True):
                for model_id, model_data in models.items():
                    if model_id in available_models:
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
        
        if 'selected_model' in st.session_state:
            selected_model = st.session_state.selected_model
            model_info = st.session_state.get('model_info', '')
        else:
            if "gemini-2.5-flash-preview-05-20" in available_models:
                selected_model = "gemini-2.5-flash-preview-05-20"
                model_info = "💰 最新Flash（高性能・低コスト・推奨）"
            elif "gemini-2.0-flash" in available_models:
                selected_model = "gemini-2.0-flash"
                model_info = "🎯 次世代Flash（バランス型・安定）"
            else:
                selected_model = available_models[0]
                model_info = "選択されたモデルの詳細情報"
            st.session_state.selected_model = selected_model
            st.session_state.model_info = model_info
    
    else:
        default_index = 0
        if "gemini-2.5-flash-preview-05-20" in available_models:
            default_index = available_models.index("gemini-2.5-flash-preview-05-20")
        elif "gemini-2.0-flash" in available_models:
            default_index = available_models.index("gemini-2.0-flash")
        
        selected_model = st.sidebar.selectbox(
            "使用するモデルを選択",
            available_models,
            index=default_index
        )
        
        for category, models in model_categories.items():
            if selected_model in models:
                model_info = models[selected_model]['description']
                break
        else:
            model_info = "選択されたモデルの詳細情報"
    
    if selected_model:
        st.sidebar.success(f"✅ 選択中: **{selected_model}**")
        st.sidebar.info(model_info)
        
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
    """CSVから会話履歴を読み込み、Gemini API形式に変換"""
    if not csv_file:
        return []
        
    try:
        df = pd.read_csv(csv_file)
        df = df.dropna()
        messages = []
        
        for _, row in df.iterrows():
            role = "user" if row['side'] == 'human' else "model"
            content = str(row['prompt']).strip()
            
            if content and content != 'nan':
                messages.append({"role": role, "parts": [{"text": content}]})
        
        return messages
    except FileNotFoundError:
        st.warning(f"{csv_file} が見つかりません。履歴なしで続行します。")
        return []
    except Exception as e:
        st.error(f"履歴読み込みエラー: {str(e)}")
        return []

def generate_with_gemini(orientation: str, stage_prompt: str, conversation_messages: List[Dict], model: str = "gemini-2.0-flash", temperature: float = 0.9) -> str:
    """Gemini APIを使用してコピー生成"""
    genai.configure(api_key=GEMINI_API_KEY)
    
    try:
        gemini_model = genai.GenerativeModel(model)
        
        if conversation_messages:
            conversation_text = "\n\n".join([f"{msg['role']}: {msg['parts'][0]['text']}" for msg in conversation_messages])
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
        
        chat = gemini_model.start_chat(history=conversation_messages)
        
        # Gemini 2.5系モデルはtemperatureサポートが限定的
        supports_temperature = not any(x in model.lower() for x in ['2.5-pro', '2.5-flash'])
        
        generation_config = {}
        if supports_temperature:
            generation_config["temperature"] = temperature
            generation_config["max_output_tokens"] = 1200
        
        if generation_config:
            response = chat.send_message(user_message, generation_config=generation_config)
        else:
            response = chat.send_message(user_message)
        
        return response.text
            
    except Exception as e:
        error_msg = str(e)
        
        if "2.5" in model:
            st.warning(f"⚠️ {model}でエラーが発生しました: {error_msg}")
            fallback_model = "gemini-2.0-flash"
            st.info(f"🔄 {fallback_model}にフォールバックします。")
            return generate_with_gemini(orientation, stage_prompt, conversation_messages, fallback_model, temperature)
        
        return f"エラーが発生しました: {error_msg}"

# Streamlit UI設定
st.set_page_config(
    page_title="コピージェネレーター - Gemini版",
    page_icon="✏️",
    layout="wide"
)

st.title("✏️ コピージェネレーター - Gemini版")
st.markdown("段階的にコピーを改善していくシステムです。Google Gemini APIを使用しています。")
st.markdown("---")

# モデル選択
selected_model, model_info = display_model_selector()

st.sidebar.markdown("---")

# Temperature設定
st.sidebar.header("🌡️ 創造性設定")

supports_temperature = not any(x in selected_model.lower() for x in ['2.5-pro', '2.5-flash'])

if supports_temperature:
    temperature = st.sidebar.slider(
        "Temperature（創造性レベル）",
        min_value=0.0,
        max_value=1.5,
        value=1.2,
        step=0.1,
        help="0.0: 一貫性重視 ← → 1.5: 創造性重視"
    )
    
    if temperature <= 0.3:
        temp_desc = "🔒 非常に一貫性重視（決定論的）"
    elif temperature <= 0.6:
        temp_desc = "📋 やや保守的"
    elif temperature <= 1.0:
        temp_desc = "⚖️ バランス型"
    elif temperature <= 1.3:
        temp_desc = "🎨 創造性重視（推奨）"
    else:
        temp_desc = "⚠️ 非常に創造的（実験的・不安定）"

    st.sidebar.success(f"現在設定: **{temperature}** - {temp_desc}")
else:
    temperature = 1.0
    st.sidebar.info("⚠️ 選択されたモデルはTemperature設定をサポートしていません。")
    st.sidebar.markdown("**💡 Note:** Gemini 2.5モデルは内部で自動調整されます")

st.sidebar.markdown("---")

# 会話履歴設定
st.sidebar.header("📁 会話履歴設定")

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
    help="段階的生成：3段階で改善\n一括生成：従来の一度で生成"
)

# メインエリア
if generation_mode == "段階的生成":
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
        
        default_orientation = """【課題商品・サービスの訴求したいポイント】
ルイボスとグリーンルイボスの2種の茶葉をブレンドし、ルイボスティーらしい豊かな香り立ちがありながら、すっきりとした飲みやすさを実現。クセのあるイメージのルイボスティーですが、すっきりゴクゴク飲める味わいです。アレルギー特定原材料等28品目不使用、カフェインゼロなのに、ルイボスティーの豊かな香りですっきりリフレッシュ。仕事中、食中食後、喉が渇いたときなどさまざまなシーンでおすすめです。

【今回、募集する作品に期待すること】
「GREEN DA・KA・RA」は"やさしさ"を大事にした心とカラダにやさしいブランドです。数あるルイボスティーの中でも、「GREEN DA・KA・RA やさしいルイボス」を選びたくなる、やさしさのつまった表現アイディアを期待しています。

【制作にあたっての注意事項】
「GREEN DA・KA・RAブランドの愛嬌を大切にしながら表現を検討してください。今回のお題では、さまざまな生活シーンで水分補給をする20~30代男女をターゲットにします。"""
        
        orientation = st.text_area(
            "企業情報・課題・ターゲット等を入力してください",
            value=st.session_state.get('staged_orientation', default_orientation),
            height=300
        )
        
        st.markdown("### 🚀 段階的生成（並列実行可能）")
        
        completed_stages = len(st.session_state.staged_results)
        total_stages = len(STAGED_PROMPTS)
        st.markdown(f"**完了状況**: {completed_stages}/{total_stages} 段階完了")
        
        for i, stage_info in enumerate(STAGED_PROMPTS):
            stage_num = stage_info['stage']
            
            if stage_num in st.session_state.staged_results:
                button_label = f"🔄 {stage_info['title']} (再実行)"
                button_type = "secondary"
            else:
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
                        st.session_state.staged_orientation = orientation
                        
                        if not st.session_state.staged_conversation:
                            csv_file = selected_csv if selected_csv != "履歴なし" else None
                            initial_history = load_conversation_history(csv_file)
                            st.session_state.staged_conversation = initial_history.copy()
                        
                        with st.spinner(f"{stage_info['title']}を生成中... (使用モデル: {selected_model})"):
                            result = generate_with_gemini(
                                orientation, 
                                stage_info['prompt'], 
                                st.session_state.staged_conversation,
                                selected_model,
                                temperature
                            )
                            
                        st.session_state.staged_results[stage_num] = result
                        
                        # 会話履歴に追加
                        found_existing = False
                        for j, msg in enumerate(st.session_state.staged_conversation):
                            if (msg['role'] == 'user' and 
                                msg['parts'][0]['text'] == stage_info['prompt']):
                                if j + 1 < len(st.session_state.staged_conversation):
                                    st.session_state.staged_conversation[j + 1]['parts'][0]['text'] = result
                                else:
                                    st.session_state.staged_conversation.append({
                                        "role": "model", 
                                        "parts": [{"text": result}]
                                    })
                                found_existing = True
                                break
                        
                        if not found_existing:
                            st.session_state.staged_conversation.append({
                                "role": "user", 
                                "parts": [{"text": stage_info['prompt']}]
                            })
                            st.session_state.staged_conversation.append({
                                "role": "model", 
                                "parts": [{"text": result}]
                            })
                        
                        st.rerun()
            
            with col_desc:
                st.markdown(f"*{stage_info['description']}*")
        
        if len(st.session_state.staged_results) > 0:
            if st.button("🔄 段階的生成をリセット", type="secondary"):
                st.session_state.staged_results = {}
                st.session_state.staged_conversation = []
                st.session_state.staged_orientation = ""
                st.rerun()
    
    with col2:
        st.subheader("✨ 段階別生成結果")
        
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
                    
                    col_download, col_reflect = st.columns([1, 1])
                    
                    with col_download:
                        st.download_button(
                            label=f"📄 段階{stage_num}の結果をダウンロード",
                            data=result,
                            file_name=f"copy_stage_{stage_num}.txt",
                            mime="text/plain",
                            key=f"download_{stage_num}"
                        )
                    
                    with col_reflect:
                        if st.button(
                            f"🤔 段階{stage_num}を自省して再生成",
                            key=f"reflect_{stage_num}",
                            help="現在の結果を自省・改善してより良いコピーを生成します"
                        ):
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
                                reflected_result = generate_with_gemini(
                                    st.session_state.staged_orientation,
                                    reflect_prompt,
                                    st.session_state.staged_conversation,
                                    selected_model,
                                    temperature
                                )
                                
                                st.session_state.staged_results[stage_num] = reflected_result
                                
                                for i, msg in enumerate(st.session_state.staged_conversation):
                                    if (msg['role'] == 'model' and 
                                        i > 0 and 
                                        st.session_state.staged_conversation[i-1]['parts'][0]['text'] == stage_info['prompt']):
                                        st.session_state.staged_conversation[i]['parts'][0]['text'] = reflected_result
                                        break
                                
                                st.success(f"段階{stage_num}の自省再生成が完了しました！")
                                st.rerun()
            
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
    # 一括生成モード
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📋 オリエンテーション入力")
        
        default_orientation_simple = """【課題商品・サービスの訴求したいポイント】
ルイボスとグリーンルイボスの2種の茶葉をブレンドし、ルイボスティーらしい豊かな香り立ちがありながら、すっきりとした飲みやすさを実現。クセのあるイメージのルイボスティーですが、すっきりゴクゴク飲める味わいです。アレルギー特定原材料等28品目不使用、カフェインゼロなのに、ルイボスティーの豊かな香りですっきりリフレッシュ。仕事中、食中食後、喉が渇いたときなどさまざまなシーンでおすすめです。

【今回、募集する作品に期待すること】
「GREEN DA・KA・RA」は"やさしさ"を大事にした心とカラダにやさしいブランドです。数あるルイボスティーの中でも、「GREEN DA・KA・RA やさしいルイボス」を選びたくなる、やさしさのつまった表現アイディアを期待しています。"""
        
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
                csv_file = selected_csv if selected_csv != "履歴なし" else None
                conversation_history = load_conversation_history(csv_file)
                
                prompt = f"""
{orientation}

上記の情報を基に、効果的なキャッチコピーを5個作成してください。
"""
                
                with st.spinner(f"コピーを生成中... (使用モデル: {selected_model})"):
                    result = generate_with_gemini(orientation, prompt, conversation_history, selected_model, temperature)
                    
                st.success("生成完了！")
                st.text_area("生成されたコピー", value=result, height=400)
                
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

# 管理者機能
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
    if GEMINI_API_KEY == "your-gemini-api-key-here":
        st.sidebar.warning("⚠️ デフォルトAPIキーが設定されています")
    else:
        st.sidebar.success("✅ APIキーが設定済み") 