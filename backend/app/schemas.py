"""Pydantic schemas: API validation + structured LLM output."""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

Category = Literal["missing_item", "divergence", "risk", "nonconformity", "recommendation"]
Severity = Literal["low", "medium", "high"]
ReviewStatus = Literal["pending", "accepted", "edited", "rejected"]


class Evidence(BaseModel):
    document_name: str
    page_or_section: str
    excerpt: str = Field(max_length=600)


class FindingOut(BaseModel):
    category: Category
    severity: Severity
    title: str
    description: str
    evidence: List[Evidence]
    recommended_action: str


class AnalysisResult(BaseModel):
    executive_summary: str
    findings: List[FindingOut]
    limitations: List[str]


class RunAnalysisRequest(BaseModel):
    mode: Literal["executive_summary", "document_comparison", "missing_items", "divergence", "risk", "action_plan"]
    document_ids: List[int] = Field(min_length=2, max_length=5)
    prompt_version: str = "v1.0.0"
    provider: str = "auto"  # auto | anthropic | openai | gemini | compat | local


class ReviewUpdate(BaseModel):
    status: ReviewStatus
    reviewer_comment: Optional[str] = ""
    title: Optional[str] = None
    description: Optional[str] = None
    recommended_action: Optional[str] = None
