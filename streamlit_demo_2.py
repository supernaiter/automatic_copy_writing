#!/usr/bin/env python3
"""
コピージェネレーター
"""

import streamlit as st
import openai
import pandas as pd
from typing import List, Dict
import os

# 固定APIキー設定（環境変数から取得、なければデフォルト値）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-proj-your-api-key-here")

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

def generate_copy_ideas(orientation: str, csv_file: str = None, num_ideas: int = 5) -> str:
    """オリエンテーション + 会話履歴ベースのコピー生成"""
    openai.api_key = OPENAI_API_KEY
    
    # 会話履歴を読み込み
    conversation_history = load_conversation_history(csv_file)
    
    # システムメッセージを設定
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
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=1200,
            temperature=0.9
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# Streamlit UI
st.set_page_config(
    page_title="コピージェネレーター",
    page_icon="✏️",
    layout="wide"
)

st.markdown("---")

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
            
            with st.spinner("コピーを生成中..."):
                result = generate_copy_ideas(orientation, csv_file, 5)
                
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
    
    if st.sidebar.button("サンプルデータ表示"):
        st.sidebar.json({
            "total_generations": 42,
            "avg_generation_time": "3.2秒"
        })
        
    # API設定確認
    if OPENAI_API_KEY == "sk-proj-your-api-key-here":
        st.sidebar.warning("⚠️ デフォルトAPIキーが設定されています")
    else:
        st.sidebar.success("✅ APIキーが設定済み") 