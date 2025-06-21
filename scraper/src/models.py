"""Data models for the research scraper system."""

from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl


class StudyType(str, Enum):
    """Types of clinical studies."""
    CLINICAL_TRIAL = "clinical_trial"
    OBSERVATIONAL = "observational"
    REGISTRY = "registry"
    EXPANDED_ACCESS = "expanded_access"
    UNKNOWN = "unknown"


class InternationalType(str, Enum):
    """Types of international involvement."""
    EXPLICIT_FOREIGN = "explicit_foreign_participants"
    INTERNATIONAL_COLLABORATION = "international_collaboration"
    MULTI_SITE = "multi_site_international"
    LANGUAGE_SUPPORT = "language_support_provided"
    IMPLICIT = "implicit_international"
    NONE = "none"


class StudyStatus(str, Enum):
    """Current status of the study."""
    RECRUITING = "recruiting"
    NOT_YET_RECRUITING = "not_yet_recruiting"
    ACTIVE = "active"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    WITHDRAWN = "withdrawn"
    UNKNOWN = "unknown"


class ResearchStudy(BaseModel):
    """Main model for a research study."""
    
    # Basic information
    study_id: str = Field(..., description="Unique identifier for the study")
    title: str = Field(..., description="Study title")
    title_en: Optional[str] = Field(None, description="English title if available")
    
    # Source information
    source_url: HttpUrl = Field(..., description="URL where the study was found")
    source_site: str = Field(..., description="Source website (AMED, JST, etc.)")
    scraped_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Study details
    study_type: StudyType = Field(default=StudyType.UNKNOWN)
    status: StudyStatus = Field(default=StudyStatus.UNKNOWN)
    phase: Optional[str] = Field(None, description="Clinical trial phase")
    
    # Dates
    start_date: Optional[datetime] = Field(None)
    completion_date: Optional[datetime] = Field(None)
    application_deadline: Optional[datetime] = Field(None)
    
    # Description
    description: str = Field(..., description="Full study description")
    brief_summary: Optional[str] = Field(None, description="Brief summary")
    
    # International indicators
    international_type: InternationalType = Field(default=InternationalType.NONE)
    international_score: float = Field(0.0, description="International relevance score")
    international_indicators: List[str] = Field(
        default_factory=list,
        description="Specific indicators found"
    )
    
    # Locations
    countries: List[str] = Field(default_factory=list)
    cities: List[str] = Field(default_factory=list)
    institutions: List[str] = Field(default_factory=list)
    
    # Languages
    languages_supported: List[str] = Field(default_factory=list)
    translation_provided: bool = Field(False)
    
    # Eligibility
    eligibility_criteria: Optional[str] = Field(None)
    target_enrollment: Optional[int] = Field(None)
    age_range: Optional[str] = Field(None)
    gender: Optional[str] = Field(None)
    
    # Contact information
    principal_investigator: Optional[str] = Field(None)
    contact_name: Optional[str] = Field(None)
    contact_email: Optional[str] = Field(None)
    contact_phone: Optional[str] = Field(None)
    
    # Funding
    funding_source: Optional[str] = Field(None)
    budget: Optional[str] = Field(None)
    grant_number: Optional[str] = Field(None)
    
    # Keywords and conditions
    keywords: List[str] = Field(default_factory=list)
    conditions: List[str] = Field(default_factory=list)
    interventions: List[str] = Field(default_factory=list)
    
    # Metadata
    raw_html: Optional[str] = Field(None, description="Raw HTML for reprocessing")
    processing_notes: List[str] = Field(default_factory=list)
    confidence_score: float = Field(1.0, description="Confidence in data extraction")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ScrapingResult(BaseModel):
    """Result of a scraping operation."""
    
    success: bool
    source_site: str
    url: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    studies_found: int = Field(0)
    studies_processed: int = Field(0)
    international_studies: int = Field(0)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    duration_seconds: float = Field(0.0)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class InternationalAnalysis(BaseModel):
    """Detailed analysis of international aspects."""
    
    study_id: str
    is_international: bool
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    
    # Detailed scoring
    scores: Dict[str, float] = Field(default_factory=dict)
    total_score: float = Field(0.0)
    
    # Evidence
    keyword_matches: List[str] = Field(default_factory=list)
    context_snippets: List[str] = Field(default_factory=list)
    
    # Classification
    primary_type: InternationalType
    secondary_types: List[InternationalType] = Field(default_factory=list)
    
    # Recommendations
    requires_translation: bool = Field(False)
    requires_cultural_adaptation: bool = Field(False)
    regulatory_considerations: List[str] = Field(default_factory=list)
    
    # ML model output (if used)
    ml_prediction: Optional[float] = Field(None)
    ml_features: Optional[Dict[str, float]] = Field(None)