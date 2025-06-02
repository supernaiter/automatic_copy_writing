# 会話継続スクリプト

CSVの会話履歴を使ってOpenAI APIで会話を継続するスクリプトです。

## セットアップ

1. **依存関係をインストール**
```bash
pip install -r requirements.txt
```

2. **OpenAI APIキーを設定**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## 使用方法

```bash
python continue_conversation.py
```

## 動作内容

1. `interaction.csv`から会話履歴を読み込み
2. OpenAI API用の`messages`形式に変換
3. 「この方向で十個考えてください」をプロンプトとして追加
4. GPT-4oでJSON形式の回答を生成
5. 結果を`api_response.json`に保存

## ファイル構成

- `continue_conversation.py` - メインスクリプト
- `interaction.csv` - 会話履歴データ
- `requirements.txt` - 依存関係
- `api_response.json` - 生成された結果（実行後に作成）

## カスタマイズ

スクリプト内の以下の部分を変更可能：

```python
NEW_PROMPT = "この方向で十個考えてください"  # プロンプト変更
model="gpt-4o"  # モデル変更
temperature=0.7  # 創造性調整
max_tokens=4000  # 最大トークン数
``` 