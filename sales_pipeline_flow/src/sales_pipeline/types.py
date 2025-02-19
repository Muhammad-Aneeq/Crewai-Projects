from pydantic import BaseModel
from typing import List, Union

class LeadPersonalInfo(BaseModel):
    name: Union[str, None] = None
    job_title: Union[str, None] = None
    role_relevance: Union[int, str, None] = None
    professional_background: Union[str, None] = None

class CompanyInfo(BaseModel):
    company_name: Union[str, None] = None
    industry: Union[str, None] = None
    company_size: Union[int, str, None] = None
    revenue: Union[float, str, None] = None
    market_presence: Union[int, str, None] = None

class LeadScore(BaseModel):
    score: Union[int, None] = None
    scoring_criteria: Union[List[str], None] = None  # Changed to allow None
    validation_notes: Union[str, None] = None

class LeadScoringResult(BaseModel):
    personal_info: Union[LeadPersonalInfo, None] = None 
    company_info: Union[CompanyInfo, None] = None
    lead_score: Union[LeadScore, None] = None
