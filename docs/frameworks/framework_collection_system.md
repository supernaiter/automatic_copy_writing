# 25フレームワーク データ収集システム 設計書

## 1. システム概要

**目的**: 25の実践フレームワークを独立コンポーネントとして実装し、各フレームワークが専門的データ収集を実行する統合システム

### 1.1 アーキテクチャ概要

```
┌─────────────────────────────────────────────────────────────┐
│                Framework Collection System                   │
├─────────────────────────────────────────────────────────────┤
│  基本フレーム(1-15)          │  高度フレーム(16-25)          │
├─────────────────────────────────────────────────────────────┤
│ ┌─ フレーム1  ブランドキー ─┐ │ ┌─ フレーム16 ベネフィット ─┐ │
│ ├─ フレーム2  CEP分布 ────┤ │ ├─ フレーム17 JTBD Grid ──┤ │
│ ├─ フレーム3  DBA Score ──┤ │ ├─ フレーム18 アーキタイプ ─┤ │
│ ├─ フレーム4  CM好感度 ───┤ │ ├─ フレーム19 トーン分析 ──┤ │
│ ├─ フレーム5  検索シェア ──┤ │ ├─ フレーム20 MMM Lite ──┤ │
│ ├─ フレーム6  文化コード ──┤ │ ├─ フレーム21 アーンド ───┤ │
│ ├─ フレーム7  記号論 ─────┤ │ ├─ フレーム22 インフル ───┤ │
│ ├─ フレーム8  Creative MVP ┤ │ ├─ フレーム23 シェルフ ───┤ │
│ ├─ フレーム9  感情視線 ───┤ │ ├─ フレーム24 注意品質 ───┤ │
│ ├─ フレーム10 タッチP ────┤ │ └─ フレーム25 文化緊張 ───┘ │
│ ├─ フレーム11 購買観察 ───┤ │                              │
│ ├─ フレーム12 コピーDNA ──┤ │                              │
│ ├─ フレーム13 ミーム分析 ─┤ │                              │
│ ├─ フレーム14 WARC対比 ───┤ │                              │
│ └─ フレーム15 ESG語り ────┘ │                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    ┌─ 統合API ─┐
                    ├─ 結果DB ──┤  
                    └─ ダッシュ ─┘
```

## 2. 独立コンポーネント設計

### 2.1 基底クラス: FrameworkComponent

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from dataclasses import dataclass
from enum import Enum

class FrameworkType(Enum):
    BASIC = "basic"      # フレーム1-15
    ADVANCED = "advanced" # フレーム16-25

class DataSource(Enum):
    INTERNAL = "internal"    # 社内データ
    WEB_API = "web_api"     # 外部API
    SCRAPING = "scraping"   # ウェブスクレイピング
    SURVEY = "survey"       # 調査データ
    OBSERVATION = "observation" # 行動観察

@dataclass
class FrameworkResult:
    framework_id: int
    framework_name: str
    success: bool
    data: Dict[str, Any]
    insights: List[str]
    confidence_score: float
    execution_time: float
    data_sources_used: List[DataSource]
    raw_data_size: int
    error_message: str = None

class FrameworkComponent(ABC):
    """全フレームワークの基底クラス"""
    
    def __init__(self, framework_id: int, name: str, framework_type: FrameworkType):
        self.framework_id = framework_id
        self.name = name
        self.framework_type = framework_type
        self.required_inputs = []
        self.data_sources = []
        self.execution_time_estimate = 0  # 秒
    
    @abstractmethod
    async def collect_data(self, input_data: Dict[str, Any]) -> FrameworkResult:
        """各フレームワーク固有のデータ収集ロジック"""
        pass
    
    @abstractmethod
    def validate_inputs(self, input_data: Dict[str, Any]) -> bool:
        """入力データの妥当性検証"""
        pass
    
    @abstractmethod
    def estimate_execution_time(self, input_data: Dict[str, Any]) -> int:
        """実行時間予測（秒）"""
        pass
    
    def get_framework_info(self) -> Dict[str, Any]:
        """フレームワーク情報取得"""
        return {
            "id": self.framework_id,
            "name": self.name,
            "type": self.framework_type.value,
            "required_inputs": self.required_inputs,
            "data_sources": [ds.value for ds in self.data_sources],
            "estimated_time": self.execution_time_estimate
        }
```

### 2.2 具体的実装例: フレーム1-5

#### フレーム1: ブランド・キーモデル

```python
class BrandKeyFramework(FrameworkComponent):
    def __init__(self):
        super().__init__(1, "ブランド・キーモデル", FrameworkType.BASIC)
        self.required_inputs = ["product_name", "category", "stakeholder_contacts"]
        self.data_sources = [DataSource.INTERNAL, DataSource.SURVEY]
        self.execution_time_estimate = 1800  # 30分
    
    async def collect_data(self, input_data: Dict[str, Any]) -> FrameworkResult:
        start_time = time.time()
        
        try:
            # Step 1: 社内ステークホルダーインタビュー
            stakeholder_insights = await self._conduct_stakeholder_interviews(
                input_data["stakeholder_contacts"]
            )
            
            # Step 2: 顧客調査データ収集
            customer_research = await self._collect_customer_research(
                input_data["product_name"], input_data["category"]
            )
            
            # Step 3: ブランド真理抽出
            brand_truth = await self._extract_brand_truth(
                stakeholder_insights, customer_research
            )
            
            # Step 4: インサイト統合
            insights = self._synthesize_insights(brand_truth)
            
            execution_time = time.time() - start_time
            
            return FrameworkResult(
                framework_id=1,
                framework_name="ブランド・キーモデル",
                success=True,
                data={
                    "brand_truth": brand_truth,
                    "stakeholder_insights": stakeholder_insights,
                    "customer_research": customer_research
                },
                insights=insights,
                confidence_score=self._calculate_confidence(brand_truth),
                execution_time=execution_time,
                data_sources_used=[DataSource.INTERNAL, DataSource.SURVEY],
                raw_data_size=len(str(stakeholder_insights)) + len(str(customer_research))
            )
            
        except Exception as e:
            return FrameworkResult(
                framework_id=1,
                framework_name="ブランド・キーモデル",
                success=False,
                data={},
                insights=[],
                confidence_score=0.0,
                execution_time=time.time() - start_time,
                data_sources_used=[],
                raw_data_size=0,
                error_message=str(e)
            )
    
    async def _conduct_stakeholder_interviews(self, contacts: List[str]) -> Dict:
        """社内ステークホルダーインタビュー実行"""
        # 実装: オンライン調査フォーム送付 + 回答収集
        pass
    
    async def _collect_customer_research(self, product: str, category: str) -> Dict:
        """顧客調査データ収集"""
        # 実装: 既存調査データ + 新規ミニ調査
        pass
    
    def validate_inputs(self, input_data: Dict[str, Any]) -> bool:
        required_keys = ["product_name", "category", "stakeholder_contacts"]
        return all(key in input_data for key in required_keys)
    
    def estimate_execution_time(self, input_data: Dict[str, Any]) -> int:
        base_time = 1800  # 30分
        stakeholder_count = len(input_data.get("stakeholder_contacts", []))
        return base_time + (stakeholder_count * 300)  # 1人あたり5分追加
```

#### フレーム2: Category Entry Points分布

```python
class CategoryEntryPointsFramework(FrameworkComponent):
    def __init__(self):
        super().__init__(2, "Category Entry Points分布", FrameworkType.BASIC)
        self.required_inputs = ["category", "time_range"]
        self.data_sources = [DataSource.WEB_API, DataSource.SCRAPING]
        self.execution_time_estimate = 900  # 15分
    
    async def collect_data(self, input_data: Dict[str, Any]) -> FrameworkResult:
        start_time = time.time()
        
        try:
            # Step 1: SNS投稿収集
            social_posts = await self._collect_social_posts(
                input_data["category"], input_data["time_range"]
            )
            
            # Step 2: 検索クエリ収集
            search_queries = await self._collect_search_queries(
                input_data["category"], input_data["time_range"]
            )
            
            # Step 3: Entry Points分類
            entry_points = await self._classify_entry_points(
                social_posts, search_queries
            )
            
            # Step 4: ヒートマップ生成
            heatmap_data = self._generate_cep_heatmap(entry_points)
            
            execution_time = time.time() - start_time
            
            return FrameworkResult(
                framework_id=2,
                framework_name="Category Entry Points分布",
                success=True,
                data={
                    "entry_points": entry_points,
                    "heatmap_data": heatmap_data,
                    "social_posts_count": len(social_posts),
                    "search_queries_count": len(search_queries)
                },
                insights=self._extract_cep_insights(entry_points),
                confidence_score=self._calculate_cep_confidence(entry_points),
                execution_time=execution_time,
                data_sources_used=[DataSource.WEB_API, DataSource.SCRAPING],
                raw_data_size=len(social_posts) + len(search_queries)
            )
            
        except Exception as e:
            return FrameworkResult(
                framework_id=2,
                framework_name="Category Entry Points分布",
                success=False,
                data={},
                insights=[],
                confidence_score=0.0,
                execution_time=time.time() - start_time,
                data_sources_used=[],
                raw_data_size=0,
                error_message=str(e)
            )
    
    def validate_inputs(self, input_data: Dict[str, Any]) -> bool:
        return "category" in input_data and "time_range" in input_data
```

#### フレーム3: Distinctive Brand Assets Score

```python
class DistinctiveBrandAssetsFramework(FrameworkComponent):
    def __init__(self):
        super().__init__(3, "Distinctive Brand Assets Score", FrameworkType.BASIC)
        self.required_inputs = ["brand_assets", "target_audience"]
        self.data_sources = [DataSource.SURVEY, DataSource.OBSERVATION]
        self.execution_time_estimate = 2400  # 40分
    
    async def collect_data(self, input_data: Dict[str, Any]) -> FrameworkResult:
        start_time = time.time()
        
        try:
            # Step 1: 100人認知調査
            recognition_survey = await self._conduct_recognition_survey(
                input_data["brand_assets"], input_data["target_audience"]
            )
            
            # Step 2: アイトラッキング想起速度測定
            eye_tracking_data = await self._measure_recognition_speed(
                input_data["brand_assets"]
            )
            
            # Step 3: DBAスコア算出
            dba_scores = self._calculate_dba_scores(
                recognition_survey, eye_tracking_data
            )
            
            execution_time = time.time() - start_time
            
            return FrameworkResult(
                framework_id=3,
                framework_name="Distinctive Brand Assets Score",
                success=True,
                data={
                    "dba_scores": dba_scores,
                    "recognition_survey": recognition_survey,
                    "eye_tracking_data": eye_tracking_data
                },
                insights=self._extract_dba_insights(dba_scores),
                confidence_score=self._calculate_dba_confidence(recognition_survey),
                execution_time=execution_time,
                data_sources_used=[DataSource.SURVEY, DataSource.OBSERVATION],
                raw_data_size=len(recognition_survey) + len(eye_tracking_data)
            )
            
        except Exception as e:
            return FrameworkResult(
                framework_id=3,
                framework_name="Distinctive Brand Assets Score", 
                success=False,
                data={},
                insights=[],
                confidence_score=0.0,
                execution_time=time.time() - start_time,
                data_sources_used=[],
                raw_data_size=0,
                error_message=str(e)
            )
```

#### フレーム4: CM好感度×記憶指標

```python
class CMPreferenceFramework(FrameworkComponent):
    def __init__(self):
        super().__init__(4, "CM好感度×記憶指標", FrameworkType.BASIC)
        self.required_inputs = ["cm_content", "target_demographic"]
        self.data_sources = [DataSource.SURVEY, DataSource.WEB_API]
        self.execution_time_estimate = 1200  # 20分
    
    async def collect_data(self, input_data: Dict[str, Any]) -> FrameworkResult:
        start_time = time.time()
        
        try:
            # Step 1: AC企画好感度調査データ取得
            preference_data = await self._get_ac_preference_data(
                input_data["cm_content"]
            )
            
            # Step 2: 30秒後再認テスト
            recall_test = await self._conduct_recall_test(
                input_data["cm_content"], input_data["target_demographic"]
            )
            
            # Step 3: 好感度×記憶相関分析
            correlation_analysis = self._analyze_preference_recall_correlation(
                preference_data, recall_test
            )
            
            execution_time = time.time() - start_time
            
            return FrameworkResult(
                framework_id=4,
                framework_name="CM好感度×記憶指標",
                success=True,
                data={
                    "preference_data": preference_data,
                    "recall_test": recall_test,
                    "correlation_analysis": correlation_analysis
                },
                insights=self._extract_cm_insights(correlation_analysis),
                confidence_score=self._calculate_cm_confidence(recall_test),
                execution_time=execution_time,
                data_sources_used=[DataSource.SURVEY, DataSource.WEB_API],
                raw_data_size=len(preference_data) + len(recall_test)
            )
            
        except Exception as e:
            return FrameworkResult(
                framework_id=4,
                framework_name="CM好感度×記憶指標",
                success=False,
                data={},
                insights=[],
                confidence_score=0.0,
                execution_time=time.time() - start_time,
                data_sources_used=[],
                raw_data_size=0,
                error_message=str(e)
            )
```

#### フレーム5: Share of Search / SOV

```python
class ShareOfSearchFramework(FrameworkComponent):
    def __init__(self):
        super().__init__(5, "Share of Search / SOV", FrameworkType.BASIC)
        self.required_inputs = ["brand_name", "competitors", "category"]
        self.data_sources = [DataSource.WEB_API]
        self.execution_time_estimate = 300  # 5分
    
    async def collect_data(self, input_data: Dict[str, Any]) -> FrameworkResult:
        start_time = time.time()
        
        try:
            # Step 1: Google Trends API抽出
            trends_data = await self._extract_google_trends(
                input_data["brand_name"], 
                input_data["competitors"],
                input_data["category"]
            )
            
            # Step 2: 検索シェア算出
            search_share = self._calculate_search_share(trends_data)
            
            # Step 3: 月次折れ線グラフ生成
            trend_chart = self._generate_trend_chart(trends_data)
            
            execution_time = time.time() - start_time
            
            return FrameworkResult(
                framework_id=5,
                framework_name="Share of Search / SOV",
                success=True,
                data={
                    "search_share": search_share,
                    "trends_data": trends_data,
                    "trend_chart": trend_chart
                },
                insights=self._extract_sos_insights(search_share),
                confidence_score=self._calculate_sos_confidence(trends_data),
                execution_time=execution_time,
                data_sources_used=[DataSource.WEB_API],
                raw_data_size=len(trends_data)
            )
            
        except Exception as e:
            return FrameworkResult(
                framework_id=5,
                framework_name="Share of Search / SOV",
                success=False,
                data={},
                insights=[],
                confidence_score=0.0,
                execution_time=time.time() - start_time,
                data_sources_used=[],
                raw_data_size=0,
                error_message=str(e)
            )
```

## 3. 統合システム設計

### 3.1 FrameworkCollectionOrchestrator

```python
class FrameworkCollectionOrchestrator:
    """25フレームワークの統制システム"""
    
    def __init__(self):
        self.frameworks = self._initialize_frameworks()
        self.execution_monitor = ExecutionMonitor()
        self.result_aggregator = ResultAggregator()
        self.data_storage = DataStorage()
    
    def _initialize_frameworks(self) -> Dict[int, FrameworkComponent]:
        """全25フレームワークを初期化"""
        frameworks = {}
        
        # 基本フレーム (1-15)
        frameworks[1] = BrandKeyFramework()
        frameworks[2] = CategoryEntryPointsFramework()
        frameworks[3] = DistinctiveBrandAssetsFramework()
        frameworks[4] = CMPreferenceFramework()
        frameworks[5] = ShareOfSearchFramework()
        # ... 継続して6-15まで
        
        # 高度フレーム (16-25) 
        frameworks[16] = BenefitLadderFramework()
        frameworks[17] = JTBDGridFramework()
        # ... 継続して18-25まで
        
        return frameworks
    
    async def execute_framework(self, framework_id: int, input_data: Dict[str, Any]) -> FrameworkResult:
        """単一フレームワーク実行"""
        
        if framework_id not in self.frameworks:
            raise ValueError(f"Framework {framework_id} not found")
        
        framework = self.frameworks[framework_id]
        
        # 入力検証
        if not framework.validate_inputs(input_data):
            raise ValueError(f"Invalid inputs for framework {framework_id}")
        
        # 実行時間予測
        estimated_time = framework.estimate_execution_time(input_data)
        self.execution_monitor.start_tracking(framework_id, estimated_time)
        
        try:
            # フレームワーク実行
            result = await framework.collect_data(input_data)
            
            # 結果保存
            await self.data_storage.save_result(result)
            
            # 監視更新
            self.execution_monitor.complete_tracking(framework_id, result.execution_time)
            
            return result
            
        except Exception as e:
            self.execution_monitor.error_tracking(framework_id, str(e))
            raise
    
    async def execute_framework_set(self, framework_ids: List[int], 
                                  input_data: Dict[str, Any]) -> List[FrameworkResult]:
        """複数フレームワーク並列実行"""
        
        tasks = []
        for framework_id in framework_ids:
            task = asyncio.create_task(
                self.execute_framework(framework_id, input_data)
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 例外処理
        successful_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Framework {framework_ids[i]} failed: {result}")
            else:
                successful_results.append(result)
        
        return successful_results
    
    async def execute_all_frameworks(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """全25フレームワーク実行"""
        
        # フェーズ分割実行
        basic_frameworks = list(range(1, 16))  # 1-15
        advanced_frameworks = list(range(16, 26))  # 16-25
        
        # Phase 1: 基本フレーム並列実行
        basic_results = await self.execute_framework_set(basic_frameworks, input_data)
        
        # Phase 2: 高度フレーム並列実行  
        advanced_results = await self.execute_framework_set(advanced_frameworks, input_data)
        
        # 結果統合
        all_results = basic_results + advanced_results
        aggregated_insights = await self.result_aggregator.aggregate_insights(all_results)
        
        return {
            "basic_framework_results": basic_results,
            "advanced_framework_results": advanced_results,
            "aggregated_insights": aggregated_insights,
            "execution_summary": self.execution_monitor.get_summary()
        }
    
    def get_framework_catalog(self) -> List[Dict[str, Any]]:
        """フレームワーク一覧取得"""
        return [framework.get_framework_info() for framework in self.frameworks.values()]
```

### 3.2 API設計

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="25 Framework Collection System")

class FrameworkRequest(BaseModel):
    framework_id: int
    input_data: Dict[str, Any]

class MultiFrameworkRequest(BaseModel):
    framework_ids: List[int]
    input_data: Dict[str, Any]

orchestrator = FrameworkCollectionOrchestrator()

@app.get("/frameworks")
async def list_frameworks():
    """利用可能フレームワーク一覧"""
    return orchestrator.get_framework_catalog()

@app.post("/framework/execute")
async def execute_single_framework(request: FrameworkRequest):
    """単一フレームワーク実行"""
    try:
        result = await orchestrator.execute_framework(
            request.framework_id, request.input_data
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/frameworks/execute")
async def execute_multiple_frameworks(request: MultiFrameworkRequest):
    """複数フレームワーク並列実行"""
    try:
        results = await orchestrator.execute_framework_set(
            request.framework_ids, request.input_data
        )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/frameworks/execute-all")
async def execute_all_frameworks(input_data: Dict[str, Any]):
    """全25フレームワーク実行"""
    try:
        results = await orchestrator.execute_all_frameworks(input_data)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/execution/status")
async def get_execution_status():
    """実行状況監視"""
    return orchestrator.execution_monitor.get_current_status()
```

## 4. 開発ロードマップ

### Phase 1: 基盤構築 (2週間)
- [ ] 基底クラス `FrameworkComponent` 実装
- [ ] オーケストレーター `FrameworkCollectionOrchestrator` 実装
- [ ] データストレージ・監視システム構築
- [ ] API基盤構築

### Phase 2: 基本フレーム実装 (4週間)
- [ ] フレーム1-5 実装・テスト
- [ ] フレーム6-10 実装・テスト
- [ ] フレーム11-15 実装・テスト
- [ ] 統合テスト・エラーハンドリング

### Phase 3: 高度フレーム実装 (4週間)
- [ ] フレーム16-20 実装・テスト
- [ ] フレーム21-25 実装・テスト
- [ ] パフォーマンス最適化
- [ ] 本格統合テスト

### Phase 4: UI・運用機能 (2週間)
- [ ] ダッシュボード構築
- [ ] 結果可視化システム
- [ ] 運用監視・ログ機能
- [ ] ドキュメント整備

## 5. 技術スタック

```python
# 必要ライブラリ
requirements = [
    "fastapi>=0.104.0",          # API基盤
    "asyncio>=3.4.3",           # 並列処理
    "aiohttp>=3.8.0",           # 非同期HTTP
    "pandas>=2.1.0",            # データ処理
    "numpy>=1.24.0",            # 数値計算
    "sqlalchemy>=2.0.0",        # データベース
    "redis>=5.0.0",             # キャッシュ・セッション
    "beautifulsoup4>=4.12.0",   # スクレイピング
    "selenium>=4.15.0",         # ブラウザ自動化
    "google-api-python-client", # Google APIs
    "tweepy>=4.14.0",          # Twitter API
    "python-dotenv>=1.0.0",    # 環境設定
    "pydantic>=2.5.0",         # データ検証
    "pytest>=7.4.0",           # テスト
    "pytest-asyncio>=0.21.0"   # 非同期テスト
]
```

---

この設計により、**25フレームワークをモジュラー化**し、段階的開発が可能になります。各フレームワークが独立コンポーネントなので、**1つずつ完成させて順次統合**できます！ 