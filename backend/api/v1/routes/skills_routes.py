from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from backend.api.v1.controllers.skills_controller import (
    extract_text_from_pdf,
    get_skills_from_resume,
    rank_jobs_from_skills,
    get_missing_skills
)

router = APIRouter(tags=["Skills"])

class SkillInput(BaseModel):
    skills: list[str]

@router.post("/rank_jobs_by_skills")
def rank_jobs_by_skills(data: SkillInput):
    real_skills = get_skills_from_resume(data.skills)
    ranking = rank_jobs_from_skills(real_skills)
    missing = get_missing_skills(real_skills)
    return {
        "skills_provided": data.skills,
        "skills_detected": real_skills,
        "ranking": ranking,
        "missing_skills_by_job": missing
    }

@router.post("/rank_jobs_from_pdf")
async def rank_jobs_from_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)
    if not text.strip():
        return {"error": "El PDF no contiene texto legible."}
    real_skills = get_skills_from_resume(text)
    ranking = rank_jobs_from_skills(real_skills)
    missing = get_missing_skills(real_skills)
    return {
        "filename": file.filename,
        "extracted_skills": real_skills,
        "ranking": ranking,
        "missing_skills_by_job": missing
    }

@router.post("/extract_skills_from_pdf")
async def extract_skills_from_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)
    if not text.strip():
        return {"error": "El PDF no contiene texto legible."}
    real_skills = get_skills_from_resume(text)
    return {
        "filename": file.filename,
        "extracted_skills": real_skills,
    }

@router.post("/extract_skills")
def extract_skills(data: SkillInput):
    text = " ".join(data.skills)
    real_skills = get_skills_from_resume(text)
    return {
        "provided_text": data.skills,
        "extracted_skills": real_skills
    }
