#!/usr/bin/env python3
"""
Framework 12: Copy DNA Audit (コピーライティング語彙・リズム・構文分析)
Creative Frameworks Component

実行方法: 
  python src/framework_12_copy_dna.py
  
独立コンポーネントとして動作します。
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
    
    def __init__(self, output_base_dir: str = "output"):
        self.framework_id = 12
        self.framework_name = "Copy DNA Audit"
        self.version = "1.0.0"
        self.component_name = "framework-creative"
        
        # 出力ディレクトリをコンポーネント内に設定
        self.output_dir = os.path.join(
            output_base_dir, 
            f"framework_12_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        # 出力ディレクトリ作成
        os.makedirs(self.output_dir, exist_ok=True)
        
        print(f"🚀 {self.framework_name} v{self.version}")
        print(f"📦 Component: {self.component_name}")
        print(f"📁 Output: {self.output_dir}")
        
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
                    "component": self.component_name,
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
                    "component": self.component_name,
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
        
        if total_chars == 0:
            return {"hiragana": 0, "katakana": 0, "kanji": 0, "other": 0}
        
        return {
            "hiragana": hiragana_count / total_chars,
            "katakana": katakana_count / total_chars,
            "kanji": kanji_count / total_chars,
            "other": (total_chars - hiragana_count - katakana_count - kanji_count) / total_chars
        }
    
    def _analyze_rhythm_patterns(self, copies: List[str]) -> Dict[str, Any]:
        """リズム・音韻分析"""
        
        # 音節数分析
        syllable_counts = []
        punctuation_frequencies = []
        
        for copy in copies:
            # 簡易音節カウント（ひらがな・カタカナ1文字 = 1音節）
            syllables = len(re.findall(r'[ひらがなァ-ヶ]', copy))
            syllable_counts.append(syllables)
            
            # 句読点頻度
            punct_count = len(re.findall(r'[。、！？…・※]', copy))
            punctuation_frequencies.append(punct_count)
        
        # リズムパターン分類
        rhythm_types = self._classify_rhythm_types(copies)
        
        # 音韻特徴
        alliteration_score = self._calculate_alliteration_score(copies)
        
        return {
            "syllable_stats": {
                "avg": np.mean(syllable_counts) if syllable_counts else 0,
                "median": np.median(syllable_counts) if syllable_counts else 0,
                "std": np.std(syllable_counts) if syllable_counts else 0
            },
            "punctuation_frequency": {
                "avg": np.mean(punctuation_frequencies) if punctuation_frequencies else 0,
                "total": sum(punctuation_frequencies)
            },
            "rhythm_types": rhythm_types,
            "alliteration_score": alliteration_score,
            "tempo_classification": self._classify_tempo(syllable_counts, punctuation_frequencies)
        }
    
    def _classify_rhythm_types(self, copies: List[str]) -> Dict[str, int]:
        """リズムタイプ分類"""
        rhythm_counts = {"short_burst": 0, "medium_flow": 0, "long_narrative": 0}
        
        for copy in copies:
            char_count = len(copy)
            if char_count <= 20:
                rhythm_counts["short_burst"] += 1
            elif char_count <= 50:
                rhythm_counts["medium_flow"] += 1
            else:
                rhythm_counts["long_narrative"] += 1
        
        return rhythm_counts
    
    def _calculate_alliteration_score(self, copies: List[str]) -> float:
        """頭韻スコア計算"""
        # 簡易版：隣接する単語の最初の文字が同じ場合をカウント
        total_score = 0
        total_pairs = 0
        
        for copy in copies:
            words = re.findall(r'[ひらがなァ-ヶ一-龯]+', copy)
            for i in range(len(words) - 1):
                if len(words[i]) > 0 and len(words[i + 1]) > 0:
                    if words[i][0] == words[i + 1][0]:
                        total_score += 1
                    total_pairs += 1
        
        return total_score / total_pairs if total_pairs > 0 else 0
    
    def _classify_tempo(self, syllable_counts: List[int], punct_counts: List[int]) -> str:
        """テンポ分類"""
        if not syllable_counts:
            return "unknown"
        
        avg_syllables = np.mean(syllable_counts)
        avg_punct = np.mean(punct_counts)
        
        if avg_syllables < 10 and avg_punct > 1:
            return "staccato"  # 短く切れ味のあるテンポ
        elif avg_syllables > 30 and avg_punct < 2:
            return "legato"    # 流れるようなテンポ
        else:
            return "moderato"  # 中庸なテンポ
    
    def _analyze_syntax_patterns(self, copies: List[str]) -> Dict[str, Any]:
        """構文パターン分析"""
        
        # 文の長さ分析
        sentence_lengths = []
        question_count = 0
        exclamation_count = 0
        
        for copy in copies:
            sentences = re.split(r'[。！？]', copy)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            for sentence in sentences:
                sentence_lengths.append(len(sentence))
            
            question_count += copy.count('？')
            exclamation_count += copy.count('！')
        
        # 修辞技法検出
        rhetorical_devices = self._detect_rhetorical_devices(copies)
        
        # 複文比率
        complex_sentence_ratio = self._calculate_complex_sentence_ratio(copies)
        
        return {
            "sentence_length_stats": {
                "avg": np.mean(sentence_lengths) if sentence_lengths else 0,
                "median": np.median(sentence_lengths) if sentence_lengths else 0,
                "std": np.std(sentence_lengths) if sentence_lengths else 0
            },
            "question_ratio": question_count / len(copies) if copies else 0,
            "exclamation_ratio": exclamation_count / len(copies) if copies else 0,
            "rhetorical_devices": rhetorical_devices,
            "complex_sentence_ratio": complex_sentence_ratio,
            "syntax_variety_score": len(set(sentence_lengths)) / len(sentence_lengths) if sentence_lengths else 0
        }
    
    def _detect_rhetorical_devices(self, copies: List[str]) -> Dict[str, int]:
        """修辞技法検出"""
        devices = {
            "repetition": 0,      # 反復
            "parallelism": 0,     # 並列
            "contrast": 0,        # 対比
            "metaphor": 0         # 比喩
        }
        
        for copy in copies:
            # 簡易検出
            words = re.findall(r'[ひらがなァ-ヶ一-龯]+', copy)
            word_freq = Counter(words)
            
            # 反復検出（同じ語が2回以上出現）
            repeated_words = [word for word, freq in word_freq.items() if freq >= 2]
            devices["repetition"] += len(repeated_words)
            
            # 対比表現検出
            contrast_patterns = ['しかし', 'でも', 'だが', 'ところが', 'けれど']
            for pattern in contrast_patterns:
                if pattern in copy:
                    devices["contrast"] += 1
                    break
        
        return devices
    
    def _calculate_complex_sentence_ratio(self, copies: List[str]) -> float:
        """複文比率計算"""
        total_sentences = 0
        complex_sentences = 0
        
        complex_indicators = ['が', 'ので', 'から', 'けれど', 'ものの', 'ため']
        
        for copy in copies:
            sentences = re.split(r'[。！？]', copy)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            for sentence in sentences:
                total_sentences += 1
                for indicator in complex_indicators:
                    if indicator in sentence:
                        complex_sentences += 1
                        break
        
        return complex_sentences / total_sentences if total_sentences > 0 else 0
    
    def _analyze_emotional_tone(self, copies: List[str]) -> Dict[str, Any]:
        """感情・トーン分析"""
        
        # 感情語辞書（簡易版）
        emotion_words = {
            "positive": ["嬉しい", "楽しい", "素晴らしい", "最高", "良い", "美しい", "新しい", "快適"],
            "negative": ["悲しい", "苦しい", "困る", "悪い", "嫌", "古い", "不快"],
            "neutral": ["普通", "まあまあ", "そこそこ", "一般的"]
        }
        
        emotion_scores = {"positive": 0, "negative": 0, "neutral": 0}
        urgency_indicators = 0
        
        for copy in copies:
            # 感情語カウント
            for emotion_type, words in emotion_words.items():
                for word in words:
                    emotion_scores[emotion_type] += copy.count(word)
            
            # 緊急性指標
            urgency_patterns = ['今すぐ', 'すぐに', '急いで', '限定', '今だけ', 'お早めに']
            for pattern in urgency_patterns:
                if pattern in copy:
                    urgency_indicators += 1
        
        # トーン分類
        tone_classification = self._classify_tones(copies)
        
        total_emotion_words = sum(emotion_scores.values())
        emotion_ratios = {
            emotion: count / total_emotion_words if total_emotion_words > 0 else 0
            for emotion, count in emotion_scores.items()
        }
        
        return {
            "emotion_scores": emotion_scores,
            "emotion_ratios": emotion_ratios,
            "urgency_score": urgency_indicators / len(copies) if copies else 0,
            "tone_classification": tone_classification,
            "dominant_emotion": max(emotion_ratios.items(), key=lambda x: x[1])[0] if emotion_ratios else "neutral"
        }
    
    def _classify_tones(self, copies: List[str]) -> Dict[str, int]:
        """トーン分類"""
        tones = {
            "formal": 0,      # 丁寧・フォーマル
            "casual": 0,      # カジュアル
            "urgent": 0,      # 緊急・切迫
            "friendly": 0,    # 親しみやすい
            "professional": 0 # プロフェッショナル
        }
        
        for copy in copies:
            # 簡易分類
            if any(pattern in copy for pattern in ['です', 'ます', 'ございます']):
                tones["formal"] += 1
            
            if any(pattern in copy for pattern in ['だよ', 'だね', 'じゃん', 'でしょ']):
                tones["casual"] += 1
            
            if any(pattern in copy for pattern in ['今すぐ', '急いで', '限定', 'お早めに']):
                tones["urgent"] += 1
            
            if any(pattern in copy for pattern in ['一緒に', 'みんなで', 'あなたと']):
                tones["friendly"] += 1
            
            if any(pattern in copy for pattern in ['効果的', '最適', '実証済み', '専門']):
                tones["professional"] += 1
        
        return tones
    
    def _extract_dna_patterns(self, vocab: Dict, rhythm: Dict, syntax: Dict, emotion: Dict) -> Dict[str, Any]:
        """DNAパターン抽出"""
        
        # 語彙特性
        vocab_profile = "rich" if vocab["vocabulary_richness"] > 0.7 else \
                       "moderate" if vocab["vocabulary_richness"] > 0.4 else "simple"
        
        # リズム特性
        rhythm_profile = rhythm["tempo_classification"]
        
        # 構文特性
        syntax_profile = "complex" if syntax["complex_sentence_ratio"] > 0.5 else \
                        "mixed" if syntax["complex_sentence_ratio"] > 0.2 else "simple"
        
        # 感情特性
        emotion_profile = emotion["dominant_emotion"]
        
        # 全体的なDNAプロファイル
        dna_signature = f"{vocab_profile}_{rhythm_profile}_{syntax_profile}_{emotion_profile}"
        
        # 特徴ベクトル
        feature_vector = {
            "vocabulary_richness": vocab["vocabulary_richness"],
            "rhythm_tempo": rhythm["syllable_stats"]["avg"],
            "syntax_complexity": syntax["complex_sentence_ratio"],
            "emotion_intensity": max(emotion["emotion_ratios"].values()) if emotion["emotion_ratios"] else 0,
            "urgency_level": emotion["urgency_score"]
        }
        
        # パターン強度スコア
        pattern_strength = {
            "consistency": self._calculate_consistency_score(vocab, rhythm, syntax),
            "distinctiveness": self._calculate_distinctiveness_score(feature_vector),
            "memorability": self._calculate_memorability_score(rhythm, emotion)
        }
        
        return {
            "dna_signature": dna_signature,
            "profiles": {
                "vocabulary": vocab_profile,
                "rhythm": rhythm_profile,
                "syntax": syntax_profile,
                "emotion": emotion_profile
            },
            "feature_vector": feature_vector,
            "pattern_strength": pattern_strength,
            "uniqueness_score": np.mean(list(pattern_strength.values()))
        }
    
    def _calculate_consistency_score(self, vocab: Dict, rhythm: Dict, syntax: Dict) -> float:
        """一貫性スコア計算"""
        # 各指標の変動係数の逆数で一貫性を測定
        cv_vocab = vocab.get("vocabulary_richness", 0)
        cv_rhythm = rhythm["syllable_stats"].get("std", 0) / max(rhythm["syllable_stats"].get("avg", 1), 1)
        cv_syntax = syntax["sentence_length_stats"].get("std", 0) / max(syntax["sentence_length_stats"].get("avg", 1), 1)
        
        avg_cv = (cv_vocab + cv_rhythm + cv_syntax) / 3
        return max(0, 1 - avg_cv)  # CVが小さいほど一貫性が高い
    
    def _calculate_distinctiveness_score(self, feature_vector: Dict) -> float:
        """特徴性スコア計算"""
        # 特徴ベクトルの分散で特徴性を測定
        values = list(feature_vector.values())
        return float(np.std(values)) if values else 0
    
    def _calculate_memorability_score(self, rhythm: Dict, emotion: Dict) -> float:
        """記憶容易性スコア計算"""
        # リズムの特徴性と感情強度で記憶容易性を測定
        rhythm_score = rhythm.get("alliteration_score", 0)
        emotion_score = max(emotion["emotion_ratios"].values()) if emotion["emotion_ratios"] else 0
        return (rhythm_score + emotion_score) / 2
    
    def _generate_insights(self, basic_stats: Dict, vocab: Dict, dna: Dict) -> List[str]:
        """インサイト生成"""
        insights = []
        
        # 基本統計からのインサイト
        avg_chars = basic_stats["character_stats"]["avg"]
        if avg_chars < 20:
            insights.append("短文中心の構成で、瞬間的なインパクトを重視している")
        elif avg_chars > 50:
            insights.append("長文構成で、詳細な説明や物語性を重視している")
        
        # 語彙からのインサイト
        vocab_richness = vocab["vocabulary_richness"]
        if vocab_richness > 0.7:
            insights.append("語彙が豊富で、表現力に富んだコピーライティング")
        elif vocab_richness < 0.3:
            insights.append("シンプルな語彙で、分かりやすさを重視したコピーライティング")
        
        # DNAプロファイルからのインサイト
        dna_signature = dna["dna_signature"]
        uniqueness = dna["uniqueness_score"]
        
        if uniqueness > 0.7:
            insights.append(f"独特なコピーDNA ({dna_signature}) を持ち、強い個性を表現している")
        elif uniqueness < 0.3:
            insights.append("標準的なコピー構造で、安定性と親しみやすさを重視している")
        
        # パターン強度からのインサイト
        consistency = dna["pattern_strength"]["consistency"]
        if consistency > 0.8:
            insights.append("高い一貫性を持ち、ブランドアイデンティティが明確")
        
        distinctiveness = dna["pattern_strength"]["distinctiveness"]
        if distinctiveness > 0.6:
            insights.append("際立った特徴を持ち、競合との差別化が図られている")
        
        return insights[:5]  # 最大5つのインサイト
    
    def save_results(self, result: Dict[str, Any]) -> None:
        """結果保存"""
        try:
            # JSON詳細結果
            json_path = os.path.join(self.output_dir, "copy_dna_analysis_result.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2, default=str)
            
            # CSV要約結果
            csv_path = os.path.join(self.output_dir, "vocabulary_frequency.csv")
            if result["success"] and "vocabulary_analysis" in result:
                vocab_data = result["vocabulary_analysis"]["top_words"]
                df = pd.DataFrame(list(vocab_data.items()), columns=["Word", "Frequency"])
                df.to_csv(csv_path, index=False, encoding='utf-8')
            
            # 可視化
            self._save_visualization(result)
            
            print(f"📄 詳細結果: {json_path}")
            print(f"📊 語彙頻度: {csv_path}")
            
        except Exception as e:
            print(f"❌ 保存エラー: {str(e)}")
    
    def _save_visualization(self, result: Dict[str, Any]) -> None:
        """可視化結果保存"""
        if not result["success"]:
            return
        
        try:
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            
            # 1. 語彙頻度
            vocab_data = result["vocabulary_analysis"]["top_words"]
            if vocab_data:
                words = list(vocab_data.keys())[:10]
                freqs = list(vocab_data.values())[:10]
                axes[0, 0].barh(words, freqs)
                axes[0, 0].set_title("Top 10 語彙頻度")
                axes[0, 0].set_xlabel("頻度")
            
            # 2. 文字種別比率
            char_ratios = result["vocabulary_analysis"]["character_type_ratio"]
            if char_ratios:
                labels = list(char_ratios.keys())
                sizes = list(char_ratios.values())
                axes[0, 1].pie(sizes, labels=labels, autopct='%1.1f%%')
                axes[0, 1].set_title("文字種別比率")
            
            # 3. トーン分析
            tone_data = result["emotion_analysis"]["tone_classification"]
            if tone_data:
                tones = list(tone_data.keys())
                counts = list(tone_data.values())
                axes[1, 0].bar(tones, counts)
                axes[1, 0].set_title("トーン分類")
                axes[1, 0].set_ylabel("出現回数")
                axes[1, 0].tick_params(axis='x', rotation=45)
            
            # 4. DNA特徴ベクトル
            feature_vector = result["dna_patterns"]["feature_vector"]
            if feature_vector:
                features = list(feature_vector.keys())
                values = list(feature_vector.values())
                axes[1, 1].radar_chart_alternative(features, values)
                axes[1, 1].set_title("DNA特徴ベクトル")
            
            plt.tight_layout()
            chart_path = os.path.join(self.output_dir, "copy_dna_analysis_chart.png")
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"📈 可視化結果: {chart_path}")
            
        except Exception as e:
            print(f"⚠️ 可視化エラー: {str(e)}")
    
    def print_summary(self, result: Dict[str, Any]) -> None:
        """結果サマリー表示"""
        if not result["success"]:
            print(f"❌ 分析失敗: {result.get('framework_info', {}).get('error', 'Unknown error')}")
            return
        
        print(f"\n{'='*60}")
        print(f"🧬 Copy DNA Analysis Summary")
        print(f"{'='*60}")
        
        # フレームワーク情報
        fw_info = result["framework_info"]
        print(f"📦 Component: {fw_info['component']}")
        print(f"⏱️  実行時間: {fw_info['execution_time']:.2f}秒")
        print(f"📅 実行日時: {fw_info['timestamp']}")
        
        # 基本統計
        basic_stats = result["basic_statistics"]
        print(f"\n📊 基本統計:")
        print(f"  • 分析コピー数: {basic_stats['total_copies']}件")
        print(f"  • 平均文字数: {basic_stats['character_stats']['avg']:.1f}文字")
        print(f"  • 平均文数: {basic_stats['sentence_stats']['avg']:.1f}文")
        
        # 語彙分析
        vocab = result["vocabulary_analysis"]
        print(f"\n🔤 語彙分析:")
        print(f"  • 語彙サイズ: {vocab['vocabulary_size']}語")
        print(f"  • 語彙豊富度: {vocab['vocabulary_richness']:.3f}")
        
        # DNAパターン
        dna = result["dna_patterns"]
        print(f"\n🧬 DNAパターン:")
        print(f"  • DNA署名: {dna['dna_signature']}")
        print(f"  • 独自性スコア: {dna['uniqueness_score']:.3f}")
        
        profiles = dna['profiles']
        print(f"  • 語彙プロファイル: {profiles['vocabulary']}")
        print(f"  • リズムプロファイル: {profiles['rhythm']}")
        print(f"  • 構文プロファイル: {profiles['syntax']}")
        print(f"  • 感情プロファイル: {profiles['emotion']}")
        
        # インサイト
        insights = result["insights"]
        print(f"\n💡 主要インサイト:")
        for i, insight in enumerate(insights, 1):
            print(f"  {i}. {insight}")
        
        print(f"\n📁 詳細結果は {self.output_dir} に保存されました")

# サンプルデータ
SAMPLE_COPY_DATA = [
    "新しい朝は、新しいコーヒーから始まる。",
    "今すぐ体験する、プレミアムな味わい。",
    "あなたの毎日を、もっと豊かに。特別な一杯で。",
    "限定ブレンド、今だけの特別価格でお届けします。",
    "香り高いコーヒーで、素晴らしい一日をスタート。",
    "こだわりの豆が生み出す、極上の味わい。",
    "忙しい朝にも、ほっと一息つける時間を。",
    "世界最高峰の農園から、直接お届けする味。"
]

async def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(description='Copy DNA Audit Framework')
    parser.add_argument('--brand', type=str, default='Sample Brand', help='ブランド名')
    parser.add_argument('--output', type=str, default='output', help='出力ディレクトリ')
    parser.add_argument('--copies', nargs='+', help='分析するコピーのリスト')
    
    args = parser.parse_args()
    
    # フレームワーク初期化
    framework = CopyDNAFramework(output_base_dir=args.output)
    
    # 分析データ準備
    copy_samples = args.copies if args.copies else SAMPLE_COPY_DATA
    
    print(f"🎯 ブランド: {args.brand}")
    print(f"📝 分析対象: {len(copy_samples)}件のコピー")
    
    # 分析実行
    result = await framework.collect_data(copy_samples, args.brand)
    
    # 結果保存
    framework.save_results(result)
    
    # サマリー表示
    framework.print_summary(result)

if __name__ == "__main__":
    asyncio.run(main()) 