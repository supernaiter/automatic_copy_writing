#!/usr/bin/env python3
"""
AIディレクター機能
会話履歴の役割を逆転させて、AIにディレクションをさせる
"""

import pandas as pd
import json
import openai
from typing import List, Dict
import os

def csv_to_director_messages(csv_file: str) -> List[Dict[str, str]]:
    """
    CSVファイルをディレクター用に役割を逆転してmessages形式に変換
    human(ユーザーの指示) → system(ディレクターの指示)
    assistant(AIの出力) → user(クリエイターの出力)
    """
    df = pd.read_csv(csv_file)
    messages = []
    
    for _, row in df.iterrows():
        # NaN値をスキップ
        if pd.isna(row['side']) or pd.isna(row['prompt']):
            continue
            
        # 役割を逆転
        if row['side'] == 'human':
            # ユーザーの指示 → ディレクターの指示
            role = "system"
            content = f"ディレクター指示: {str(row['prompt'])}"
        else:  # assistant
            # AIの出力 → クリエイターの出力
            role = "user"
            content = f"クリエイター出力: {str(row['prompt'])}"
            
        messages.append({"role": role, "content": content})
    
    return messages

def ask_ai_director(csv_file: str, api_key: str, context_prompt: str):
    """
    CSV履歴から役割を逆転して、AIディレクターに次の指示を求める
    """
    # APIキー設定
    openai.api_key = api_key
    
    # CSV履歴をディレクター用messages形式に変換
    messages = csv_to_director_messages(csv_file)
    
    print(f"読み込んだメッセージ数: {len(messages)}")
    
    # AIディレクター用のシステムメッセージを追加
    director_system_message = {
        "role": "system", 
        "content": """あなたは優秀なクリエイティブディレクターです。
過去の会話履歴を見て、次にクリエイターにどのような指示を出すべきかを考えてください。
より良いアイデアを引き出すための具体的で建設的な指示を提案してください。
結果はJSON形式で返してください。"""
    }
    
    # メッセージの先頭にディレクター用システムメッセージを挿入
    messages.insert(0, director_system_message)
    
    # コンテキストプロンプトを追加
    messages.append({"role": "user", "content": context_prompt})
    
    # OpenAI APIに送信（JSON mode使用）
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format={"type": "json_object"},
            max_tokens=4000,
            temperature=0.8
        )
        
        # レスポンスの内容を取得
        result = response.choices[0].message.content
        
        # JSONとして解析して整形
        json_result = json.loads(result)
        
        return json_result
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

def main():
    """
    メイン実行関数
    """
    # 設定
    CSV_FILE = "interaction.csv"
    CONTEXT_PROMPT = """この会話の流れを見て、次にクリエイターにどのような指示を出すべきですか？
より良いコピーやアイデアを引き出すために、どんなディレクションが効果的でしょうか？
結果をJSON形式で返してください。"""
    
    # 環境変数からAPIキーを取得
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEYが設定されていません")
        print("export OPENAI_API_KEY='your-api-key-here' で設定してください")
        return
    
    print("会話履歴を読み込み中...")
    print("役割を逆転させてAIディレクターに質問中...")
    print("OpenAI APIに送信中...")
    
    # AIディレクター実行
    result = ask_ai_director(CSV_FILE, api_key, CONTEXT_PROMPT)
    
    if result:
        print("\n=== AIディレクターからの提案 ===")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 結果をファイルに保存
        with open("ai_director_response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("\n結果をai_director_response.jsonに保存しました")
    else:
        print("AI呼び出しに失敗しました")

if __name__ == "__main__":
    main() 