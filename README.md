# コピージェネレーター - Gemini API版

Google Gemini APIを使用した段階的コピー生成システムです。

## 🚀 機能

- **段階的生成**: 4段階でコピーを改善
  - 🎯 構造化生成（what to say + 20個のコピー）
  - ⚡ 強化・改善（より強いメッセージ）
  - ✨ 最終洗練（短いフレーズに凝縮）
- **一括生成**: 従来の一度で生成
- **自省機能**: 結果を自己改善
- **モデル選択**: Gemini 2.5/2.0/1.5系対応
- **Temperature調整**: 創造性レベル設定
- **会話履歴**: CSV読み込み対応

## 🌐 Streamlit Cloudデプロイ手順

### 1. リポジトリ準備
```bash
git add .
git commit -m "Streamlit Cloud deployment ready"
git push origin main
```

### 2. Streamlit Cloudでデプロイ
1. [Streamlit Cloud](https://share.streamlit.io/) にアクセス
2. GitHubアカウントでログイン
3. 「New app」をクリック
4. リポジトリを選択: `your-username/automatic_copy_writing`
5. Main file path: `streamlit_demo_gemini.py`
6. 「Deploy!」をクリック

### 3. APIキー設定（重要）
1. デプロイ後、アプリの設定画面へ
2. 「Secrets」タブを選択
3. 以下を追加:
```toml
GOOGLE_API_KEY = "your-actual-gemini-api-key"
```
4. 「Save」をクリック

### 4. Gemini APIキー取得
1. [Google AI Studio](https://aistudio.google.com/) にアクセス
2. 「Get API Key」→「Create API key」
3. APIキーをコピーしてStreamlit Cloudのsecretsに設定

## 💻 ローカル開発

### 環境構築
```bash
# 仮想環境作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係インストール
pip install -r requirements.txt

# 環境変数設定
export GOOGLE_API_KEY="your-gemini-api-key"

# アプリ起動
streamlit run streamlit_demo_gemini.py
```

### 設定ファイル
- `requirements.txt`: 依存関係
- `.streamlit/config.toml`: Streamlit設定
- `.streamlit/secrets.toml.example`: APIキー設定テンプレート

## 📋 使用方法

1. **モデル選択**: サイドバーでGeminiモデルを選択
2. **オリエンテーション入力**: 商品情報・ターゲット等を入力
3. **生成モード選択**: 段階的生成 or 一括生成
4. **生成実行**: 各段階を並列実行可能
5. **結果ダウンロード**: 個別 or 全段階まとめて

## ⚠️ 注意事項

- **無料モデル推奨**: `gemini-2.0-flash`（高性能・無料）
- **有料モデル**: `gemini-2.5-pro-preview`は課金必要
- **商品名制約**: 全プロンプトで商品名・ブランド名使用禁止
- **Rate Limit**: API制限に注意

## 🔧 トラブルシューティング

### よくあるエラー
- **429 Error**: 無料枠超過 → 無料モデルに変更
- **Import Error**: 依存関係不足 → `pip install -r requirements.txt`
- **API Key Error**: キー未設定 → Streamlit Cloud secretsで設定

### サポートされるモデル
- ✅ `gemini-2.0-flash` (推奨・無料)
- ✅ `gemini-1.5-flash` (安定・無料)
- ⚠️ `gemini-2.5-pro-preview` (有料のみ)

## 📄 ライセンス

MIT License 