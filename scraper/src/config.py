"""Configuration settings for the research scraper system."""

from typing import Dict, List
from pydantic import BaseModel, Field
import os


class ScraperConfig(BaseModel):
    """Main configuration class for the scraper."""
    
    # API/Scraping settings
    user_agent: str = Field(
        default="Mozilla/5.0 (compatible; ResearchBot/1.0; +https://theta-tech.co.jp/bot)",
        description="User agent for web requests"
    )
    request_timeout: int = Field(default=30, description="Request timeout in seconds")
    rate_limit_delay: float = Field(default=2.0, description="Delay between requests in seconds")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    
    # Target sites
    target_sites: Dict[str, str] = Field(
        default={
            "AMED": "https://www.amed.go.jp/koubo/",
            "JST": "https://www.jst.go.jp/inter/",
            "JSPS": "https://www.jsps.go.jp/j-bottom/",
            "MHLW": "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/hokabunya/kenkyujigyou/",
            "ClinicalTrials": "https://clinicaltrials.gov/api/query/",
            "JRCT": "https://jrct.niph.go.jp/search"
        },
        description="Target websites for scraping"
    )
    
    # Database settings
    database_url: str = Field(
        default=os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/research_db"),
        description="PostgreSQL connection string"
    )
    
    # ML Model settings
    bert_model_name: str = Field(
        default="cl-tohoku/bert-base-japanese-v3",
        description="BERT model for Japanese text analysis"
    )
    
    # International research keywords
    international_keywords: List[str] = Field(
        default=[
            # Japanese keywords
            "国際共同", "外国人", "多国籍", "グローバル", "海外",
            "国際", "多施設共同", "国際臨床試験", "外国人被験者",
            "多言語対応", "翻訳", "通訳", "英語対応",
            
            # English keywords
            "international", "multinational", "global", "cross-border",
            "multicenter", "multi-site", "foreign participants",
            
            # Program names
            "ASPIRE", "e-ASIA", "SICORP", "Interstellar",
            
            # Bilateral cooperation
            "日米", "日欧", "日中", "日韓", "日印",
            
            # Regulatory bodies
            "FDA", "EMA", "PMDA", "NMPA"
        ],
        description="Keywords indicating international research"
    )
    
    # Exclusion patterns
    exclusion_patterns: List[str] = Field(
        default=[
            "動物実験", "細胞実験", "in vitro", "マウス", "ラット",
            "基礎研究のみ", "文献調査", "システマティックレビュー"
        ],
        description="Patterns to exclude non-clinical trials"
    )
    
    # Output settings
    output_format: str = Field(default="json", description="Output format (json, csv, excel)")
    data_dir: str = Field(default="./data", description="Directory for data storage")
    
    # Monitoring
    sentry_dsn: str = Field(default="", description="Sentry DSN for error tracking")
    prometheus_port: int = Field(default=8000, description="Port for Prometheus metrics")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Scoring weights for international study detection
SCORING_WEIGHTS = {
    "explicit_mention": 10,      # Direct mention of foreign participants
    "international_program": 8,   # Known international programs
    "multiple_countries": 7,      # Multiple country involvement
    "multilingual": 5,           # Language support mentioned
    "translation_required": 5,    # Translation services mentioned
    "regulatory_multi": 4,       # Multiple regulatory authorities
    "implicit_international": 3   # Implicit international indicators
}

# Minimum score threshold for classification
INTERNATIONAL_THRESHOLD = 8

# Headers for web requests
REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ja,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}