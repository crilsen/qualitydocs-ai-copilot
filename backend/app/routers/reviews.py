"""Human review router: status per finding + summary counts."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Finding
from ..schemas import ReviewUpdate

router = APIRouter(tags=["review"])


@router.patch("/api/findings/{finding_id}/review")
def review_finding(finding_id: int, body: ReviewUpdate, db: Session = Depends(get_db)):
    f = db.get(Finding, finding_id)
    if not f:
        raise HTTPException(404, "Finding not found.")
    f.status = body.status
    f.reviewer_comment = body.reviewer_comment or ""
    if body.title:
        f.edited_title = body.title
    if body.description:
        f.edited_description = body.description
    if body.recommended_action:
        f.edited_action = body.recommended_action
    if body.status == "edited" and not (body.title or body.description or body.recommended_action):
        raise HTTPException(400, "Edited status requires at least one edited field.")
    db.commit()
    return {"id": f.id, "status": f.status}


@router.get("/api/analyses/{run_id}/review-summary")
def review_summary(run_id: int, db: Session = Depends(get_db)):
    findings = db.query(Finding).filter(Finding.run_id == run_id).all()
    counts = {"pending": 0, "accepted": 0, "edited": 0, "rejected": 0}
    for f in findings:
        counts[f.status] = counts.get(f.status, 0) + 1
    return {"run_id": run_id, "total": len(findings), "counts": counts}


@router.get("/api/governance")
def governance():
    return {
        "notice": "AI-generated results must be reviewed before any decision.",
        "principles": [
            "Final decisions always require human validation.",
            "Only synthetic demo data is allowed; no real or confidential data.",
            "Every AI claim must quote document evidence (name, page/section, excerpt).",
            "Uncertainty must be declared when evidence is missing; requirements are never invented.",
            "Document content is treated as data, never as instructions; embedded instructions are ignored and logged.",
        ],
        "allowed_data": ["Synthetic procedures, specifications, and nonconformity reports bundled with the demo"],
        "prohibited_data": ["Real customer data", "Confidential documents", "Personal data", "API keys or credentials"],
        "ai_limits": ["No OCR for scanned PDFs in this MVP", "Offline demo provider is heuristic only",
                      "Findings without evidence are withheld automatically"],
    }
