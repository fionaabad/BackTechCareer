import json
import os

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
        "ml", "models", "skills", "skill_dict.json"
)

skill_dict = {}

def load_model():
    global skill_dict
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Skill dictionary not found at {MODEL_PATH}")

    if os.path.getsize(MODEL_PATH) == 0:
        raise ValueError(f"Skill dictionary at {MODEL_PATH} is empty")

    with open(MODEL_PATH, "r") as f:
        skill_dict = json.load(f)

load_model()

def match_jobs(resume):
    job_match_count = {}
    job_matched_skills = {}

    for skill in resume:
        if skill in skill_dict:
            for job in skill_dict[skill]:
                job_match_count[job] = job_match_count.get(job, 0) + 1
                if job not in job_matched_skills:
                    job_matched_skills[job] = set()
                job_matched_skills[job].add(skill)

    ranking = sorted(
        job_match_count.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top10 = []
    for job, count in ranking[:10]:
        top10.append({
            "job_title": job,
            "matching_skills_count": count,
            "matching_skills": sorted(list(job_matched_skills[job]))
        })

    return top10

def get_skills_in_dict(resume):
    return [s for s in resume if s in skill_dict]


