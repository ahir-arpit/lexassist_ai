from pydantic import BaseModel
from typing import List, Dict, Optional

class RiskAnalysisResponse(BaseModel):
    risk_score: int
    risk_level: str
    detected_clauses: List[str]

class EntityResponse(BaseModel):
    text: str
    type: str

class StatutoryComparisonResponse(BaseModel):
    concept: str
    section: str
    legal_provision: str
    compliance_note: str

class AnalysisResponse(BaseModel):
    filename: str
    entities: List[EntityResponse]
    risk_analysis: RiskAnalysisResponse
    summary: str
    statutory_comparison: List[StatutoryComparisonResponse]
    status: str = "success"

class ErrorResponse(BaseModel):
    detail: str
    status: str = "error"
