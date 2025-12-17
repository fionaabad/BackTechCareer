import io
import joblib
import numpy as np
import pdfplumber
import re
import json

MODEL_PATH = "backend/ml/models/cv_role/model.pkl"
VECTORIZER_PATH = "backend/ml/models/cv_role/vectorizer.pkl"
SKILLS_INFO_PATH = "backend/ml/models/skills/skills_info.json"
JOB_SKILLS_PATH = "backend/ml/models/skills/jobs_dict.json"

modelo = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

with open(SKILLS_INFO_PATH, "r", encoding="utf-8") as f:
    skill_dict = {k.lower(): v for k, v in json.load(f).items()}

with open(JOB_SKILLS_PATH, "r", encoding="utf-8") as f:
    job_skills = json.load(f)

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    pdf_file = io.BytesIO(pdf_bytes)
    with pdfplumber.open(pdf_file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def predict_text(cv_text: str):
    vector = vectorizer.transform([cv_text]).toarray()
    probs = modelo.predict_proba(vector)[0]

    best_idx = int(np.argmax(probs))
    best_title = modelo.classes_[best_idx]

    top3_idx = probs.argsort()[-3:][::-1]
    top3 = [
        {"job_title": modelo.classes_[i], "prob": float(probs[i])}
        for i in top3_idx
    ]

    probs_dict = {modelo.classes_[i]: float(prob) for i, prob in enumerate(probs)}

    return {"prediccion": best_title, "top3": top3, "probabilidades": probs_dict}

def extract_skills(text: str) -> list[dict]:
    text = text.lower()
    found = set()

    for skill in skill_dict.keys():
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found.add(skill)

    enriched_skills = [
        {"skill": s, **skill_dict.get(s, {})} for s in sorted(found)
    ]

    return enriched_skills


def skills_for_jobs(skills: list[str], predicted_jobs: list[str]) -> list[dict]:
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
            "matching_skills": [
                {"skill": s, **skill_dict.get(s, {})} for s in matching_skills
            ],
            "missing_skills": [
                {"skill": s, **skill_dict.get(s, {})} for s in missing_skills
            ],
            "matching_skills_count": len(matching_skills),
            "missing_skills_count": len(missing_skills),
        })

    return results