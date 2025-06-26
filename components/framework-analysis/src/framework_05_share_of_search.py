#!/usr/bin/env python3
"""
Framework 5: Share of Search Analysis
Analysis Frameworks Component

実行方法:
  python src/framework_05_share_of_search.py

独立コンポーネントとして動作します。
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
    
    def __init__(self, output_base_dir: str = "output"):
        self.framework_id = 5
        self.framework_name = "Share of Search"
        self.version = "1.0.0"
        self.component_name = "framework-analysis"
        
        # 出力ディレクトリをコンポーネント内に設定
        self.output_dir = os.path.join(
            output_base_dir,
            f"framework_05_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        # 出力ディレクトリ作成
        os.makedirs(self.output_dir, exist_ok=True)
        
        print(f"🚀 {self.framework_name} v{self.version}")
        print(f"📦 Component: {self.component_name}")
        print(f"📁 Output: {self.output_dir}")
    
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
                    "component": self.component_name,
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
                    "component": self.component_name,
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
        
        # ギャップ分析
        gap = competitive_analysis["gap_to_leader"]
        if gap > 20:
            insights.append(f"リーダーとのギャップが大きい（{gap:.1f}ポイント差）")
        elif gap > 0:
            insights.append(f"リーダーに接戦中（{gap:.1f}ポイント差）")
        
        return insights
    
    def save_results(self, result: Dict[str, Any]) -> None:
        """結果保存"""
        try:
            # JSON結果保存
            json_path = os.path.join(self.output_dir, "sos_analysis_result.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2, default=self._json_serializer)
            
            print(f"📄 結果保存: {json_path}")
            
            # 可視化
            if result["success"]:
                self._save_visualization(result)
            
        except Exception as e:
            print(f"❌ 保存エラー: {str(e)}")
    
    def _json_serializer(self, obj):
        """JSON serialization helper"""
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        elif hasattr(obj, 'item'):  # numpy types
            return obj.item()
        elif hasattr(obj, 'tolist'):  # numpy arrays
            return obj.tolist()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    def _save_visualization(self, result: Dict[str, Any]) -> None:
        """可視化結果保存"""
        try:
            sos_data = result["share_of_search"]
            
            # Share of Search円グラフ
            plt.figure(figsize=(10, 8))
            
            brands = list(sos_data.keys())
            shares = list(sos_data.values())
            
            colors = plt.cm.Set3(range(len(brands)))
            
            plt.pie(shares, labels=brands, autopct='%1.1f%%', colors=colors, startangle=90)
            plt.title('Share of Search Analysis', fontsize=16, pad=20)
            plt.axis('equal')
            
            # 日本語フォント設定（エラーハンドリング付き）
            try:
                plt.rcParams['font.family'] = 'DejaVu Sans'
            except:
                pass
            
            chart_path = os.path.join(self.output_dir, "share_of_search_chart.png")
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"📈 可視化保存: {chart_path}")
            
        except Exception as e:
            print(f"⚠️ 可視化エラー: {str(e)}")
    
    def print_summary(self, result: Dict[str, Any]) -> None:
        """結果サマリー表示"""
        if not result["success"]:
            print(f"❌ 分析失敗: {result.get('framework_info', {}).get('error', 'Unknown error')}")
            return
        
        print(f"\n{'='*60}")
        print(f"📊 Share of Search Analysis Summary")
        print(f"{'='*60}")
        
        # フレームワーク情報
        fw_info = result["framework_info"]
        print(f"📦 Component: {fw_info['component']}")
        print(f"⏱️  実行時間: {fw_info['execution_time']:.2f}秒")
        print(f"📅 実行日時: {fw_info['timestamp']}")
        
        # 入力パラメータ
        params = result["input_parameters"]
        print(f"\n🎯 分析対象:")
        print(f"  • メインブランド: {params['brand_name']}")
        print(f"  • 競合ブランド: {', '.join(params['competitors'])}")
        print(f"  • カテゴリ: {params['category']}")
        print(f"  • 期間: {params['time_range']}")
        
        # Share of Search結果
        sos_data = result["share_of_search"]
        print(f"\n📈 Share of Search結果:")
        sorted_sos = sorted(sos_data.items(), key=lambda x: x[1], reverse=True)
        for i, (brand, share) in enumerate(sorted_sos, 1):
            print(f"  {i}位: {brand} - {share:.1f}%")
        
        # 競合分析
        comp_analysis = result["competitive_analysis"]
        print(f"\n🏆 競合ポジション:")
        print(f"  • 順位: {comp_analysis['brand_rank']}/{comp_analysis['total_brands']}位")
        print(f"  • マーケットリーダー: {comp_analysis['market_leader']}")
        print(f"  • リーダーとのギャップ: {comp_analysis['gap_to_leader']:.1f}ポイント")
        
        # インサイト
        insights = result["insights"]
        print(f"\n💡 主要インサイト:")
        for i, insight in enumerate(insights, 1):
            print(f"  {i}. {insight}")
        
        print(f"\n📁 詳細結果は {self.output_dir} に保存されました")

# サンプルデータ
SAMPLE_BRAND_DATA = {
    "brand_name": "コカコーラ",
    "competitors": ["ペプシ", "午後の紅茶", "伊右衛門"],
    "category": "飲料",
    "time_range": "today 12-m"
}

async def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(description='Share of Search Analysis Framework')
    parser.add_argument('--brand', type=str, default=SAMPLE_BRAND_DATA['brand_name'], help='メインブランド名')
    parser.add_argument('--competitors', nargs='+', default=SAMPLE_BRAND_DATA['competitors'], help='競合ブランドリスト')
    parser.add_argument('--category', type=str, default=SAMPLE_BRAND_DATA['category'], help='カテゴリ名')
    parser.add_argument('--timerange', type=str, default=SAMPLE_BRAND_DATA['time_range'], help='時間範囲')
    parser.add_argument('--output', type=str, default='output', help='出力ディレクトリ')
    
    args = parser.parse_args()
    
    # フレームワーク初期化
    framework = ShareOfSearchFramework(output_base_dir=args.output)
    
    print(f"🎯 ブランド: {args.brand}")
    print(f"🏃 競合: {args.competitors}")
    print(f"📂 カテゴリ: {args.category}")
    
    # 分析実行
    result = await framework.collect_data(
        args.brand, 
        args.competitors, 
        args.category, 
        args.timerange
    )
    
    # 結果保存
    framework.save_results(result)
    
    # サマリー表示
    framework.print_summary(result)

if __name__ == "__main__":
    asyncio.run(main()) 