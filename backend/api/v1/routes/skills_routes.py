from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from backend.api.v1.controllers.predict_controller import extract_text_from_pdf
from backend.api.v1.controllers.skills_controller import (
    extract_skills,
    match_jobs,
    get_missing_skills_by_job
)

router = APIRouter(tags=["Skills"])

class TextInput(BaseModel):
    text: str

@router.post("/extract_skills")
def extract_skills_from_text(payload: TextInput):
    skills_detected = extract_skills(payload.text)
    ranking = match_jobs(skills_detected)
    top1 = ranking[0]["job_title"] if ranking else None
    missing = get_missing_skills_by_job(skills_detected)
    return {
        "extracted_skills": skills_detected,
        "ranking": ranking,
        "missing_skills_by_job": missing,
        "top1": top1
    }