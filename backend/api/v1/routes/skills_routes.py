from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.api.v1.controllers.predict_controller import extract_text_from_pdf
from backend.api.v1.controllers.skills_controller import (
    extract_skills,
    skills_for_jobs,
)

router = APIRouter(tags=["Skills"])

class SkillsRequest(BaseModel):
    text: str
    predicted_jobs: list[str]

@router.post("/skills")
def calculate_skills(payload: SkillsRequest):
    extracted_skills = extract_skills(payload.text)
    results = skills_for_jobs(
        skills=extracted_skills,
        predicted_jobs=payload.predicted_jobs,
    )

    if not results:
        raise HTTPException(
            status_code=400,
            detail="None of the predicted jobs exist in job_skills",
        )

    return {
        "extracted_skills": extracted_skills,
        "results": results,
    }