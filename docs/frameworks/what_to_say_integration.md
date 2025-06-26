# What-to-Say Finder の三層ループシステム統合設計

## 1. 統合の本質

What-to-Say Finderは、三層ループシステムの**「意図理解エンジン」**を強化し、**「WHATの発見力」**を飛躍的に向上させるコンポーネント群として統合されます。

### 1.1 概念的位置づけ

```
┌─────────────────────────────────────────────────┐
│               三層ループシステム                  │
├─────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────┐  │
│  │          意図理解エンジン                  │  │
│  │  ┌─────────────────────────────────────┐  │  │
│  │  │      What-to-Say Finder           │  │  │
│  │  │                                   │  │  │
│  │  │ • 競合分析型システム              │  │  │
│  │  │ • 顧客インサイト発掘システム      │  │  │
│  │  │ • トレンド連動型システム          │  │  │
│  │  │ • ペルソナ対話システム            │  │  │
│  │  │ • A/Bテスト自動生成              │  │  │
│  │  │ • 業界知識ベース型               │  │  │
│  │  └─────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────┘  │
├─────────────────────────────────────────────────┤
│  共感シミュレータ │ 創造的変異器 │ 価値評価システム │
└─────────────────────────────────────────────────┘
```

## 2. 具体的統合アーキテクチャ

### 2.1 意図理解エンジンの拡張

既存の`IntentParser`を以下のように拡張：

```python
class EnhancedIntentParser:
    """What-to-Say Finder統合版意図理解エンジン"""
    
    def __init__(self):
        # What-to-Say Finderコンポーネント
        self.competitive_analyzer = CompetitiveAnalysisSystem()
        self.insight_excavator = CustomerInsightSystem() 
        self.trend_connector = TrendAnalysisSystem()
        self.persona_interviewer = PersonaDialogueSystem()
        self.ab_generator = ABTestGenerationSystem()
        self.knowledge_integrator = IndustryKnowledgeSystem()
        
        # 統合オーケストレーター
        self.insight_synthesizer = InsightSynthesizer()
    
    def discover_what_to_say(self, brief: ProductBrief) -> List[WhatToSayCandidate]:
        """6つのシステムから多角的にWHATを発見"""
        
        # 1. 競合分析からの差別化ポイント発見
        competitive_gaps = self.competitive_analyzer.find_gaps(brief)
        
        # 2. 顧客の潜在ニーズ発掘  
        hidden_insights = self.insight_excavator.mine_insights(brief)
        
        # 3. トレンドとの接点発見
        trend_connections = self.trend_connector.connect_trends(brief)
        
        # 4. ペルソナ深層対話
        persona_voices = self.persona_interviewer.deep_interview(brief)
        
        # 5. 業界知識との融合
        expert_perspectives = self.knowledge_integrator.analyze(brief)
        
        # 6. 統合・合成
        candidates = self.insight_synthesizer.synthesize([
            competitive_gaps, hidden_insights, trend_connections,
            persona_voices, expert_perspectives
        ])
        
        return candidates
```

### 2.2 6つのサブシステム詳細

#### 2.2.1 競合分析型システム

```python
class CompetitiveAnalysisSystem:
    """競合分析によるホワイトスペース発見"""
    
    def find_gaps(self, brief: ProductBrief) -> List[DifferentiationPoint]:
        # 競合サイト・広告の自動収集
        competitors = self.crawl_competitive_messages(brief.category)
        
        # LLMによる競合メッセージ分析
        competitive_map = self.analyze_positioning(competitors)
        
        # 未開拓領域の特定
        white_spaces = self.identify_gaps(competitive_map, brief.product_features)
        
        return [
            DifferentiationPoint(
                axis="未開拓訴求軸",
                insight="競合が言っていない価値",
                evidence=competitive_map,
                confidence=0.8
            )
        ]
```

#### 2.2.2 顧客インサイト発掘システム

```python
class CustomerInsightSystem:
    """レビュー・SNS分析による真のニーズ発見"""
    
    def mine_insights(self, brief: ProductBrief) -> List[CustomerInsight]:
        # レビューデータ収集
        reviews = self.collect_reviews(brief.product_name, brief.category)
        
        # 感情分析・課題抽出
        pain_points = self.extract_pain_points(reviews)
        hidden_desires = self.extract_latent_needs(reviews)
        
        # 顧客の言葉でのニーズ表現
        customer_language = self.extract_natural_expressions(reviews)
        
        return [
            CustomerInsight(
                type="潜在的願望",
                insight="顧客が本当に求めているもの",
                customer_voice=customer_language,
                frequency_score=0.75
            )
        ]
```

#### 2.2.3 トレンド連動型システム

```python
class TrendAnalysisSystem:
    """時流との接点発見"""
    
    def connect_trends(self, brief: ProductBrief) -> List[TrendConnection]:
        # トレンドデータ収集
        google_trends = self.get_google_trends(brief.category)
        social_trends = self.get_social_trends()
        
        # 製品との関連性発見
        connections = self.find_connections(brief.product_features, google_trends)
        
        # 時流メッセージ生成
        trend_messages = self.generate_trend_messages(connections)
        
        return [
            TrendConnection(
                trend="社会的トレンド",
                connection_point="製品との接点",
                message_opportunity="訴求機会",
                relevance_score=0.6
            )
        ]
```

#### 2.2.4 ペルソナ対話システム

```python
class PersonaDialogueSystem:
    """仮想ペルソナとの深層対話"""
    
    def deep_interview(self, brief: ProductBrief) -> List[PersonaVoice]:
        # ペルソナ生成
        personas = self.generate_target_personas(brief.target_attributes)
        
        # 各ペルソナとの仮想インタビュー
        insights = []
        for persona in personas:
            dialogue = self.conduct_virtual_interview(persona, brief)
            deep_needs = self.extract_deep_needs(dialogue)
            insights.append(PersonaVoice(
                persona=persona,
                deep_needs=deep_needs,
                authentic_language=dialogue.natural_expressions
            ))
        
        return insights
```

#### 2.2.5 業界知識ベース型システム

```python
class IndustryKnowledgeSystem:
    """専門知識による価値発見"""
    
    def analyze(self, brief: ProductBrief) -> List[ExpertPerspective]:
        # 業界レポート・論文収集
        expert_content = self.collect_expert_knowledge(brief.category)
        
        # 製品との関連性分析
        connections = self.analyze_expert_connections(expert_content, brief)
        
        # 専門的価値の抽出
        expert_values = self.extract_expert_values(connections)
        
        return [
            ExpertPerspective(
                domain="専門分野",
                insight="専門的視点からの価値",
                credibility="権威性の根拠",
                applicability=0.7
            )
        ]
```

### 2.3 How-to-Say フレームワークの統合

What-to-Say Finderの表現技法を**創造的変異器**に統合：

```python
class EnhancedMutationEngine:
    """How-to-Say統合版変異エンジン"""
    
    def __init__(self):
        # 修辞技法ライブラリ
        self.rhetoric_toolkit = RhetoricToolkit()
        # 表現フレームワーク
        self.expression_frameworks = {
            'AIDA': AidaFramework(),
            'PASONA': PasonaFramework(), 
            'QUEST': QuestFramework(),
            'CREMA': CremaFramework()
        }
    
    def mutate_with_rhetoric(self, candidate: Candidate, weak_axes: List[str]) -> List[Candidate]:
        """修辞技法を使った変異"""
        
        variants = []
        
        for axis in weak_axes:
            if axis == "emotional_impact":
                # 比喩・擬人化で感情訴求強化
                variants.extend(self.rhetoric_toolkit.apply_metaphor(candidate))
                variants.extend(self.rhetoric_toolkit.apply_personification(candidate))
                
            elif axis == "memorability": 
                # 韻律・反復で記憶性向上
                variants.extend(self.rhetoric_toolkit.apply_rhythm(candidate))
                variants.extend(self.rhetoric_toolkit.apply_repetition(candidate))
                
            elif axis == "clarity":
                # 体言止め・対比で明確性向上
                variants.extend(self.rhetoric_toolkit.apply_contrast(candidate))
                
        return variants
    
    def structure_with_framework(self, candidate: Candidate, framework: str) -> Candidate:
        """表現フレームワークでの再構成"""
        
        framework_engine = self.expression_frameworks[framework]
        return framework_engine.restructure(candidate)
```

## 3. システム連携フロー

### 3.1 発見→評価→改善のループ

```
プロダクトブリーフ
      ↓
┌─────────────────┐
│ What-to-Say     │ ← 6つのシステムが並列動作
│ Discovery       │   競合/顧客/トレンド/ペルソナ/知識分析  
└─────────────────┘
      ↓
候補WHAT群 (20-30個)
      ↓
┌─────────────────┐
│ ペルソナ評価     │ ← 既存の共感シミュレータ
│ システム        │
└─────────────────┘
      ↓
評価結果 + 弱点分析
      ↓
┌─────────────────┐
│ How-to-Say     │ ← 修辞技法 + フレームワーク
│ Enhancement    │
└─────────────────┘
      ↓
最適化されたWHY/WHAT/HOW
```

### 3.2 実時間学習ループ

```python
class AdaptiveLearningLoop:
    """What-to-Say発見の精度向上"""
    
    def learn_from_results(self, optimization_history: List[OptimizationRun]):
        """過去の結果から学習"""
        
        # どの発見手法が高スコアを生んだか分析
        method_effectiveness = self.analyze_method_success(optimization_history)
        
        # 業界・製品タイプ別の成功パターン学習
        success_patterns = self.extract_success_patterns(optimization_history)
        
        # 各システムの重み調整
        self.adjust_system_weights(method_effectiveness)
        
        # ペルソナモデルの精度向上
        self.refine_persona_models(success_patterns)
```

## 4. 具体的実装例

### 4.1 統合API設計

```python
POST /api/discover-and-optimize
{
  "brief": {
    "product_name": "健康サプリメント",
    "category": "ヘルスケア",
    "target_attributes": {
      "age": "30-50代",
      "lifestyle": "忙しい会社員"
    }
  },
  "discovery_config": {
    "enable_competitive": true,
    "enable_insight_mining": true,
    "enable_trend_analysis": true,
    "enable_persona_dialogue": true,
    "enable_expert_knowledge": true
  },
  "optimization_config": {
    "max_iterations": 5,
    "target_score": 8.0
  }
}

Response:
{
  "discovered_insights": [
    {
      "source": "customer_insight", 
      "insight": "忙しさで健康管理が後回しになる罪悪感",
      "evidence": "レビュー分析結果",
      "strength": 0.85
    }
  ],
  "optimized_candidates": [
    {
      "why": "忙しい現代人の健康への罪悪感を解消する",
      "what": "5秒で済む健康習慣",
      "how": {
        "headline": "忙しくても、自分を大切にできる。",
        "body": "朝のコーヒーと一緒に。それだけで、今日も頑張れる。",
        "framework": "PASONA",
        "rhetoric": ["体言止め", "共感的トーン"]
      },
      "scores": {
        "relevance": 9.2,
        "emotional_impact": 8.8,
        "action_intent": 8.5
      }
    }
  ]
}
```

## 5. 期待される効果

### 5.1 WHAT発見力の向上

- **従来**: 1つのブリーフから5-8個のWHAT候補
- **統合後**: 1つのブリーフから20-30個の多角的WHAT候補

### 5.2 精度の向上

- **競合分析**: 市場でのポジショニング精度+30%
- **顧客インサイト**: 真のニーズ発見率+50%
- **トレンド連動**: 時流適応度+40%

### 5.3 表現品質の向上

- **修辞技法**: 感情訴求力+25%
- **フレームワーク**: 論理的説得力+35%
- **記憶性**: ブランド想起率+20%

## 6. 段階的実装計画

### Phase 1: Discovery Enhancement (4週間)
- 競合分析システム + 顧客インサイト発掘システム
- 既存IntentParserとの統合

### Phase 2: Multi-Source Integration (3週間)  
- トレンド分析 + ペルソナ対話システム
- 統合シンセサイザーの実装

### Phase 3: Expression Enhancement (3週間)
- 修辞技法ライブラリ + フレームワーク統合
- 創造的変異器の拡張

### Phase 4: Learning & Optimization (2週間)
- 学習ループの実装
- 精度向上メカニズム

---

What-to-Say Finderの統合により、三層ループシステムは単なる生成・評価システムから、**「真のニーズ発見→最適表現→継続学習」**の高度なインテリジェンスシステムへと進化します。 