#!/usr/bin/env python3
"""
フレーム12: Copy DNA Audit (コピーライティング語彙・リズム・構文分析)
実行方法: python framework_12_copy_dna.py
"""

import asyncio
import json
import time
import argparse
from datetime import datetime
from typing import List, Dict, Any, Tuple
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import re
from collections import Counter, defaultdict
import numpy as np

# 依存ライブラリチェック
try:
    import jieba
    import wordcloud
except ImportError:
    print("❌ 必要なライブラリがインストールされていません。以下のコマンドでインストールしてください:")
    print("pip install jieba wordcloud matplotlib seaborn pandas numpy")
    sys.exit(1)

class CopyDNAFramework:
    """Copy DNA Audit フレームワーク - スタンドアロン版"""
    
    def __init__(self):
        self.framework_id = 12
        self.framework_name = "Copy DNA Audit"
        self.version = "1.0.0"
        self.output_dir = f"data/output/output_framework_12_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 出力ディレクトリ作成
        os.makedirs(self.output_dir, exist_ok=True)
        
        print(f"🚀 {self.framework_name} v{self.version} 開始")
        print(f"📁 出力ディレクトリ: {self.output_dir}")
        
        # 日本語テキスト分析用パターン
        self.hiragana_pattern = re.compile(r'[ひらがな]+')
        self.katakana_pattern = re.compile(r'[カタカナ]+')
        self.kanji_pattern = re.compile(r'[一-龯]+')
        self.punctuation_pattern = re.compile(r'[。、！？…・※]')
        
    async def collect_data(self, copy_samples: List[str], brand_name: str = "Unknown") -> Dict[str, Any]:
        """Copy DNA データ収集・分析"""
        
        start_time = time.time()
        print(f"\n📊 分析開始: {len(copy_samples)}件のコピー分析")
        
        try:
            # Step 1: 基本統計分析
            print("📝 基本統計分析中...")
            basic_stats = self._analyze_basic_statistics(copy_samples)
            
            # Step 2: 語彙分析
            print("🔤 語彙分析中...")
            vocabulary_analysis = await self._analyze_vocabulary(copy_samples)
            
            # Step 3: リズム・音韻分析
            print("🎵 リズム分析中...")
            rhythm_analysis = self._analyze_rhythm_patterns(copy_samples)
            
            # Step 4: 構文パターン分析
            print("🏗️ 構文分析中...")
            syntax_analysis = self._analyze_syntax_patterns(copy_samples)
            
            # Step 5: 感情・トーン分析
            print("😊 感情トーン分析中...")
            emotion_analysis = self._analyze_emotional_tone(copy_samples)
            
            # Step 6: DNAパターン抽出
            print("🧬 DNAパターン抽出中...")
            dna_patterns = self._extract_dna_patterns(
                vocabulary_analysis, rhythm_analysis, syntax_analysis, emotion_analysis
            )
            
            execution_time = time.time() - start_time
            
            result = {
                "framework_info": {
                    "id": self.framework_id,
                    "name": self.framework_name,
                    "version": self.version,
                    "execution_time": execution_time,
                    "timestamp": datetime.now().isoformat()
                },
                "input_parameters": {
                    "brand_name": brand_name,
                    "copy_count": len(copy_samples),
                    "sample_copies": copy_samples[:3]  # 最初の3件をサンプルとして保存
                },
                "basic_statistics": basic_stats,
                "vocabulary_analysis": vocabulary_analysis,
                "rhythm_analysis": rhythm_analysis,
                "syntax_analysis": syntax_analysis,
                "emotion_analysis": emotion_analysis,
                "dna_patterns": dna_patterns,
                "insights": self._generate_insights(basic_stats, vocabulary_analysis, dna_patterns),
                "success": True
            }
            
            print(f"✅ 分析完了 ({execution_time:.2f}秒)")
            return result
            
        except Exception as e:
            error_result = {
                "framework_info": {
                    "id": self.framework_id,
                    "name": self.framework_name,
                    "error": str(e)
                },
                "success": False,
                "execution_time": time.time() - start_time
            }
            print(f"❌ エラー: {str(e)}")
            return error_result
    
    def _analyze_basic_statistics(self, copies: List[str]) -> Dict[str, Any]:
        """基本統計分析"""
        char_counts = [len(copy) for copy in copies]
        word_counts = [len(copy.split()) for copy in copies]
        sentence_counts = [len(re.split(r'[。！？]', copy)) for copy in copies]
        
        return {
            "total_copies": len(copies),
            "character_stats": {
                "avg": np.mean(char_counts),
                "median": np.median(char_counts),
                "min": min(char_counts),
                "max": max(char_counts),
                "std": np.std(char_counts)
            },
            "word_stats": {
                "avg": np.mean(word_counts),
                "median": np.median(word_counts),
                "std": np.std(word_counts)
            },
            "sentence_stats": {
                "avg": np.mean(sentence_counts),
                "median": np.median(sentence_counts),
                "std": np.std(sentence_counts)
            }
        }
    
    async def _analyze_vocabulary(self, copies: List[str]) -> Dict[str, Any]:
        """語彙分析"""
        all_text = ' '.join(copies)
        
        # 形態素解析（簡易版）
        words = []
        for copy in copies:
            # ひらがな、カタカナ、漢字の分離
            hiragana_words = re.findall(r'[ひらがな]+', copy)
            katakana_words = re.findall(r'[ァ-ヶ]+', copy)
            kanji_words = re.findall(r'[一-龯]+', copy)
            
            words.extend(hiragana_words + katakana_words + kanji_words)
        
        # 語彙統計
        word_freq = Counter(words)
        unique_words = len(word_freq)
        total_words = sum(word_freq.values())
        
        # N-gram分析
        bigrams = self._extract_ngrams(all_text, 2)
        trigrams = self._extract_ngrams(all_text, 3)
        
        # 文字種別分析
        char_type_ratio = self._analyze_character_types(all_text)
        
        return {
            "vocabulary_size": unique_words,
            "total_words": total_words,
            "vocabulary_richness": unique_words / total_words if total_words > 0 else 0,
            "top_words": dict(word_freq.most_common(20)),
            "top_bigrams": dict(Counter(bigrams).most_common(10)),
            "top_trigrams": dict(Counter(trigrams).most_common(10)),
            "character_type_ratio": char_type_ratio,
            "rare_words": [word for word, freq in word_freq.items() if freq == 1][:10]
        }
    
    def _extract_ngrams(self, text: str, n: int) -> List[str]:
        """N-gram抽出"""
        # 簡易版：文字単位のN-gram
        cleaned_text = re.sub(r'[^\w]', '', text)
        return [cleaned_text[i:i+n] for i in range(len(cleaned_text)-n+1)]
    
    def _analyze_character_types(self, text: str) -> Dict[str, float]:
        """文字種別比率分析"""
        total_chars = len(re.sub(r'\s', '', text))
        
        hiragana_count = len(re.findall(r'[ひらがな]', text))
        katakana_count = len(re.findall(r'[ァ-ヶ]', text))
        kanji_count = len(re.findall(r'[一-龯]', text))
        number_count = len(re.findall(r'[0-9]', text))
        alphabet_count = len(re.findall(r'[a-zA-Z]', text))
        
        return {
            "hiragana_ratio": hiragana_count / total_chars if total_chars > 0 else 0,
            "katakana_ratio": katakana_count / total_chars if total_chars > 0 else 0,
            "kanji_ratio": kanji_count / total_chars if total_chars > 0 else 0,
            "number_ratio": number_count / total_chars if total_chars > 0 else 0,
            "alphabet_ratio": alphabet_count / total_chars if total_chars > 0 else 0
        }
    
    def _analyze_rhythm_patterns(self, copies: List[str]) -> Dict[str, Any]:
        """リズム・音韻パターン分析"""
        
        # 句読点パターン
        punctuation_patterns = []
        for copy in copies:
            pattern = re.findall(r'[。、！？…・※]', copy)
            punctuation_patterns.append(''.join(pattern))
        
        # 文末パターン
        ending_patterns = []
        for copy in copies:
            sentences = re.split(r'[。！？]', copy)
            for sentence in sentences:
                if sentence.strip():
                    ending = sentence.strip()[-2:] if len(sentence.strip()) >= 2 else sentence.strip()
                    ending_patterns.append(ending)
        
        # 長文・短文比率
        sentence_lengths = []
        for copy in copies:
            sentences = re.split(r'[。！？]', copy)
            for sentence in sentences:
                if sentence.strip():
                    sentence_lengths.append(len(sentence.strip()))
        
        # リズムタイプ分類
        rhythm_types = self._classify_rhythm_types(copies)
        
        return {
            "punctuation_frequency": Counter(punctuation_patterns),
            "ending_patterns": dict(Counter(ending_patterns).most_common(10)),
            "sentence_length_distribution": {
                "short": len([s for s in sentence_lengths if s <= 15]),
                "medium": len([s for s in sentence_lengths if 16 <= s <= 30]),
                "long": len([s for s in sentence_lengths if s > 30])
            },
            "avg_sentence_length": np.mean(sentence_lengths) if sentence_lengths else 0,
            "rhythm_types": rhythm_types,
            "exclamation_ratio": sum(copy.count('！') for copy in copies) / len(copies),
            "question_ratio": sum(copy.count('？') for copy in copies) / len(copies)
        }
    
    def _classify_rhythm_types(self, copies: List[str]) -> Dict[str, int]:
        """リズムタイプ分類"""
        rhythm_counts = defaultdict(int)
        
        for copy in copies:
            # 体言止め
            if re.search(r'[。！？]$', copy) and not re.search(r'[です|ます|である]', copy[-10:]):
                rhythm_counts["体言止め"] += 1
            
            # 疑問形
            if '？' in copy or re.search(r'[ですか|ますか|でしょうか]', copy):
                rhythm_counts["疑問形"] += 1
            
            # 感嘆形
            if '！' in copy or re.search(r'[だ！|です！|ます！]', copy):
                rhythm_counts["感嘆形"] += 1
            
            # 丁寧語
            if re.search(r'[です|ます]', copy):
                rhythm_counts["丁寧語"] += 1
            
            # 短文連続
            sentences = re.split(r'[。！？]', copy)
            short_sentences = [s for s in sentences if len(s.strip()) <= 10]
            if len(short_sentences) >= 2:
                rhythm_counts["短文連続"] += 1
        
        return dict(rhythm_counts)
    
    def _analyze_syntax_patterns(self, copies: List[str]) -> Dict[str, Any]:
        """構文パターン分析"""
        
        # 文型パターン
        sentence_patterns = []
        modifier_patterns = []
        
        for copy in copies:
            # 修飾語パターン
            modifiers = re.findall(r'[新しい|美しい|素晴らしい|最高の|究極の|革新的な]', copy)
            modifier_patterns.extend(modifiers)
            
            # 文型判定（簡易版）
            if re.search(r'[です|ます]$', copy):
                sentence_patterns.append("丁寧語")
            elif re.search(r'[だ|である]$', copy):
                sentence_patterns.append("断定語")
            elif copy.endswith('。'):
                sentence_patterns.append("普通語")
        
        # 接続詞分析
        conjunctions = re.findall(r'[そして|また|しかし|だから|なので|つまり|例えば]', ' '.join(copies))
        
        # 強調表現
        emphasis_patterns = []
        for copy in copies:
            if re.search(r'[とても|非常に|かなり|絶対に|必ず|きっと]', copy):
                emphasis_patterns.append("程度副詞")
            if '！' in copy:
                emphasis_patterns.append("感嘆符")
            if re.search(r'[〜〜|…|！！]', copy):
                emphasis_patterns.append("記号強調")
        
        return {
            "sentence_patterns": dict(Counter(sentence_patterns)),
            "modifier_frequency": dict(Counter(modifier_patterns)),
            "conjunction_usage": dict(Counter(conjunctions)),
            "emphasis_patterns": dict(Counter(emphasis_patterns)),
            "complex_sentence_ratio": self._calculate_complex_sentence_ratio(copies)
        }
    
    def _calculate_complex_sentence_ratio(self, copies: List[str]) -> float:
        """複文比率計算"""
        complex_count = 0
        total_sentences = 0
        
        for copy in copies:
            sentences = re.split(r'[。！？]', copy)
            for sentence in sentences:
                if sentence.strip():
                    total_sentences += 1
                    # 複文判定（簡易版）
                    if re.search(r'[が、|けれど|ので|から|ため]', sentence):
                        complex_count += 1
        
        return complex_count / total_sentences if total_sentences > 0 else 0
    
    def _analyze_emotional_tone(self, copies: List[str]) -> Dict[str, Any]:
        """感情・トーン分析"""
        
        # 感情語辞書（簡易版）
        positive_words = ['嬉しい', '楽しい', '素晴らしい', '最高', '良い', '美味しい', '快適', '安心']
        negative_words = ['悲しい', '困る', '心配', '不安', '辛い', '苦しい', '悪い', 'ダメ']
        urgency_words = ['今すぐ', '急いで', '限定', '緊急', 'お急ぎ', 'すぐに']
        luxury_words = ['高級', '贅沢', 'プレミアム', '特別', '限定', 'VIP']
        
        emotion_scores = {
            'positive': 0,
            'negative': 0,
            'urgency': 0,
            'luxury': 0
        }
        
        for copy in copies:
            for word in positive_words:
                emotion_scores['positive'] += copy.count(word)
            for word in negative_words:
                emotion_scores['negative'] += copy.count(word)
            for word in urgency_words:
                emotion_scores['urgency'] += copy.count(word)
            for word in luxury_words:
                emotion_scores['luxury'] += copy.count(word)
        
        # トーン分類
        tone_classification = self._classify_tones(copies)
        
        return {
            "emotion_scores": emotion_scores,
            "dominant_emotion": max(emotion_scores.items(), key=lambda x: x[1])[0],
            "tone_classification": tone_classification,
            "emotional_intensity": sum(emotion_scores.values()) / len(copies)
        }
    
    def _classify_tones(self, copies: List[str]) -> Dict[str, int]:
        """トーン分類"""
        tone_counts = defaultdict(int)
        
        for copy in copies:
            copy_lower = copy.lower()
            
            # フォーマル度
            if re.search(r'[いたします|させていただき|ございます]', copy):
                tone_counts["フォーマル"] += 1
            elif re.search(r'[だよ|だね|じゃん]', copy):
                tone_counts["カジュアル"] += 1
            
            # 説得タイプ
            if re.search(r'[証明|実証|データ|研究]', copy):
                tone_counts["論理的"] += 1
            elif re.search(r'[感動|体験|物語]', copy):
                tone_counts["感情的"] += 1
            
            # アプローチ
            if re.search(r'[あなた|お客様|皆様]', copy):
                tone_counts["個人的"] += 1
            elif re.search(r'[社会|世界|未来]', copy):
                tone_counts["社会的"] += 1
        
        return dict(tone_counts)
    
    def _extract_dna_patterns(self, vocab: Dict, rhythm: Dict, syntax: Dict, emotion: Dict) -> Dict[str, Any]:
        """DNAパターン抽出"""
        
        # 語彙DNAパターン
        vocab_dna = {
            "signature_words": list(vocab["top_words"].keys())[:5],
            "vocabulary_richness_level": "高" if vocab["vocabulary_richness"] > 0.7 else "中" if vocab["vocabulary_richness"] > 0.4 else "低",
            "preferred_bigrams": list(vocab["top_bigrams"].keys())[:3]
        }
        
        # リズムDNAパターン
        rhythm_dna = {
            "preferred_sentence_length": "短文" if rhythm["avg_sentence_length"] < 15 else "長文" if rhythm["avg_sentence_length"] > 30 else "中文",
            "dominant_rhythm": max(rhythm["rhythm_types"].items(), key=lambda x: x[1])[0] if rhythm["rhythm_types"] else "標準",
            "punctuation_style": "感嘆多用" if rhythm["exclamation_ratio"] > 0.5 else "疑問多用" if rhythm["question_ratio"] > 0.3 else "標準"
        }
        
        # 構文DNAパターン
        syntax_dna = {
            "sentence_style": max(syntax["sentence_patterns"].items(), key=lambda x: x[1])[0] if syntax["sentence_patterns"] else "標準",
            "complexity_level": "高" if syntax["complex_sentence_ratio"] > 0.6 else "低" if syntax["complex_sentence_ratio"] < 0.3 else "中",
            "emphasis_preference": max(syntax["emphasis_patterns"].items(), key=lambda x: x[1])[0] if syntax["emphasis_patterns"] else "なし"
        }
        
        # 感情DNAパターン
        emotion_dna = {
            "emotional_tendency": emotion["dominant_emotion"],
            "intensity_level": "高" if emotion["emotional_intensity"] > 2 else "低" if emotion["emotional_intensity"] < 0.5 else "中",
            "tone_preference": max(emotion["tone_classification"].items(), key=lambda x: x[1])[0] if emotion["tone_classification"] else "ニュートラル"
        }
        
        # 統合DNAプロファイル
        dna_profile = f"{vocab_dna['vocabulary_richness_level']}語彙×{rhythm_dna['preferred_sentence_length']}×{emotion_dna['emotional_tendency']}トーン"
        
        return {
            "vocabulary_dna": vocab_dna,
            "rhythm_dna": rhythm_dna,
            "syntax_dna": syntax_dna,
            "emotion_dna": emotion_dna,
            "integrated_dna_profile": dna_profile
        }
    
    def _generate_insights(self, basic_stats: Dict, vocab: Dict, dna: Dict) -> List[str]:
        """洞察生成"""
        insights = []
        
        # 基本統計洞察
        avg_chars = basic_stats["character_stats"]["avg"]
        if avg_chars < 20:
            insights.append("短文主体のコンパクトなコピー")
        elif avg_chars > 50:
            insights.append("長文での詳細説明型コピー")
        
        # 語彙洞察
        if vocab["vocabulary_richness"] > 0.7:
            insights.append("語彙の多様性が高く表現豊か")
        elif vocab["vocabulary_richness"] < 0.3:
            insights.append("シンプルな語彙で統一感を重視")
        
        # DNAパターン洞察
        dna_profile = dna["integrated_dna_profile"]
        insights.append(f"DNAプロファイル: {dna_profile}")
        
        # 強みと特徴
        if dna["emotion_dna"]["emotional_tendency"] == "positive":
            insights.append("ポジティブ感情でのブランディング重視")
        
        if dna["rhythm_dna"]["dominant_rhythm"] == "体言止め":
            insights.append("体言止めによるインパクト重視")
        
        return insights
    
    def save_results(self, result: Dict[str, Any]) -> None:
        """結果保存"""
        # JSON保存
        json_path = os.path.join(self.output_dir, "copy_dna_analysis_result.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"💾 結果保存: {json_path}")
        
        # CSV保存（語彙頻度）
        if result.get("success") and "vocabulary_analysis" in result:
            vocab_df = pd.DataFrame(list(result["vocabulary_analysis"]["top_words"].items()), 
                                  columns=["Word", "Frequency"])
            csv_path = os.path.join(self.output_dir, "vocabulary_frequency.csv")
            vocab_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"📊 語彙頻度CSV保存: {csv_path}")
        
        # 可視化グラフ保存
        if result.get("success"):
            self._save_visualization(result)
    
    def _save_visualization(self, result: Dict[str, Any]) -> None:
        """可視化グラフ生成・保存"""
        try:
            plt.style.use('default')
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
            
            # 1. 語彙頻度グラフ
            vocab_data = result["vocabulary_analysis"]["top_words"]
            words = list(vocab_data.keys())[:10]
            freqs = list(vocab_data.values())[:10]
            
            ax1.bar(words, freqs)
            ax1.set_title("Top 10 語彙頻度")
            ax1.set_ylabel("頻度")
            ax1.tick_params(axis='x', rotation=45)
            
            # 2. 文字種別比率
            char_ratio = result["vocabulary_analysis"]["character_type_ratio"]
            ax2.pie(char_ratio.values(), labels=char_ratio.keys(), autopct='%1.1f%%')
            ax2.set_title("文字種別比率")
            
            # 3. リズムパターン
            rhythm_types = result["rhythm_analysis"]["rhythm_types"]
            if rhythm_types:
                ax3.bar(rhythm_types.keys(), rhythm_types.values())
                ax3.set_title("リズムパターン分布")
                ax3.set_ylabel("出現回数")
                ax3.tick_params(axis='x', rotation=45)
            
            # 4. 感情スコア
            emotion_scores = result["emotion_analysis"]["emotion_scores"]
            ax4.bar(emotion_scores.keys(), emotion_scores.values())
            ax4.set_title("感情スコア分布")
            ax4.set_ylabel("スコア")
            
            plt.tight_layout()
            
            chart_path = os.path.join(self.output_dir, "copy_dna_analysis_chart.png")
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"📈 グラフ保存: {chart_path}")
            
        except Exception as e:
            print(f"⚠️  グラフ生成エラー: {str(e)}")
    
    def print_summary(self, result: Dict[str, Any]) -> None:
        """結果サマリー表示"""
        if not result.get("success"):
            print(f"\n❌ 実行失敗: {result.get('framework_info', {}).get('error', 'Unknown error')}")
            return
        
        print(f"\n📋 {self.framework_name} 実行結果サマリー")
        print("=" * 50)
        
        # 基本情報
        print(f"🎯 分析対象: {result['input_parameters']['brand_name']}")
        print(f"📝 コピー数: {result['input_parameters']['copy_count']}件")
        print(f"⏱️  実行時間: {result['framework_info']['execution_time']:.2f}秒")
        
        # DNAプロファイル
        dna = result["dna_patterns"]
        print(f"\n🧬 DNAプロファイル: {dna['integrated_dna_profile']}")
        
        # 語彙特徴
        vocab = result["vocabulary_analysis"]
        print(f"\n📚 語彙特徴:")
        print(f"  語彙数: {vocab['vocabulary_size']}語")
        print(f"  語彙豊富度: {vocab['vocabulary_richness']:.2f}")
        print(f"  頻出語: {', '.join(list(vocab['top_words'].keys())[:5])}")
        
        # リズム特徴
        rhythm = result["rhythm_analysis"]
        print(f"\n🎵 リズム特徴:")
        print(f"  平均文長: {rhythm['avg_sentence_length']:.1f}文字")
        print(f"  感嘆符比率: {rhythm['exclamation_ratio']:.2f}")
        dominant_rhythm = max(rhythm['rhythm_types'].items(), key=lambda x: x[1])[0] if rhythm['rhythm_types'] else "標準"
        print(f"  主要リズム: {dominant_rhythm}")
        
        # 感情特徴
        emotion = result["emotion_analysis"]
        print(f"\n😊 感情特徴:")
        print(f"  主要感情: {emotion['dominant_emotion']}")
        print(f"  感情強度: {emotion['emotional_intensity']:.2f}")
        
        # 洞察
        print(f"\n💡 主要洞察:")
        for insight in result["insights"]:
            print(f"  • {insight}")
        
        print(f"\n📁 詳細結果は {self.output_dir} フォルダに保存されました")

# サンプルデータ
SAMPLE_DATA = {
    "copy_samples": [
        "新しい朝が始まる。一杯のコーヒーから。",
        "美味しさに、こだわり続けて50年。",
        "あなたの毎日を、もっと素晴らしく！",
        "今すぐ体験してください。この感動を。",
        "健康で美しい肌へ。自然の力で。",
        "限定発売！プレミアムな味わいを。",
        "家族みんなで楽しめる、安心の品質。",
        "革新的な技術が、未来を変える。"
    ],
    "brand_name": "サンプルブランド"
}

async def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(description="Copy DNA Audit 分析フレームワーク")
    parser.add_argument("--brand", default=SAMPLE_DATA["brand_name"], help="ブランド名")
    parser.add_argument("--file", help="コピーリストが含まれるテキストファイル")
    parser.add_argument("--config", help="設定JSONファイルパス")
    
    args = parser.parse_args()
    
    # 設定ファイル読み込み
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        copy_samples = config.get("copy_samples", SAMPLE_DATA["copy_samples"])
        brand_name = config.get("brand_name", args.brand)
    elif args.file and os.path.exists(args.file):
        with open(args.file, 'r', encoding='utf-8') as f:
            copy_samples = [line.strip() for line in f.readlines() if line.strip()]
        brand_name = args.brand
    else:
        copy_samples = SAMPLE_DATA["copy_samples"]
        brand_name = args.brand
        print("🔧 サンプルデータを使用して実行します")
    
    # フレームワーク実行
    framework = CopyDNAFramework()
    result = await framework.collect_data(copy_samples, brand_name)
    
    # 結果保存・表示
    framework.save_results(result)
    framework.print_summary(result)

if __name__ == "__main__":
    asyncio.run(main()) 