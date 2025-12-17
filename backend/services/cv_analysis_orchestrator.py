from typing import Dict, List, Any

from backend.api.v1.controllers.predict_controller import (
    predict_text,
    extract_skills,
    skills_for_jobs,
)

from backend.api.v1.controllers.seniority_controller import (
    predict_seniority_from_text,
)

from backend.api.v1.controllers.salary_controller import (
    predict_salary_from_profile,
)


# =========================
# HELPERS
# =========================

def prettify_label(label: str) -> str:
    return label.replace("_", " ").title()


def slugify_group(group: str) -> str:
    return (
        group.lower()
        .replace("&", "and")
        .replace(",", "")
        .replace(" ", "_")
    )


def enrich_skill(skill: dict) -> Dict:
    group = skill.get("group", "other")

    return {
        "name": skill.get("skill", "").replace("_", " ").title(),
        "description": skill.get(
            "description",
            "Skill relevante para el perfil profesional."
        ),
        "group": group,
        "logo": f"{slugify_group(group)}.svg"
    }


def enrich_skill_list(skills: List[dict]) -> List[Dict]:
    return [enrich_skill(s) for s in skills]


# =========================
# ORCHESTRATOR
# =========================

def analyze_cv_orchestrator(
    text: str,
    salary_params: Dict
) -> Dict:

    # -------------------------
    # 1️⃣ ROLES (TOP 3)
    # -------------------------
    role_result = predict_text(text)

    available_roles = []
    for r in role_result.get("top3", []):
        job = r.get("job_title")
        if not job:
            continue

        available_roles.append({
            "role_id": job,
            "label": prettify_label(job),
            "probability": round(r.get("prob", 0), 2),
        })

    active_role = available_roles[0]["role_id"]

    # -------------------------
    # 2️⃣ SENIORITY
    # -------------------------
    try:
        seniority = predict_seniority_from_text(text)
    except Exception:
        seniority = "Unknown"

    # -------------------------
    # 3️⃣ SKILLS DETECTADAS
    # -------------------------
    raw_skills = extract_skills(text)
    detected_skills = enrich_skill_list(raw_skills)

    raw_skill_names = [s["skill"] for s in raw_skills]

    # -------------------------
    # 4️⃣ SKILLS POR ROL
    # -------------------------
    predicted_job_ids = [r["role_id"] for r in available_roles]

    skills_by_role_raw = skills_for_jobs(
        skills=raw_skill_names,
        predicted_jobs=predicted_job_ids,
    )

    role_insights = {}

    for item in skills_by_role_raw:
        role_id = item["job_title"]

        role_insights[role_id] = {
            "matching_skills": enrich_skill_list(item["matching_skills"]),
            "missing_skills": enrich_skill_list(item["missing_skills"]),
            "matching_skills_count": item["matching_skills_count"],
            "missing_skills_count": item["missing_skills_count"],
        }

    # -------------------------
    # 5️⃣ SALARY
    # -------------------------
    salary = None
    if seniority != "Unknown":
        try:
            salary = predict_salary_from_profile(
                role_label=available_roles[0]["role_id"],
                seniority=seniority,
                **salary_params
            )
        except Exception:
            salary = None

    # -------------------------
    # 6️⃣ FINAL RESPONSE
    # -------------------------
    return {
        "roles": {
            "available_roles": available_roles,
            "active_role": active_role,
        },
        "seniority": seniority,
        "salary": salary,
        "skills": {
            "detected": detected_skills,
        },
        "role_insights": role_insights,
    }
