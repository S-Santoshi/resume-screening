from pypdf import PdfReader
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import spacy
import gensim.downloader as api
from gensim.models import Word2Vec, Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from nltk.tokenize import word_tokenize
nlp = spacy.load("en_core_web_md")

texts=[]
jd_texts=[]
tagged_texts=[]
def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return tokens

for i in range(1,56):
    print(i)
    reader = PdfReader(f'sample_resume/resume{i}.pdf') 
    page = reader.pages[0] 
    text = page.extract_text() 
    text=preprocess_text(text)
    texts.append(text)

jd_files=['jd_cs_jr','jd_ds_jr','jd_fd_jr','jd_pm_jr','jd_qa_jr','jd_cs_sr','jd_ds_sr','jd_fd_sr','jd_pm_sr','jd_qa_sr','jd_ba_jr','jd_ba_jr']

print("Text for Resumes Collected")

for i in jd_files:
    reader = PdfReader(f'sample_resume/{i}.pdf') 
    page = reader.pages[0] 
    text = page.extract_text() 
    start_pos = text.find("Requirements:")
    requirements_section = text[start_pos:]
    jd_text=preprocess_text(requirements_section)
    jd_texts.append(jd_text)

print("Text for JDS Collected")

for i, text in enumerate(texts):
    if i >=0 and i<=11:
        tag="Data science Resume"
    if i>=12 and i<=17:
        tag="Cyber Security Resume"
    if i>=18 and i<=28:
        tag="Project Management Resume"
    if i>=29 and i<=39:
        tag="Front-end Developer Resume"
    if i>=40 and i<=44:
        tag="Quality Testing Resume"
    if i>=45 and i<=54:
        tag="Business Analyst Resume"
    tagged_texts.append(TaggedDocument(words=text, tags=[tag]))

print("Taggs assigned for resume")

for jd_file,text in zip(jd_files,jd_texts):
    if jd_file.startswith("jd_ds"):
        tag="Job description for Data Science"
    elif jd_file.startswith("jd_cs"):
        tag="Job description for Cyber Security"
    elif jd_file.startswith("jd_fd"):
        tag="Job description for Front-end Developer"
    elif jd_file.startswith("jd_pm"):
        tag="Job description for Project Managment"
    elif jd_file.startswith("jd_qa"):
        tag="Job description for Quality Testing"
    tagged_texts.append(TaggedDocument(words=text, tags=[tag]))

print("Taggs assigned for jd")
doc2vec_model = Doc2Vec(vector_size=100, window=5, min_count=1, workers=4, epochs=20)
doc2vec_model.build_vocab(tagged_texts)
doc2vec_model.train(tagged_texts, total_examples=doc2vec_model.corpus_count, epochs=doc2vec_model.epochs)

model_path = "doc2vec_model"
doc2vec_model.save(model_path)
