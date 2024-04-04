from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

resume_text = """
Jane Smith
Master of Science in Data Science, University of Data Science, 2022, GPA: 3.8/4.0
Bachelor of Science in Computer Science, Tech University, 2020, GPA: 3.7/4.0
Technical Skills: Python (Advanced), R (Intermediate), SQL (Intermediate), Machine Learning (Advanced), Deep Learning (Intermediate), Statistical Analysis (Advanced), Data Visualization (Advanced), Big Data Technologies (Hadoop, Spark) (Intermediate), Natural Language Processing (NLP) (Intermediate), Time Series Analysis (Intermediate), Predictive Modeling (Advanced)
Soft Skills: Problem-solving, Critical thinking, Attention to detail, Communication skills, Teamwork, Adaptability, Creativity, Time management
Certifications: Certified Data Scientist (Data Science Institute, 2021), Machine Learning Engineer Certification (Machine Learning Society, 2020)
Projects: Predictive Sales Analysis, Sentiment Analysis of Twitter Data, Customer Churn Prediction
"""

job_description_text = """
We are seeking a talented Software Development Engineer in Test (SDET) to join our dynamic team. As an SDET, you will play a crucial role in ensuring the quality and reliability of our software products through advanced test automation and problem-solving skills. Qualifications: - Bachelor's degree in Computer Science or a related field. - Proficiency in Java, Python, and Selenium for test automation. - Experience with web development technologies and frameworks. - Strong understanding of software testing methodologies and best practices. - Excellent problem-solving skills with a keen attention to detail. - Ability to thrive in a fast-paced, agile environment and adapt to changing priorities. - Effective communication skills and the ability to work collaboratively in a team environment. 
"""

job_description_text="""
We are seeking a talented and experienced Data Scientist to join our team. The ideal candidate will have a passion for turning data into actionable insights and possess strong analytical skills. As a Data Scientist at [Company Name], you will be responsible for analyzing complex datasets, developing predictive models, and delivering insights to drive business decisions. requirements:
Bachelor's or Master's degree in Computer Science, Statistics, Mathematics, or related field. Proficiency in programming languages such as Python, R, or SQL. Strong analytical and problem-solving skills. Experience with machine learning algorithms and statistical techniques. Excellent communication and collaboration skills. Ability to work independently and in a team environment."""
vectorizer = TfidfVectorizer(stop_words='english')
vectorizer.fit([job_description_text])
vector = vectorizer.transform([job_description_text])
Job_Desc = vector.toarray()

vector = vectorizer.transform([resume_text])
aaa = vector.toarray()
neigh = NearestNeighbors(n_neighbors=1)
neigh.fit(aaa) 
NearestNeighbors(algorithm='auto', leaf_size=30)
print(neigh.kneighbors(Job_Desc)[0][0].tolist())
