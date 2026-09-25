"""Text extraction for PDF and DOCX with friendly errors."""
from io import BytesIO


def extract_text(filename: str, data: bytes) -> tuple[str, str]:
    lower = filename.lower()
    if lower.endswith(".pdf"):
        from pypdf import PdfReader
        try:
            reader = PdfReader(BytesIO(data))
            parts = []
            for i, page in enumerate(reader.pages, start=1):
                t = page.extract_text() or ""
                if t.strip():
                    parts.append(f"[Page {i}]\n{t.strip()}")
            text = "\n\n".join(parts)
            label = f"{len(reader.pages)} pages"
            if not text.strip():
                raise ValueError("No extractable text found (scanned PDF without OCR is not supported in this MVP).")
            return text, label
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Could not extract PDF text: {e}")
    if lower.endswith(".docx"):
        from docx import Document as Docx
        try:
            doc = Docx(BytesIO(data))
            paras = [p.text for p in doc.paragraphs if p.text.strip()]
            text = "\n".join(paras)
            for table in doc.tables:
                for row in table.rows:
                    text += "\n" + " | ".join(c.text for c in row.cells)
            if not text.strip():
                raise ValueError("No extractable text found in DOCX.")
            sections = len(paras)
            return text, f"{sections} paragraphs"
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Could not extract DOCX text: {e}")
    raise ValueError("Unsupported file type. Only PDF and DOCX are allowed.")
