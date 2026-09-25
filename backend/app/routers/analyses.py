"""Analyses router: run mode analysis, history, prompt/model/latency recorded."""
import json
import time
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import AnalysisRun, Document, Finding
from ..schemas import AnalysisResult, RunAnalysisRequest
from ..services.injection_guard import scan, wrap_as_data
from ..services.llm import ProviderUnavailableError, get_provider, list_providers
from ..services.prompt_registry import list_prompts, load_prompt

router = APIRouter(tags=["analyses"])


@router.get("/api/prompts")
def prompts():
    return {"prompts": list_prompts()}


@router.get("/api/providers")
def providers():
    return {"providers": list_providers()}


@router.post("/api/analyses/run")
def run_analysis(req: RunAnalysisRequest, db: Session = Depends(get_db)):
    if not (2 <= len(req.document_ids) <= 5):
        raise HTTPException(400, "Select 2 to 5 documents for analysis.")
    docs = db.query(Document).filter(Document.id.in_(req.document_ids)).all()
    if len(docs) != len(req.document_ids):
        raise HTTPException(404, "One or more documents not found.")
    version, prompt_text, _src = load_prompt(req.mode, req.prompt_version)
    ctx_parts, injection_notes = [], []
    for d in docs:
        hits = scan(d.text_content or "")
        if hits or d.suspicious_flag:
            injection_notes.append(f"Suspicious instruction-like text detected in {d.filename}; treated strictly as data.")
        ctx_parts.append(wrap_as_data(d.filename, d.pages_or_sections, d.text_content or ""))
    context = "\n\n".join(ctx_parts)
    try:
        provider = get_provider(req.provider or "auto")
    except ProviderUnavailableError as e:
        raise HTTPException(400, str(e))
    t0 = time.perf_counter()
    try:
        raw, model_name = provider.analyze(prompt_text, context, req.mode)
    except Exception as e:
        raise HTTPException(502, f"Analysis provider failed: {type(e).__name__}. Check API key and try again.")
    latency_ms = int((time.perf_counter() - t0) * 1000)
    try:
        validated = AnalysisResult.model_validate(raw)
    except Exception as e:
        raise HTTPException(502, f"Provider returned invalid JSON for the required schema: {e}")
    # Drop findings without evidence (never show conclusion without evidence)
    kept = [f for f in validated.findings if f.evidence]
    dropped = len(validated.findings) - len(kept)
    limitations = list(validated.limitations)
    if dropped:
        limitations.append(f"{dropped} finding(s) were withheld because they had no evidence.")
    limitations.extend(injection_notes)
    run = AnalysisRun(mode=req.mode, prompt_version=version, prompt_text=prompt_text[:8000],
                      model=f"{provider.id}:{model_name}", latency_ms=latency_ms,
                      document_ids=",".join(map(str, req.document_ids)),
                      executive_summary=validated.executive_summary,
                      limitations=json.dumps(limitations), raw_json=json.dumps(raw)[:50000])
    db.add(run)
    db.flush()
    for f in kept:
        db.add(Finding(run_id=run.id, category=f.category, severity=f.severity, title=f.title,
                       description=f.description, evidence_json=f.evidence_dump_json() if hasattr(f, "evidence_dump_json") else json.dumps([e.model_dump() for e in f.evidence]),
                       recommended_action=f.recommended_action))
    db.commit()
    return {"run_id": run.id, "mode": req.mode, "prompt_version": version, "model": run.model,
            "latency_ms": latency_ms, "result": {"executive_summary": validated.executive_summary,
             "findings": [f.model_dump() for f in kept], "limitations": limitations}}


@router.get("/api/analyses/{run_id}")
def get_analysis(run_id: int, severity: str = Query(""), category: str = Query(""), db: Session = Depends(get_db)):
    run = db.get(AnalysisRun, run_id)
    if not run:
        raise HTTPException(404, "Analysis run not found.")
    q = db.query(Finding).filter(Finding.run_id == run_id)
    if severity:
        q = q.filter(Finding.severity == severity)
    if category:
        q = q.filter(Finding.category == category)
    findings = q.all()
    return {"run": {"id": run.id, "mode": run.mode, "prompt_version": run.prompt_version,
                    "model": run.model, "latency_ms": run.latency_ms, "document_ids": run.document_ids,
                    "executive_summary": run.executive_summary,
                    "limitations": json.loads(run.limitations or "[]"),
                    "created_at": run.created_at.isoformat()},
            "findings": [{"id": f.id, "category": f.category, "severity": f.severity,
                          "title": f.edited_title or f.title,
                          "description": f.edited_description or f.description,
                          "evidence": json.loads(f.evidence_json or "[]"),
                          "recommended_action": f.edited_action or f.recommended_action,
                          "status": f.status, "reviewer_comment": f.reviewer_comment} for f in findings]}


@router.get("/api/history")
def history(db: Session = Depends(get_db)):
    runs = db.query(AnalysisRun).order_by(AnalysisRun.id.desc()).all()
    out = []
    for r in runs:
        n = db.query(Finding).filter(Finding.run_id == r.id).count()
        out.append({"id": r.id, "mode": r.mode, "prompt_version": r.prompt_version, "model": r.model,
                    "latency_ms": r.latency_ms, "findings_count": n,
                    "created_at": r.created_at.isoformat()})
    return {"runs": out}
