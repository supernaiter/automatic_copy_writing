#!/usr/bin/env python3
"""
詳細AIディレクター機能
より具体的で実行可能な指示を出すAIディレクター
"""

import pandas as pd
import json
import openai
from typing import List, Dict
import os

def csv_to_director_messages(csv_file: str) -> List[Dict[str, str]]:
    """
    CSVファイルをディレクター用に役割を逆転してmessages形式に変換
    """
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

def ask_detailed_ai_director(csv_file: str, api_key: str):
    """
    詳細なディレクション指示を求める
    """
    openai.api_key = api_key
    
    messages = csv_to_director_messages(csv_file)
    
    director_system_message = {
        "role": "system", 
        "content": """あなたは経験豊富なクリエイティブディレクターです。
過去の会話を分析して、次に取るべき具体的なアクションを提案してください。

以下の観点から詳細な指示を出してください：
1. 最も有望なアイデアの特定と理由
2. そのアイデアをさらに強化するための具体的な手法
3. ターゲット（就活生）により刺さる要素の追加
4. 実際のキャンペーンで使える形への発展
5. 次のクリエイティブステップの提案

結果はJSON形式で、実行可能な指示として返してください。"""
    }
    
    messages.insert(0, director_system_message)
    
    context_prompt = """この会話の流れと生成されたアイデアを見て、カシワバラ・コーポレーションの施工管理職採用キャンペーンを成功させるために、次に何をすべきでしょうか？

具体的で実行可能な指示をJSON形式で提案してください。特に：
- どのアイデアを推すべきか
- どうやってさらに強化するか  
- 実際のキャンペーンにどう活用するか
を含めてください。"""
    
    messages.append({"role": "user", "content": context_prompt})
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format={"type": "json_object"},
            max_tokens=4000,
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        json_result = json.loads(result)
        return json_result
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

def main():
    """
    詳細ディレクター実行
    """
    CSV_FILE = "interaction.csv"
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEYが設定されていません")
        return
    
    print("詳細AIディレクターを実行中...")
    result = ask_detailed_ai_director(CSV_FILE, api_key)
    
    if result:
        print("\n=== 詳細AIディレクターからの提案 ===")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        with open("detailed_director_response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("\n結果をdetailed_director_response.jsonに保存しました")
    else:
        print("AI呼び出しに失敗しました")

if __name__ == "__main__":
    main() 