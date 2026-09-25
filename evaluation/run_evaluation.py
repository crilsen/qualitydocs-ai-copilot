"""Run demo analyses and score: citations present, JSON adherence, findings without evidence, latency.
Usage: python run_evaluation.py --output report.md  (run from repo root or evaluation/)
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.database import SessionLocal, init_db  # noqa: E402
from app.models import Document  # noqa: E402
from app.schemas import AnalysisResult  # noqa: E402
from app.seed import DOCS  # noqa: E402
from app.services.injection_guard import wrap_as_data  # noqa: E402
from app.services.llm import LocalDemoProvider  # noqa: E402
from app.services.prompt_registry import load_prompt  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="evaluation/report.md")
    args = ap.parse_args()

    init_db()
    db = SessionLocal()
    for name, label, text in DOCS:
        if not db.query(Document).filter_by(filename=name).first():
            db.add(Document(filename=name, file_type="txt", pages_or_sections=label, text_content=text, char_count=len(text)))
    db.commit()
    docs = db.query(Document).all()

    with open(os.path.join(os.path.dirname(__file__), "questions.json")) as f:
        questions = json.load(f)

    provider = LocalDemoProvider()
    rows = []
    for q in questions:
        ver, prompt, _ = load_prompt("document_comparison" if q["mode"] == "divergence" else ("risk" if q["mode"] in ("risk", "nonconformity") else ("missing_items" if q["mode"] == "missing_items" else "action_plan")))
        ctx = "\n\n".join(wrap_as_data(d.filename, d.pages_or_sections, d.text_content) for d in docs)
        t0 = time.perf_counter()
        raw, model = provider.analyze(prompt, ctx, q["mode"])
        latency = int((time.perf_counter() - t0) * 1000)
        try:
            v = AnalysisResult.model_validate(raw)
            json_ok = True
            no_evidence = sum(1 for f in v.findings if not f.evidence)
            citations = sum(len(f.evidence) for f in v.findings)
            hit = any(q["expected"].split()[0].lower() in (f.title + f.description + str(f.evidence)).lower() or
                      any(tok.lower() in (f.title + f.description).lower() for tok in q["expected"].split() if len(tok) > 3)
                      for f in v.findings)
        except Exception as e:
            json_ok, no_evidence, citations, hit = False, -1, 0, False
            print("schema error:", e)
        rows.append({"id": q["id"], "mode": q["mode"], "json_ok": json_ok, "citations": citations,
                     "findings_without_evidence": no_evidence, "expected_mentioned": hit,
                     "latency_ms": latency, "model": model})

    total = len(rows)
    ok = sum(1 for r in rows if r["json_ok"])
    md = ["# Evaluation report (synthetic data only)", "",
          f"Provider: local-demo-v1 (offline heuristic). Cases: {total}. JSON adherence: {ok}/{total}.",
          "| case | mode | json | citations | no-evidence | expected hit | latency |",
          "|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['id']} | {r['mode']} | {r['json_ok']} | {r['citations']} | {r['findings_without_evidence']} | {r['expected_mentioned']} | {r['latency_ms']} ms |")
    md += ["", "Notes:", "- Findings without evidence must always be 0 (withheld automatically).",
           "- Cost estimate: local provider = $0. With Anthropic API, estimate tokens x model price at runtime.",
           "- AI results must be reviewed before any decision."]
    out = args.output if os.path.isabs(args.output) else os.path.join(os.getcwd(), args.output)
    if args.output == "evaluation/report.md" and os.path.basename(os.getcwd()) == "evaluation":
        out = os.path.join(os.getcwd(), "report.md")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w") as f:
        f.write("\n".join(md) + "\n")
    with open(os.path.splitext(out)[0] + ".json", "w") as f:
        json.dump(rows, f, indent=2)
    print("\n".join(md))


if __name__ == "__main__":
    main()
