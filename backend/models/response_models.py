from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Any

class ScoreBreakdown(BaseModel):
    skills_match: int = Field(ge=0, le=100)
    experience_match: int = Field(ge=0, le=100)
    education_match: int = Field(ge=0, le=100)
    keyword_density: int = Field(ge=0, le=100)

class ImprovementSuggestion(BaseModel):
    section: str
    original: str
    improved: str
    reason: str

class ATSKeywords(BaseModel):
    found: List[str]
    missing: List[str]

class AnalysisResult(BaseModel):
    match_score: int = Field(ge=0, le=100)
    score_breakdown: Optional[ScoreBreakdown] = None
    matching_skills: List[str] = []
    missing_skills: List[str] = []
    extra_skills: List[str] = []
    ats_keywords: Optional[ATSKeywords] = None
    experience_analysis: Optional[str] = None
    improvement_suggestions: List[ImprovementSuggestion] = []
    summary: str
    hire_likelihood: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def sanitize_data(cls, data: Any) -> Any:
        if isinstance(data, dict):
            score = data.get("match_score")
            if isinstance(score, float):
                if score <= 1.0:
                    data["match_score"] = int(score * 100)
                else:
                    data["match_score"] = int(score)
            elif isinstance(score, str):
                try:
                    data["match_score"] = int(float(score) * 100) if float(score) <= 1.0 else int(float(score))
                except ValueError:
                    pass

            suggs = data.get("improvement_suggestions")
            if isinstance(suggs, list):
                new_suggs = []
                for item in suggs:
                    if isinstance(item, str):
                        new_suggs.append({
                            "section": "General",
                            "original": "N/A",
                            "improved": item,
                            "reason": "AI suggestion"
                        })
                    else:
                        new_suggs.append(item)
                data["improvement_suggestions"] = new_suggs
        return data

class AnalysisResponse(BaseModel):
    result: AnalysisResult
    model_used: str
    processing_time_ms: int










