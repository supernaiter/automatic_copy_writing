#!/usr/bin/env python3
"""
全25フレームワーク 一括実行スクリプト
実行方法: python run_all_frameworks.py
"""

import asyncio
import subprocess
import time
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any
import argparse

class FrameworkBatchRunner:
    """25フレームワーク一括実行システム"""
    
    def __init__(self):
        self.runner_name = "Framework Batch Runner"
        self.version = "1.0.0"
        self.start_time = datetime.now()
        self.results_dir = f"data/output/batch_results_{self.start_time.strftime('%Y%m%d_%H%M%S')}"
        
        # 実行結果ディレクトリ作成
        os.makedirs(self.results_dir, exist_ok=True)
        
        print(f"🚀 {self.runner_name} v{self.version} 開始")
        print(f"📁 実行結果ディレクトリ: {self.results_dir}")
        
        # フレームワーク実行順序定義
        self.frameworks = [
            {
                "id": 5,
                "name": "Share of Search",
                "script": "framework_05_share_of_search.py",
                "priority": "P0",
                "estimated_time": "30秒",
                "dependencies": ["pytrends", "pandas", "matplotlib"]
            },
            {
                "id": 12,
                "name": "Copy DNA Audit",
                "script": "framework_12_copy_dna.py",
                "priority": "P0", 
                "estimated_time": "15秒",
                "dependencies": ["jieba", "wordcloud", "pandas"]
            },
            {
                "id": 3,
                "name": "DBA Score",
                "script": "framework_03_dba_score.py",
                "priority": "P0",
                "estimated_time": "10秒",
                "dependencies": ["pandas", "numpy"]
            },
            {
                "id": 2,
                "name": "CEP Distribution",
                "script": "framework_02_cep_distribution.py",
                "priority": "P1",
                "estimated_time": "45秒",
                "dependencies": ["tweepy", "openai", "pandas"]
            },
            {
                "id": 13,
                "name": "Meme & Emoji Analysis",
                "script": "framework_13_meme_emoji.py",
                "priority": "P1",
                "estimated_time": "60秒",
                "dependencies": ["tweepy", "transformers"]
            },
            {
                "id": 1,
                "name": "Brand Key Analysis",
                "script": "framework_01_brand_key.py",
                "priority": "P1",
                "estimated_time": "90秒",
                "dependencies": ["openai", "pandas"]
            },
            # 以下のフレームワークは実装予定
            {
                "id": 4,
                "name": "Sound Pattern Analysis",
                "script": "framework_04_sound_pattern.py",
                "priority": "P2",
                "estimated_time": "120秒",
                "dependencies": ["librosa", "pyaudio"],
                "status": "planned"
            },
            {
                "id": 6,
                "name": "Price Sensitivity",
                "script": "framework_06_price_sensitivity.py",
                "priority": "P2",
                "estimated_time": "20秒",
                "dependencies": ["pandas", "scipy"],
                "status": "planned"
            },
            {
                "id": 7,
                "name": "Purchase Timing",
                "script": "framework_07_purchase_timing.py",
                "priority": "P2",
                "estimated_time": "30秒",
                "dependencies": ["pandas", "statsmodels"],
                "status": "planned"
            },
            {
                "id": 8,
                "name": "A/B Test Design",
                "script": "framework_08_ab_test_design.py",
                "priority": "P2",
                "estimated_time": "25秒",
                "dependencies": ["scipy", "statsmodels"],
                "status": "planned"
            },
            {
                "id": 9,
                "name": "Emotion Recognition",
                "script": "framework_09_emotion_recognition.py",
                "priority": "P3",
                "estimated_time": "180秒",
                "dependencies": ["opencv-python", "torch", "transformers"],
                "status": "planned"
            },
            {
                "id": 10,
                "name": "Color Psychology",
                "script": "framework_10_color_psychology.py",
                "priority": "P3",
                "estimated_time": "40秒",
                "dependencies": ["colormath", "matplotlib"],
                "status": "planned"
            },
            {
                "id": 11,
                "name": "Shopper Journey",
                "script": "framework_11_shopper_journey.py",
                "priority": "P3",
                "estimated_time": "60秒",
                "dependencies": ["networkx", "pandas"],
                "status": "planned"
            },
            {
                "id": 14,
                "name": "Competitive Analysis",
                "script": "framework_14_competitive_analysis.py",
                "priority": "P3",
                "estimated_time": "90秒",
                "dependencies": ["beautifulsoup4", "selenium"],
                "status": "planned"
            },
            {
                "id": 15,
                "name": "Viral Prediction",
                "script": "framework_15_viral_prediction.py",
                "priority": "P3",
                "estimated_time": "75秒",
                "dependencies": ["networkx", "scipy"],
                "status": "planned"
            },
            {
                "id": 16,
                "name": "Persona Dialogue",
                "script": "framework_16_persona_dialogue.py",
                "priority": "P3",
                "estimated_time": "120秒",
                "dependencies": ["openai"],
                "status": "planned"
            },
            {
                "id": 17,
                "name": "Emotion Journey",
                "script": "framework_17_emotion_journey.py",
                "priority": "P3",
                "estimated_time": "100秒",
                "dependencies": ["transformers"],
                "status": "planned"
            },
            {
                "id": 18,
                "name": "Expert Knowledge Integration",
                "script": "framework_18_expert_knowledge.py",
                "priority": "P4",
                "estimated_time": "150秒",
                "dependencies": ["transformers", "openai"],
                "status": "planned"
            },
            {
                "id": 19,
                "name": "Social Listening",
                "script": "framework_19_social_listening.py",
                "priority": "P4",
                "estimated_time": "90秒",
                "dependencies": ["tweepy", "textblob"],
                "status": "planned"
            },
            {
                "id": 20,
                "name": "Media Mix Optimization",
                "script": "framework_20_media_mix.py",
                "priority": "P4",
                "estimated_time": "60秒",
                "dependencies": ["pandas", "scipy"],
                "status": "planned"
            },
            {
                "id": 21,
                "name": "Search Query Mining",
                "script": "framework_21_search_query_mining.py",
                "priority": "P4",
                "estimated_time": "70秒",
                "dependencies": ["pytrends", "beautifulsoup4"],
                "status": "planned"
            },
            {
                "id": 22,
                "name": "Trend Prediction",
                "script": "framework_22_trend_prediction.py",
                "priority": "P4",
                "estimated_time": "80秒",
                "dependencies": ["statsmodels", "sklearn"],
                "status": "planned"
            },
            {
                "id": 23,
                "name": "Influencer Analysis",
                "script": "framework_23_influencer_analysis.py",
                "priority": "P4",
                "estimated_time": "110秒",
                "dependencies": ["tweepy", "networkx"],
                "status": "planned"
            },
            {
                "id": 24,
                "name": "ROI Prediction",
                "script": "framework_24_roi_prediction.py",
                "priority": "P4",
                "estimated_time": "90秒",
                "dependencies": ["sklearn", "statsmodels"],
                "status": "planned"
            },
            {
                "id": 25,
                "name": "Real-time Monitoring",
                "script": "framework_25_realtime_monitoring.py",
                "priority": "P4",
                "estimated_time": "継続実行",
                "dependencies": ["asyncio", "websockets"],
                "status": "planned"
            }
        ]
    
    async def run_all_frameworks(self, priority_filter: str = "all", dry_run: bool = False) -> Dict[str, Any]:
        """全フレームワーク実行"""
        
        execution_start = time.time()
        print(f"\n🎯 実行開始: 優先度フィルタ={priority_filter}")
        
        # 実行対象フレームワーク選択
        target_frameworks = self._filter_frameworks(priority_filter)
        
        if dry_run:
            print(f"🔧 ドライラン: {len(target_frameworks)}個のフレームワークをシミュレート")
            return self._simulate_execution(target_frameworks)
        
        # 実行結果保存用
        execution_results = {
            "batch_info": {
                "runner_name": self.runner_name,
                "version": self.version,
                "start_time": self.start_time.isoformat(),
                "priority_filter": priority_filter,
                "target_count": len(target_frameworks)
            },
            "framework_results": [],
            "summary": {},
            "errors": []
        }
        
        # 順次実行
        for i, framework in enumerate(target_frameworks, 1):
            print(f"\n{'='*60}")
            print(f"📦 フレームワーク {i}/{len(target_frameworks)}: {framework['name']}")
            print(f"📄 スクリプト: {framework['script']}")
            print(f"⏱️  推定時間: {framework['estimated_time']}")
            print(f"{'='*60}")
            
            framework_result = await self._run_single_framework(framework)
            execution_results["framework_results"].append(framework_result)
            
            # 進捗表示
            success_rate = len([r for r in execution_results["framework_results"] if r["success"]]) / len(execution_results["framework_results"]) * 100
            print(f"📊 進捗: {i}/{len(target_frameworks)} ({success_rate:.1f}% 成功率)")
        
        # サマリー生成
        execution_results["summary"] = self._generate_summary(execution_results["framework_results"])
        execution_results["batch_info"]["total_execution_time"] = time.time() - execution_start
        
        # 結果保存
        self._save_batch_results(execution_results)
        
        # サマリー表示
        self._print_batch_summary(execution_results)
        
        return execution_results
    
    def _filter_frameworks(self, priority_filter: str) -> List[Dict[str, Any]]:
        """優先度によるフレームワークフィルタリング"""
        if priority_filter == "all":
            return self.frameworks
        elif priority_filter == "ready":
            # 実際に実装済みのファイルのみ返す
            ready_frameworks = []
            for f in self.frameworks:
                if f.get("status", "ready") == "ready":
                    script_path = f["script"]
                    if not os.path.exists(script_path):
                        script_path = os.path.join("src", "frameworks", script_path)
                    if os.path.exists(script_path):
                        ready_frameworks.append(f)
            return ready_frameworks
        elif priority_filter in ["P0", "P1", "P2", "P3", "P4"]:
            return [f for f in self.frameworks if f["priority"] == priority_filter and f.get("status", "ready") == "ready"]
        else:
            print(f"⚠️  不明な優先度フィルタ: {priority_filter}")
            return self.frameworks
    
    async def _run_single_framework(self, framework: Dict[str, Any]) -> Dict[str, Any]:
        """単一フレームワーク実行"""
        
        framework_start = time.time()
        script_path = os.path.join("src", "frameworks", framework["script"])
        
        try:
            # スクリプト存在確認
            if not os.path.exists(script_path):
                raise FileNotFoundError(f"スクリプトファイルが見つかりません: {framework['script']}")
            
            # 依存関係チェック（簡易版）
            missing_deps = self._check_dependencies(framework.get("dependencies", []))
            if missing_deps:
                print(f"⚠️  不足依存関係: {missing_deps}")
                print("pip install で追加インストールしてください")
            
            # 非同期でプロセス実行
            print(f"🚀 実行中: {script_path}")
            process = await asyncio.create_subprocess_exec(
                sys.executable, script_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            execution_time = time.time() - framework_start
            
            if process.returncode == 0:
                print(f"✅ 成功: {framework['name']} ({execution_time:.2f}秒)")
                return {
                    "framework_id": framework["id"],
                    "framework_name": framework["name"],
                    "script": script_path,
                    "success": True,
                    "execution_time": execution_time,
                    "stdout": stdout.decode('utf-8', errors='ignore'),
                    "stderr": stderr.decode('utf-8', errors='ignore'),
                    "return_code": process.returncode
                }
            else:
                print(f"❌ 失敗: {framework['name']} (終了コード: {process.returncode})")
                return {
                    "framework_id": framework["id"],
                    "framework_name": framework["name"],
                    "script": script_path,
                    "success": False,
                    "execution_time": execution_time,
                    "error": stderr.decode('utf-8', errors='ignore'),
                    "return_code": process.returncode
                }
                
        except Exception as e:
            execution_time = time.time() - framework_start
            print(f"💥 例外エラー: {framework['name']} - {str(e)}")
            return {
                "framework_id": framework["id"],
                "framework_name": framework["name"],
                "script": script_path,
                "success": False,
                "execution_time": execution_time,
                "error": str(e),
                "exception": True
            }
    
    def _check_dependencies(self, dependencies: List[str]) -> List[str]:
        """依存関係チェック（簡易版）"""
        missing = []
        for dep in dependencies:
            try:
                __import__(dep)
            except ImportError:
                missing.append(dep)
        return missing
    
    def _simulate_execution(self, frameworks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """実行シミュレーション（ドライラン）"""
        print("\n🔧 ドライラン結果:")
        print("=" * 50)
        
        total_estimated_time = 0
        for i, framework in enumerate(frameworks, 1):
            print(f"{i:2d}. {framework['name']}")
            print(f"    📄 {framework['script']}")
            print(f"    ⏱️  {framework['estimated_time']}")
            print(f"    🏷️  {framework['priority']}")
            
            # 推定時間の数値抽出（簡易版）
            time_str = framework['estimated_time']
            if '秒' in time_str:
                try:
                    time_val = int(time_str.replace('秒', ''))
                    total_estimated_time += time_val
                except:
                    pass
            print()
        
        print(f"📊 実行予定: {len(frameworks)}個のフレームワーク")
        print(f"⏱️  推定実行時間: 約{total_estimated_time}秒 ({total_estimated_time/60:.1f}分)")
        
        return {
            "dry_run": True,
            "framework_count": len(frameworks),
            "estimated_time": total_estimated_time
        }
    
    def _generate_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """実行サマリー生成"""
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]
        
        total_time = sum(r["execution_time"] for r in results)
        avg_time = total_time / len(results) if results else 0
        
        return {
            "total_frameworks": len(results),
            "successful_count": len(successful),
            "failed_count": len(failed),
            "success_rate": len(successful) / len(results) * 100 if results else 0,
            "total_execution_time": total_time,
            "average_execution_time": avg_time,
            "fastest_framework": min(results, key=lambda x: x["execution_time"])["framework_name"] if results else None,
            "slowest_framework": max(results, key=lambda x: x["execution_time"])["framework_name"] if results else None
        }
    
    def _save_batch_results(self, results: Dict[str, Any]) -> None:
        """バッチ実行結果保存"""
        results_path = os.path.join(self.results_dir, "batch_execution_results.json")
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"💾 バッチ結果保存: {results_path}")
    
    def _print_batch_summary(self, results: Dict[str, Any]) -> None:
        """バッチ実行サマリー表示"""
        summary = results["summary"]
        
        print(f"\n🏁 バッチ実行完了サマリー")
        print("=" * 60)
        print(f"📊 実行結果: {summary['successful_count']}/{summary['total_frameworks']} 成功 ({summary['success_rate']:.1f}%)")
        print(f"⏱️  総実行時間: {summary['total_execution_time']:.1f}秒 ({summary['total_execution_time']/60:.1f}分)")
        print(f"📈 平均実行時間: {summary['average_execution_time']:.1f}秒")
        
        if summary['fastest_framework']:
            print(f"🚀 最速: {summary['fastest_framework']}")
        if summary['slowest_framework']:
            print(f"🐌 最低速: {summary['slowest_framework']}")
        
        # 失敗フレームワーク一覧
        failed_frameworks = [r for r in results["framework_results"] if not r["success"]]
        if failed_frameworks:
            print(f"\n❌ 失敗フレームワーク ({len(failed_frameworks)}件):")
            for failed in failed_frameworks:
                print(f"  • {failed['framework_name']}: {failed.get('error', 'Unknown error')[:100]}")
        
        print(f"\n📁 詳細結果: {self.results_dir}/")

async def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(description="25フレームワーク 一括実行システム")
    parser.add_argument("--priority", default="ready", choices=["all", "ready", "P0", "P1", "P2", "P3", "P4"],
                       help="実行優先度フィルタ")
    parser.add_argument("--dry-run", action="store_true", help="実際に実行せずにシミュレート")
    parser.add_argument("--list", action="store_true", help="利用可能なフレームワーク一覧表示")
    
    args = parser.parse_args()
    
    runner = FrameworkBatchRunner()
    
    if args.list:
        print("\n📋 利用可能フレームワーク一覧:")
        print("=" * 80)
        for fw in runner.frameworks:
            status = fw.get("status", "ready")
            status_emoji = "✅" if status == "ready" else "🚧"
            print(f"{status_emoji} {fw['id']:2d}. {fw['name']} ({fw['priority']}) - {fw['estimated_time']}")
        return
    
    # バッチ実行
    await runner.run_all_frameworks(
        priority_filter=args.priority,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    asyncio.run(main()) 