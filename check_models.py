#!/usr/bin/env python3
"""
OpenAI API利用可能モデル確認スクリプト
"""

import openai
import os
from datetime import datetime

# APIキー設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-proj-your-api-key-here")
openai.api_key = OPENAI_API_KEY

def main():
    print("=" * 60)
    print("OpenAI API 利用可能モデル一覧")
    print(f"確認日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # モデル一覧を取得
        models = openai.models.list()
        
        # チャット用モデルをフィルタリング
        chat_models = []
        other_models = []
        
        for model in models.data:
            model_id = model.id
            if any(prefix in model_id.lower() for prefix in ['gpt-', 'o1-', 'o3-']):
                chat_models.append(model_id)
            else:
                other_models.append(model_id)
        
        # チャット用モデルを表示
        print("\n🤖 チャット用モデル（推奨）:")
        print("-" * 40)
        for model in sorted(chat_models, reverse=True):
            print(f"• {model}")
        
        # その他のモデルを表示
        print(f"\n📊 その他のモデル ({len(other_models)}個):")
        print("-" * 40)
        for model in sorted(other_models):
            print(f"• {model}")
        
        print(f"\n📈 合計: {len(models.data)}個のモデルが利用可能")
        
        # 推奨モデル情報
        print("\n" + "=" * 60)
        print("推奨モデル情報")
        print("=" * 60)
        
        recommendations = {
            "o3-mini": "💰 最新推論モデル（高性能・低コスト・推奨）",
            "o1-pro": "🧠 最高性能推論モデル（複雑なタスク向け・高コスト）",
            "o1-mini": "⚡ 高速推論モデル（バランス型）",
            "gpt-4o": "🎯 最新GPT-4（バランス型・安定）",
            "gpt-4o-mini": "💨 軽量版GPT-4（高速・低コスト）"
        }
        
        for model, description in recommendations.items():
            if model in chat_models:
                print(f"✅ {model}: {description}")
            else:
                print(f"❌ {model}: 利用不可")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {str(e)}")
        
        if "api_key" in str(e).lower():
            print("\n💡 APIキーが正しく設定されていない可能性があります。")
            print("   環境変数 OPENAI_API_KEY を確認してください。")

if __name__ == "__main__":
    main() 