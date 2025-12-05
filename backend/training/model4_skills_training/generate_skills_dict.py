import pandas as pd

df = pd.read_json("hf://datasets/NxtGenIntern/IT_Job_Roles_Skills_Certifications_Dataset/Top_207_IT_Job_Roles_Skills_Database.json")
df["Skills"] = df["Skills"].apply(lambda x: [s.strip() for s in x.split(",")])
df["Certifications"] = df["Certifications"].apply(lambda x: [c.strip() for c in x.split(",")])

merged_data = {}

for index, row in df.iterrows():
    job = row["Job Title"]
    skills = row["Skills"]          
    certifications = row["Certifications"]  
    
    if job not in merged_data:
        merged_data[job] = {
            "Skills": set(skills),
            "Certifications": set(certifications)
        }
    else:
        merged_data[job]["Skills"].update(skills)
        merged_data[job]["Certifications"].update(certifications)

df = pd.DataFrame({
    "Job Title": list(merged_data.keys()),
    "Skills": [list(v["Skills"]) for v in merged_data.values()],
    "Certifications": [list(v["Certifications"]) for v in merged_data.values()]
})

skill_dict = {}

for index, row in df.iterrows():
    job = row["Job Title"]
    for skill in row["Skills"]:
        skill_lower = skill.lower()
        if skill_lower not in skill_dict:
            skill_dict[skill_lower] = [job]
        else:
            skill_dict[skill_lower].append(job)

import json
with open("skill_dict.json", "w") as f:
    json.dump(skill_dict, f)

