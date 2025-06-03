#!/usr/bin/env python3
"""
コピー特化ループシステム
短いキャッチコピーのみに集中したクリエイティブループ
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

def get_copy_director_instruction(csv_file: str, api_key: str) -> str:
    """コピー特化ディレクターから次の指示を取得"""
    openai.api_key = api_key
    messages = csv_to_director_messages(csv_file)
    
    director_system_message = {
        "role": "system", 
        "content": """あなたは優秀なコピーライター・ディレクターです。
カシワバラ・コーポレーションの施工管理職採用の「短いキャッチコピー」のみに集中してください。

以下の具体的なアプローチから1つ選んで指示してください：

【時間軸アプローチ】
- 未来への影響を表現したコピー
- 過去から現在への継続を表現したコピー
- 瞬間の価値を表現したコピー

【感覚アプローチ】  
- 音を使ったコピー（聞こえない音、隠れた音など）
- 触感を使ったコピー（質感、温度、振動など）
- 匂いや空気感を使ったコピー

【対比アプローチ】
- 地上と地下の対比
- 見える世界と見えない世界の対比
- 普通の人と施工管理者の視点の対比

【秘密・特権アプローチ】
- 知らない場所を知っている
- 秘密の瞬間を目撃している  
- 特別なアクセス権を持っている

【感情アプローチ】
- 誇り、達成感を表現
- 責任感、使命感を表現
- 発見の喜びを表現

1つのアプローチを選んで、具体的で実行可能な指示を出してください。
回答は指示文のみをシンプルに返してください。"""
    }
    
    messages.insert(0, director_system_message)
    messages.append({
        "role": "user", 
        "content": "上記のアプローチから1つ選んで、具体的なキャッチコピー作成指示を1つ教えてください。指示文のみお願いします。"
    })
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=300,
            temperature=1.0  # 温度を上げてバリエーション増加
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"ディレクター呼び出しエラー: {e}")
        return None

def get_copy_creator_response(csv_file: str, director_instruction: str, api_key: str) -> str:
    """コピー特化クリエイターからアイデアを取得"""
    openai.api_key = api_key
    messages = csv_to_creator_messages(csv_file)
    
    # 最新のディレクター指示を追加
    messages.append({"role": "user", "content": director_instruction})
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=800,
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

def copy_focused_loop(csv_file: str, api_key: str, iterations: int = 5):
    """コピー特化クリエイティブループの実行"""
    print(f"コピー特化ループを{iterations}回実行します...")
    
    for i in range(iterations):
        print(f"\n=== ループ {i+1}/{iterations} ===")
        
        # Step 1: ディレクターから指示を取得
        print("コピーディレクターから指示を取得中...")
        instruction = get_copy_director_instruction(csv_file, api_key)
        if not instruction:
            print("ディレクター呼び出し失敗")
            break
            
        print(f"ディレクター指示: {instruction}")
        
        # Step 2: ディレクター指示をCSVに追加
        append_to_csv(csv_file, "human", instruction)
        
        # Step 3: クリエイターからアイデアを取得
        print("コピークリエイターからアイデア取得中...")
        ideas = get_copy_creator_response(csv_file, instruction, api_key)
        if not ideas:
            print("クリエイター呼び出し失敗")
            break
            
        print(f"コピー出力: {ideas[:200]}...")
        
        # Step 4: クリエイター出力をCSVに追加
        append_to_csv(csv_file, "assistant", ideas)
        
        # Step 5: 少し待機してAPI制限を回避
        if i < iterations - 1:
            print("次のループまで待機中...")
            time.sleep(2)
    
    print(f"\nコピー特化ループ完了！更新されたファイル: {csv_file}")

def main():
    """メイン実行関数"""
    CSV_FILE = "interaction_copy_focused.csv"
    ITERATIONS = 10  # コピー特化なので多めに
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEYが設定されていません")
        return
    
    print(f"元のファイル行数: {len(pd.read_csv(CSV_FILE))}")
    
    # コピー特化ループ実行
    copy_focused_loop(CSV_FILE, api_key, ITERATIONS)
    
    print(f"\n最終結果を確認するには: tail -30 {CSV_FILE}")

if __name__ == "__main__":
    main() 