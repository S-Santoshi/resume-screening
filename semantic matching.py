from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import torch
import numpy as np

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

job_description = """
We are seeking a talented and experienced Data Scientist to join our team. The ideal candidate will have a passion for turning data into actionable insights and possess strong analytical skills. As a Data Scientist at [Company Name], you will be responsible for analyzing complex datasets, developing predictive models, and delivering insights to drive business decisions.

requirements:
Bachelor's or Master's degree in Computer Science, Statistics, Mathematics, or related field.
Proficiency in programming languages such as Python, R, or SQL.
Strong analytical and problem-solving skills.
Experience with machine learning algorithms and statistical techniques.
Excellent communication and collaboration skills.
Ability to work independently and in a team environment.
"""
# job_description=""""
# We are seeking a passionate and motivated Junior Software Testing Engineer to join our QA team. This is an excellent opportunity for a recent graduate with a strong foundation in software testing methodologies and automation using Python. As a Junior Software Testing Engineer at [Company Name], you will have the opportunity to learn and grow your skills in software testing and automation while ensuring the quality and reliability of our software products.

# Requirements:

# Bachelor's degree in Computer Science, Software Engineering, or related field.
# Strong understanding of software testing fundamentals and methodologies.
# Basic knowledge of programming languages, with a focus on Python for automation.
# Familiarity with automation testing tools such as Selenium, TestNG, or similar is a plus.
# Ability to learn quickly and adapt to new technologies and tools.
# Good analytical and problem-solving skills, with attention to detail.
# Excellent communication and interpersonal skills, with the ability to work effectively in a team environment.
# A strong passion for quality and a desire to contribute to the success of our software products.
# """

job_description="""
We are looking for a dynamic and experienced Human Resources Manager to join our team. The ideal candidate will have a passion for HR management and possess strong interpersonal and organizational skills. As a Human Resources Manager, you will play a key role in supporting our employees and driving initiatives to enhance the employee experience.

Requirements:

Bachelor's or Master's degree in Human Resources Management, Business Administration, or related field.
Proven experience as an HR Manager or in a similar role.
Strong knowledge of HR principles, practices, and regulations.
Excellent interpersonal and communication skills.
Ability to handle confidential information with integrity and discretion.
Strong organizational and time management skills.
Proficiency in HR software and Microsoft Office Suite.
Ability to work independently and collaboratively in a team environment.
"""
##improve resume to add context

with open("resume_formatted.txt","r") as f:
    resume=f.read()

def get_bert_embedding(text):
    encoded_input = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        output = model(**encoded_input)
    cls_embedding = output.last_hidden_state[:, 0, :]
    embedding = cls_embedding.numpy()
    return embedding

def compute_relevance_score(job_description, resume_text):
    job_description_embedding= get_bert_embedding(job_description)
    resume_embedding= get_bert_embedding(resume_text)
    cosine_sim = cosine_similarity(job_description_embedding, resume_embedding)
    relevance_score = np.mean(cosine_sim)
    return relevance_score

relevance_score = compute_relevance_score(job_description, resume)
print("Relevance Score:", relevance_score)
