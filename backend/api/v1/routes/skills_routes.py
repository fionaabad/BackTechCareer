from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from backend.api.v1.controllers.skills_controller import (
    extract_text_from_pdf,
    extract_skills_from_text,
    rank_jobs_from_skills
)

router = APIRouter(tags=["Skills"])

class SkillInput(BaseModel):
    skills: list[str]

@router.post("/rank_jobs_by_skills")
def rank_jobs_by_skills(data: SkillInput):
    ranking = rank_jobs_from_skills(data.skills)
    return {
        "skills_provided": data.skills,
        "ranking": [
            {"job_title": job, "matching_skills": count}
            for job, count in ranking
        ]
    }

@router.post("/rank_jobs_from_pdf")
async def rank_jobs_from_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    if not text.strip():
        return {"error": "El PDF no contiene texto legible."}

    skills = extract_skills_from_text(text)
    ranking = rank_jobs_from_skills(skills)

    return {
        "filename": file.filename,
        "ranking": [
            {"job_title": job, "matching_skills": count}
            for job, count in ranking
        ]
    }
