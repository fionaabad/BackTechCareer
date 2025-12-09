import os

project_path = "BackTechCareer"  # replace with your project folder

for root, dirs, files in os.walk(project_path):
    level = root.replace(project_path, "").count(os.sep)
    indent = "    " * level
    print(f"{indent}{os.path.basename(root)}/")  # folder
    subindent = "    " * (level + 1)
    for f in files:
        print(f"{subindent}{f}")  # file


