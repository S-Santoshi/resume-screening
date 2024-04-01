from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json


jd_keywords = ["java", "selenium", "python", "web development", "test automation", "software testing", "problem-solving", "teamwork","computer science"]
with open('resume.json', 'r') as file:
    resume = json.load(file)
def get_all_values(json_data):
    values = []
    if isinstance(json_data, dict):
        for value in json_data.values():
            values.extend(get_all_values(value))
    elif isinstance(json_data, list):
        for item in json_data:
            values.extend(get_all_values(item))
    else:
        values.append(json_data)

    return values
resume_text = get_all_values(resume)
resume_text=" ".join(resume_text)
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform([resume_text])

matching_score = 0
for keyword in jd_keywords:
    if keyword in tfidf_vectorizer.vocabulary_:
        matching_score += tfidf_matrix[0, tfidf_vectorizer.vocabulary_[keyword]]

print("Matching Score:", matching_score)