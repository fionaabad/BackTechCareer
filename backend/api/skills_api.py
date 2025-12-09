from fastapi import APIRouter
from pydantic import BaseModel
from .skills_logic import match_jobs

router = APIRouter()


class SkillInput(BaseModel):
    skills: list[str]


@router.post("/rank_jobs_by_skills")
def rank_jobs_by_skills(data: SkillInput):
    ranking = match_jobs(data.skills)

    return {
        "skills_provided": data.skills,
        "ranking": [
            {"job_title": job, "matching_skills": count}
            for job, count in ranking
        ]
    }
