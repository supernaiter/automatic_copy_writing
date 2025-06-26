# コンポーネントアーキテクチャ実装ガイド

## 目次
1. [アーキテクチャ概要](#アーキテクチャ概要)
2. [コンポーネント構造詳細](#コンポーネント構造詳細)
3. [開発ワークフロー](#開発ワークフロー)
4. [新規コンポーネント作成手順](#新規コンポーネント作成手順)
5. [ベストプラクティス](#ベストプラクティス)
6. [トラブルシューティング](#トラブルシューティング)

---

## アーキテクチャ概要

### 基本構造
```
automatic_copy_writing/
├── components/           # 独立コンポーネント群
│   ├── framework-analysis/    # 分析系フレームワーク
│   ├── framework-creative/    # クリエイティブ系フレームワーク
│   ├── framework-evaluation/  # 評価系フレームワーク（予定）
│   └── engine-llm/           # LLM統合エンジン（予定）
├── scripts/              # 全体管理スクリプト
├── docs/                # プロジェクト全体ドキュメント
└── data/                # 共有データ（最小限）
```

### 設計原則

#### 1. **完全独立性**
- 各コンポーネントは他に依存しない
- 単独でインストール・実行・テスト可能
- 独自の依存関係管理

#### 2. **リポジトリ型構造**
- 各コンポーネントが標準的なプロジェクト構造を持つ
- IDE最適化済み設定
- 完全なドキュメント・テスト完備

#### 3. **統一的インターフェース**
- 共通の実行パターン
- 標準的な出力形式
- 一貫したエラーハンドリング

---

## コンポーネント構造詳細

### 標準ディレクトリ構造
```
components/[component-name]/
├── src/                      # ソースコード
│   ├── framework_XX_name.py      # メインフレームワーク
│   └── __init__.py               # パッケージ初期化
├── tests/                    # テストスイート
│   ├── test_framework_XX.py      # ユニットテスト
│   └── conftest.py               # テスト設定
├── docs/                     # コンポーネント固有ドキュメント
├── data/                     # サンプル・設定データ
│   ├── samples/                  # サンプルデータ
│   └── schemas/                  # データスキーマ
├── examples/                 # 使用例・サンプル
├── output/                   # 実行結果（自動生成）
├── .vscode/                  # VSCode/Cursor設定
│   ├── settings.json             # エディタ設定
│   └── launch.json               # デバッグ設定
├── requirements.txt          # 依存関係
├── setup.py                  # パッケージ設定
├── pyproject.toml           # モダンPython設定
├── Makefile                 # 開発効率化コマンド
└── README.md                # 使用説明書
```

### 各ファイルの役割

#### 1. **メインフレームワーク** (`src/framework_XX_name.py`)
```python
#!/usr/bin/env python3
"""
Framework XX: [Name]
[Component Name] Component

実行方法:
  python src/framework_XX_name.py

独立コンポーネントとして動作します。
"""

class FrameworkXX:
    def __init__(self, output_base_dir: str = "output"):
        self.framework_id = XX
        self.framework_name = "[Name]"
        self.version = "1.0.0"
        self.component_name = "[component-name]"
        
    async def collect_data(self, params) -> Dict[str, Any]:
        # メイン処理
        
    def save_results(self, result: Dict[str, Any]) -> None:
        # 結果保存
        
    def print_summary(self, result: Dict[str, Any]) -> None:
        # サマリー表示

# サンプルデータ
SAMPLE_DATA = {...}

async def main():
    # 実行エントリーポイント
    
if __name__ == "__main__":
    asyncio.run(main())
```

#### 2. **テストファイル** (`tests/test_framework_XX.py`)
```python
import pytest
import asyncio
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from framework_XX_name import FrameworkXX

class TestFrameworkXX:
    def setup_method(self):
        self.framework = FrameworkXX(output_base_dir="test_output")
    
    def test_framework_initialization(self):
        assert self.framework.framework_id == XX
        # その他のテスト
        
    def teardown_method(self):
        # クリーンアップ
```

#### 3. **Makefile**
```makefile
.PHONY: help install test lint format run clean

help:
	@echo "[Component Name] Component - 利用可能なコマンド:"
	@echo "  install      - 依存関係インストール"
	@echo "  test         - テスト実行"
	@echo "  run          - フレームワーク実行"

install:
	python -m venv venv
	./venv/bin/pip install -r requirements.txt

test:
	./venv/bin/python -m pytest tests/ -v

run:
	./venv/bin/python src/framework_XX_name.py
```

---

## 開発ワークフロー

### 1. 単一コンポーネント開発

#### Cursorでの開発フロー
```bash
# 1. コンポーネントをCursorで開く
cursor components/framework-analysis

# 2. 開発環境セットアップ（初回のみ）
make setup-dev

# 3. 開発サイクル
# - src/framework_XX.py 編集
# - F5でデバッグ実行
# - tests/test_framework_XX.py 編集
# - Ctrl+Shift+P > Python: Run Tests

# 4. コード品質確認
make lint
make format

# 5. 動作確認
make run
```

#### 利点
- **フォーカス**: 単一コンポーネントに集中
- **高速**: 必要最小限のファイルのみ読み込み
- **AI最適化**: Cursorが的確にコードを理解・提案

### 2. 統合開発・テスト

#### プロジェクト全体での管理
```bash
# 1. ルートディレクトリで作業
cd /path/to/automatic_copy_writing

# 2. コンポーネント一覧確認
python scripts/run_component.py --list

# 3. 特定コンポーネント実行
python scripts/run_component.py framework-analysis 5

# 4. カスタムオプション付き実行
python scripts/run_component.py framework-analysis 5 \
  --brand "トヨタ" --competitors "ホンダ" "日産"
```

---

## 新規コンポーネント作成手順

### Step 1: 基本構造作成
```bash
# 1. ディレクトリ作成
mkdir -p components/new-component/{src,tests,docs,data/{samples,schemas},examples}

# 2. IDE設定ディレクトリ作成
mkdir -p components/new-component/.vscode
```

### Step 2: 必須ファイル作成

#### requirements.txt
```
pandas>=2.0.0
numpy>=1.24.0
# コンポーネント固有の依存関係
```

#### setup.py
```python
from setuptools import setup, find_packages

setup(
    name="new-component",
    version="1.0.0",
    description="New Component Description",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # 依存関係
    ],
    python_requires=">=3.8",
)
```

#### README.md
```markdown
# New Component

## 概要
このコンポーネントは...

## 使用方法
```bash
cd components/new-component
python src/framework_XX_name.py
```

## 依存関係
```bash
pip install -r requirements.txt
```
```

### Step 3: フレームワーク実装
- メインフレームワーククラス作成
- サンプルデータ追加
- テスト実装

### Step 4: 統合管理スクリプト更新
```python
# scripts/run_component.py の COMPONENTS 辞書に追加
COMPONENTS = {
    # 既存コンポーネント...
    "new-component": {
        "path": "components/new-component",
        "frameworks": {
            XX: "src/framework_XX_name.py"
        }
    }
}
```

---

## ベストプラクティス

### 1. コード構造

#### 非同期処理の活用
```python
class Framework:
    async def collect_data(self, params):
        # 外部API呼び出しは非同期で
        tasks = [
            self._api_call_1(params),
            self._api_call_2(params),
            self._analysis_task(params)
        ]
        results = await asyncio.gather(*tasks)
        return self._combine_results(results)
```

#### エラーハンドリング
```python
async def collect_data(self, params):
    start_time = time.time()
    try:
        # メイン処理
        result = await self._main_analysis(params)
        result["success"] = True
        return result
    except Exception as e:
        return {
            "framework_info": {
                "id": self.framework_id,
                "error": str(e)
            },
            "success": False,
            "execution_time": time.time() - start_time
        }
```

#### 出力標準化
```python
def save_results(self, result: Dict[str, Any]) -> None:
    # JSON詳細結果
    json_path = os.path.join(self.output_dir, "analysis_result.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    
    # CSV数値データ（可能な場合）
    if "numerical_data" in result:
        csv_path = os.path.join(self.output_dir, "numerical_data.csv")
        df = pd.DataFrame(result["numerical_data"])
        df.to_csv(csv_path, index=False, encoding='utf-8')
    
    # PNG可視化（可能な場合）
    if result["success"]:
        self._save_visualization(result)
```

### 2. テスト戦略

#### 単体テスト
```python
def test_calculation_logic(self):
    # ビジネスロジックのテスト
    result = self.framework._calculate_metrics(sample_data)
    assert result["accuracy"] > 0.8

@pytest.mark.asyncio
async def test_api_integration(self):
    # API統合テスト（モック使用）
    with patch('framework.ExternalAPI') as mock_api:
        mock_api.return_value.get_data.return_value = mock_data
        result = await self.framework.collect_data(test_params)
        assert result["success"] is True
```

#### 統合テスト
```python
def test_end_to_end_execution(self):
    # エンドツーエンドテスト
    result = asyncio.run(self.framework.collect_data(real_params))
    assert result["success"] is True
    assert "insights" in result
    assert len(result["insights"]) > 0
```

### 3. ドキュメント

#### 自己説明的コード
```python
def _calculate_share_of_search(self, data: pd.DataFrame, keywords: List[str]) -> Dict[str, float]:
    """
    検索シェア計算
    
    Args:
        data: Google Trendsから取得した検索ボリュームデータ
        keywords: 分析対象キーワードリスト
        
    Returns:
        各キーワードの検索シェア（%）
        
    Example:
        >>> data = pd.DataFrame({...})
        >>> result = self._calculate_share_of_search(data, ["brand1", "brand2"])
        >>> result
        {"brand1": 65.5, "brand2": 34.5}
    """
```

#### README.md の充実
- 明確な使用方法
- 実行例の提示
- 出力結果の説明
- トラブルシューティング

---

## トラブルシューティング

### よくある問題と解決方法

#### 1. 依存関係の問題
```bash
# 問題: モジュールが見つからない
ModuleNotFoundError: No module named 'package_name'

# 解決:
cd components/component-name
pip install -r requirements.txt
```

#### 2. パスの問題
```python
# 問題: 相対インポートエラー
# 解決: テストファイルでパス追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
```

#### 3. 出力ディレクトリの問題
```python
# 問題: 出力ディレクトリが作成されない
# 解決: 確実にディレクトリ作成
os.makedirs(self.output_dir, exist_ok=True)
```

#### 4. 非同期実行の問題
```python
# 問題: asyncio.run() でエラー
# 解決: Jupyter環境では異なる実行方法
if 'ipykernel' in sys.modules:
    # Jupyter環境
    result = await framework.collect_data(params)
else:
    # 通常の実行環境
    result = asyncio.run(framework.collect_data(params))
```

### デバッグのベストプラクティス

#### 1. ログ活用
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Framework:
    async def collect_data(self, params):
        logger.info(f"Starting analysis with params: {params}")
        # 処理
        logger.info(f"Analysis completed in {execution_time:.2f}s")
```

#### 2. 段階的デバッグ
```python
# 1. サンプルデータで基本動作確認
# 2. 実データの小さなサブセットでテスト
# 3. 本格的なデータで実行
```

#### 3. 出力内容の検証
```python
def print_debug_info(self, result):
    print(f"Result keys: {list(result.keys())}")
    if "data" in result:
        print(f"Data shape: {result['data'].shape}")
    print(f"Success: {result.get('success', 'Unknown')}")
```

---

このガイドに従うことで、一貫性のある高品質なコンポーネントを効率的に開発できます。 