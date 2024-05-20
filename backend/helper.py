import spacy
from gensim.models import Doc2Vec
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
import google.generativeai as genai
import shutil
import zipfile
import os

GOOGLE_API_KEY='AIzaSyBIcnlFK8DcWQFFDm_Axw5OevHwmKxK2VM'
# nltk.download('punkt')
loaded_model = Doc2Vec.load("doc2vec_model")
nlp = spacy.load("en_core_web_md")

def unzip_resumes(name):
    if os.path.exists("resumes"):
        shutil.rmtree("resumes")
    os.makedirs("resumes", exist_ok=True)
    with zipfile.ZipFile(name, 'r') as zip_ref:
        zip_ref.extractall("resumes")
        
def get_text(filename):
    reader = PdfReader(filename) 
    page = reader.pages[0] 
    resume_text = page.extract_text() 
    return resume_text

def get_jd_text(filename):
    reader = PdfReader(filename) 
    page = reader.pages[0] 
    jd_text = page.extract_text() 
    start_pos = jd_text.find("Requirements:")
    jd_text = jd_text[start_pos:]
    return jd_text


def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return tokens


def get_embedding(tokens):
    emb = loaded_model.infer_vector(tokens)
    return emb

def get_score(res,jd):
    score = (cosine_similarity(res.reshape(1, -1), jd.reshape(1, -1))[0][0])*100
    return round(score, 2)

def get_question(res_text):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    prompt=f"The following is a resume of a candidate \n {res_text} \n. You are an HR. Generate 5 follow-up questions based on this resume. Rephrase the questions and make them shorter. Add an enter after each question Do not add any text effects or aestricks in the response"
    response = model.generate_content(prompt)
    return response.text
