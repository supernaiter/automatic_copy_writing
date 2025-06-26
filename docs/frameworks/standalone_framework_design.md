# スタンドアロン フレームワーク設計書

## 1. 設計思想：Complete Standalone

### 1.1 実行方式

```bash
# 各フレームワークが完全独立で動作
python framework_01_brand_key.py
python framework_02_cep_distribution.py
python framework_05_share_of_search.py
python framework_13_meme_emoji.py

# 設定ファイルやパラメータ指定も可能
python framework_05_share_of_search.py --config config.json
python framework_02_cep_distribution.py --brand "コカコーラ" --category "飲料"
```

### 1.2 完全独立の原則

**✅ 依存関係ゼロ**
- 他のフレームワークファイルに依存しない
- 共通ライブラリなし（各ファイルに必要な関数を内包）
- データベースやAPIキー設定もファイル内完結

**✅ 即座実行可能**
- `python framework_XX.py`でいきなり動く
- 設定や初期化処理もスクリプト内で完結
- サンプルデータ内蔵でデモ動作可能

**✅ 結果ファイル出力**
- 実行結果をJSONファイルに自動保存
- CSV、画像ファイルも生成
- ターミナルにも要約結果を表示

## 2. スタンドアロン実装例

### 2.1 フレーム5: Share of Search (framework_05_share_of_search.py)

```python
#!/usr/bin/env python3
"""
フレーム5: Share of Search 分析
実行方法: python framework_05_share_of_search.py
"""

import asyncio
import json
import time
import argparse
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
import os

class ShareOfSearchFramework:
    """Share of Search 分析フレームワーク - スタンドアロン版"""
    
    def __init__(self):
        self.framework_id = 5
        self.framework_name = "Share of Search"
        self.version = "1.0.0"
        self.output_dir = f"output_framework_05_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 出力ディレクトリ作成
        os.makedirs(self.output_dir, exist_ok=True)
        
        print(f"🚀 {self.framework_name} v{self.version} 開始")
        print(f"📁 出力ディレクトリ: {self.output_dir}")
    
    async def collect_data(self, brand_name: str, competitors: List[str], 
                          category: str, time_range: str = "today 12-m") -> Dict[str, Any]:
        """Share of Search データ収集・分析"""
        
        start_time = time.time()
        print(f"\n📊 分析開始: {brand_name} vs {competitors}")
        
        try:
            # Step 1: Google Trends API接続
            print("🔗 Google Trends API接続中...")
            pytrends = TrendReq(hl='ja-JP', tz=360, timeout=(10, 25))
            
            # Step 2: キーワード検索データ取得
            all_keywords = [brand_name] + competitors
            print(f"🔍 検索データ取得: {all_keywords}")
            
            pytrends.build_payload(all_keywords, timeframe=time_range, geo='JP')
            interest_data = pytrends.interest_over_time()
            
            if interest_data.empty:
                raise Exception("検索データが取得できませんでした")
            
            # Step 3: Share of Search 計算
            print("🧮 Share of Search 計算中...")
            sos_data = self._calculate_share_of_search(interest_data, all_keywords)
            
            # Step 4: トレンド分析
            trend_analysis = self._analyze_trends(interest_data, all_keywords)
            
            # Step 5: 競合ポジション分析
            competitive_analysis = self._analyze_competitive_position(sos_data, brand_name)
            
            execution_time = time.time() - start_time
            
            result = {
                "framework_info": {
                    "id": self.framework_id,
                    "name": self.framework_name,
                    "version": self.version,
                    "execution_time": execution_time,
                    "timestamp": datetime.now().isoformat()
                },
                "input_parameters": {
                    "brand_name": brand_name,
                    "competitors": competitors,
                    "category": category,
                    "time_range": time_range
                },
                "share_of_search": sos_data,
                "trend_analysis": trend_analysis,
                "competitive_analysis": competitive_analysis,
                "insights": self._generate_insights(sos_data, trend_analysis, competitive_analysis),
                "raw_data": interest_data.to_dict(),
                "success": True
            }
            
            print(f"✅ 分析完了 ({execution_time:.2f}秒)")
            return result
            
        except Exception as e:
            error_result = {
                "framework_info": {
                    "id": self.framework_id,
                    "name": self.framework_name,
                    "error": str(e)
                },
                "success": False,
                "execution_time": time.time() - start_time
            }
            print(f"❌ エラー: {str(e)}")
            return error_result
    
    def _calculate_share_of_search(self, data: pd.DataFrame, keywords: List[str]) -> Dict[str, float]:
        """検索シェア計算"""
        # NaN値を0で置換
        data_clean = data[keywords].fillna(0)
        
        # 期間平均での各ブランドシェア
        total_searches = data_clean.sum(axis=1)
        share_data = {}
        
        for keyword in keywords:
            if total_searches.sum() > 0:
                share_data[keyword] = (data_clean[keyword].sum() / data_clean.sum().sum() * 100)
            else:
                share_data[keyword] = 0.0
        
        return share_data
    
    def _analyze_trends(self, data: pd.DataFrame, keywords: List[str]) -> Dict[str, Any]:
        """トレンド分析"""
        trends = {}
        
        for keyword in keywords:
            keyword_data = data[keyword].fillna(0)
            if len(keyword_data) > 1:
                # 線形回帰で傾向計算
                x = range(len(keyword_data))
                correlation = pd.Series(x).corr(keyword_data)
                
                trend_direction = "increasing" if correlation > 0.1 else "decreasing" if correlation < -0.1 else "stable"
                trend_strength = abs(correlation)
                
                trends[keyword] = {
                    "direction": trend_direction,
                    "strength": trend_strength,
                    "recent_peak": keyword_data.max(),
                    "recent_avg": keyword_data.mean()
                }
        
        return trends
    
    def _analyze_competitive_position(self, sos_data: Dict[str, float], brand_name: str) -> Dict[str, Any]:
        """競合ポジション分析"""
        sorted_brands = sorted(sos_data.items(), key=lambda x: x[1], reverse=True)
        brand_rank = next((i+1 for i, (brand, _) in enumerate(sorted_brands) if brand == brand_name), None)
        
        market_leader = sorted_brands[0][0] if sorted_brands else None
        brand_share = sos_data.get(brand_name, 0)
        leader_share = sorted_brands[0][1] if sorted_brands else 0
        
        gap_to_leader = leader_share - brand_share if market_leader != brand_name else 0
        
        return {
            "brand_rank": brand_rank,
            "total_brands": len(sos_data),
            "market_leader": market_leader,
            "brand_share": brand_share,
            "leader_share": leader_share,
            "gap_to_leader": gap_to_leader,
            "competitive_intensity": len([s for s in sos_data.values() if s > 10])  # 10%以上のブランド数
        }
    
    def _generate_insights(self, sos_data: Dict[str, float], 
                          trend_analysis: Dict[str, Any], 
                          competitive_analysis: Dict[str, Any]) -> List[str]:
        """洞察生成"""
        insights = []
        
        # 検索シェア洞察
        top_brand = max(sos_data.items(), key=lambda x: x[1])
        insights.append(f"検索シェア1位は{top_brand[0]}で{top_brand[1]:.1f}%")
        
        # トレンド洞察
        increasing_brands = [brand for brand, data in trend_analysis.items() 
                           if data["direction"] == "increasing" and data["strength"] > 0.3]
        if increasing_brands:
            insights.append(f"上昇トレンド: {', '.join(increasing_brands)}")
        
        # 競合状況洞察
        if competitive_analysis["competitive_intensity"] > 3:
            insights.append("激戦カテゴリ（10%以上シェアブランド多数）")
        
        # ギャップ洞察
        if competitive_analysis["gap_to_leader"] > 20:
            insights.append(f"リーダーとの差が大きい（{competitive_analysis['gap_to_leader']:.1f}%差）")
        
        return insights
    
    def save_results(self, result: Dict[str, Any]) -> None:
        """結果保存"""
        # JSON保存
        json_path = os.path.join(self.output_dir, "sos_analysis_result.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"💾 結果保存: {json_path}")
        
        # CSV保存
        if result.get("success") and "share_of_search" in result:
            sos_df = pd.DataFrame(list(result["share_of_search"].items()), 
                                columns=["Brand", "Share_of_Search_%"])
            csv_path = os.path.join(self.output_dir, "share_of_search.csv")
            sos_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"📊 CSV保存: {csv_path}")
        
        # 可視化グラフ保存
        if result.get("success"):
            self._save_visualization(result)
    
    def _save_visualization(self, result: Dict[str, Any]) -> None:
        """可視化グラフ生成・保存"""
        try:
            plt.style.use('default')
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Share of Search 円グラフ
            sos_data = result["share_of_search"]
            ax1.pie(sos_data.values(), labels=sos_data.keys(), autopct='%1.1f%%')
            ax1.set_title("Share of Search Distribution")
            
            # トレンド方向棒グラフ  
            trend_data = result["trend_analysis"]
            brands = list(trend_data.keys())
            strengths = [data["strength"] for data in trend_data.values()]
            colors = ['green' if trend_data[brand]["direction"] == "increasing" 
                     else 'red' if trend_data[brand]["direction"] == "decreasing" 
                     else 'gray' for brand in brands]
            
            ax2.bar(brands, strengths, color=colors)
            ax2.set_title("Trend Strength by Brand")
            ax2.set_ylabel("Trend Strength")
            ax2.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            chart_path = os.path.join(self.output_dir, "sos_analysis_chart.png")
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"📈 グラフ保存: {chart_path}")
            
        except Exception as e:
            print(f"⚠️  グラフ生成エラー: {str(e)}")
    
    def print_summary(self, result: Dict[str, Any]) -> None:
        """結果サマリー表示"""
        if not result.get("success"):
            print(f"\n❌ 実行失敗: {result.get('framework_info', {}).get('error', 'Unknown error')}")
            return
        
        print(f"\n📋 {self.framework_name} 実行結果サマリー")
        print("=" * 50)
        
        # 基本情報
        print(f"🎯 対象ブランド: {result['input_parameters']['brand_name']}")
        print(f"🆚 競合ブランド: {', '.join(result['input_parameters']['competitors'])}")
        print(f"⏱️  実行時間: {result['framework_info']['execution_time']:.2f}秒")
        
        # Share of Search結果
        print(f"\n📊 Share of Search結果:")
        for brand, share in result["share_of_search"].items():
            print(f"  {brand}: {share:.1f}%")
        
        # 競合分析結果
        comp_analysis = result["competitive_analysis"]
        print(f"\n🏆 競合ポジション:")
        print(f"  順位: {comp_analysis['brand_rank']}/{comp_analysis['total_brands']}位")
        print(f"  市場リーダー: {comp_analysis['market_leader']}")
        print(f"  リーダーとの差: {comp_analysis['gap_to_leader']:.1f}%")
        
        # 洞察
        print(f"\n💡 主要洞察:")
        for insight in result["insights"]:
            print(f"  • {insight}")
        
        print(f"\n📁 詳細結果は {self.output_dir} フォルダに保存されました")

# サンプルデータ
SAMPLE_DATA = {
    "brand_name": "コカコーラ",
    "competitors": ["ペプシ", "伊右衛門", "午後の紅茶"],
    "category": "飲料",
    "time_range": "today 12-m"
}

async def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(description="Share of Search 分析フレームワーク")
    parser.add_argument("--brand", default=SAMPLE_DATA["brand_name"], help="対象ブランド名")
    parser.add_argument("--competitors", nargs='+', default=SAMPLE_DATA["competitors"], help="競合ブランド")
    parser.add_argument("--category", default=SAMPLE_DATA["category"], help="カテゴリ")
    parser.add_argument("--timerange", default=SAMPLE_DATA["time_range"], help="分析期間")
    parser.add_argument("--config", help="設定JSONファイルパス")
    
    args = parser.parse_args()
    
    # 設定ファイルがあれば読み込み
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        brand_name = config.get("brand_name", args.brand)
        competitors = config.get("competitors", args.competitors)
        category = config.get("category", args.category)
        time_range = config.get("time_range", args.timerange)
    else:
        brand_name = args.brand
        competitors = args.competitors
        category = args.category  
        time_range = args.timerange
    
    # フレームワーク実行
    framework = ShareOfSearchFramework()
    result = await framework.collect_data(brand_name, competitors, category, time_range)
    
    # 結果保存・表示
    framework.save_results(result)
    framework.print_summary(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### 2.2 フレーム2: CEP分布 (framework_02_cep_distribution.py)

```python
#!/usr/bin/env python3
"""
フレーム2: Category Entry Points 分布分析
実行方法: python framework_02_cep_distribution.py
"""

import asyncio
import json
import time
import argparse
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tweepy
import openai
import os
from collections import Counter
import re

class CategoryEntryPointsFramework:
    """Category Entry Points 分析フレームワーク - スタンドアロン版"""
    
    def __init__(self):
        self.framework_id = 2
        self.framework_name = "Category Entry Points Distribution"
        self.version = "1.0.0"
        self.output_dir = f"output_framework_02_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 出力ディレクトリ作成
        os.makedirs(self.output_dir, exist_ok=True)
        
        # API設定（環境変数から取得）
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.twitter_bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        
        print(f"🚀 {self.framework_name} v{self.version} 開始")
        print(f"📁 出力ディレクトリ: {self.output_dir}")
    
    async def collect_data(self, category: str, time_range: str = "30d") -> Dict[str, Any]:
        """Category Entry Points データ収集・分析"""
        
        start_time = time.time()
        print(f"\n📊 分析開始: カテゴリ '{category}'")
        
        try:
            # Step 1: SNS投稿収集
            print("🐦 SNS投稿収集中...")
            social_posts = await self._collect_social_posts(category, time_range)
            
            # Step 2: 検索クエリ収集 (模擬データ)
            print("🔍 検索クエリ収集中...")
            search_queries = await self._collect_search_queries(category)
            
            # Step 3: Entry Points分類
            print("🧩 Entry Points分類中...")
            entry_points = await self._classify_entry_points(social_posts, search_queries)
            
            # Step 4: ヒートマップデータ生成
            print("📈 ヒートマップ生成中...")
            heatmap_data = self._generate_heatmap_data(entry_points)
            
            # Step 5: 機会発見
            opportunities = self._find_opportunities(entry_points)
            
            execution_time = time.time() - start_time
            
            result = {
                "framework_info": {
                    "id": self.framework_id,
                    "name": self.framework_name,
                    "version": self.version,
                    "execution_time": execution_time,
                    "timestamp": datetime.now().isoformat()
                },
                "input_parameters": {
                    "category": category,
                    "time_range": time_range
                },
                "entry_points": entry_points,
                "heatmap_data": heatmap_data,
                "opportunities": opportunities,
                "data_summary": {
                    "total_posts": len(social_posts),
                    "total_queries": len(search_queries),
                    "unique_entry_points": len(entry_points)
                },
                "insights": self._generate_insights(entry_points, opportunities),
                "success": True
            }
            
            print(f"✅ 分析完了 ({execution_time:.2f}秒)")
            return result
            
        except Exception as e:
            error_result = {
                "framework_info": {
                    "id": self.framework_id,
                    "name": self.framework_name,
                    "error": str(e)
                },
                "success": False,
                "execution_time": time.time() - start_time
            }
            print(f"❌ エラー: {str(e)}")
            return error_result
    
    async def _collect_social_posts(self, category: str, time_range: str) -> List[str]:
        """SNS投稿収集（サンプルデータ使用）"""
        # 実際の実装ではTwitter API等を使用
        sample_posts = [
            f"朝の忙しい時に{category}が欲しくなる",
            f"運動後に{category}を摂取",
            f"ストレス感じた時に{category}で癒される",
            f"夜寝る前の{category}タイム",
            f"仕事の休憩時間に{category}",
            f"友達と{category}を楽しむ",
            f"一人の時間に{category}",
            f"疲れた時こそ{category}",
            f"頑張った自分への{category}ご褒美",
            f"罪悪感を感じながらも{category}",
        ]
        
        await asyncio.sleep(0.5)  # API呼び出し模擬
        return sample_posts
    
    async def _collect_search_queries(self, category: str) -> List[str]:
        """検索クエリ収集（サンプルデータ）"""
        sample_queries = [
            f"{category} 朝",
            f"{category} 運動後",
            f"{category} ストレス",
            f"{category} 夜",
            f"{category} 休憩",
            f"{category} おすすめ",
            f"{category} 効果",
            f"{category} 続ける方法",
        ]
        
        await asyncio.sleep(0.3)
        return sample_queries
    
    async def _classify_entry_points(self, posts: List[str], queries: List[str]) -> Dict[str, Dict]:
        """Entry Points分類"""
        
        # 文脈カテゴリ定義
        context_patterns = {
            "朝の忙しい時": ["朝", "忙しい", "急いで", "時間ない"],
            "運動後": ["運動", "ジム", "トレーニング", "汗"],
            "ストレス時": ["ストレス", "疲れ", "イライラ", "癒し"],
            "夜のリラックス": ["夜", "寝る前", "リラックス", "くつろぎ"],
            "仕事の休憩": ["休憩", "仕事", "オフィス", "会社"],
            "ご褒美タイム": ["ご褒美", "頑張った", "自分へ", "贅沢"],
            "罪悪感": ["罪悪感", "だめだ", "また", "いけない"],
            "社交": ["友達", "みんなで", "一緒に", "シェア"]
        }
        
        entry_points = {}
        all_text = posts + queries
        
        for context, keywords in context_patterns.items():
            frequency = 0
            sentiment_scores = []
            
            for text in all_text:
                if any(keyword in text for keyword in keywords):
                    frequency += 1
                    # 簡易感情分析（実際の実装ではAI使用）
                    if any(negative in text for negative in ["疲れ", "ストレス", "罪悪感"]):
                        sentiment_scores.append(0.3)
                    elif any(positive in text for positive in ["ご褒美", "癒し", "楽しむ"]):
                        sentiment_scores.append(0.8)
                    else:
                        sentiment_scores.append(0.5)
            
            if frequency > 0:
                entry_points[context] = {
                    "frequency": frequency,
                    "percentage": frequency / len(all_text) * 100,
                    "avg_sentiment": sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.5,
                    "keywords": keywords
                }
        
        return entry_points
    
    def _generate_heatmap_data(self, entry_points: Dict[str, Dict]) -> Dict[str, Any]:
        """ヒートマップデータ生成"""
        
        # 時間軸 x 文脈軸のマトリクス
        time_slots = ["朝", "昼", "夕方", "夜"]
        contexts = list(entry_points.keys())
        
        # 簡易マッピング
        time_context_mapping = {
            "朝": ["朝の忙しい時"],
            "昼": ["仕事の休憩", "社交"],
            "夕方": ["運動後", "ストレス時"],
            "夜": ["夜のリラックス", "ご褒美タイム", "罪悪感"]
        }
        
        heatmap_matrix = []
        for time_slot in time_slots:
            row = []
            for context in contexts:
                if context in time_context_mapping.get(time_slot, []):
                    intensity = entry_points[context]["frequency"] * entry_points[context]["avg_sentiment"]
                else:
                    intensity = 0
                row.append(intensity)
            heatmap_matrix.append(row)
        
        return {
            "matrix": heatmap_matrix,
            "time_slots": time_slots,
            "contexts": contexts
        }
    
    def _find_opportunities(self, entry_points: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """機会発見"""
        opportunities = []
        
        # 低頻度だが高感情価値の文脈
        for context, data in entry_points.items():
            if data["frequency"] < 3 and data["avg_sentiment"] > 0.6:
                opportunities.append({
                    "type": "underexplored_high_value",
                    "context": context,
                    "frequency": data["frequency"],
                    "sentiment": data["avg_sentiment"],
                    "opportunity": f"高感情価値だが未開拓の'{context}'文脈"
                })
        
        # 高頻度だが低感情価値（改善機会）
        for context, data in entry_points.items():
            if data["frequency"] >= 3 and data["avg_sentiment"] < 0.4:
                opportunities.append({
                    "type": "high_frequency_low_satisfaction",
                    "context": context,
                    "frequency": data["frequency"],
                    "sentiment": data["avg_sentiment"],
                    "opportunity": f"頻出だが満足度低い'{context}'の改善機会"
                })
        
        return opportunities
    
    def _generate_insights(self, entry_points: Dict[str, Dict], 
                          opportunities: List[Dict[str, Any]]) -> List[str]:
        """洞察生成"""
        insights = []
        
        # 最頻出Entry Point
        if entry_points:
            top_context = max(entry_points.items(), key=lambda x: x[1]["frequency"])
            insights.append(f"最頻出Entry Point: '{top_context[0]}' ({top_context[1]['frequency']}回)")
        
        # 最高感情価値Entry Point
        if entry_points:
            best_sentiment = max(entry_points.items(), key=lambda x: x[1]["avg_sentiment"])
            insights.append(f"最高感情価値: '{best_sentiment[0]}' (感情スコア{best_sentiment[1]['avg_sentiment']:.2f})")
        
        # 機会数
        insights.append(f"発見された機会: {len(opportunities)}件")
        
        # 未開拓機会
        underexplored = [opp for opp in opportunities if opp["type"] == "underexplored_high_value"]
        if underexplored:
            insights.append(f"未開拓高価値文脈: {len(underexplored)}件")
        
        return insights

# [続く - save_results, print_summary, main関数は同様のパターン]

# サンプルデータ
SAMPLE_DATA = {
    "category": "健康食品",
    "time_range": "30d"
}

async def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(description="Category Entry Points 分析フレームワーク")
    parser.add_argument("--category", default=SAMPLE_DATA["category"], help="分析カテゴリ")
    parser.add_argument("--timerange", default=SAMPLE_DATA["time_range"], help="分析期間")
    parser.add_argument("--config", help="設定JSONファイルパス")
    
    args = parser.parse_args()
    
    # 設定ファイル読み込み
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        category = config.get("category", args.category)
        time_range = config.get("time_range", args.timerange)
    else:
        category = args.category
        time_range = args.timerange
    
    # フレームワーク実行
    framework = CategoryEntryPointsFramework()
    result = await framework.collect_data(category, time_range)
    
    # 結果保存・表示
    framework.save_results(result)
    framework.print_summary(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## 3. 共通設計パターン

### 3.1 ファイル構造統一

```python
# 全フレームワーク共通のファイル構造
"""
#!/usr/bin/env python3
フレームX: [フレームワーク名]
実行方法: python framework_XX_name.py
"""

import asyncio
import json
import time
import argparse
from datetime import datetime
from typing import List, Dict, Any
import os

class FrameworkXXXX:
    def __init__(self):
        self.framework_id = XX
        self.framework_name = "Framework Name"
        self.version = "1.0.0"
        self.output_dir = f"output_framework_{self.framework_id:02d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def collect_data(self, **kwargs) -> Dict[str, Any]:
        """メインデータ収集・分析ロジック"""
        pass
    
    def save_results(self, result: Dict[str, Any]) -> None:
        """結果保存（JSON, CSV, 画像等）"""
        pass
    
    def print_summary(self, result: Dict[str, Any]) -> None:
        """結果サマリー表示"""
        pass

# サンプルデータ定義
SAMPLE_DATA = {...}

async def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(description="フレームワーク説明")
    # 引数定義
    args = parser.parse_args()
    
    # フレームワーク実行
    framework = FrameworkXXXX()
    result = await framework.collect_data(**params)
    
    # 結果処理
    framework.save_results(result)
    framework.print_summary(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### 3.2 統一出力形式

```bash
# 実行例
$ python framework_05_share_of_search.py --brand "コカコーラ" --competitors "ペプシ" "伊右衛門"

🚀 Share of Search v1.0.0 開始
📁 出力ディレクトリ: output_framework_05_20241201_143022
📊 分析開始: コカコーラ vs ['ペプシ', '伊右衛門']
🔗 Google Trends API接続中...
🔍 検索データ取得: ['コカコーラ', 'ペプシ', '伊右衛門']
🧮 Share of Search 計算中...
✅ 分析完了 (12.34秒)
💾 結果保存: output_framework_05_20241201_143022/sos_analysis_result.json
📊 CSV保存: output_framework_05_20241201_143022/share_of_search.csv
📈 グラフ保存: output_framework_05_20241201_143022/sos_analysis_chart.png

📋 Share of Search 実行結果サマリー
==================================================
🎯 対象ブランド: コカコーラ
🆚 競合ブランド: ペプシ, 伊右衛門
⏱️  実行時間: 12.34秒

📊 Share of Search結果:
  コカコーラ: 45.2%
  ペプシ: 28.7%
  伊右衛門: 26.1%

🏆 競合ポジション:
  順位: 1/3位
  市場リーダー: コカコーラ
  リーダーとの差: 0.0%

💡 主要洞察:
  • 検索シェア1位はコカコーラで45.2%
  • 上昇トレンド: コカコーラ
  • 競合激戦状況

📁 詳細結果は output_framework_05_20241201_143022 フォルダに保存されました
```

## 4. 実装優先順リスト

### 4.1 即座実装可能（P0）

1. **framework_05_share_of_search.py** 
   - Google Trends API使用
   - 技術リスク低・効果明確

2. **framework_12_copy_dna.py**
   - テキスト分析のみ
   - 外部API依存なし

3. **framework_03_dba_score.py**
   - 調査データ模擬可能

### 4.2 中期実装（P1）

4. **framework_02_cep_distribution.py**
5. **framework_13_meme_emoji.py**
6. **framework_01_brand_key.py**

### 4.3 高度実装（P2）

7. **framework_09_emotion_eye.py**
8. **framework_11_shopper_journey.py**
9. **framework_20_media_mix.py**

## 5. 実行・テスト方法

### 5.1 基本実行

```bash
# デフォルト実行
python framework_05_share_of_search.py

# パラメータ指定実行
python framework_05_share_of_search.py --brand "Apple" --competitors "Samsung" "Google"

# 設定ファイル使用
python framework_05_share_of_search.py --config myconfig.json
```

### 5.2 設定ファイル例

```json
{
  "brand_name": "iPhone",
  "competitors": ["Galaxy", "Pixel", "Xperia"],
  "category": "スマートフォン",
  "time_range": "today 6-m"
}
```

### 5.3 バッチ実行

```bash
# 複数フレームワーク連続実行
python framework_05_share_of_search.py
python framework_02_cep_distribution.py
python framework_13_meme_emoji.py
```

---

この設計により、**各フレームワークが完全独立**で動作し、`python framework_XX.py`で即座に実行可能になります！ 