"""Documents router: upload 2-5 handled at analysis level; each upload validated."""
import datetime
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from ..config import settings
from ..database import get_db
from ..models import Document
from ..services.extractor import extract_text
from ..services.injection_guard import scan

router = APIRouter(prefix="/api/documents", tags=["documents"])


def _allowed(filename: str) -> bool:
    exts = [e.strip().lower() for e in settings.allowed_extensions.split(",")]
    return any(filename.lower().endswith(e) for e in exts)


@router.post("/upload")
def upload(files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    if len(files) < 1 or len(files) > 5:
        raise HTTPException(400, "Upload between 1 and 5 files per request (analysis requires 2-5).")
    out = []
    for f in files:
        data = f.file.read()
        size_mb = len(data) / (1024 * 1024)
        if not _allowed(f.filename or ""):
            raise HTTPException(400, f"File {f.filename}: only PDF and DOCX are allowed.")
        if size_mb > settings.max_upload_mb:
            raise HTTPException(400, f"File {f.filename}: exceeds {settings.max_upload_mb} MB.")
        try:
            text, label = extract_text(f.filename, data)
        except ValueError as e:
            raise HTTPException(422, f"File {f.filename}: {e}")
        hits = scan(text)
        doc = Document(filename=f.filename, file_type=f.filename.rsplit(".", 1)[-1].lower(),
                       pages_or_sections=label, text_content=text[:200000],
                       char_count=len(text), suspicious_flag=1 if hits else 0)
        db.add(doc)
        db.commit()
        db.refresh(doc)
        out.append({"id": doc.id, "filename": doc.filename, "file_type": doc.file_type,
                    "pages_or_sections": label, "char_count": len(text),
                    "suspicious_detected": bool(hits), "suspicious_hints": hits[:3],
                    "created_at": doc.created_at.isoformat()})
    return {"documents": out}


@router.get("")
def list_docs(db: Session = Depends(get_db)):
    docs = db.query(Document).order_by(Document.id.desc()).all()
    return {"documents": [{"id": d.id, "filename": d.filename, "file_type": d.file_type,
                           "pages_or_sections": d.pages_or_sections, "char_count": d.char_count,
                           "suspicious_flag": bool(d.suspicious_flag),
                           "created_at": d.created_at.isoformat() if isinstance(d.created_at, datetime.datetime) else d.created_at}
                          for d in docs]}


@router.delete("/{doc_id}")
def delete_doc(doc_id: int, db: Session = Depends(get_db)):
    d = db.get(Document, doc_id)
    if not d:
        raise HTTPException(404, "Document not found.")
    db.delete(d)
    db.commit()
    return {"deleted": doc_id}
