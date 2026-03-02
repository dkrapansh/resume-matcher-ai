from io import BytesIO
import pdfplumber
from docx import Document

def extract_text(filename: str, content: bytes) -> str:
    name = filename.lower()

    if name.endswith(".pdf"):
        text_parts = []
        with pdfplumber.open(BytesIO(content)) as pdf:
            for page in pdf.pages:
                text_parts.append(page.extract_text() or "")
        return "\n".join(text_parts).strip()

    if name.endswith(".docx"):
        doc = Document(BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs).strip()

    raise ValueError("Unsupported file type. Upload PDF or DOCX.")
