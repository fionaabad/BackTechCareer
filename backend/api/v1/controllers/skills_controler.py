import io
import pdfplumber
from skills_logic import match_jobs

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    pdf_file = io.BytesIO(pdf_bytes)
    with pdfplumber.open(pdf_file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def extract_skills_from_text(text: str) -> list[str]:
    words = [w.lower().strip() for w in text.replace(",", "\n").split()]
    return [w for w in words if w]

def rank_jobs_from_skills(skills: list[str]):
    return match_jobs(skills)
