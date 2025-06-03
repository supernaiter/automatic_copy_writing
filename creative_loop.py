#!/usr/bin/env python3
"""
クリエイティブループシステム
ディレクターとクリエイターを交互に実行してアイデアを自動生成
"""

import pandas as pd
import json
import openai
from typing import List, Dict
import os
import time

def csv_to_director_messages(csv_file: str) -> List[Dict[str, str]]:
    """CSVファイルをディレクター用messages形式に変換"""
    df = pd.read_csv(csv_file)
    messages = []
    
    for _, row in df.iterrows():
        if pd.isna(row['side']) or pd.isna(row['prompt']):
            continue
            
        if row['side'] == 'human':
            role = "system"
            content = f"ディレクター指示: {str(row['prompt'])}"
        else:
            role = "user"
            content = f"クリエイター出力: {str(row['prompt'])}"
            
        messages.append({"role": role, "content": content})
    
    return messages

def csv_to_creator_messages(csv_file: str) -> List[Dict[str, str]]:
    """CSVファイルを通常のmessages形式に変換"""
    df = pd.read_csv(csv_file)
    messages = []
    
    for _, row in df.iterrows():
        if pd.isna(row['side']) or pd.isna(row['prompt']):
            continue
            
        role = "system" if row['side'] == 'human' else "assistant"
        messages.append({"role": role, "content": str(row['prompt'])})
    
    return messages

def get_director_instruction(csv_file: str, api_key: str) -> str:
    """ディレクターから次の指示を取得"""
    openai.api_key = api_key
    messages = csv_to_director_messages(csv_file)
    
    director_system_message = {
        "role": "system", 
        "content": """あなたは優秀なコピーライター・ディレクターです。
過去の会話を見て、次にクリエイターに出すべき「コピーライティング」に特化した指示を1つ提案してください。
カシワバラ・コーポレーションの施工管理職採用の「短いキャッチコピー」をさらに良くするための指示です。

重要：
- ビジュアル、ムービー、ストーリーボードの話は一切しない
- 短いコピー・キャッチフレーズの言葉の力に集中する
- 「新幹線が、地下で眠る場所を知ってる」レベルの簡潔さを保つ
- 異なる切り口やアプローチでのコピー案を求める

回答は指示文のみをシンプルに返してください。JSON形式は不要です。"""
    }
    
    messages.insert(0, director_system_message)
    messages.append({
        "role": "user", 
        "content": "この流れを見て、次にクリエイターに出すべきコピーライティング指示を1つ教えてください。指示文のみお願いします。"
    })
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=500,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"ディレクター呼び出しエラー: {e}")
        return None

def get_creator_response(csv_file: str, director_instruction: str, api_key: str) -> str:
    """クリエイターからアイデアを取得"""
    openai.api_key = api_key
    messages = csv_to_creator_messages(csv_file)
    
    # 最新のディレクター指示を追加
    messages.append({"role": "user", "content": director_instruction})
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=1000,
            temperature=0.9
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"クリエイター呼び出しエラー: {e}")
        return None

def append_to_csv(csv_file: str, side: str, prompt: str):
    """CSVに新しいやり取りを追加"""
    new_row = pd.DataFrame({"side": [side], "prompt": [prompt]})
    
    try:
        df = pd.read_csv(csv_file)
        df = pd.concat([df, new_row], ignore_index=True)
    except FileNotFoundError:
        df = new_row
    
    df.to_csv(csv_file, index=False)

def creative_loop(csv_file: str, api_key: str, iterations: int = 5):
    """クリエイティブループの実行"""
    print(f"クリエイティブループを{iterations}回実行します...")
    
    for i in range(iterations):
        print(f"\n=== ループ {i+1}/{iterations} ===")
        
        # Step 1: ディレクターから指示を取得
        print("ディレクターから指示を取得中...")
        instruction = get_director_instruction(csv_file, api_key)
        if not instruction:
            print("ディレクター呼び出し失敗")
            break
            
        print(f"ディレクター指示: {instruction}")
        
        # Step 2: ディレクター指示をCSVに追加
        append_to_csv(csv_file, "human", instruction)
        
        # Step 3: クリエイターからアイデアを取得
        print("クリエイターからアイデア取得中...")
        ideas = get_creator_response(csv_file, instruction, api_key)
        if not ideas:
            print("クリエイター呼び出し失敗")
            break
            
        print(f"クリエイター出力: {ideas[:200]}...")
        
        # Step 4: クリエイター出力をCSVに追加
        append_to_csv(csv_file, "assistant", ideas)
        
        # Step 5: 少し待機してAPI制限を回避
        if i < iterations - 1:
            print("次のループまで待機中...")
            time.sleep(2)
    
    print(f"\nクリエイティブループ完了！更新されたファイル: {csv_file}")

def main():
    """メイン実行関数"""
    CSV_FILE = "interaction.csv"
    ITERATIONS = 5  # ループ回数
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEYが設定されていません")
        return
    
    # バックアップを作成
    backup_file = f"{CSV_FILE}.backup"
    try:
        df = pd.read_csv(CSV_FILE)
        df.to_csv(backup_file, index=False)
        print(f"バックアップを作成: {backup_file}")
    except FileNotFoundError:
        print(f"{CSV_FILE}が見つかりません")
        return
    
    # クリエイティブループ実行
    creative_loop(CSV_FILE, api_key, ITERATIONS)
    
    print(f"\n最終結果を確認するには: head -20 {CSV_FILE}")

if __name__ == "__main__":
    main() 