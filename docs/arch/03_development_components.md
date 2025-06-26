# 三層ループシステム 開発コンポーネント設計

## 1. コンポーネント全体マップ

```
┌─────────────────────────────────────────────────────────────┐
│                    UI/API Layer                             │
├─────────────────────────────────────────────────────────────┤
│  Input Handler  │  Response Formatter  │  Status Monitor    │
├─────────────────────────────────────────────────────────────┤
│                   Core Engine Layer                         │
├─────────────────────────────────────────────────────────────┤
│ Generation    │ Evaluation      │ Selection    │ Mutation   │
│ Engine        │ Engine          │ Engine       │ Engine     │
├─────────────────────────────────────────────────────────────┤
│                  Support Layer                              │
├─────────────────────────────────────────────────────────────┤
│ Persona       │ Scoring         │ Loop         │ Config     │
│ Manager       │ Calculator      │ Controller   │ Manager    │
├─────────────────────────────────────────────────────────────┤
│                  Infrastructure Layer                       │
├─────────────────────────────────────────────────────────────┤
│ LLM Client    │ Data Store      │ Cache        │ Logger     │
└─────────────────────────────────────────────────────────────┘
```

## 2. 開発コンポーネント詳細

### 2.1 優先度A（MVP必須）

#### A1. Core Engine Components

**1. Generation Engine (`generation_engine.py`)**
```python
class GenerationEngine:
    """WHY/WHAT/HOW生成エンジン"""
    
    def generate_candidates(self, brief: ProductBrief, num_candidates: int = 8) -> List[Candidate]
    def generate_variants(self, base_candidate: Candidate, improvement_hints: Dict) -> List[Candidate]
    def _build_generation_prompt(self, brief: ProductBrief) -> str
    def _parse_llm_response(self, response: str) -> List[Candidate]
```

**2. Evaluation Engine (`evaluation_engine.py`)**
```python
class EvaluationEngine:
    """ユーザー反応シミュレータ"""
    
    def evaluate_candidate(self, candidate: Candidate, personas: List[Persona]) -> EvaluationResult
    def batch_evaluate(self, candidates: List[Candidate], personas: List[Persona]) -> List[EvaluationResult]
    def _build_evaluation_prompt(self, candidate: Candidate, persona: Persona) -> str
    def _parse_evaluation_response(self, response: str) -> PersonaScore
```

**3. Selection Engine (`selection_engine.py`)**
```python
class SelectionEngine:
    """スコア統合・選抜エンジン"""
    
    def select_top_candidates(self, evaluations: List[EvaluationResult], k: int = 3) -> List[Candidate]
    def calculate_composite_score(self, evaluation: EvaluationResult, weights: Dict[str, float]) -> float
    def should_continue_iteration(self, best_score: float, target_score: float, iteration: int) -> bool
```

**4. Loop Controller (`loop_controller.py`)**
```python
class LoopController:
    """メインループ制御"""
    
    def run_optimization_loop(self, brief: ProductBrief, config: LoopConfig) -> OptimizationResult
    def _single_iteration(self, candidates: List[Candidate], config: LoopConfig) -> IterationResult
    def _should_terminate(self, results: List[IterationResult], config: LoopConfig) -> bool
```

#### A2. Data Models (`models/`)

**1. Core Models (`models/core.py`)**
```python
@dataclass
class ProductBrief:
    product_name: str
    main_features: List[str]
    target_attributes: Dict[str, str]
    business_goals: Dict[str, str]
    constraints: Optional[List[str]] = None

@dataclass
class Candidate:
    why: str
    what: str
    how: CopyContent
    metadata: Dict[str, Any]

@dataclass
class CopyContent:
    headline: str
    body: str
    char_count: int
```

**2. Evaluation Models (`models/evaluation.py`)**
```python
@dataclass
class Persona:
    name: str
    age: int
    goals: str
    pain: str
    brand_attitude: str
    language_preference: str

@dataclass
class PersonaScore:
    relevance: float
    clarity: float
    emotional_impact: float
    action_intent: float
    novelty: float
    memorability: float
    policy_safe: bool
    reasoning: Dict[str, str]

@dataclass
class EvaluationResult:
    candidate_id: str
    persona_scores: List[PersonaScore]
    composite_score: float
    detailed_feedback: Dict[str, Any]
```

#### A3. Infrastructure Components

**1. LLM Client (`infrastructure/llm_client.py`)**
```python
class LLMClient:
    """LLM API統合クライアント"""
    
    def generate_text(self, prompt: str, model: str = "gpt-4o", temperature: float = 0.8) -> str
    def evaluate_text(self, prompt: str, model: str = "claude-3", temperature: float = 0.2) -> str
    def batch_request(self, prompts: List[str], model: str) -> List[str]
    def _handle_rate_limits(self)
    def _retry_on_failure(self, request_func, max_retries: int = 3)
```

**2. Configuration Manager (`infrastructure/config.py`)**
```python
class ConfigManager:
    """設定管理"""
    
    def load_config(self) -> SystemConfig
    def get_evaluation_weights(self) -> Dict[str, float]
    def get_default_personas(self) -> List[Persona]
    def update_weights(self, new_weights: Dict[str, float])
```

### 2.2 優先度B（拡張機能）

#### B1. Advanced Features

**1. Persona Manager (`persona_manager.py`)**
```python
class PersonaManager:
    """ペルソナ管理・最適化"""
    
    def create_persona_from_data(self, user_data: Dict) -> Persona
    def optimize_personas(self, feedback_data: List[FeedbackData]) -> List[Persona]
    def generate_synthetic_personas(self, base_personas: List[Persona], variations: int) -> List[Persona]
```

**2. Mutation Engine (`mutation_engine.py`)**
```python
class MutationEngine:
    """変異・改善エンジン"""
    
    def mutate_candidate(self, candidate: Candidate, weak_points: List[str]) -> List[Candidate]
    def analyze_weakness(self, evaluation: EvaluationResult) -> List[str]
    def generate_improvement_hints(self, weak_points: List[str]) -> Dict[str, str]
```

**3. Multi-layer Evaluator (`multi_layer_evaluator.py`)**
```python
class MultiLayerEvaluator:
    """多層評価システム"""
    
    def evaluate_layer_0_format(self, candidate: Candidate) -> LayerScore
    def evaluate_layer_1_phonetics(self, candidate: Candidate) -> LayerScore
    def evaluate_layer_2_diversity(self, candidate: Candidate) -> LayerScore
    def evaluate_layer_3_semantics(self, candidate: Candidate) -> LayerScore
    def evaluate_layer_4_emotion(self, candidate: Candidate) -> LayerScore
    def evaluate_layer_5_llm_judge(self, candidate: Candidate) -> LayerScore
    def evaluate_layer_6_kpi_proxy(self, candidate: Candidate) -> LayerScore
```

#### B2. Data & Analytics

**1. Data Store (`infrastructure/data_store.py`)**
```python
class DataStore:
    """データ永続化"""
    
    def save_optimization_run(self, run_data: OptimizationRun)
    def load_historical_data(self, filters: Dict) -> List[OptimizationRun]
    def save_feedback(self, feedback: UserFeedback)
    def get_performance_metrics(self, time_range: Tuple[datetime, datetime]) -> PerformanceMetrics
```

**2. Learning Engine (`learning_engine.py`)**
```python
class LearningEngine:
    """継続学習・重み最適化"""
    
    def update_evaluation_weights(self, real_kpi_data: List[KPIData]) -> Dict[str, float]
    def refine_persona_accuracy(self, feedback_data: List[FeedbackData]) -> List[Persona]
    def analyze_generation_patterns(self, historical_data: List[OptimizationRun]) -> AnalysisReport
```

### 2.3 優先度C（運用支援）

#### C1. API & UI

**1. REST API (`api/main.py`)**
```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/api/generate")
async def generate_copy(request: GenerationRequest) -> GenerationResponse

@app.post("/api/evaluate") 
async def evaluate_copy(request: EvaluationRequest) -> EvaluationResponse

@app.get("/api/status")
async def get_system_status() -> SystemStatus
```

**2. Streamlit Dashboard (`dashboard/app.py`)**
```python
def main():
    st.title("三層ループシステム ダッシュボード")
    
    tab1, tab2, tab3 = st.tabs(["生成", "評価", "分析"])
    
    with tab1:
        render_generation_interface()
    with tab2:
        render_evaluation_interface() 
    with tab3:
        render_analytics_interface()
```

#### C2. Monitoring & Logging

**1. System Monitor (`monitoring/monitor.py`)**
```python
class SystemMonitor:
    """システム監視"""
    
    def track_generation_quality(self, results: List[OptimizationResult])
    def monitor_api_performance(self, metrics: APIMetrics)
    def alert_on_anomalies(self, threshold_config: Dict)
    def generate_health_report(self) -> HealthReport
```

**2. Logger (`infrastructure/logger.py`)**
```python
class StructuredLogger:
    """構造化ログ"""
    
    def log_generation_attempt(self, brief: ProductBrief, result: OptimizationResult)
    def log_evaluation_session(self, evaluation_data: EvaluationSession)
    def log_performance_metrics(self, metrics: PerformanceMetrics)
```

## 3. 開発フェーズ計画

### Phase 1: MVP Development (4週間)
```
Week 1-2: Core Models + Generation Engine + LLM Client
Week 3-4: Evaluation Engine + Selection Engine + Loop Controller
```

### Phase 2: Essential Features (3週間)
```
Week 5-6: Multi-layer Evaluator + Persona Manager
Week 7: Basic API + Simple Dashboard
```

### Phase 3: Advanced Features (3週間)
```
Week 8-9: Mutation Engine + Learning Engine
Week 10: Full Dashboard + Monitoring
```

### Phase 4: Production Ready (2週間)
```
Week 11: Performance Optimization + Error Handling
Week 12: Testing + Documentation + Deployment
```

## 4. 技術スタック提案

| Layer | Technology | Purpose |
|-------|------------|---------|
| API | FastAPI + Pydantic | REST API + バリデーション |
| UI | Streamlit | プロトタイプダッシュボード |
| Core Logic | Python 3.11+ | メインロジック |
| LLM Integration | OpenAI SDK + Anthropic SDK | LLM API連携 |
| Data Storage | SQLite → PostgreSQL | データ永続化 |
| Caching | Redis | パフォーマンス向上 |
| Monitoring | Prometheus + Grafana | メトリクス監視 |
| Testing | pytest + Factory Boy | テスト自動化 |

## 5. 次のアクション

1. **Phase 1の詳細設計** - Core Models と Generation Engine から開始
2. **開発環境セットアップ** - プロジェクト構造とCI/CD
3. **プロトタイプ実装** - 最小構成での動作確認

どのコンポーネントから実装を開始しますか？ 