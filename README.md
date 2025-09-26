# コピージェネレーター - GPT-5対応版（フォールバック機能付き）

OpenAI GPT-5ファミリーを使用した段階的コピー生成システムです。

## 🚀 機能

- **段階的生成**: 4段階でコピーを改善
  - 🎯 構造化生成（what to say + 20個のコピー）
  - ⚡ 強化・改善（より強いメッセージ）
  - ✨ 最終洗練（短いフレーズに凝縮）
- **一括生成**: 従来の一度で生成
- **自省機能**: 結果を自己改善
- **モデル選択**: GPT-5/GPT-4シリーズ対応
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
5. Main file path: `streamlit_demo_7.py`
6. 「Deploy!」をクリック

### 3. APIキー設定（重要）
1. デプロイ後、アプリの設定画面へ
2. 「Secrets」タブを選択
3. 以下を追加:
```toml
OPENAI_API_KEY = "your-openai-api-key"
```
4. 「Save」をクリック

### 4. OpenAI APIキー取得
1. [OpenAI プラットフォーム](https://platform.openai.com/) にアクセス
2. 「API Keys」から新しい秘密鍵を生成
3. APIキーをコピーしてStreamlit Cloudのsecretsに設定

## 💻 ローカル開発

### 環境構築
```bash
# uvで仮想環境構築
uv sync

# 環境変数設定
export OPENAI_API_KEY="your-openai-api-key"

# アプリ起動
uv run streamlit run streamlit_demo_7.py
```

### CLIでの自動テスト

UI を介さずに GPT-5 パイプラインを検証したい場合は `copy_pipeline_runner.py` を利用できます。

```bash
uv run --no-project \
  --with openai --with pandas --with numpy \
  --with python-dateutil --with typing-extensions \
  python copy_pipeline_runner.py
```

#### 主なオプション

- `--orientation-file`: オリエンテーション文を含むテキストファイルへのパス
- `--model`: 使用するモデル ID（既定は `gpt-5`）
- `--temperature`: サンプリング温度（GPT-5 系は自動的に 1.0 に正規化）
- `--history-csv`: 会話履歴 CSV（列：`side`,`prompt`）

スクリプトは以下のフローを順に実行し、各段階の結果を標準出力に記録します。

1. モデル導通チェック
2. 3 段階のコピー生成
3. フィードバック分析による再生成
4. How-to-Say 洗練
5. カスタムプロンプトとアイデア生成

返却が JSON でない場合もフォールバックしてローデータを保持し、処理を継続します。

### 設定ファイル
- `requirements.txt`: 依存関係
- `.streamlit/config.toml`: Streamlit設定
- `.streamlit/secrets.toml.example`: APIキー設定テンプレート

## 📋 使用方法

1. **モデル選択**: サイドバーでGPT-5/GPT-4モデルを選択
2. **オリエンテーション入力**: 商品情報・ターゲット等を入力
3. **生成モード選択**: 段階的生成 or 一括生成
4. **生成実行**: 各段階を並列実行可能
5. **結果ダウンロード**: 個別 or 全段階まとめて

## 🎧 GPT Realtime API（gpt-realtime 系モデル）

OpenAIのRealtime APIを用いると、gpt-realtimeファミリーのモデルに対して音声・テキスト・ビジョンを低レイテンシでストリーミング接続できます。典型的な利用フローを以下にまとめます。

### 1. バックエンドでエフェメラルキーを発行

```bash
curl https://api.openai.com/v1/realtime/sessions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "gpt-realtime-preview",
        "voice": "verse",
        "instructions": "Keep responses concise."
      }'
```

- 応答JSONの `client_secret.value` をフロントエンドへ渡す（有効期限は約1分）。
- `model` は `gpt-realtime-preview` のほか `gpt-realtime-mini` などを指定可能。

### 2. WebRTC で双方向ストリームを確立

```javascript
const pc = new RTCPeerConnection();
pc.addTrack(localAudioTrack);

const offer = await pc.createOffer();
await pc.setLocalDescription(offer);

const token = await fetch("/ephemeral-key").then(r => r.text());
const resp = await fetch("https://api.openai.com/v1/realtime?model=gpt-realtime-preview", {
  method: "POST",
  body: offer.sdp,
  headers: {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/sdp"
  }
});

await pc.setRemoteDescription({ type: "answer", sdp: await resp.text() });
```

- `localAudioTrack` は `getUserMedia` で取得したマイクやカメラ映像。
- 受信音声は `pc.ontrack` で再生。テキスト等のイベントはデータチャネルで受信。

### 3. WebSocket での簡易接続（サーバー用途）

```bash
uv run --no-project python - <<'PY'
import asyncio, json, os, websockets

async def main():
    url = "wss://api.openai.com/v1/realtime?model=gpt-realtime-preview"
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "OpenAI-Beta": "realtime=v1"
    }
    async with websockets.connect(url, extra_headers=headers) as ws:
        await ws.send(json.dumps({"type": "response.create", "response": {"instructions": "hello"}}))
        async for message in ws:
            print(message)

asyncio.run(main())
PY
```

- WebSocketでは音声ストリームは扱えないが、テキスト指示やツール呼び出しを高速に送受信できる。
- `response.create` イベントでプロンプトを送信し、`response.delta` / `input_audio_buffer.commit` 等のイベントで逐次結果を受け取る。

### 4. ベストプラクティス

- バックエンドではエフェメラルキー生成のみにAPIキーを使用し、ブラウザに長期キーを渡さない。
- 音声入力は16kHzモノラルPCMでエンコードされるため、必要に応じて自前で圧縮（Opus）してから送信。
- `session.update` イベントでシステムインストラクションやツール定義をリアルタイムに変更可能。
- レイテンシ重視の場合はWebRTC、ロギングや非音声用途ではWebSocketが扱いやすい。

### 5. Python簡易クライアント（音声→テキスト）

ローカルマイクから音声を録音し、`gpt-realtime-mini` がテキストで返答するサンプルは `realtime_audio_text_demo.py` にあります。

```bash
uv run --no-project --with sounddevice --with websockets realtime_audio_text_demo.py
```

- `OPENAI_API_KEY` を環境変数に設定。
- 録音秒数は `REALTIME_RECORD_SECONDS`（既定4秒）で変更可能。
- システムプロンプトは `REALTIME_SYSTEM_PROMPT` で上書き。
- 既定モデルは `gpt-4o-realtime-preview`（必要に応じ `REALTIME_MODEL` を上書き）
- 取得した音声を16kHz PCMでAPIに送信し、テキスト返信を標準出力に表示。

### 6. ブラウザ版（WebRTC, マイク→テキスト）

`realtime_ephemeral_server.py` でエフェメラルキーを発行し、`realtime_web_demo.html` からWebRTC接続します。

```bash
export OPENAI_API_KEY="your-openai-api-key"
uv run --no-project --with fastapi --with "uvicorn[standard]" \
  uvicorn realtime_ephemeral_server:app --port 5057
```

ブラウザで `http://127.0.0.1:5057/demo` を開くとデモ画面が表示されます。


## ⚠️ 注意事項

- **推奨モデル**: `gpt-5`（最高品質） / `gpt-5-mini`（高速・低コスト）
- **互換モデル**: `gpt-4o` / `gpt-4.1` も利用可能
- **GPT-5フォールバック**: GPT-5が空レスポンスを返した場合、自動的にGPT-4oで再試行
- **商品名制約**: 全プロンプトで商品名・ブランド名使用禁止
- **Rate Limit**: API制限に注意

## 🧵 Structured Streaming Demo (`structured_streaming_demo.py`)

OpenAI Responses API の Structured Outputs をストリーミングしながら検証するサンプルです。

```bash
# APIキーを環境変数で設定
export OPENAI_API_KEY="your-openai-api-key"

# スキーマ強制ストリーミングの実行
uv run --no-project structured_streaming_demo.py
```

実行すると生成途中のJSON断片をそのまま標準出力し、完了後にスキーマ検証済みの構造化結果を整形表示します。`uv run` で `ModuleOrPackageNotFoundError` が出る場合は `--no-project` を付けてください。

## ✍️ Structured Copy Insight (`structured_copy_insight.py`)

独白テキストを入力すると、Responses API の Structured Outputs で核心コピーを抽出し、トップ1案のみをJSONとMarkdownで保存します。

```bash
export OPENAI_API_KEY="your-openai-api-key"
uv run --no-project structured_copy_insight.py
```

1. プロンプトが表示されたら独白を貼り付け、空行で確定。
2. アナウンス用に `gpt-5-mini` が短い進捗テキストをストリーミング表示します（必要に応じ `--no-progress` で無効化）。
3. `gpt-5` が内部で詳細分析を行い、最終的なトップコピーだけをJSON/Markdownで表示・保存します。

### Verbose モード

詳細なプロンプトやレスポンスを確認したい場合は `--verbose` を追加してください。

```bash
uv run --no-project structured_copy_insight.py --verbose
```

進捗ストリームを止めたい場合は `--no-progress` を指定します。

## 🔧 トラブルシューティング

### よくあるエラー
- **401 Error**: APIキー未設定 → `OPENAI_API_KEY` を確認
- **429 Error**: Rate Limit超過 → `gpt-5-mini`など軽量モデルを使用
- **Import Error**: 依存関係不足 → `uv sync` を再実行

### サポートされるモデル
- ✅ `gpt-5` / `gpt-5-chat-latest` / `gpt-5-mini` / `gpt-5-nano`
- ✅ `gpt-4o` / `gpt-4o-mini` / `gpt-4.1`
- ⚠️ `o1` / `o3` 系列（JSONモード非対応）

## 📄 ライセンス

MIT License 

## CHANGELOG
- 2025-09-25: GPT-5モデル対応に更新し、READMEを刷新
- 2025-09-25: GPT-5空レスポンス問題に対応し、GPT-4oフォールバック機能を追加
- 2025-09-25: Structured streaming demo スクリプトと利用手順を追加
- 2025-09-26: Structured copy insight スクリプトを追加し、README更新
- 2025-09-26: Structured copy insight に verbose オプションを追加
- 2025-09-26: Structured copy insight をトップコピー出力＋進捗ストリーミング対応に更新
- 2025-09-26: README に gpt-realtime の利用手順を追加
- 2025-09-26: Realtime音声→テキストPythonサンプルを追加し、READMEを更新

## 🧪 Copy Experiment Lab (streamlit_experiment.py)

デザイナーやプランナーが自由にプロンプトを試せる実験用UIです。テンプレートボタン＋自由入力欄でプロンプトを書き換え、任意のモデルでコピーを生成できます。

### 使い方
1. サイドバーでモデル・temperature・コピー数を設定
2. 「プロンプトテンプレート」ボタンで定型文を入力欄にロード（または自由入力）
3. 「オリエンテーション / 背景情報」を必要に応じて編集
4. 「コピーを生成」を押して結果を確認
5. RAWレスポンスや履歴、ログを使って試行錯誤

### 起動方法
```bash
uv run --no-project   --with streamlit --with openai --with pandas --with numpy   --with python-dateutil --with typing-extensions   streamlit run streamlit_experiment.py --server.port 8501
```

### 主な機能
- カスタム入力欄 + テンプレートボタン
- GPT-5向けJSONスキーマ＋フォールバック制御
- RAWレスポンス/生成履歴/ログ表示
- コピー数やmax_completion_tokensをUIから調整可能
- 2025-09-25: Copy Experiment Lab (実験用UI) を追加

## 🔁 Copy Chain Lab (streamlit_chain_lab.py)

チェイン生成を維持しながらプロンプトを試せるUIです。前回の生成結果が会話履歴として渡され、段階的なブラッシュアップが可能です。

### 使い方
1. サイドバーでモデル・temperature・コピー数・max_completion_tokensを設定
2. テンプレートボタンで定型プロンプトをロード、または自由入力
3. 生成実行で、前回までの会話履歴を踏まえたコピー案を出力
4. 「チェイン履歴をクリア」でリセット可能

### 起動方法
```bash
uv run --no-project   --with streamlit --with openai --with pandas --with numpy   --with python-dateutil --with typing-extensions   streamlit run streamlit_chain_lab.py --server.port 8501
```
- 2025-09-25: Copy Chain Lab (チェイン実験UI) を追加
