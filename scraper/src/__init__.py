"""Research scraper package."""

from .config import ScraperConfig
from .scraper import ResearchScraper
from .analyzer import InternationalAnalyzer
from .models import (
    ResearchStudy,
    ScrapingResult,
    InternationalAnalysis,
    StudyType,
    InternationalType,
    StudyStatus
)

__all__ = [
    "ScraperConfig",
    "ResearchScraper",
    "InternationalAnalyzer",
    "ResearchStudy",
    "ScrapingResult",
    "InternationalAnalysis",
    "StudyType",
    "InternationalType",
    "StudyStatus"
]

__version__ = "1.0.0"