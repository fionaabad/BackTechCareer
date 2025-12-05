import json

file_path = "BackTechCareer/src/model4_skills_training/skill_dict.json"

with open(file_path, "r") as f:
    skill_dict = json.load(f)


def get_skill_dict():
    resume_skills = input().split(",")
    resume_skills = [s.lower() for s in resume_skills]
    job_match_count = {}
    for skill in resume_skills:
        if skill in skill_dict:
            for job in skill_dict[skill]:
                job_match_count[job] = job_match_count.get(job, 0) + 1
    
    job_match_list = list(job_match_count.items())
    job_match_list.sort(key=lambda item: item[1], reverse=True)
    job_match_sorted = job_match_list
    for job, count in job_match_sorted:
        print(f"{job}: {count} matching skills")















resume_skills = ["C#"]



# Count how many skills match per job
job_match_count = {}

for skill in resume_skills:
    if skill in skill_dict:
        for job in skill_dict[skill]:
            job_match_count[job] = job_match_count.get(job, 0) + 1

job_match_list = list(job_match_count.items())
job_match_list.sort(key=lambda item: item[1], reverse=True)
job_match_sorted = job_match_list
for job, count in job_match_sorted:
    print(f"{job}: {count} matching skills")

print(job_match_sorted)

