import pandas as pd

def extract_skills(text, skills_file="data/skills.csv"):
    skills_df = pd.read_csv(skills_file)
    skills = skills_df["skill"].str.lower().tolist()
    found_skills = [skill for skill in skills if skill in text]
    return list(set(found_skills))
