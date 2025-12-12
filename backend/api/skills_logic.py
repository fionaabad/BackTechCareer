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

skill_dict = {}          
job_skills = {}        

def load_model():
    """Load skill dictionary and job→skills mapping for missing skills."""
    global skill_dict, job_skills

    if not os.path.exists(SKILLS_DICT_PATH):
        raise FileNotFoundError(f"Skill dictionary not found at {SKILLS_DICT_PATH}")
    if os.path.getsize(SKILLS_DICT_PATH) == 0:
        raise ValueError(f"Skill dictionary at {SKILLS_DICT_PATH} is empty")

    with open(SKILLS_DICT_PATH, "r", encoding="utf-8") as f:
        skill_dict = {k.lower(): v for k, v in json.load(f).items()}

    if not os.path.exists(JOB_SKILLS_PATH):
        raise FileNotFoundError(f"Job skills dict not found at {JOB_SKILLS_PATH}")
    with open(JOB_SKILLS_PATH, "r", encoding="utf-8") as f:
        job_skills.update(json.load(f))

load_model()

def extract_skills(text: str) -> list[str]:
    text = text.lower()
    found = []
    for skill in skill_dict.keys():
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
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

    top10 = []
    for job, count in ranking[:10]:
        top10.append({
            "job_title": job,
            "matching_skills_count": count,
            "matching_skills": sorted(list(job_matched_skills[job]))
        })

    return top10

def get_missing_skills_by_job(skills: list[str]) -> dict:
    top_jobs = match_jobs(skills)
    skills_set = set(skills)
    missing = {}

    for entry in top_jobs:
        job_title = entry["job_title"]
        missing_skills = set(job_skills[job_title]) - skills_set
        missing[job_title] = sorted(missing_skills)

    return missing
