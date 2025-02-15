import google.generativeai as genai

GOOGLE_API_KEY='AIzaSyBIcnlFK8DcWQFFDm_Axw5OevHwmKxK2VM'

resume_text="""Emma Davis
Amazon Data Scientist
Dynamic data scientist with a strong foundation in machine
learning, data analysis, and problem-solving. Eager to join
Amazon's world-class data science team to leverage data-driven
insights that drive business growth.e.davis@email.com
(123) 456-7890
San Jose, CA
LinkedIn
Work Experience
Adobe-Data Scientist
2018 - current San Jose, CA
Led data analysis initiatives that resulted in a 37% increase in customer retention rates.
Developed predictive models using TensorFlow, reducing forecasting errors by 21%.
Implemented Apache Hadoop to analyze large-scale datasets, improving data processing speed by
33%.
Utilized Pandas and Python for data manipulation, resulting in a 2-hour reduction in data cleaning
time.
Cisco Systems-Junior Data Engineer
2015 - 2018 San Jose, CA
Collaborated with a cross-functional team to develop ETL pipelines, improving data processing
efﬁciency by 26%.
Leveraged Amazon Redshift to optimize data warehouse performance, resulting in a 3-hour reduction
in query execution times.
Automated data ingestion processes using AWS Glue, reducing manual effort by 32%.
Conducted sentiment analysis on customer reviews using NLTK, providing valuable insights to the
marketing team.
eBay-Trainee Data Analyst
2012 - 2015 San Jose, CA
Set up Kafka clusters and integrated data sources, resulting in a 30% improvement in data processing
efﬁciency.
Achieved a $4K reduction in infrastructure costs by containerizing data processing components.
Spearheaded automated deployment scripts and version control using Git, resulting in a 27% decrease
in deployment errors.
Used Python and SQL to clean and preprocess data, achieving a data quality improvement of 18%.
Education
Stanford University-Bachelor of Science,Computer Science
2008 - 2012 Stanford, CA
Skills
Python;Pandas;TensorFlow;Apache Hadoop;Amazon Redshift;AWS;NLTK;Apache Kafka;Git;Docker"""

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
prompt=f"The following is a resume of a candidate \n {resume_text} \n. You are an HR. Generate 5 follow-up questions based on this resume. Rephrase the questions and make them shorter. Do not add any text effects or aestricks in the response"
response = model.generate_content(prompt)
print(response.text)
