# データ収集・現状分析フレームワーク

## 1. 基本データフォーマット

| フォーマット | 中身の例 | ひと目でわかるポイント |
|-------------|---------|---------------------|
| KPIダッシュボード | 売上・粗利・新規率・LTV・NPS・Web流入 | 量的な健康状態 |
| ブランド健診シート | 認知率／好意度／想起ワード／ポジネガ比率 | 生活者の頭の中での位置 |
| SWOT＋ギャップ表 | Want → Is を縦軸に、強み／弱みを横軸 | 何を伸ばし何を埋めるか |
| CXマップ | 認知→検討→購入→使用→推奨 各タッチの満足度 | 体験のボトルネック |
| BSC（バランス・スコアカード） | 財務／顧客／内部プロセス／学習と成長 | "儲け筋"と"組織力"の両面 |
| 競合ポジショニング図 | 価格×価値軸、機能×情緒軸など | 差別化余白 |

---

## 2. 調べ方・導き方：5ステップ

### ステップ1：社内データ棚卸し
- CRM・ERP・販促レポートを抽出 → 指標を一本化

### ステップ2：ステークホルダーインタビュー
- **経営層**：ビジョンと痛点
- **現場**：顧客の生声・運用課題

### ステップ3：顧客・市場リサーチ
- **オンライン調査**：認知・購買要因
- **ソーシャルリスニング**：感情ワード抽出
- **業界統計**：市場成長率・競合売上

### ステップ4：観察＆体験テスト
- **店頭／ECサイト**の行動トラッキング
- **ユーザビリティテスト**で摩擦点を特定

### ステップ5：統合分析 → 可視化
- **定量**：スプレッドシートでスコアリング
- **定性**：テーマ別にタグ付け → 上記フォーマットに落とし込む

---

## 3. 広告業界の現状分析 25の実践フレーム

### フレーム1-15：基本分析手法

| # | アプローチ／切り口 | 何を測る・見るか | どう調べ、どう使うか |
|---|------------------|------------------|-------------------|
| 1 | ブランド・キーモデル (Unilever式) | 真理インサイト／ベネフィット／RTB／パーソナリティ | ワークショップでポストイット→1枚シート化 |
| 2 | Category Entry Points (CEP) 分布 | "○○したい時" の想起数と重み | SNS投稿と検索クエリを分類→ヒートマップ化 |
| 3 | Distinctive Brand Assets Score | ロゴ／カラー／音／キャラの認知率 | 100人調査＋アイトラで想起速度を測定 |
| 4 | CM 好感度×記憶指標 | 好感トップボックス／ブランド想起率 | AC企画「CM好感度調査」＋30秒後再認テスト |
| 5 | Share of Search / SOV | ブランド名検索量 vs 競合 | Google Trends API 抽出→月次折れ線 |
| 6 | Cultural Codes Decode (Holt) | カテゴリ内の支配的メッセージ群 | 過去CM・雑誌広告を言語化→コード一覧表 |
| 7 | Semiotics "3 層" 分析 | デノテーション／コノテーション／神話 | キービジュアルを分解→意味連鎖マップ |
| 8 | Creative MVP テスト | 6秒スケッチ動画で感情反応 | UserTestingでAB→System 1 ウィール評価 |
| 9 | Emotion-Eye Tracker | 視線集中点＋微表情 (AU) | Eye-trackingカメラ＋FaceReader→時系列グラフ |
| 10 | Touchpoint Atlas | 接触頻度×影響度マトリクス | 消費者日記+インタビュ→チャネル別気泡図 |
| 11 | Shopper Journey Shadowing | 店頭〜購入の動線・言葉 | GoPro装着同行→行動ログと発話書き起こし |
| 12 | Copy DNA Audit | 過去コピーの語彙・リズム・構文 | 100本をテキストマイニング→頻出n-gram表 |
| 13 | Meme & Emoji Trend Scan | TikTok/Redditで拡散中のビジュアル言語 | Hashtag抽出→使用シーン一覧カード |
| 14 | WARC 成功パターン対比 | IPA/WARCケースにおける施策→効果指標 | 類似事例5件の施策図解→ギャップ抽出 |
| 15 | ESG Narrative Heatmap | "サステナ"言及密度と感情極性 | CSR報告×SNS投稿を感情分析→2Dヒート図 |

### フレーム16-25：高度分析手法

| # | レンズ | 計測・観察するもの | 調べ方／コピーへの使い方 |
|---|-------|------------------|----------------------|
| 16 | Benefit Ladder | 製品属性 → 機能便益 → 情緒便益の段差 | 社内ワークで属性列挙→顧客発話を当てはめて階段化 |
| 17 | Jobs-to-be-Done Grid | "〜したい" 状況×評価基準×妥協点 | インデプスで JTBD 抽出→重要度×満足度マトリクス |
| 18 | Brand Archetype Fit | 12 archetypes との親和度スコア | 対象コピーを感性評価→適合上位2 archetype で語調指針 |
| 19 | Tone-of-Voice Spectrum | Formal↔Casual、Rational↔Emotional 度合い | 競合コピーを座標化→自社の許容レンジを決定 |
| 20 | Media-Mix Model Lite | 広告投下量 vs 流入・売上の短期係数 | 3年分の spend×KPI を回帰→高弾力チャネルを強調コピーに |
| 21 | Earned-Media Echo Map | 記事・UGC の量＆拡散脈絡 | GDELT/SNS API→クラスタリング→語彙をコピーに輸入 |
| 22 | Influencer Network Graph | インフルエンサー同士の共受信率 | Social Graph 抽出→ハブ的5人を指名→証言コピー化 |
| 23 | Shelf-Impact Simulation | パッケージ視認率と瞬時連想語 | 3Dシェルフ + Eye-tracking→「3秒で伝わる語」を抽出 |
| 24 | Attention Quality Index | Viewability, On-Screen Time, Scroll-Speed | アドサーバ＋ヒートマップ→高AQi面に長いコピーを配置 |
| 25 | Cultural Tension Radar | 社会的論点と温度感（賛否＋熱量） | ニュース/掲示板感情分析→避ける or 突くテーマを明示 |

---

## 使用ガイド

### 基本フレーム（1-15）の使い分け
- **ブランド診断**：フレーム1-5
- **クリエイティブ分析**：フレーム6-9
- **カスタマージャーニー**：フレーム10-11
- **競合・市場分析**：フレーム12-15

### 高度フレーム（16-25）の使い分け
- **戦略策定**：フレーム16-19
- **メディア最適化**：フレーム20-22
- **実行最適化**：フレーム23-25
