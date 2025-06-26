import pytest
import asyncio
from unittest.mock import Mock, patch
import pandas as pd
import sys
import os

# テスト用にsrcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from framework_05_share_of_search import ShareOfSearchFramework

class TestShareOfSearchFramework:
    """Share of Search Framework のテストクラス"""
    
    def setup_method(self):
        """各テストメソッドの前に実行される初期化処理"""
        self.framework = ShareOfSearchFramework(output_base_dir="test_output")
    
    def test_framework_initialization(self):
        """フレームワークの初期化テスト"""
        assert self.framework.framework_id == 5
        assert self.framework.framework_name == "Share of Search"
        assert self.framework.version == "1.0.0"
        assert self.framework.component_name == "framework-analysis"
    
    def test_calculate_share_of_search(self):
        """Share of Search計算のテスト"""
        # サンプルデータ作成
        data = pd.DataFrame({
            'ブランドA': [50, 60, 40],
            'ブランドB': [30, 20, 35],
            'ブランドC': [20, 20, 25]
        })
        keywords = ['ブランドA', 'ブランドB', 'ブランドC']
        
        result = self.framework._calculate_share_of_search(data, keywords)
        
        # 結果検証
        assert isinstance(result, dict)
        assert len(result) == 3
        assert all(brand in result for brand in keywords)
        assert abs(sum(result.values()) - 100.0) < 0.01  # 合計が100%に近い
    
    def test_analyze_trends(self):
        """トレンド分析のテスト"""
        # 増加傾向のサンプルデータ
        data = pd.DataFrame({
            'ブランドA': [10, 20, 30, 40, 50],  # 増加傾向
            'ブランドB': [50, 40, 30, 20, 10],  # 減少傾向
            'ブランドC': [25, 30, 25, 30, 25]   # 安定
        })
        keywords = ['ブランドA', 'ブランドB', 'ブランドC']
        
        result = self.framework._analyze_trends(data, keywords)
        
        # 結果検証
        assert isinstance(result, dict)
        assert len(result) == 3
        
        # ブランドAは増加傾向
        assert result['ブランドA']['direction'] == 'increasing'
        
        # ブランドBは減少傾向
        assert result['ブランドB']['direction'] == 'decreasing'
    
    def test_analyze_competitive_position(self):
        """競合ポジション分析のテスト"""
        sos_data = {
            'ブランドA': 45.0,
            'ブランドB': 30.0,
            'ブランドC': 15.0,
            'ブランドD': 10.0
        }
        brand_name = 'ブランドB'
        
        result = self.framework._analyze_competitive_position(sos_data, brand_name)
        
        # 結果検証
        assert result['brand_rank'] == 2  # ブランドBは2位
        assert result['total_brands'] == 4
        assert result['market_leader'] == 'ブランドA'
        assert result['brand_share'] == 30.0
        assert result['gap_to_leader'] == 15.0  # 45.0 - 30.0
    
    def test_generate_insights(self):
        """インサイト生成のテスト"""
        sos_data = {'ブランドA': 50.0, 'ブランドB': 30.0, 'ブランドC': 20.0}
        trend_analysis = {
            'ブランドA': {'direction': 'increasing', 'strength': 0.8},
            'ブランドB': {'direction': 'stable', 'strength': 0.1},
            'ブランドC': {'direction': 'decreasing', 'strength': 0.5}
        }
        competitive_analysis = {
            'competitive_intensity': 4,
            'gap_to_leader': 0
        }
        
        insights = self.framework._generate_insights(
            sos_data, trend_analysis, competitive_analysis
        )
        
        # 結果検証
        assert isinstance(insights, list)
        assert len(insights) > 0
        assert any('ブランドA' in insight for insight in insights)
    
    @pytest.mark.asyncio
    async def test_collect_data_error_handling(self):
        """エラーハンドリングのテスト"""
        # 無効なブランド名でテスト
        with patch('framework_05_share_of_search.TrendReq') as mock_trends:
            mock_instance = Mock()
            mock_instance.interest_over_time.return_value = pd.DataFrame()  # 空のデータフレーム
            mock_trends.return_value = mock_instance
            
            result = await self.framework.collect_data(
                brand_name="存在しないブランド",
                competitors=["競合A", "競合B"],
                category="テストカテゴリ"
            )
            
            # エラー結果の検証
            assert result['success'] is False
            assert 'error' in result['framework_info']
    
    def teardown_method(self):
        """各テストメソッドの後に実行されるクリーンアップ処理"""
        # テスト用出力ディレクトリのクリーンアップ
        import shutil
        if os.path.exists("test_output"):
            shutil.rmtree("test_output")

if __name__ == "__main__":
    pytest.main([__file__]) 