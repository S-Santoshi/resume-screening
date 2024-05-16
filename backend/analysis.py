# Assuming 'new_documents' is a list of new documents (list of lists of words)
from pypdf import PdfReader
import spacy
from gensim.models import Doc2Vec


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

for i in jd_files:
    reader = PdfReader(f'sample_resume/{i}.pdf') 
    page = reader.pages[0] 
    text = page.extract_text() 
    start_pos = text.find("Requirements:")
    requirements_section = text[start_pos:]
    jd_text=preprocess_text(requirements_section)
    jd_texts.append(jd_text)

loaded_model = Doc2Vec.load("doc2vec_model")
li=texts+jd_texts
new_doc_embeddings = [loaded_model.infer_vector(doc) for doc in li]

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
# Assuming doc_embeddings is a list of document embeddings obtained from the Doc2Vec model
# Each document embedding is a high-dimensional vector
new_doc_embeddings_np = np.array(new_doc_embeddings)
print(new_doc_embeddings_np.shape)
# Reduce dimensionality using t-SNE
tsne = TSNE(n_components=2, random_state=42)
doc_embeddings_tsne = tsne.fit_transform(new_doc_embeddings_np)
num_documents = len(doc_embeddings_tsne)

# Generate dummy cluster labels (random integers between 0 and 4)
clusters = np.random.randint(0, 7, size=num_documents)
# Plot the t-SNE embeddings
plt.figure(figsize=(10, 8))
plt.scatter(doc_embeddings_tsne[:, 0], doc_embeddings_tsne[:, 1], marker='o', alpha=0.5)
plt.title('t-SNE Visualization of Document Embeddings')
plt.xlabel('t-SNE Dimension 1')
plt.ylabel('t-SNE Dimension 2')
plt.show()

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score,calinski_harabasz_score
k = 7

kmeans = KMeans(n_clusters=k, random_state=42)
clusters = kmeans.fit_predict(new_doc_embeddings)
silhouette_avg = silhouette_score(new_doc_embeddings, clusters)
print("Silhouette Score:", silhouette_avg)
davies_bouldin_avg = davies_bouldin_score(new_doc_embeddings, clusters)
print("Davies–Bouldin Index:", davies_bouldin_avg)
calinski_harabasz_index = calinski_harabasz_score(new_doc_embeddings, clusters)
print("Calinski-Harabasz Index:", calinski_harabasz_index)


