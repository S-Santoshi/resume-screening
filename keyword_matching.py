import json

jd_keywords = {
    "java": 2,
    "selenium": 3,
    "python": 3,
    "web development": 1,
    "test automation": 2,
    "software testing": 2,
    "problem-solving": 1,
    "teamwork": 1,
    "computer science":1
}
# with open('ds_resume.json', 'r') as file:
#     resume = json.load(file)

with open('st_resume.json', 'r') as file:
    resume = json.load(file)

matching_score = 0
total_weight = sum(jd_keywords.values())

technical_skills = resume["skills"]["technical"]
for skill, expertise in technical_skills.items():
    if skill.lower() in jd_keywords:
        skill_weight = jd_keywords[skill.lower()]
        if expertise == "Advanced" and skill_weight<=3:
            matching_score += skill_weight 
        elif expertise == "Intermediate" and skill_weight<=2:
            matching_score += skill_weight
        if expertise == "Beginner" and skill_weight<=1:
            matching_score += skill_weight 

soft_skills = set(resume["skills"]["soft"])
for skill in soft_skills:
    if skill.lower() in jd_keywords:
        matching_score += jd_keywords[skill.lower()]

experience_keywords = []
for education in resume["education"]:
    experience_keywords.append(education["degree"])
for certification in resume["certifications"]:
    experience_keywords.append(certification["name"])
for project in resume["projects"]:
    experience_keywords.append(project["title"])
for keyword in experience_keywords:
    if keyword.lower() in jd_keywords:
        matching_score += jd_keywords[keyword.lower()]

normalized_score = matching_score / total_weight * 100

print("Matching Score:", normalized_score)