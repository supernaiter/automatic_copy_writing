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
import os
import sys

# 依存ライブラリチェック
try:
    from pytrends.request import TrendReq
except ImportError:
    print("❌ pytrends がインストールされていません。以下のコマンドでインストールしてください:")
    print("pip install pytrends pandas matplotlib")
    sys.exit(1)

class ShareOfSearchFramework:
    """Share of Search 分析フレームワーク - スタンドアロン版"""
    
    def __init__(self):
        self.framework_id = 5
        self.framework_name = "Share of Search"
        self.version = "1.0.0"
        self.output_dir = f"data/output/output_framework_05_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
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
                "raw_data_info": {
                    "rows": len(interest_data),
                    "columns": list(interest_data.columns),
                    "date_range": {
                        "start": interest_data.index[0].isoformat() if not interest_data.empty else None,
                        "end": interest_data.index[-1].isoformat() if not interest_data.empty else None
                    }
                },
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
        # JSON保存（numpy型を標準Python型に変換）
        json_path = os.path.join(self.output_dir, "sos_analysis_result.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2, default=self._json_serializer)
        print(f"💾 結果保存: {json_path}")
    
    def _json_serializer(self, obj):
        """JSON serialization helper for numpy and pandas types"""
        import numpy as np
        import pandas as pd
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        elif hasattr(obj, 'item'):  # numpy scalars
            return obj.item()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
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