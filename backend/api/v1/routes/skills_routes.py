from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from api.v1.controllers.skills_controller import (
    extract_text_from_pdf,
    extract_skills_from_text,
    rank_jobs_from_skills,
    get_skills_from_resume,
    get_missing_skills
)

router = APIRouter(tags=["Skills"])

class SkillInput(BaseModel):
    skills: list[str]

@router.post("/rank_jobs_by_skills")
def rank_jobs_by_skills(data: SkillInput):
    ranking = rank_jobs_from_skills(data.skills)
    missing = get_missing_skills(data.skills)
    return {
        "skills_provided": data.skills,
        "ranking": ranking,
        "missing_skills_by_job": missing
    }

@router.post("/rank_jobs_from_pdf")
async def rank_jobs_from_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    if not text.strip():
        return {"error": "El PDF no contiene texto legible."}

    skills = extract_skills_from_text(text)
    ranking = rank_jobs_from_skills(skills)
    missing = get_missing_skills(skills)

    return {
        "filename": file.filename,
        "extracted_skills": skills,
        "ranking": ranking,
        "missing_skills_by_job": missing
    }

@router.post("/extract_skills_from_pdf")
async def extract_skills_from_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    if not text.strip():
        return {"error": "El PDF no contiene texto legible."}

    skills = extract_skills_from_text(text)
    return {
        "filename": file.filename,
        "extracted_skills": skills
    }   

@router.post("/extract_skills")
def extract_skills(data: SkillInput):
    skills = extract_skills_from_text(" ".join(data.skills))
    return {
        "provided_text": data.skills,
        "extracted_skills": skills
    }
