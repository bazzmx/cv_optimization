from typing import List

from pydantic import BaseModel, Field


class Improvement(BaseModel):
    """Improvement model.
    This is the model for each element of the list of improvements that
    the LLM will return."""

    category: str
    issue: str
    recommendation: str
    priority: int


class CVAnalysisResponse(BaseModel):
    """CV analysis response model.
    Base response model for the CV analysis endpoint."""

    summary: str
    strengths: List[str] = Field(default_factory=list)
    improvements: List[Improvement] = Field(default_factory=list)
