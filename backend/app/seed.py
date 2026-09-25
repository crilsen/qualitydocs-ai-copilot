"""Seed synthetic demo documents (no real data). Run: python -m app.seed"""
from .database import SessionLocal, init_db
from .models import Document

DOCS = [
    ("PROC-014-synthetic-procedure-v3.txt",
     "3 sections",
     "Section 1 — Document Control (Page 1)\nProcedure PROC-014 Receiving Inspection v3.0. Owner: Quality. Approval signature: MISSING (no signature on file).\n\nSection 2 — Inspection (Page 2)\nAll incoming lots require sampling per AQL 1.0. Calibration of calipers must be current. NOTE: caliper CAL-07 calibration expired 2026-02-10.\n\nSection 3 — Records (Page 3)\nRetain inspection records for 5 years. Two lots (LOT-881, LOT-882) have no inspection record on file."),
    ("SPEC-208-synthetic-specification.txt",
     "2 sections",
     "Section 4 — Parameters (Page 1)\nSPEC-208 Torque specification: 12.0 Nm +/- 0.5 Nm. Operating temperature max 85 C.\n\nSection 5 — Acceptance (Page 2)\nAcceptance requires 100% torque log. Sampling AQL 1.5 stated here, which DIVERGES from PROC-014 AQL 1.0."),
    ("NCR-031-synthetic-nonconformity-report.txt",
     "2 sections",
     "Section 1 — Finding (Page 1)\nNCR-031: Lot LOT-881 released without inspection record. Severity: high. Containment overdue since 2026-09-10.\n\nSection 2 — Cause (Page 2)\nRoot cause pending. Torque log for LOT-881 shows 11.2 Nm, which is OUT OF SPEC vs SPEC-208 (12.0 +/- 0.5). Corrective action has no owner and no due date."),
    ("PROC-014-synthetic-procedure-v2.txt",
     "2 sections",
     "Section 1 — Document Control (Page 1)\nProcedure PROC-014 Receiving Inspection v2.0 (superseded). Sampling AQL 2.5.\n\nSection 2 — Records (Page 2)\nRetain inspection records for 3 years. Approved by J. Smith."),
]


def main():
    init_db()
    db = SessionLocal()
    for name, label, text in DOCS:
        if db.query(Document).filter_by(filename=name).first():
            continue
        db.add(Document(filename=name, file_type="txt", pages_or_sections=label,
                        text_content=text, char_count=len(text)))
    db.commit()
    print(f"Seeded {len(DOCS)} synthetic documents.")


if __name__ == "__main__":
    main()
