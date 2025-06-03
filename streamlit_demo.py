#!/usr/bin/env python3
"""
カシワバラ・コーポレーション コピージェネレーター
Streamlit営業デモ版
"""

import streamlit as st
import openai
import pandas as pd
from typing import List, Dict
import os

def generate_copy_ideas(prompt: str, api_key: str, num_ideas: int = 5) -> str:
    """シンプルなコピー生成"""
    openai.api_key = api_key
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": """あなたは優秀なコピーライターです。
カシワバラ・コーポレーションの施工管理職採用用の短いキャッチコピーを作成してください。

参考例：
- 「新幹線が、地下で眠る場所を知ってる。」
- 「渋谷が、深呼吸する音を聴いてる。」
- 「街の心臓を診る特権。」

特徴：
- 短い（10-15文字程度）
- 都市の秘密・特権的視点
- 就活生の心に刺さる
- 施工管理の魅力を表現"""
                },
                {"role": "user", "content": f"{prompt}\n\n{num_ideas}個のキャッチコピーを作成してください。"}
            ],
            max_tokens=800,
            temperature=0.9
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# Streamlit UI
st.set_page_config(
    page_title="コピージェネレーター - カシワバラ・コーポレーション",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ カシワバラ・コーポレーション")
st.header("施工管理職採用 コピージェネレーター")
st.markdown("---")

# サイドバー - API設定
st.sidebar.header("⚙️ 設定")
api_key_input = st.sidebar.text_input(
    "OpenAI APIキー", 
    type="password",
    help="デモ用にAPIキーを入力してください"
)

# メインエリア
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("💭 アイデア入力")
    
    # プリセット選択肢
    preset_prompts = {
        "都市の秘密": "都市の見えない部分や秘密を知る特権的立場を表現したコピー",
        "時間軸": "未来への影響や瞬間の価値を表現したコピー", 
        "感覚表現": "音や触感、空気感を使った感覚的なコピー",
        "対比構造": "地上と地下、見える世界と見えない世界の対比を使ったコピー",
        "感情表現": "誇りや達成感、使命感を表現したコピー",
        "カスタム": "独自のアイデアを入力"
    }
    
    selected_preset = st.selectbox("アプローチを選択", list(preset_prompts.keys()))
    
    if selected_preset == "カスタム":
        user_prompt = st.text_area(
            "カスタムプロンプト",
            placeholder="どんなコピーを作りたいですか？",
            height=100
        )
    else:
        user_prompt = preset_prompts[selected_preset]
        st.text_area("選択されたアプローチ", value=user_prompt, height=100, disabled=True)
    
    num_ideas = st.slider("生成するアイデア数", 3, 10, 5)
    
    generate_button = st.button("🚀 コピー生成", type="primary")

with col2:
    st.subheader("✨ 生成結果")
    
    if generate_button:
        if not api_key_input:
            st.error("APIキーを入力してください")
        elif not user_prompt:
            st.error("プロンプトを入力してください")
        else:
            with st.spinner("コピーを生成中..."):
                result = generate_copy_ideas(user_prompt, api_key_input, num_ideas)
                
            st.success("生成完了！")
            st.text_area("生成されたコピー", value=result, height=400)
            
            # ダウンロードボタン
            st.download_button(
                label="📄 結果をダウンロード",
                data=result,
                file_name="copy_ideas.txt",
                mime="text/plain"
            )

# フッター情報
st.markdown("---")
st.markdown("### 📋 使用例")

example_col1, example_col2, example_col3 = st.columns(3)

with example_col1:
    st.markdown("""
    **都市の秘密アプローチ**
    - 新幹線が、地下で眠る場所を知ってる。
    - 街の心臓を診る特権。
    - 地下世界の設計者。
    """)

with example_col2:
    st.markdown("""
    **感覚表現アプローチ**
    - 渋谷が、深呼吸する音を聴いてる。
    - 東京の体温を、はかってる。
    - 駅の、産声を聴く。
    """)

with example_col3:
    st.markdown("""
    **対比構造アプローチ**
    - 見えない基盤で、街の景色を描く。
    - 静かに街を、影から守る。
    - 未来の街を、いま築く。
    """)

st.markdown("---")
st.markdown("""
**💡 このツールについて**
- AI（GPT-4o）を活用したコピー生成システム
- カシワバラ・コーポレーション施工管理職採用特化
- リアルタイムでバリエーション豊富なアイデア創出
""")

# 隠し機能 - 管理者用
if st.sidebar.checkbox("🔧 管理者モード", value=False):
    st.sidebar.markdown("---")
    st.sidebar.subheader("管理者設定")
    
    if st.sidebar.button("サンプルデータ表示"):
        st.sidebar.json({
            "total_generations": 42,
            "most_popular_approach": "都市の秘密",
            "avg_generation_time": "2.3秒"
        }) 