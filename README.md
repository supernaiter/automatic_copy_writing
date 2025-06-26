# 25フレームワーク スタンドアロン実行システム

## 概要

各フレームワークが**完全独立**で動作するコピーライティング分析システムです。`python framework_XX.py`でいきなり実行可能。

## 🚀 クイックスタート

### 1. 依存関係インストール

```bash
# 基本パッケージのみ（最小構成）
pip install pandas numpy matplotlib seaborn

# 全機能利用（推奨）
pip install -r requirements_standalone.txt
```

### 2. 単体実行

```bash
# フレーム5: Share of Search 分析
python framework_05_share_of_search.py

# フレーム12: Copy DNA 分析
python framework_12_copy_dna.py

# パラメータ指定実行
python framework_05_share_of_search.py --brand "iPhone" --competitors "Galaxy" "Pixel"
```

### 3. 一括実行

```bash
# 実装済みフレームワークを全実行
python run_all_frameworks.py --priority ready

# P0優先度のみ実行
python run_all_frameworks.py --priority P0

# 実行シミュレート
python run_all_frameworks.py --dry-run
```

## 📦 実装済みフレームワーク

| ID | フレームワーク名 | 実行コマンド | 優先度 | 推定時間 |
|----|-----------------|-------------|--------|---------|
| 5  | Share of Search | `python framework_05_share_of_search.py` | P0 | 30秒 |
| 12 | Copy DNA Audit | `python framework_12_copy_dna.py` | P0 | 15秒 |
| 3  | DBA Score | `framework_03_dba_score.py` | P0 | 10秒 |

## 🎯 個別フレームワーク詳細

### フレーム5: Share of Search

**機能**: Google Trendsデータから検索シェア分析

```bash
# 基本実行
python framework_05_share_of_search.py

# ブランド指定
python framework_05_share_of_search.py --brand "コカコーラ" --competitors "ペプシ" "伊右衛門"

# 設定ファイル使用
python framework_05_share_of_search.py --config config_sos.json
```

**設定ファイル例 (config_sos.json)**:
```json
{
  "brand_name": "iPhone",
  "competitors": ["Galaxy", "Pixel", "Xperia"],
  "category": "スマートフォン",
  "time_range": "today 6-m"
}
```

**出力ファイル**:
- `output_framework_05_YYYYMMDD_HHMMSS/sos_analysis_result.json`
- `output_framework_05_YYYYMMDD_HHMMSS/share_of_search.csv`
- `output_framework_05_YYYYMMDD_HHMMSS/sos_analysis_chart.png`

### フレーム12: Copy DNA Audit

**機能**: コピーライティングの語彙・リズム・構文分析

```bash
# サンプルデータで実行
python framework_12_copy_dna.py

# テキストファイルから読み込み
python framework_12_copy_dna.py --file copy_samples.txt --brand "マイブランド"

# 設定ファイル使用
python framework_12_copy_dna.py --config config_dna.json
```

**入力ファイル例 (copy_samples.txt)**:
```
新しい朝が始まる。一杯のコーヒーから。
美味しさに、こだわり続けて50年。
あなたの毎日を、もっと素晴らしく！
```

**設定ファイル例 (config_dna.json)**:
```json
{
  "brand_name": "コーヒーブランド",
  "copy_samples": [
    "新しい朝が始まる。一杯のコーヒーから。",
    "美味しさに、こだわり続けて50年。",
    "あなたの毎日を、もっと素晴らしく！"
  ]
}
```

**出力ファイル**:
- `output_framework_12_YYYYMMDD_HHMMSS/copy_dna_analysis_result.json`
- `output_framework_12_YYYYMMDD_HHMMSS/vocabulary_frequency.csv`
- `output_framework_12_YYYYMMDD_HHMMSS/copy_dna_analysis_chart.png`

## 🔧 一括実行システム

### 基本使用法

```bash
# 利用可能フレームワーク一覧
python run_all_frameworks.py --list

# 実装済みフレームワーク全実行
python run_all_frameworks.py --priority ready

# P0優先度のみ実行
python run_all_frameworks.py --priority P0

# 実行シミュレート（実際に実行しない）
python run_all_frameworks.py --dry-run --priority P0
```

### 実行結果例

```
🚀 Framework Batch Runner v1.0.0 開始
📁 実行結果ディレクトリ: batch_results_20241201_143022

🎯 実行開始: 優先度フィルタ=ready

============================================================
📦 フレームワーク 1/3: Share of Search
📄 スクリプト: framework_05_share_of_search.py
⏱️  推定時間: 30秒
============================================================
🚀 実行中: framework_05_share_of_search.py
✅ 成功: Share of Search (12.34秒)
📊 進捗: 1/3 (100.0% 成功率)

============================================================
📦 フレームワーク 2/3: Copy DNA Audit
📄 スクリプト: framework_12_copy_dna.py
⏱️  推定時間: 15秒
============================================================
🚀 実行中: framework_12_copy_dna.py
✅ 成功: Copy DNA Audit (8.76秒)
📊 進捗: 2/3 (100.0% 成功率)

🏁 バッチ実行完了サマリー
============================================================
📊 実行結果: 3/3 成功 (100.0%)
⏱️  総実行時間: 35.2秒 (0.6分)
📈 平均実行時間: 11.7秒
🚀 最速: DBA Score
🐌 最低速: Share of Search

📁 詳細結果: batch_results_20241201_143022/
```

## 📂 出力ファイル構造

各フレームワーク実行後、以下のような構造でファイルが生成されます：

```
project_root/
├── framework_05_share_of_search.py
├── framework_12_copy_dna.py
├── run_all_frameworks.py
├── output_framework_05_20241201_143022/
│   ├── sos_analysis_result.json       # 分析結果JSON
│   ├── share_of_search.csv           # 数値データCSV
│   └── sos_analysis_chart.png        # 可視化グラフ
├── output_framework_12_20241201_143530/
│   ├── copy_dna_analysis_result.json  # 分析結果JSON
│   ├── vocabulary_frequency.csv      # 語彙頻度CSV
│   └── copy_dna_analysis_chart.png   # 可視化グラフ
└── batch_results_20241201_143022/
    └── batch_execution_results.json   # 一括実行結果
```

## 🛠️ カスタマイズ

### 新しいフレームワーク追加

1. `framework_XX_name.py`ファイル作成
2. 共通インターフェースに従って実装
3. `run_all_frameworks.py`の`frameworks`リストに追加

### 共通インターフェース仕様

```python
#!/usr/bin/env python3
"""
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

async def main():
    """メイン実行関数"""
    # argparse設定
    # フレームワーク実行
    # 結果保存・表示

if __name__ == "__main__":
    asyncio.run(main())
```

## 🚨 トラブルシューティング

### 依存関係エラー

```bash
# エラー: ModuleNotFoundError: No module named 'pytrends'
pip install pytrends

# 一括インストール
pip install -r requirements_standalone.txt
```

### Google Trends API制限

```
❌ エラー: 検索データが取得できませんでした
```

**解決策**:
- 5分待ってから再実行
- キーワード数を減らす（5個以下推奨）
- VPN使用時は無効化

### 日本語テキスト処理エラー

```bash
# MeCab関連エラーの場合
pip install mecab-python3

# jieba使用エラーの場合
pip install jieba
```

## 📈 パフォーマンス最適化

### 並列実行

```bash
# 複数フレームワークを並列実行（手動）
python framework_05_share_of_search.py &
python framework_12_copy_dna.py &
wait
```

### 大量データ処理

- CSVファイルは pandas.read_csv(chunksize=1000) 使用
- メモリ使用量監視: `htop` コマンド
- 長時間実行時は nohup 使用

## 🔐 API キー設定

環境変数でAPIキーを設定：

```bash
# .envファイル作成
echo "OPENAI_API_KEY=your_openai_key" >> .env
echo "TWITTER_BEARER_TOKEN=your_twitter_token" >> .env

# 環境変数読み込み
export $(cat .env | xargs)

# Python内で使用
import os
api_key = os.getenv("OPENAI_API_KEY")
```

## 📊 開発ロードマップ

### Phase 1: Foundation (完了)
- ✅ フレーム5: Share of Search
- ✅ フレーム12: Copy DNA Audit  
- ✅ 一括実行システム

### Phase 2: Core Expansion (進行中)
- 🚧 フレーム2: CEP Distribution
- 🚧 フレーム13: Meme & Emoji Analysis
- 🚧 フレーム1: Brand Key Analysis

### Phase 3: Advanced Features (計画中)
- 📋 フレーム9: Emotion Recognition
- 📋 フレーム11: Shopper Journey
- 📋 フレーム16: Persona Dialogue

### Phase 4: Full Integration (計画中)
- 📋 全25フレームワーク統合
- 📋 リアルタイムダッシュボード
- 📋 自動レポート生成

## 🤝 コントリビューション

1. Issue作成で機能要求・バグ報告
2. Fork & Pull Request
3. テストカバレッジ維持
4. ドキュメント更新

## 📝 ライセンス

MIT License - 商用利用可能

---

**作成**: 2024年12月1日  
**最終更新**: 2024年12月1日  
**バージョン**: 1.0.0 