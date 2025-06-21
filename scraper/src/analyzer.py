"""International study analyzer module."""

import re
from typing import List, Dict, Tuple
from collections import defaultdict
from loguru import logger

from .config import ScraperConfig, SCORING_WEIGHTS, INTERNATIONAL_THRESHOLD
from .models import ResearchStudy, InternationalAnalysis, InternationalType


class InternationalAnalyzer:
    """Analyzer for identifying international research studies."""
    
    def __init__(self, config: ScraperConfig):
        self.config = config
        self.keywords = config.international_keywords
        self.exclusions = config.exclusion_patterns
        
    def analyze(self, study: ResearchStudy) -> InternationalAnalysis:
        """Analyze a study for international indicators."""
        analysis = InternationalAnalysis(
            study_id=study.study_id,
            is_international=False,
            primary_type=InternationalType.NONE
        )
        
        # Combine all text fields
        full_text = self._get_full_text(study)
        
        # Check exclusions first
        if self._is_excluded(full_text):
            logger.debug(f"Study {study.study_id} excluded due to exclusion patterns")
            return analysis
        
        # Perform various analyses
        scores = defaultdict(float)
        
        # 1. Keyword matching
        keyword_results = self._match_keywords(full_text)
        scores["keyword_matching"] = keyword_results[0]
        analysis.keyword_matches = keyword_results[1]
        
        # 2. Context analysis
        context_results = self._analyze_context(full_text, keyword_results[1])
        scores["context_relevance"] = context_results[0]
        analysis.context_snippets = context_results[1]
        
        # 3. Program identification
        program_score = self._identify_programs(full_text)
        scores["program_identification"] = program_score
        
        # 4. Multi-country detection
        countries = self._detect_countries(full_text)
        if len(countries) > 1:
            scores["multi_country"] = SCORING_WEIGHTS["multiple_countries"]
            study.countries = countries
        
        # 5. Language support detection
        languages = self._detect_languages(full_text)
        if len(languages) > 1:
            scores["multilingual"] = SCORING_WEIGHTS["multilingual"]
            study.languages_supported = languages
            study.translation_provided = self._check_translation_support(full_text)
        
        # 6. Regulatory analysis
        regulatory_score = self._analyze_regulatory(full_text)
        scores["regulatory"] = regulatory_score
        
        # Calculate total score
        total_score = sum(scores.values())
        analysis.scores = dict(scores)
        analysis.total_score = total_score
        
        # Determine if international
        analysis.is_international = total_score >= INTERNATIONAL_THRESHOLD
        
        # Classify type
        if analysis.is_international:
            analysis.primary_type = self._determine_primary_type(scores, full_text)
            analysis.secondary_types = self._determine_secondary_types(scores, full_text)
        
        # Calculate confidence
        analysis.confidence = self._calculate_confidence(scores, analysis.keyword_matches)
        
        # Add recommendations
        self._add_recommendations(analysis, full_text, languages)
        
        logger.info(f"Study {study.study_id} analyzed: "
                   f"international={analysis.is_international}, "
                   f"score={total_score:.2f}, "
                   f"type={analysis.primary_type}")
        
        return analysis
    
    def _get_full_text(self, study: ResearchStudy) -> str:
        """Combine all text fields for analysis."""
        text_fields = [
            study.title,
            study.title_en or "",
            study.description,
            study.brief_summary or "",
            study.eligibility_criteria or "",
            " ".join(study.keywords),
            " ".join(study.conditions),
            " ".join(study.interventions)
        ]
        
        return " ".join(text_fields).lower()
    
    def _is_excluded(self, text: str) -> bool:
        """Check if study should be excluded."""
        for pattern in self.exclusions:
            if pattern.lower() in text:
                return True
        return False
    
    def _match_keywords(self, text: str) -> Tuple[float, List[str]]:
        """Match international keywords and calculate score."""
        matches = []
        score = 0.0
        
        for keyword in self.keywords:
            if keyword.lower() in text:
                matches.append(keyword)
                
                # Higher score for explicit mentions
                if keyword in ["外国人被験者", "foreign participants"]:
                    score += SCORING_WEIGHTS["explicit_mention"]
                elif keyword in ["ASPIRE", "e-ASIA", "SICORP"]:
                    score += SCORING_WEIGHTS["international_program"]
                else:
                    score += SCORING_WEIGHTS["implicit_international"]
        
        return score, matches
    
    def _analyze_context(self, text: str, keywords: List[str]) -> Tuple[float, List[str]]:
        """Analyze context around matched keywords."""
        snippets = []
        relevance_score = 0.0
        
        # Create regex pattern for keywords
        if not keywords:
            return 0.0, []
        
        pattern = "|".join(re.escape(kw.lower()) for kw in keywords)
        
        # Find context windows (±50 characters)
        for match in re.finditer(pattern, text):
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            snippet = text[start:end]
            
            # Check if context indicates actual international participation
            positive_contexts = [
                "募集", "参加", "対象", "被験者", "患者",
                "recruit", "participant", "eligible", "subject", "patient"
            ]
            
            if any(ctx in snippet for ctx in positive_contexts):
                relevance_score += 1.0
                snippets.append(f"...{snippet}...")
        
        # Normalize score
        if len(keywords) > 0:
            relevance_score = (relevance_score / len(keywords)) * 3.0
        
        return relevance_score, snippets[:5]  # Limit to 5 snippets
    
    def _identify_programs(self, text: str) -> float:
        """Identify known international research programs."""
        programs = {
            "aspire": SCORING_WEIGHTS["international_program"],
            "e-asia": SCORING_WEIGHTS["international_program"],
            "sicorp": SCORING_WEIGHTS["international_program"],
            "interstellar": SCORING_WEIGHTS["international_program"],
            "horizon": SCORING_WEIGHTS["international_program"] * 0.8,
            "erasmus": SCORING_WEIGHTS["international_program"] * 0.8
        }
        
        total_score = 0.0
        for program, score in programs.items():
            if program in text:
                total_score = max(total_score, score)  # Take highest score
        
        return total_score
    
    def _detect_countries(self, text: str) -> List[str]:
        """Detect mentioned countries."""
        countries = []
        
        # Country patterns
        country_patterns = {
            "日本": "Japan",
            "アメリカ": "USA",
            "米国": "USA",
            "カナダ": "Canada",
            "イギリス": "UK",
            "英国": "UK",
            "ドイツ": "Germany",
            "フランス": "France",
            "中国": "China",
            "韓国": "South Korea",
            "インド": "India",
            "オーストラリア": "Australia",
            "シンガポール": "Singapore",
            "タイ": "Thailand",
            "ベトナム": "Vietnam"
        }
        
        for jp_name, en_name in country_patterns.items():
            if jp_name in text or en_name.lower() in text:
                if en_name not in countries:
                    countries.append(en_name)
        
        return countries
    
    def _detect_languages(self, text: str) -> List[str]:
        """Detect supported languages."""
        languages = []
        
        language_patterns = {
            "日本語": "Japanese",
            "英語": "English",
            "中国語": "Chinese",
            "韓国語": "Korean",
            "スペイン語": "Spanish",
            "フランス語": "French",
            "ドイツ語": "German",
            "ポルトガル語": "Portuguese",
            "タイ語": "Thai",
            "ベトナム語": "Vietnamese"
        }
        
        for jp_name, en_name in language_patterns.items():
            if jp_name in text or en_name.lower() in text:
                if en_name not in languages:
                    languages.append(en_name)
        
        # Check for general multilingual mentions
        if "多言語" in text or "multilingual" in text:
            if "Multiple" not in languages:
                languages.append("Multiple")
        
        return languages
    
    def _check_translation_support(self, text: str) -> bool:
        """Check if translation support is mentioned."""
        translation_indicators = [
            "翻訳", "通訳", "translation", "interpreter",
            "言語サポート", "language support"
        ]
        
        return any(indicator in text for indicator in translation_indicators)
    
    def _analyze_regulatory(self, text: str) -> float:
        """Analyze regulatory aspects."""
        regulatory_bodies = {
            "fda": 1.0,
            "ema": 1.0,
            "pmda": 0.5,  # Lower score as it's Japan's own
            "nmpa": 1.0,
            "mhra": 1.0,
            "anvisa": 1.0
        }
        
        count = 0
        for body in regulatory_bodies.keys():
            if body in text:
                count += regulatory_bodies[body]
        
        if count >= 2:
            return SCORING_WEIGHTS["regulatory_multi"]
        elif count > 0:
            return SCORING_WEIGHTS["regulatory_multi"] * 0.5
        
        return 0.0
    
    def _determine_primary_type(self, scores: Dict[str, float], text: str) -> InternationalType:
        """Determine the primary international type."""
        # Check for explicit foreign participants
        if "外国人被験者" in text or "foreign participants" in text:
            return InternationalType.EXPLICIT_FOREIGN
        
        # Check for known programs
        if scores.get("program_identification", 0) > 0:
            return InternationalType.INTERNATIONAL_COLLABORATION
        
        # Check for multi-site
        if scores.get("multi_country", 0) > 0:
            return InternationalType.MULTI_SITE
        
        # Check for language support
        if scores.get("multilingual", 0) > 0:
            return InternationalType.LANGUAGE_SUPPORT
        
        # Default to implicit
        return InternationalType.IMPLICIT
    
    def _determine_secondary_types(self, scores: Dict[str, float], text: str) -> List[InternationalType]:
        """Determine secondary international types."""
        types = []
        
        if scores.get("multi_country", 0) > 0:
            types.append(InternationalType.MULTI_SITE)
        
        if scores.get("multilingual", 0) > 0:
            types.append(InternationalType.LANGUAGE_SUPPORT)
        
        if scores.get("program_identification", 0) > 0:
            types.append(InternationalType.INTERNATIONAL_COLLABORATION)
        
        return types
    
    def _calculate_confidence(self, scores: Dict[str, float], matches: List[str]) -> float:
        """Calculate confidence score (0-1)."""
        # Base confidence on number of indicators
        indicator_count = len([s for s in scores.values() if s > 0])
        keyword_count = len(matches)
        
        # Calculate base confidence
        confidence = min(1.0, (indicator_count * 0.15) + (keyword_count * 0.05))
        
        # Boost for explicit mentions
        if any(score >= SCORING_WEIGHTS["explicit_mention"] for score in scores.values()):
            confidence = min(1.0, confidence + 0.3)
        
        # Reduce for very low scores
        total_score = sum(scores.values())
        if total_score < INTERNATIONAL_THRESHOLD * 0.5:
            confidence *= 0.5
        
        return round(confidence, 2)
    
    def _add_recommendations(self, analysis: InternationalAnalysis, 
                           text: str, languages: List[str]):
        """Add recommendations for international support."""
        # Translation needs
        if len(languages) > 1 or "英語" in text or "english" in text:
            analysis.requires_translation = True
        
        # Cultural adaptation
        if len(analysis.keyword_matches) > 3:
            analysis.requires_cultural_adaptation = True
        
        # Regulatory considerations
        reg_considerations = []
        
        if "fda" in text:
            reg_considerations.append("FDA compliance required for US participants")
        if "ema" in text:
            reg_considerations.append("EMA compliance required for EU participants")
        if "gdpr" in text or "個人情報" in text:
            reg_considerations.append("Data privacy regulations (GDPR/APPI) apply")
        
        analysis.regulatory_considerations = reg_considerations