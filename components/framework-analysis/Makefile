# Framework Analysis Component Makefile

.PHONY: help install test lint format run clean dev-install

# デフォルトターゲット
help:
	@echo "Framework Analysis Component - 利用可能なコマンド:"
	@echo ""
	@echo "  install      - 本番依存関係インストール"
	@echo "  dev-install  - 開発依存関係インストール"
	@echo "  test         - テスト実行"
	@echo "  lint         - リンター実行"
	@echo "  format       - コードフォーマット"
	@echo "  run          - Framework 5 実行"
	@echo "  run-custom   - カスタムパラメータでFramework 5 実行"
	@echo "  clean        - 生成ファイル削除"
	@echo ""

# 仮想環境作成とインストール
install:
	python -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt

# 開発用依存関係インストール
dev-install: install
	./venv/bin/pip install pytest black flake8 pylint mypy

# テスト実行
test:
	./venv/bin/python -m pytest tests/ -v

# リンター実行
lint:
	./venv/bin/python -m flake8 src/ tests/
	./venv/bin/python -m pylint src/

# コードフォーマット
format:
	./venv/bin/python -m black src/ tests/

# Framework 5 実行（サンプルデータ）
run:
	./venv/bin/python src/framework_05_share_of_search.py

# カスタムパラメータでFramework 5 実行
run-custom:
	./venv/bin/python src/framework_05_share_of_search.py \
		--brand "トヨタ" \
		--competitors "ホンダ" "日産" "マツダ" \
		--category "自動車"

# 生成ファイル削除
clean:
	rm -rf output/
	rm -rf test_output/
	rm -rf __pycache__/
	rm -rf src/__pycache__/
	rm -rf tests/__pycache__/
	rm -rf .pytest_cache/
	rm -rf *.egg-info/
	find . -name "*.pyc" -delete

# 開発環境セットアップ
setup-dev: dev-install
	@echo "開発環境セットアップ完了!"
	@echo "Cursor/VSCodeで開く準備ができました。" 