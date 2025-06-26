# Automatic Copy Writing - Component Architecture

## 概要

本プロジェクトは、コピーライティング分析・最適化のための25フレームワークシステムを、**独立コンポーネント**として構築しています。

## 新しいアーキテクチャ

### リポジトリ型コンポーネント設計
- 各コンポーネントが独立したリポジトリ構造を持つ
- 単独でインストール・実行・開発が可能
- 他のコンポーネントに依存しない自己完結性

### 現在のコンポーネント

#### 1. framework-analysis
**分析系フレームワーク群**
```
components/framework-analysis/
├── src/
│   └── framework_05_share_of_search.py    # Google Trends検索シェア分析
├── tests/
├── docs/
├── requirements.txt
├── setup.py
└── README.md
```

#### 2. framework-creative
**クリエイティブ系フレームワーク群**
```
components/framework-creative/
├── src/
│   └── framework_12_copy_dna.py           # コピーライティングDNA分析
├── tests/
├── docs/
├── requirements.txt
├── setup.py
└── README.md
```

## 使用方法

### 1. 個別コンポーネント実行

#### Framework 5: Share of Search
```bash
cd components/framework-analysis
python src/framework_05_share_of_search.py
```

#### Framework 12: Copy DNA Audit
```bash
cd components/framework-creative  
python src/framework_12_copy_dna.py
```

### 2. 統合管理スクリプト実行

#### コンポーネント一覧表示
```bash
python scripts/run_component.py --list
```

#### フレームワーク実行
```bash
# Framework 5 実行
python scripts/run_component.py framework-analysis 5

# Framework 12 実行  
python scripts/run_component.py framework-creative 12

# カスタムオプション付き実行
python scripts/run_component.py framework-analysis 5 --brand "トヨタ" --competitors "ホンダ" "日産"
```

## 依存関係管理

### 全体依存関係
```bash
# 基本ライブラリ（全コンポーネント共通）
pip install pandas numpy matplotlib
```

### コンポーネント固有依存関係
```bash
# framework-analysis
cd components/framework-analysis
pip install -r requirements.txt

# framework-creative
cd components/framework-creative
pip install -r requirements.txt
```

## 出力管理

各コンポーネントは独自の出力ディレクトリを持ちます：

```
components/
├── framework-analysis/
│   └── output/
│       └── framework_05_YYYYMMDD_HHMMSS/
├── framework-creative/
│   └── output/
│       └── framework_12_YYYYMMDD_HHMMSS/
```

## 開発・拡張

### 新しいフレームワーク追加

1. 適切なコンポーネントの `src/` ディレクトリに追加
2. `scripts/run_component.py` のCOMPONENTS辞書を更新
3. コンポーネントのREADMEを更新

### 新しいコンポーネント作成

```bash
mkdir -p components/new-component/{src,tests,docs,data,examples}
cd components/new-component
# setup.py, requirements.txt, README.md を作成
```

## 利点

### 独立性
- 他コンポーネントへの依存なし
- 単独でテスト・デプロイ可能
- チーム並行開発可能

### 拡張性
- フレームワーク単位での機能追加
- コンポーネント単位でのバージョン管理
- 段階的リリース対応

### 保守性
- 責任分離による保守性向上
- 依存関係の明確化
- 独立したテスト実行

## 今後の計画

### Phase 2: 追加コンポーネント
- `framework-evaluation`: 評価系フレームワーク
- `framework-optimization`: 最適化系フレームワーク
- `engine-llm`: LLM統合エンジン
- `api-integrations`: 外部API統合

### Phase 3: 高度機能
- コンポーネント間オーケストレーション
- 分散実行システム
- 結果統合・比較機能

## 移行状況

- ✅ framework-analysis (Framework 5)
- ✅ framework-creative (Framework 12)  
- 🔄 25フレームワーク完全移行 (進行中)
- 📋 統合管理システム (完了)

---

本アーキテクチャにより、巨大システムを管理可能な独立コンポーネントとして分割し、開発・運用・拡張の効率を大幅に向上させています。 