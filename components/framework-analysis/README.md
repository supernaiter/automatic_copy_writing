# Framework Analysis Component

データ分析系フレームワークを提供するスタンドアロンコンポーネント

## 概要

このコンポーネントは、市場分析・競合分析・検索トレンド分析などのデータ分析関連フレームワークを独立実行可能な形で提供します。

## 含まれるフレームワーク

### Framework 5: Share of Search Analysis
- **機能**: Google Trendsを使った検索シェア分析
- **実行**: `python src/framework_05_share_of_search.py`
- **出力**: JSON詳細分析、PNG円グラフ

## 使用方法

### 基本実行（サンプルデータ）
```bash
cd components/framework-analysis
python src/framework_05_share_of_search.py
```

### カスタム分析
```bash
python src/framework_05_share_of_search.py \
  --brand "任意のブランド" \
  --competitors "競合1" "競合2" "競合3" \
  --category "カテゴリ名" \
  --timerange "today 12-m"
```

### 実行例
```bash
# 飲料ブランド分析
python src/framework_05_share_of_search.py \
  --brand "コカコーラ" \
  --competitors "ペプシ" "午後の紅茶" "伊右衛門" \
  --category "飲料"

# 自動車ブランド分析  
python src/framework_05_share_of_search.py \
  --brand "トヨタ" \
  --competitors "ホンダ" "日産" "マツダ" \
  --category "自動車"
```

## 依存関係

```bash
pip install pandas matplotlib pytrends
```

## 出力構造

```
output/
├── framework_05_YYYYMMDD_HHMMSS/
│   ├── sos_analysis_result.json       # 詳細分析結果
│   └── share_of_search_chart.png      # 検索シェア円グラフ
```

## 分析項目

- **Share of Search**: 各ブランドの検索シェア比率
- **トレンド分析**: 検索ボリュームの増減傾向
- **競合ポジション**: 市場内でのランキングとギャップ
- **インサイト**: データから導出される戦略的示唆

## API制限

- Google Trends API使用のため、短時間での大量リクエストは制限される場合があります
- 1回の分析で最大5ブランドまでの比較を推奨

## 独立性

このコンポーネントは：
- 他のコンポーネントに依存しない
- Google Trends APIに直接アクセス
- 独自の出力ディレクトリ管理
- サンプルデータ内蔵で即座実行可能

## 開発・拡張

新しい分析フレームワークを追加する場合は、`src/`ディレクトリに追加し、このREADMEを更新してください。 