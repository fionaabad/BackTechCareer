import io
import pdfplumber

from backend.api.skills_logic import (
    extract_skills,
    match_jobs,
    get_missing_skills_by_job,
)

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    pdf_file = io.BytesIO(pdf_bytes)
    with pdfplumber.open(pdf_file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def get_skills_from_resume(text: str) -> list[str]:
    return extract_skills(text)

def rank_jobs_from_skills(skills: list[str]):
    return match_jobs(skills)

def get_missing_skills(skills: list[str]):
    return get_missing_skills_by_job(skills)
