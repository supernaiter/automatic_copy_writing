# Data Collection → What-to-Say Discovery 統合設計

## 1. 統合の全体像

**25の実践フレーム** → **6つの並列システム** → **統合洞察**

```
data_collection.mdの25フレーム
         ↓
┌─────────────────────────────┐
│  What-to-Say Discovery      │
│  6つの並列システム           │
│                            │
│ 1. 競合分析システム         │ ← フレーム5,6,14,19,21
│ 2. 顧客インサイト発掘       │ ← フレーム1,2,7,16,17
│ 3. トレンド連動システム     │ ← フレーム13,15,25,22
│ 4. ペルソナ対話システム     │ ← フレーム10,11,16,17
│ 5. 業界知識統合システム     │ ← フレーム14,18,20,24
│ 6. A/Bテスト仮説生成       │ ← フレーム8,9,23,24
└─────────────────────────────┘
         ↓
   統合された洞察
```

## 2. システム別フレームワーク統合詳細

### 2.1 競合分析システム強化

**活用フレーム**: 5, 6, 14, 19, 21

```python
class EnhancedCompetitiveAnalysisSystem:
    def __init__(self):
        self.analysis_frameworks = {
            'share_of_search': ShareOfSearchAnalyzer(),      # フレーム5
            'cultural_codes': CulturalCodesDecoder(),        # フレーム6
            'warc_patterns': WARCPatternAnalyzer(),          # フレーム14
            'tone_spectrum': ToneOfVoiceAnalyzer(),          # フレーム19
            'earned_media': EarnedMediaMapper()              # フレーム21
        }
    
    async def find_gaps_enhanced(self, brief: ProductBrief) -> List[DifferentiationPoint]:
        """25フレーム活用の強化競合分析"""
        
        # フレーム5: Share of Search分析
        search_share = await self.analysis_frameworks['share_of_search'].analyze(
            brand=brief.product_name,
            competitors=brief.competitors,
            category=brief.category
        )
        
        # フレーム6: Cultural Codes分析
        cultural_codes = await self.analysis_frameworks['cultural_codes'].decode(
            category_messages=await self.collect_category_ads(brief.category)
        )
        
        # フレーム14: WARC成功パターン対比
        success_patterns = await self.analysis_frameworks['warc_patterns'].compare(
            category=brief.category,
            target_metrics=brief.business_goals
        )
        
        # フレーム19: Tone-of-Voice Spectrum
        tone_positioning = await self.analysis_frameworks['tone_spectrum'].map(
            competitor_copy=await self.collect_competitor_copy(brief.competitors)
        )
        
        # フレーム21: Earned Media Echo Map
        earned_mentions = await self.analysis_frameworks['earned_media'].map(
            category=brief.category,
            time_range='6_months'
        )
        
        # 統合分析
        gaps = self.synthesize_competitive_gaps([
            search_share, cultural_codes, success_patterns, 
            tone_positioning, earned_mentions
        ])
        
        return [
            DifferentiationPoint(
                axis="検索可視性",
                gap=f"検索シェア{search_share.competitor_dominance}%劣後",
                opportunity="ロングテールキーワードでの差別化",
                framework_source="Share of Search",
                confidence=search_share.reliability
            ),
            DifferentiationPoint(
                axis="文化的記号",
                gap=f"支配コード'{cultural_codes.dominant_themes[0]}'に依存",
                opportunity=f"新記号'{cultural_codes.white_space_opportunities[0]}'開拓",
                framework_source="Cultural Codes",
                confidence=cultural_codes.pattern_strength
            )
        ]
```

### 2.2 顧客インサイト発掘システム強化

**活用フレーム**: 1, 2, 7, 16, 17

```python
class EnhancedCustomerInsightSystem:
    def __init__(self):
        self.insight_frameworks = {
            'brand_key_model': BrandKeyAnalyzer(),           # フレーム1
            'category_entry_points': CEPAnalyzer(),          # フレーム2
            'semiotics': SemioticsAnalyzer(),                # フレーム7
            'benefit_ladder': BenefitLadderMapper(),         # フレーム16
            'jtbd_grid': JobsToBeGoneGridder()               # フレーム17
        }
    
    async def mine_insights_enhanced(self, brief: ProductBrief) -> List[CustomerInsight]:
        """多層フレームワークによる深層洞察発掘"""
        
        # フレーム1: ブランド・キーモデル分析
        brand_truth = await self.insight_frameworks['brand_key_model'].extract(
            stakeholder_interviews=await self.conduct_internal_interviews(brief),
            customer_research=await self.conduct_customer_research(brief)
        )
        
        # フレーム2: Category Entry Points分布
        cep_distribution = await self.insight_frameworks['category_entry_points'].map(
            social_posts=await self.collect_social_mentions(brief.category),
            search_queries=await self.collect_search_data(brief.category)
        )
        
        # フレーム7: Semiotics 3層分析
        semiotic_insights = await self.insight_frameworks['semiotics'].analyze(
            visual_assets=await self.collect_category_visuals(brief.category),
            brand_assets=brief.brand_assets
        )
        
        # フレーム16: Benefit Ladder構築
        benefit_hierarchy = await self.insight_frameworks['benefit_ladder'].build(
            product_attributes=brief.product_features,
            customer_interviews=await self.conduct_benefit_interviews(brief)
        )
        
        # フレーム17: Jobs-to-be-Done Grid
        jtbd_analysis = await self.insight_frameworks['jtbd_grid'].analyze(
            customer_contexts=await self.collect_usage_contexts(brief),
            satisfaction_gaps=await self.identify_satisfaction_gaps(brief)
        )
        
        # 統合洞察生成
        insights = self.synthesize_customer_insights([
            brand_truth, cep_distribution, semiotic_insights,
            benefit_hierarchy, jtbd_analysis
        ])
        
        return [
            CustomerInsight(
                type="真理インサイト",
                insight=brand_truth.core_insight,
                customer_voice=brand_truth.supporting_quotes[0],
                evidence_count=brand_truth.evidence_strength,
                emotional_intensity=brand_truth.emotional_resonance,
                framework_source="Brand Key Model"
            ),
            CustomerInsight(
                type="利用文脈ギャップ",
                insight=f"'{cep_distribution.underserved_moments[0]}'での想起不足",
                customer_voice=cep_distribution.moment_expressions[0],
                evidence_count=cep_distribution.data_points,
                emotional_intensity=cep_distribution.frustration_level,
                framework_source="Category Entry Points"
            )
        ]
```

### 2.3 トレンド連動システム強化

**活用フレーム**: 13, 15, 25, 22

```python
class EnhancedTrendAnalysisSystem:
    def __init__(self):
        self.trend_frameworks = {
            'meme_emoji_scan': MemeEmojiScanner(),           # フレーム13
            'esg_narrative': ESGNarrativeMapper(),           # フレーム15
            'cultural_tension': CulturalTensionRadar(),      # フレーム25
            'influencer_network': InfluencerNetworkGrapher() # フレーム22
        }
    
    async def connect_trends_enhanced(self, brief: ProductBrief) -> List[TrendConnection]:
        """文化的洞察とインフルエンサーネットワーク活用"""
        
        # フレーム13: Meme & Emoji Trend Scan
        viral_language = await self.trend_frameworks['meme_emoji_scan'].scan(
            platforms=['TikTok', 'Instagram', 'Twitter'],
            category_hashtags=brief.category_hashtags,
            time_window='30_days'
        )
        
        # フレーム15: ESG Narrative Heatmap
        sustainability_trends = await self.trend_frameworks['esg_narrative'].map(
            category=brief.category,
            brand_csr=brief.sustainability_initiatives
        )
        
        # フレーム25: Cultural Tension Radar
        cultural_tensions = await self.trend_frameworks['cultural_tension'].detect(
            news_sources=['NHK', 'Yahoo News', 'Twitter Trends'],
            category_relevance=brief.category
        )
        
        # フレーム22: Influencer Network Graph
        influencer_insights = await self.trend_frameworks['influencer_network'].analyze(
            category=brief.category,
            target_demographics=brief.target_attributes
        )
        
        # トレンド統合
        connections = self.synthesize_trend_connections([
            viral_language, sustainability_trends, 
            cultural_tensions, influencer_insights
        ])
        
        return [
            TrendConnection(
                trend=f"バイラル語彙: {viral_language.trending_expressions[0]}",
                connection=f"製品価値'{brief.core_value}'との親和性",
                message_opportunity=f"'{viral_language.usage_contexts[0]}'文脈での訴求",
                relevance_score=viral_language.category_relevance,
                trend_strength=viral_language.viral_velocity,
                framework_source="Meme & Emoji Scan"
            ),
            TrendConnection(
                trend=f"ESG焦点: {sustainability_trends.hot_topics[0]}",
                connection="環境意識の高まり→製品選択基準変化",
                message_opportunity="サステナブル価値での差別化",
                relevance_score=sustainability_trends.brand_fit,
                trend_strength=sustainability_trends.narrative_heat,
                framework_source="ESG Narrative"
            )
        ]
```

### 2.4 ペルソナ対話システム強化

**活用フレーム**: 10, 11, 16, 17

```python
class EnhancedPersonaDialogueSystem:
    def __init__(self):
        self.dialogue_frameworks = {
            'touchpoint_atlas': TouchpointAtlasMapper(),     # フレーム10
            'shopper_journey': ShopperJourneyShadower(),     # フレーム11
            'benefit_ladder': BenefitLadderBuilder(),        # フレーム16 (再利用)
            'jtbd_interviewer': JTBDInterviewer()            # フレーム17 (再利用)
        }
    
    async def deep_interview_enhanced(self, brief: ProductBrief) -> List[PersonaVoice]:
        """行動観察とJTBD深掘りによる高精度ペルソナ対話"""
        
        # 強化ペルソナ生成
        enhanced_personas = await self.generate_personas_with_frameworks(brief, [
            self.dialogue_frameworks['touchpoint_atlas'],
            self.dialogue_frameworks['shopper_journey']
        ])
        
        interview_results = []
        
        for persona in enhanced_personas:
            # フレーム10: Touchpoint Atlas活用
            touchpoint_data = await self.dialogue_frameworks['touchpoint_atlas'].analyze(
                persona_profile=persona,
                category=brief.category
            )
            
            # フレーム11: Shopper Journey観察データ
            journey_insights = await self.dialogue_frameworks['shopper_journey'].extract(
                persona_type=persona.archetype,
                product_category=brief.category
            )
            
            # 深層インタビュー実行
            interview = await self.conduct_framework_enhanced_interview(
                persona, brief, touchpoint_data, journey_insights
            )
            
            # フレーム16&17: Benefit Ladder & JTBD深掘り
            deep_needs = await self.extract_layered_needs(
                interview, 
                self.dialogue_frameworks['benefit_ladder'],
                self.dialogue_frameworks['jtbd_interviewer']
            )
            
            interview_results.append(PersonaVoice(
                persona=persona,
                deep_needs=deep_needs,
                authentic_expressions=interview.natural_language,
                emotional_triggers=interview.trigger_points,
                touchpoint_insights=touchpoint_data,
                journey_friction_points=journey_insights.pain_points,
                framework_evidence=[
                    f"Touchpoint Atlas: {touchpoint_data.key_insights[0]}",
                    f"Journey Shadowing: {journey_insights.critical_moments[0]}",
                    f"Benefit Ladder: {deep_needs.emotional_benefits[0]}",
                    f"JTBD: {deep_needs.core_job_to_be_done}"
                ]
            ))
        
        return interview_results
```

### 2.5 業界知識統合システム強化

**活用フレーム**: 14, 18, 20, 24

```python
class EnhancedIndustryKnowledgeSystem:
    def __init__(self):
        self.knowledge_frameworks = {
            'warc_analyzer': WARCCaseAnalyzer(),             # フレーム14
            'brand_archetype': BrandArchetypeFitter(),       # フレーム18
            'media_mix_model': MediaMixModeler(),            # フレーム20
            'attention_quality': AttentionQualityIndexer()   # フレーム24
        }
    
    async def analyze_enhanced(self, brief: ProductBrief) -> List[ExpertPerspective]:
        """業界ベストプラクティス×ブランド理論×メディア科学統合"""
        
        # フレーム14: WARC成功パターン詳細分析
        warc_insights = await self.knowledge_frameworks['warc_analyzer'].deep_analyze(
            category=brief.category,
            target_metrics=brief.business_goals,
            budget_range=brief.media_budget,
            geographic_scope=brief.target_markets
        )
        
        # フレーム18: Brand Archetype適合度
        archetype_fit = await self.knowledge_frameworks['brand_archetype'].assess(
            brand_personality=brief.brand_attributes,
            category_archetypes=await self.get_category_archetypes(brief.category),
            target_persona=brief.target_attributes
        )
        
        # フレーム20: Media-Mix Model Lite
        media_effectiveness = await self.knowledge_frameworks['media_mix_model'].model(
            historical_spend=brief.historical_media_data,
            kpi_correlations=brief.kpi_history,
            category_benchmarks=await self.get_category_benchmarks(brief.category)
        )
        
        # フレーム24: Attention Quality Index
        attention_insights = await self.knowledge_frameworks['attention_quality'].analyze(
            format_types=brief.planned_formats,
            placement_contexts=brief.planned_placements,
            creative_elements=brief.creative_brief
        )
        
        # 統合エキスパート視点生成
        perspectives = self.synthesize_expert_perspectives([
            warc_insights, archetype_fit, media_effectiveness, attention_insights
        ])
        
        return [
            ExpertPerspective(
                domain="広告効果研究",
                insight=f"類似カテゴリで{warc_insights.success_patterns[0].effect_size}%効果向上",
                credibility=f"WARC Awards {warc_insights.award_years}",
                message_opportunity=warc_insights.applicable_strategies[0],
                authority_score=warc_insights.credibility_score,
                framework_source="WARC Pattern Analysis"
            ),
            ExpertPerspective(
                domain="ブランド心理学",
                insight=f"'{archetype_fit.optimal_archetype}'原型で共感度{archetype_fit.resonance_lift}%向上",
                credibility="Carl Jung アーキタイプ理論",
                message_opportunity=archetype_fit.messaging_guidelines,
                authority_score=archetype_fit.theoretical_strength,
                framework_source="Brand Archetype Theory"
            )
        ]
```

### 2.6 A/Bテスト仮説生成システム強化

**活用フレーム**: 8, 9, 23, 24

```python
class EnhancedABTestGenerationSystem:
    def __init__(self):
        self.test_frameworks = {
            'creative_mvp': CreativeMVPTester(),             # フレーム8
            'emotion_tracker': EmotionEyeTracker(),          # フレーム9
            'shelf_impact': ShelfImpactSimulator(),          # フレーム23
            'attention_quality': AttentionQualityIndexer()   # フレーム24 (再利用)
        }
    
    async def generate_hypotheses_enhanced(self, brief: ProductBrief) -> List[TestHypothesis]:
        """科学的測定手法に基づく高精度A/Bテスト設計"""
        
        # フレーム8: Creative MVP事前テスト
        mvp_results = await self.test_frameworks['creative_mvp'].test(
            concept_sketches=await self.generate_concept_sketches(brief),
            target_audience=brief.target_attributes
        )
        
        # フレーム9: Emotion-Eye Tracker分析
        emotional_patterns = await self.test_frameworks['emotion_tracker'].analyze(
            existing_category_ads=await self.collect_category_video_ads(brief.category),
            emotional_targets=brief.emotional_objectives
        )
        
        # フレーム23: Shelf Impact Simulation
        shelf_performance = await self.test_frameworks['shelf_impact'].simulate(
            package_designs=brief.package_variants,
            competitive_shelf=await self.get_category_shelf_data(brief.category)
        )
        
        # フレーム24: Attention Quality最適化
        attention_optimization = await self.test_frameworks['attention_quality'].optimize(
            ad_formats=brief.planned_formats,
            content_lengths=brief.copy_variants,
            placement_contexts=brief.media_plan
        )
        
        # 統合テスト仮説生成
        hypotheses = self.synthesize_test_hypotheses([
            mvp_results, emotional_patterns, shelf_performance, attention_optimization
        ])
        
        return [
            TestHypothesis(
                dimension="感情反応パターン",
                hypothesis=f"'{emotional_patterns.high_performance_emotions[0]}'軸で{emotional_patterns.expected_lift}%向上",
                test_design=f"感情軸A vs B: {emotional_patterns.test_variants}",
                expected_lift=emotional_patterns.expected_lift,
                confidence_level=emotional_patterns.statistical_confidence,
                measurement_method="Eye-tracking + 微表情分析",
                framework_source="Emotion-Eye Tracker"
            ),
            TestHypothesis(
                dimension="認知瞬間力",
                hypothesis=f"視認3秒で'{shelf_performance.optimal_message}'が{shelf_performance.recognition_rate}%認知",
                test_design=f"短縮コピー vs フル訴求: {shelf_performance.test_messages}",
                expected_lift=shelf_performance.recognition_improvement,
                confidence_level=shelf_performance.simulation_accuracy,
                measurement_method="3Dシェルフ + Eye-tracking",
                framework_source="Shelf Impact Simulation"
            )
        ]
```

## 3. 統合効果: フレームワーク×並列システム

### 3.1 発見精度の飛躍的向上

```
従来の単発分析:
フレーム1つ → 洞察1-2個

強化並列システム:
25フレーム × 6システム → 洞察50-100個 → 統合候補20-30個
```

### 3.2 科学的根拠の強化

各フレームワークが提供する**権威性**:

- **学術理論**: フレーム7(記号論)、18(アーキタイプ理論)
- **業界ベンチマーク**: フレーム14(WARC)、20(MMM)
- **行動科学**: フレーム9(Eye-tracking)、11(行動観察)
- **統計的検証**: フレーム5(検索データ)、24(注意品質指標)

### 3.3 実装の段階化

**Phase 1**: 基本フレーム(1-15)で基盤システム構築
**Phase 2**: 高度フレーム(16-25)で精度向上
**Phase 3**: AI学習による最適フレーム選択

---

**25の実践フレーム**により、What-to-Say Discoveryは単なるAIシステムから、**広告業界の集合知を結集したプロフェッショナルツール**へと進化します。 