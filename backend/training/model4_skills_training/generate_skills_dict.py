import pandas as pd
import json

# Load dataset
df = pd.read_json("hf://datasets/NxtGenIntern/IT_Job_Roles_Skills_Certifications_Dataset/Top_207_IT_Job_Roles_Skills_Database.json")

# Split skills and certifications, strip spaces, and lowercase
df["Skills"] = df["Skills"].apply(lambda x: [s.strip().lower() for s in x.split(",")])
df["Certifications"] = df["Certifications"].apply(lambda x: [c.strip().lower() for c in x.split(",")])
df["Job Title"] = df["Job Title"].str.lower()  # lowercase job titles

# Merge duplicates per job
merged_data = {}

for index, row in df.iterrows():
    job = row["Job Title"]
    skills = set(row["Skills"])
    certifications = set(row["Certifications"])

    if job not in merged_data:
        merged_data[job] = {
            "Skills": skills,
            "Certifications": certifications
        }
    else:
        merged_data[job]["Skills"].update(skills)
        merged_data[job]["Certifications"].update(certifications)

# Build skill dictionary: skill -> list of job titles
skill_dict = {}
for job, values in merged_data.items():
    for skill in values["Skills"]:
        if skill not in skill_dict:
            skill_dict[skill] = set()
        skill_dict[skill].add(job)

# Convert sets to lists for JSON
skill_dict = {skill: sorted(list(jobs)) for skill, jobs in skill_dict.items()}

# Save to JSON
with open("skill_dict.json", "w") as f:
    json.dump(skill_dict, f, indent=2)

