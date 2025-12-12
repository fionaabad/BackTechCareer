import json
import os
import re

SKILLS_DICT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "ml", "models", "skills", "skill_dict.json"
)

JOB_SKILLS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "ml", "models", "skills", "job_skills.json"
)

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


def match_jobs(skills: list[str]) -> list[dict]:
    job_match_count = {}
    job_matched_skills = {}

    for skill in skills:
        if skill in skill_dict:
            for job in skill_dict[skill]:
                job_match_count[job] = job_match_count.get(job, 0) + 1
                job_matched_skills.setdefault(job, set()).add(skill)

    ranking = sorted(job_match_count.items(), key=lambda x: x[1], reverse=True)

    return [
        {
            "job_title": job,
            "matching_skills_count": count,
            "matching_skills": sorted(list(job_matched_skills[job]))
        }
        for job, count in ranking[:10]
    ]

def get_missing_skills_by_job(skills: list[str]) -> dict:
    top_jobs = match_jobs(skills)
    skills_set = set(skills)

    return {
        entry["job_title"]: sorted(set(job_skills[entry["job_title"]]) - skills_set)
        for entry in top_jobs
    }
