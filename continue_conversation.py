#!/usr/bin/env python3
"""
OpenAI APIを使って会話履歴から継続する
CSV -> messages形式に変換してGPT-4oで続行
"""

import pandas as pd
import json
import openai
from typing import List, Dict
import os

def csv_to_messages(csv_file: str) -> List[Dict[str, str]]:
    """
    CSVファイルをOpenAI API用のmessages形式に変換
    """
    df = pd.read_csv(csv_file)
    messages = []
    
    for _, row in df.iterrows():
        # NaN値をスキップ
        if pd.isna(row['side']) or pd.isna(row['prompt']):
            continue
            
        role = "user" if row['side'] == 'human' else "assistant"
        content = str(row['prompt'])  # 文字列に変換
        messages.append({"role": role, "content": content})
    
    return messages

def continue_conversation(csv_file: str, api_key: str, new_prompt: str):
    """
    CSV履歴から会話を継続してJSON形式で結果を取得
    """
    # APIキー設定
    openai.api_key = api_key
    
    # CSV履歴をmessages形式に変換
    messages = csv_to_messages(csv_file)
    
    print(f"読み込んだメッセージ数: {len(messages)}")
    
    # 新しいプロンプトを追加
    messages.append({"role": "user", "content": new_prompt})
    
    # OpenAI APIに送信（JSON mode使用）
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format={"type": "json_object"},
            max_tokens=4000,
            temperature=0.7
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
    NEW_PROMPT = "この方向で十個考えてください。結果をJSON形式で返してください。"
    
    # 環境変数からAPIキーを取得
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEYが設定されていません")
        print("export OPENAI_API_KEY='your-api-key-here' で設定してください")
        return
    
    print("会話履歴を読み込み中...")
    print(f"新しいプロンプト: {NEW_PROMPT}")
    print("OpenAI APIに送信中...")
    
    # 会話継続実行
    result = continue_conversation(CSV_FILE, api_key, NEW_PROMPT)
    
    if result:
        print("\n=== 結果 ===")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 結果をファイルに保存
        with open("api_response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("\n結果をapi_response.jsonに保存しました")
    else:
        print("API呼び出しに失敗しました")

if __name__ == "__main__":
    main() 