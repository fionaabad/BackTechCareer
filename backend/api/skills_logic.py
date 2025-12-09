import pandas as pd

MODEL_PATH = "BackTechCareer/backend/ml/models/skills/skill_dict.json"

df = None
skill_dict = None


def load_model():
    global skill_dict

    skill_dict = pd.read_json(MODEL_PATH)

load_model()


def match_jobs(resume):
    resume = [s.lower() for s in resume]

    job_match_count = {}

    for skill in resume:
        if skill in skill_dict:
            for job in skill_dict[skill]:
                job_match_count[job] = job_match_count.get(job, 0) + 1

    ranking = sorted(job_match_count.items(), key=lambda x: x[1], reverse=True)
    return ranking
