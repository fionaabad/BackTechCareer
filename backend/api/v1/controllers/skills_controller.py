import json
import re

SKILLS_DICT_PATH = "backend/ml/models/skills/skill_dict.json"
JOB_SKILLS_PATH = "backend/ml/models/skills/job_skills.json"

with open(SKILLS_DICT_PATH, "r", encoding="utf-8") as f:
    skill_dict = {k.lower(): v for k, v in json.load(f).items()}

with open(JOB_SKILLS_PATH, "r", encoding="utf-8") as f:
    job_skills = json.load(f)


def extract_skills(text: str) -> list[str]:
    text = text.lower()
    found = []

    for skill in skill_dict.keys():
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found.append(skill)

    return sorted(set(found))


def skills_for_jobs(
    skills: list[str],
    predicted_jobs: list[str],
) -> list[dict]:

    user_skills = set(skills)
    results = []

    for job_title in predicted_jobs:
        if job_title not in job_skills:
            continue 

        required_skills = set(job_skills[job_title])

        matching_skills = sorted(required_skills & user_skills)
        missing_skills = sorted(required_skills - user_skills)

        results.append({
            "job_title": job_title,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "matching_skills_count": len(matching_skills),
            "missing_skills_count": len(missing_skills),
        })

    return results
