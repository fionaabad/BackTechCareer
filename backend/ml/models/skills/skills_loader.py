import json
from pathlib import Path


def load_skills_info():
    path = Path(__file__).parent / "skills_info.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
