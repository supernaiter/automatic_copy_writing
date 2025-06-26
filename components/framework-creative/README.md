# Framework Creative Component

クリエイティブ系フレームワークを提供するスタンドアロンコンポーネント

## 概要

このコンポーネントは、コピーライティング・クリエイティブ分析関連のフレームワークを独立実行可能な形で提供します。

## 含まれるフレームワーク

### Framework 12: Copy DNA Audit
- **機能**: コピーライティングの語彙・リズム・構文分析
- **実行**: `python src/framework_12_copy_dna.py`
- **出力**: JSON詳細分析、CSV語彙頻度、PNG可視化

## 使用方法

### 基本実行
```bash
cd components/framework-creative
python src/framework_12_copy_dna.py
```

### カスタム実行
```bash
python src/framework_12_copy_dna.py --brand "ブランド名" --output "custom_output"
```

### 独自コピー分析
```bash
python src/framework_12_copy_dna.py --copies "コピー1" "コピー2" "コピー3"
```

## 依存関係

```bash
pip install pandas numpy matplotlib seaborn jieba wordcloud
```

## 出力構造

```
output/
├── framework_12_YYYYMMDD_HHMMSS/
│   ├── copy_dna_analysis_result.json  # 詳細分析結果
│   ├── vocabulary_frequency.csv       # 語彙頻度データ
│   └── copy_dna_analysis_chart.png    # 可視化グラフ
```

## 分析項目

- **基本統計**: 文字数、文数、語数の統計
- **語彙分析**: 語彙豊富度、N-gram、文字種別比率
- **リズム分析**: 音節数、句読点頻度、テンポ分類
- **構文分析**: 文の長さ、修辞技法、複文比率
- **感情分析**: トーン分類、感情比率、緊急性
- **DNAパターン**: 統合的特徴プロファイル

## 独立性

このコンポーネントは：
- 他のコンポーネントに依存しない
- 単独でインストール・実行可能
- 独自の依存関係管理
- 専用の出力ディレクトリ

## 開発・拡張

新しいクリエイティブフレームワークを追加する場合は、`src/`ディレクトリに追加し、このREADMEを更新してください。 