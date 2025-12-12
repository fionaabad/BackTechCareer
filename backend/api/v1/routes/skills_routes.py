from fastapi import APIRouter
from pydantic import BaseModel
from backend.api.v1.controllers.skills_controller import (
    extract_skills,
    match_jobs,
    get_missing_skills_by_job
)

router = APIRouter(tags=["Skills"])

class TextInput(BaseModel):
    text: str


@router.post("/rank_jobs_by_skills")
def rank_jobs_by_skills(data: TextInput):
    skills_detected = extract_skills(data.text)
    ranking = match_jobs(skills_detected)
    missing = get_missing_skills_by_job(skills_detected)
    return {
        "extracted_skills": skills_detected,
        "ranking": ranking,
        "missing_skills_by_job": missing
    }


@router.post("/extract_skills")
def extract_skills_only(data: TextInput):
    skills_detected = extract_skills(data.text)
    return {
        "extracted_skills": skills_detected
    }
