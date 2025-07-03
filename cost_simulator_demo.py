#!/usr/bin/env python3
"""
展示用コストシミュレータ
常時生成し続ける場合のコスト予測に特化
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json

# ページ設定
st.set_page_config(
    page_title="展示用コストシミュレータ",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# モデル料金設定
MODEL_PRICING = {
    "gpt-4o": {
        "input_per_million": 2.50,
        "output_per_million": 10.00,
        "description": "GPT-4o（標準）"
    },
    "gpt-4o-mini": {
        "input_per_million": 0.15,
        "output_per_million": 0.60,
        "description": "GPT-4o-mini（軽量）"
    },
    "gpt-4.1": {
        "input_per_million": 2.00,
        "output_per_million": 8.00,
        "description": "GPT-4.1（ベータ）"
    },
    "gpt-4.1-mini": {
        "input_per_million": 0.15,
        "output_per_million": 0.60,
        "description": "GPT-4.1-mini（ベータ）"
    },
    "gpt-3.5-turbo": {
        "input_per_million": 0.50,
        "output_per_million": 1.50,
        "description": "GPT-3.5-turbo（経済的）"
    }
}

# セッション状態の初期化
if 'simulation_data' not in st.session_state:
    st.session_state.simulation_data = []
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

def calculate_cost(prompt_tokens, completion_tokens, model):
    """コスト計算"""
    if model not in MODEL_PRICING:
        return 0.0
    
    pricing = MODEL_PRICING[model]
    input_cost = (prompt_tokens / 1_000_000) * pricing['input_per_million']
    output_cost = (completion_tokens / 1_000_000) * pricing['output_per_million']
    return input_cost + output_cost

def generate_simulation_data(model, avg_prompt_tokens, avg_completion_tokens, interval_seconds):
    """シミュレーションデータ生成"""
    current_time = datetime.now()
    
    # ランダムな変動を加えたトークン数
    import random
    prompt_tokens = int(avg_prompt_tokens * random.uniform(0.8, 1.2))
    completion_tokens = int(avg_completion_tokens * random.uniform(0.8, 1.2))
    
    cost = calculate_cost(prompt_tokens, completion_tokens, model)
    
    return {
        'timestamp': current_time,
        'model': model,
        'prompt_tokens': prompt_tokens,
        'completion_tokens': completion_tokens,
        'total_tokens': prompt_tokens + completion_tokens,
        'cost_usd': cost,
        'interval_seconds': interval_seconds
    }

def run_simulation():
    """シミュレーション実行"""
    while st.session_state.is_running:
        # 現在の設定を取得
        model = st.session_state.current_model
        avg_prompt = st.session_state.avg_prompt_tokens
        avg_completion = st.session_state.avg_completion_tokens
        interval = st.session_state.interval_seconds
        
        # データ生成
        data = generate_simulation_data(model, avg_prompt, avg_completion, interval)
        st.session_state.simulation_data.append(data)
        
        # 指定間隔で待機
        time.sleep(interval)
        
        # ページ更新
        st.rerun()

# メインUI
st.title("💰 展示用コストシミュレータ")
st.markdown("### 常時生成し続ける場合のコスト予測")

# サイドバー設定
st.sidebar.header("⚙️ シミュレーション設定")

# モデル選択
selected_model = st.sidebar.selectbox(
    "使用モデル",
    list(MODEL_PRICING.keys()),
    format_func=lambda x: f"{x} - {MODEL_PRICING[x]['description']}"
)

# トークン数設定
st.sidebar.subheader("📊 トークン数設定")
avg_prompt_tokens = st.sidebar.number_input(
    "平均入力トークン数",
    min_value=100,
    max_value=10000,
    value=3000,
    step=100
)

avg_completion_tokens = st.sidebar.number_input(
    "平均出力トークン数", 
    min_value=100,
    max_value=10000,
    value=2000,
    step=100
)

# 生成間隔
st.sidebar.subheader("⏱️ 生成間隔")
interval_seconds = st.sidebar.slider(
    "生成間隔（秒）",
    min_value=0.1,
    max_value=10.0,
    value=5.0,
    step=0.1
)

# 予測期間
st.sidebar.subheader("📅 予測期間")
prediction_hours = st.sidebar.slider(
    "予測期間（時間）",
    min_value=1,
    max_value=24,
    value=8,
    step=1
)

# コスト情報表示
st.sidebar.markdown("---")
st.sidebar.subheader("💰 現在の料金")
if selected_model in MODEL_PRICING:
    pricing = MODEL_PRICING[selected_model]
    st.sidebar.info(f"""
    **{selected_model}**
    - 入力: ${pricing['input_per_million']:.2f}/1M tokens
    - 出力: ${pricing['output_per_million']:.2f}/1M tokens
    """)

# 1回あたりのコスト計算
single_cost = calculate_cost(avg_prompt_tokens, avg_completion_tokens, selected_model)
st.sidebar.metric("1回あたりのコスト", f"${single_cost:.4f}")

# 時間あたりの予測コスト
generations_per_hour = 3600 / interval_seconds
hourly_cost = single_cost * generations_per_hour
st.sidebar.metric("時間あたりのコスト", f"${hourly_cost:.4f}")

# 予測期間の総コスト
total_predicted_cost = hourly_cost * prediction_hours
st.sidebar.metric("予測期間の総コスト", f"${total_predicted_cost:.4f}")

# メインエリア
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 リアルタイムコスト追跡")
    
    # シミュレーション制御
    if not st.session_state.is_running:
        if st.button("🚀 シミュレーション開始", type="primary", use_container_width=True):
            st.session_state.is_running = True
            st.session_state.start_time = datetime.now()
            st.session_state.current_model = selected_model
            st.session_state.avg_prompt_tokens = avg_prompt_tokens
            st.session_state.avg_completion_tokens = avg_completion_tokens
            st.session_state.interval_seconds = interval_seconds
            st.rerun()
    else:
        if st.button("⏹️ シミュレーション停止", type="secondary", use_container_width=True):
            st.session_state.is_running = False
            st.rerun()
    
    # リアルタイムデータ表示
    if st.session_state.simulation_data:
        df = pd.DataFrame(st.session_state.simulation_data)
        
        # 累計コスト計算
        total_cost = df['cost_usd'].sum()
        total_tokens = df['total_tokens'].sum()
        generation_count = len(df)
        
        # メトリクス表示
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        with metric_col1:
            st.metric("累計コスト", f"${total_cost:.4f}")
        with metric_col2:
            st.metric("累計トークン", f"{total_tokens:,}")
        with metric_col3:
            st.metric("生成回数", f"{generation_count}")
        with metric_col4:
            if st.session_state.start_time:
                elapsed = datetime.now() - st.session_state.start_time
                st.metric("経過時間", f"{elapsed.seconds//60}分")
        
        # コスト推移グラフ
        fig_cost = px.line(
            df, 
            x='timestamp', 
            y='cost_usd',
            title='コスト推移（1回あたり）',
            labels={'cost_usd': 'コスト（USD）', 'timestamp': '時刻'}
        )
        fig_cost.update_layout(height=300)
        st.plotly_chart(fig_cost, use_container_width=True)
        
        # 累計コストグラフ
        df['cumulative_cost'] = df['cost_usd'].cumsum()
        fig_cumulative = px.line(
            df,
            x='timestamp',
            y='cumulative_cost', 
            title='累計コスト推移',
            labels={'cumulative_cost': '累計コスト（USD）', 'timestamp': '時刻'}
        )
        fig_cumulative.update_layout(height=300)
        st.plotly_chart(fig_cumulative, use_container_width=True)
        
        # トークン使用量グラフ
        fig_tokens = px.bar(
            df,
            x='timestamp',
            y=['prompt_tokens', 'completion_tokens'],
            title='トークン使用量',
            labels={'value': 'トークン数', 'timestamp': '時刻', 'variable': '種類'},
            barmode='stack'
        )
        fig_tokens.update_layout(height=300)
        st.plotly_chart(fig_tokens, use_container_width=True)
        
    else:
        st.info("シミュレーションを開始すると、リアルタイムでコストデータが表示されます。")

with col2:
    st.subheader("📊 予測分析")
    
    # 予測データ生成
    if st.button("🔮 予測シミュレーション実行", use_container_width=True):
        st.session_state.prediction_data = []
        
        # 予測期間のデータを生成
        current_time = datetime.now()
        for hour in range(prediction_hours):
            # 1時間あたりの生成回数を計算
            generations_per_hour = int(3600 / interval_seconds)
            
            for gen in range(generations_per_hour):
                # ランダムな変動を加えたトークン数
                import random
                prompt_tokens = int(avg_prompt_tokens * random.uniform(0.8, 1.2))
                completion_tokens = int(avg_completion_tokens * random.uniform(0.8, 1.2))
                
                cost = calculate_cost(prompt_tokens, completion_tokens, selected_model)
                
                # 生成時刻を計算
                seconds_elapsed = gen * interval_seconds
                timestamp = current_time + timedelta(hours=hour, seconds=seconds_elapsed)
                
                st.session_state.prediction_data.append({
                    'timestamp': timestamp,
                    'cost_usd': cost,
                    'total_tokens': prompt_tokens + completion_tokens
                })
        
        st.success("予測シミュレーション完了！")
        st.rerun()
    
    # 予測結果表示
    if 'prediction_data' in st.session_state and st.session_state.prediction_data:
        pred_df = pd.DataFrame(st.session_state.prediction_data)
        
        # 予測メトリクス
        pred_total_cost = pred_df['cost_usd'].sum()
        pred_total_tokens = pred_df['total_tokens'].sum()
        pred_generations = len(pred_df)
        
        st.metric("予測総コスト", f"${pred_total_cost:.4f}")
        st.metric("予測総トークン", f"{pred_total_tokens:,}")
        st.metric("予測生成回数", f"{pred_generations}")
        
        # 予測コスト推移
        pred_df['cumulative_cost'] = pred_df['cost_usd'].cumsum()
        fig_pred = px.line(
            pred_df,
            x='timestamp',
            y='cumulative_cost',
            title='予測コスト推移',
            labels={'cumulative_cost': '累計コスト（USD）', 'timestamp': '時刻'}
        )
        fig_pred.update_layout(height=250)
        st.plotly_chart(fig_pred, use_container_width=True)
        
        # 時間別コスト分析
        pred_df['hour'] = pred_df['timestamp'].dt.hour
        hourly_cost = pred_df.groupby('hour')['cost_usd'].sum().reset_index()
        
        fig_hourly = px.bar(
            hourly_cost,
            x='hour',
            y='cost_usd',
            title='時間別コスト分布',
            labels={'cost_usd': 'コスト（USD）', 'hour': '時間'}
        )
        fig_hourly.update_layout(height=200)
        st.plotly_chart(fig_hourly, use_container_width=True)

# フッター
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💰 展示用コストシミュレータ - 常時生成のコスト予測ツール</p>
    <p>リアルタイムでコストを追跡し、展示運用の予算計画に活用できます</p>
</div>
""", unsafe_allow_html=True)

# 自動更新（リアルタイムシミュレーション用）
if st.session_state.is_running:
    time.sleep(1)
    st.rerun() 