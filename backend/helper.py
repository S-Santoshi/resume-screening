import spacy
from spacy.tokens import Doc
# from spacy.lang.en.stop_words import STOP_WORDS
# import nltk
from gensim.models import Word2Vec, Doc2Vec
from sklearn.metrics.pairwise import cosine_similarity
# nltk.download('punkt')

from nltk.tokenize import word_tokenize
nlp = spacy.load("en_core_web_md")

print("Started")
from pypdf import PdfReader
reader = PdfReader('sample_resume/resume40.pdf') 
page = reader.pages[0] 
resume_text = page.extract_text() 

reader = PdfReader('sample_resume/jd_fd_jr.pdf') 
page = reader.pages[0] 
jd_text = page.extract_text() 
start_pos = jd_text.find("Requirements:")
jd_text = jd_text[start_pos:]
print("Text Recieved")

def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return tokens

preprocessed_resume = preprocess_text(resume_text)
preprocessed_jd = preprocess_text(jd_text)
loaded_model = Doc2Vec.load("doc2vec_model")

resume_doc_embedding = loaded_model.infer_vector(preprocessed_resume)
jd_doc_embedding = loaded_model.infer_vector(preprocessed_jd)
doc_similarity_score = cosine_similarity(resume_doc_embedding.reshape(1, -1), jd_doc_embedding.reshape(1, -1))[0][0]
print("Cosine Similarity Score (Doc Embeddings):", doc_similarity_score)