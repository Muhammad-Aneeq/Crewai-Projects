from typing import Optional, List, Union
from pydantic import BaseModel

class LeadPersonalInfo(BaseModel):
    name: Optional[str] = None
    job_title: Optional[str] = None
    role_relevance: Optional[Union[int, str]] = None
    professional_background: Optional[str] = None

class CompanyInfo(BaseModel):
    company_name: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[Union[int, str]] = None
    revenue: Optional[Union[float, str]] = None
    market_presence: Optional[Union[int, str]] = None

class LeadScore(BaseModel):
    score: Optional[int] = None
    scoring_criteria: Optional[List[str]] = None
    validation_notes: Optional[str] = None

class LeadScoringResult(BaseModel):
    personal_info: Optional[LeadPersonalInfo] = None
    company_info: Optional[CompanyInfo] = None
    lead_score: Optional[LeadScore] = None
