# 三層ループシステム アーキテクチャ設計書

## 1. システム概要

三層ループシステムは、WHY（存在意義）→ WHAT（価値の核）→ HOW（伝達設計）の循環構造により、自動的にコピーライティングを最適化するAIシステムです。

### 基本コンセプト

```
WHY（存在意義）  ─┐
                    ├─▶ WHAT（価値の核） ─┐
施策学習ループ      │                      │
                    └───── HOW（伝達設計）◀─┘
```

- **WHY**: 事業・ブランドが世の中に提供したい根源的価値
- **WHAT**: WHYを"顧客の課題解決文"に翻訳したもの
- **HOW**: WHATを具体行動に導くストーリー＆表現

## 2. システムアーキテクチャ

### 2.1 全体フロー

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 0. プロダクト・ブリーフ      ┃←人間が一度だけ入力
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 1. WHY / WHAT / HOW 生成      ┃LLM①（生成用）
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 2. ユーザ反応シミュレータ     ┃LLM②（評価用）×ペルソナN
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 3. スコア統合・選抜           ┃ループ・コントローラ
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 4. 変異・再生成               ┃LLM①へフィードバック
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛   ↑
        └───────────────迭代（max K 周 or 目標スコア到達で停止）
```

### 2.2 多層評価システム

```
           ▶ LAYER-0  形式チェック      (字数･季語･禁止語…)
生成テキスト ▶ LAYER-1  音韻＋韻律      (Rhyme/Meter/定型遵守)
           ▶ LAYER-2  語彙＋多様性      (Distinct-n, Self-BLEU…)
           ▶ LAYER-3  セマンティック    (BERTScore, 製品適合度)
           ▶ LAYER-4  感情＋説得性      (感情分類, 行動動機語)
           ▶ LAYER-5  LLM-JUDGE         (ペルソナ別7軸評価)
           ▶ LAYER-6  KPI Proxy         (CTR 予測モデル)
                         ▼
                    合成スコア (重み付け or 学習)
```

## 3. 各層の詳細設計

### 3.1 入力層（Layer 0）: プロダクト・ブリーフ

```json
{
  "product_name": "製品名",
  "main_features": ["主要機能1", "主要機能2"],
  "target_attributes": {
    "age": "ターゲット年齢",
    "challenges": "課題",
    "situation": "状況"
  },
  "business_goals": {
    "target_metric": "LP CVR",
    "target_value": "≥ 3%"
  }
}
```

### 3.2 生成層（Layer 1）: WHY/WHAT/HOW 生成

**プロンプト構造**:
```
You are a senior Japanese copywriter.
Task: propose N=8 candidate sets of
• WHY (1 sentence)
• WHAT (<=30 Japanese characters)
• HOW (headline + 50-word body)
Constraints: ...  // 業種制限や薬機法など
Return as JSON list.
```

**出力形式**:
```json
[
  {
    "why": "事業の存在意義",
    "what": "価値の核心メッセージ",
    "how": {
      "headline": "キャッチコピー",
      "body": "説明文（50字以内）"
    }
  }
]
```

### 3.3 評価層（Layer 2）: ユーザー反応シミュレータ

#### 3.3.1 ペルソナ定義

```json
{
  "name": "Haruka",
  "age": 38,
  "goals": "育児と仕事を両立しながら健康維持",
  "pain": "運動習慣が続かない",
  "brand_attitude": "Appleは高いけど信頼",
  "language_preference": "シンプルで分かりやすい表現"
}
```

#### 3.3.2 評価軸

| 軸 | 説明 | スコア範囲 |
|---|-----|-----------|
| Relevance | ペルソナへの関連性 | 1-10 |
| Clarity | 明確性・理解しやすさ | 1-10 |
| Emotional Impact | 感情的インパクト | 1-10 |
| Action Intent | 行動意図の喚起 | 1-10 |
| Novelty | 新奇性・独自性 | 1-10 |
| Memorability | 記憶残存度 | 1-10 |
| Policy Safe | 法的・倫理的安全性 | 0/1 |

#### 3.3.3 評価プロンプト

```
Persona JSON: {ペルソナ情報}

Ad Copy:
WHY: {存在意義}
WHAT: {価値の核}
HOW: {表現}

Task: score each item 1-10 for
1. Relevance
2. Clarity
3. Emotional Impact
4. Likelihood to take action (CTA)
5. Novelty
6. Memorability
7. Policy Safety (0/1)

Return as JSON + short reasoning.
```

### 3.4 統合層（Layer 3）: スコア統合・選抜

#### 3.4.1 スコア合成アルゴリズム

```python
overall = Σ wi * normalized_metric_i

# 重み例
weights = {
    'PolicySafe': 0,      # 必須: 0以外は不合格
    'Clarity': 1,
    'Relevance': 1,
    'ActionIntent': 1.5,
    'EmotionalImpact': 1,
    'Novelty': 0.8,
    'Memorability': 0.8
}
```

#### 3.4.2 選抜ロジック

```python
def select_candidates(copies, target_score=7.0, max_iterations=10):
    top_k = select_top(copies, k=3, key="mean_score")
    
    if max(top_k.scores) >= target_score or iterations >= max_iterations:
        return top_k
    else:
        return mutate_and_regenerate(top_k)
```

### 3.5 フィードバック層（Layer 4）: 変異・再生成

#### 3.5.1 変異ルール

| 評価軸 | スコア閾値 | 改善指示 |
|--------|-----------|---------|
| Emotional Impact | <6 | "共感語を追加し、感情的な響きを強化" |
| Action Intent | <6 | "行動を促す動詞と緊急性を追加" |
| Clarity | <7 | "専門用語を平易な言葉に置換" |
| Novelty | <6 | "比喩や新しい視点を導入" |

#### 3.5.2 改善プロンプト

```
Improve this copy to raise {低評価軸} score >8.
Keep the same WHY.

Current copy: {現在のコピー}
Weakness: {具体的な問題点}
Improvement direction: {改善方向性}

Generate 3 variants.
```

## 4. 技術実装仕様

### 4.1 システム構成

| コンポーネント | 技術選択 | 役割 |
|---------------|---------|------|
| 生成エンジン | GPT-4o (temperature=0.8) | WHY/WHAT/HOW生成 |
| 評価エンジン | Claude-3 (temperature=0.2) | ユーザー反応評価 |
| スコア統合 | Python + pandas | 評価統合・選抜 |
| データ管理 | JSON + SQLite | 履歴・学習データ |

### 4.2 API設計

#### 4.2.1 生成API

```python
POST /api/generate
{
  "brief": {プロダクトブリーフ},
  "config": {
    "num_candidates": 8,
    "max_iterations": 10,
    "target_score": 7.5
  }
}

Response:
{
  "candidates": [候補リスト],
  "best_candidate": {最高スコア候補},
  "iteration_history": [反復履歴],
  "final_scores": {最終評価}
}
```

#### 4.2.2 評価API

```python
POST /api/evaluate
{
  "copy": {WHY/WHAT/HOW},
  "personas": [ペルソナリスト],
  "evaluation_config": {評価設定}
}

Response:
{
  "persona_scores": {ペルソナ別スコア},
  "aggregated_score": {統合スコア},
  "detailed_feedback": {詳細フィードバック}
}
```

### 4.3 学習・最適化機能

#### 4.3.1 重み学習

```python
def update_weights(real_kpi_data, predicted_scores):
    """
    実際のKPI（CTR、CVR等）と予測スコアの相関から
    評価軸の重みを機械学習で更新
    """
    correlation_matrix = calculate_correlation(real_kpi_data, predicted_scores)
    new_weights = optimize_weights(correlation_matrix)
    return new_weights
```

#### 4.3.2 ペルソナ精度向上

```python
def refine_personas(user_feedback, actual_responses):
    """
    実際のユーザー反応とペルソナ予測の差分から
    ペルソナモデルを継続改善
    """
    accuracy_scores = compare_predictions(user_feedback, actual_responses)
    updated_personas = adjust_persona_attributes(accuracy_scores)
    return updated_personas
```

## 5. 運用・監視

### 5.1 品質監視指標

| 指標 | 計算方法 | 目標値 |
|------|---------|--------|
| 生成品質一貫性 | 同条件での複数生成の分散 | <0.3 |
| 評価精度 | 実KPIとの相関係数 | >0.7 |
| 処理速度 | 1候補あたりの生成時間 | <30秒 |
| システム稼働率 | 正常応答率 | >99% |

### 5.2 継続改善サイクル

1. **週次**: 生成候補の実KPI収集・分析
2. **月次**: 評価重みの再学習・更新
3. **四半期**: ペルソナモデルの見直し・追加
4. **年次**: システムアーキテクチャの大幅改善

## 6. 拡張可能性

### 6.1 マルチモーダル対応

- 画像生成APIとの連携でバナー自動生成
- 音声合成でCM音声まで自動化
- 動画生成APIでショート動画制作

### 6.2 業界特化

- 薬機法チェッカーの内蔵
- 金融広告規制への対応
- BtoB特化ペルソナの追加

### 6.3 リアルタイム最適化

- A/Bテスト結果の即座フィードバック
- リアルタイムCTR予測モデル
- 動的重み調整システム

---

**設計責任者**: [作成者名]  
**最終更新**: [更新日]  
**バージョン**: 1.0 