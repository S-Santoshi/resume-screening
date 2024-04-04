import numpy as np
import pandas as pd
import pdfplumber
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import CountVectorizer
from scipy import stats
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from tqdm import tqdm
def pdf2Text(filename):

    ''' load pdf and return the text'''
    text = ''
    with pdfplumber.open(filename) as pdfObj:
        for page in pdfObj.pages:
            text += page.extract_text()
    return text

jd = pdf2Text('Job description.pdf')

print(jd)
csvData = pd.read_csv('train.csv')

def concat(s):

    '''Concatenate words like "D A T A  S C I E N C E" to get "DATA SCIENCE"'''
    s = ' '+s+' '
    while True:
        x = re.search(r"(\s[a-zA-Z]){2,}\s", s)
        if x==None:
            break
        s = s.replace(x.group(),' '+x.group().replace(' ','')+' ')
    return s
def preprocess_text(x, removeStopWords=False):
    x = str(x).lower()
    x = x.replace("′", "'").replace("’", "'")
    x = x.replace("\n", " ")
    x = concat(x)
    x = re.sub(r"http\S+", "", x)
    x = re.sub(r"\s+b[.]?[ ]?tech[(. /]{1}", " btech bachelor of technology ", x)
    x = re.sub(r"\s+m[.]?[ ]?tech[(. ]{1}", " mtech master of technology ", x)
    x = re.sub(r"\s+b[.]?[ ]?a[(. ]{1}", " ba bachelor of arts ", x)
    x = re.sub(r"\s+m[.]?[ ]?a[(. ]{1}", " ma master of arts ", x)
    x = re.sub(r"\s+b[.]?[ ]?sc[(. ]{1}", " bsc bachelor of science ", x)
    x = re.sub(r"\s+m[.]?[ ]?sc[(. ]{1}", " msc master of science ", x)
    x = re.sub(r"\s+b[.]?[ ]?e[(. ]{1}", " beng bachelor of engineering ", x)
    x = re.sub(r"\s+m[.]?[ ]?e[(. ]{1}", " meng master of engineering ", x)
    x = re.sub(r"\s+b[.]?[ ]?c[.]?[ ]?a[(. ]{1}", " bca bachelor of computer applications ", x)
    x = re.sub(r"\s+m[.]?[ ]?c[.]?[ ]?a[(. ]{1}", " mca master of computer applications ", x)
    x = re.sub(r"\s+b[.]?[ ]?b[.]?[ ]?a[(. ]{1}", " bba bachelor of business administration ", x)
    x = re.sub(r"\s+m[.]?[ ]?b[.]?[ ]?a[(. ]{1}", " mba master of business administration ", x)
    x = x.replace("c++", "cplusplus")
    x = x.replace("c#", "csharp")
    x = x.replace(".net", "dotnet")
    x = re.sub('\W', ' ', x)
    z = []
    for i in x.split():
        if not (removeStopWords and i in stopwords.words('english')):
            lemmatizer = WordNetLemmatizer()
            i = lemmatizer.lemmatize(i)
            z.append(i)
    z = ' '.join(z)
    z = z.strip()
    return z


jd_processed = preprocess_text(jd, removeStopWords=True)

print(jd_processed)
resumes = []

for candidateID in csvData.CandidateID.values:
    resume = pdf2Text('trainResumes/'+candidateID+'.pdf')
    resume_processed = preprocess_text(resume, removeStopWords=True)
    resumes.append(resume_processed)

data = pd.DataFrame({'job_description': [jd_processed]*len(csvData), 'processed_resume': resumes, 'match_percentage': csvData['Match Percentage']})
def feature_extract(data):

    '''extract features'''

    data['resume_word_num'] = data.processed_resume.apply(lambda x: len(x.split()))
    data['total_unique_word_num'] = data.apply(lambda x: len(set(x.job_description.split()).union(set(x.processed_resume.split()))) ,axis=1)
    data['common_word_num'] = data.apply(lambda x: len(set(x.job_description.split()).intersection(set(x.processed_resume.split()))) ,axis=1)
    data['common_word_ratio'] = data['common_word_num'] / data.apply(lambda x: len(set(x.job_description.split()).union(set(x.processed_resume.split()))) ,axis=1)
    data['common_word_ratio_min'] = data['common_word_num'] / data.apply(lambda x: min(len(set(x.job_description.split())), len(set(x.processed_resume.split()))) ,axis=1) 
    data['common_word_ratio_max'] = data['common_word_num'] / data.apply(lambda x: max(len(set(x.job_description.split())), len(set(x.processed_resume.split()))) ,axis=1) 
    data["fuzz_ratio"] = data.apply(lambda x: fuzz.WRatio(x.job_description, x.processed_resume), axis=1)
    data["fuzz_partial_ratio"] = data.apply(lambda x: fuzz.partial_ratio(x.job_description, x.processed_resume), axis=1)
    data["fuzz_token_set_ratio"] = data.apply(lambda x: fuzz.token_set_ratio(x.job_description, x.processed_resume), axis=1)
    data["fuzz_token_sort_ratio"] = data.apply(lambda x: fuzz.token_sort_ratio(x.job_description, x.processed_resume), axis=1)
    data['is_fresher'] = data.processed_resume.apply(lambda x: int('fresher' in x.split()))
    data.fillna(0, inplace=True)
    return data


data_feature = feature_extract(data)

vectorizer = CountVectorizer(ngram_range=(1,3), min_df=4, max_df=.99, binary=True)
vocab_text = np.unique(np.append(data_feature.processed_resume.values, data_feature.job_description.values))
vectorizer.fit(vocab_text)
bow_vocab = np.array(list(vectorizer.vocabulary_.keys()))
with open('bow_vocab.npy', 'wb') as f:
    np.save(f, bow_vocab, allow_pickle=True)

bow_resume = vectorizer.transform(data_feature.processed_resume.values).toarray()
with open('bow_resume.npy', 'wb') as f:
    np.save(f, bow_resume, allow_pickle=True)

bow_jd = vectorizer.transform(data_feature.job_description.values).toarray()
with open('bow_jd.npy', 'wb') as f:
    np.save(f, bow_jd, allow_pickle=True)

def cosine_euclidean(u, v):
    return np.array([np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)), np.linalg.norm(u - v)])


cosine_euclidean_data = np.array([cosine_euclidean(bow_jd[i], bow_resume[i]) for i in range(len(bow_resume))])
data_feature[["cosine_similarity", "euclidean_distance"]] = cosine_euclidean_data

data_feature.to_csv('data_feature.csv', index=False)


data_feature2 = data_feature.drop(columns=['cosine_similarity', 'euclidean_distance'])
w2v_model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
w2v_words = list(w2v_model.key_to_index)
def getAverageWord2Vec(sentence):

    ''' get Average Word2Vec given a sentence'''

    sentence_vector = np.zeros(300)
    count_words = 0
    for word in sentence.split():
        if word in w2v_words:
            vector = w2v_model[word]
            sentence_vector = sentence_vector + vector
            count_words = count_words + 1
    if count_words != 0:
        sentence_vector /= count_words
    return sentence_vector


w2v_resume = []

for sentence in tqdm(data_feature2.processed_resume.values):
    w2v_resume.append(getAverageWord2Vec(sentence))

w2v_resume = np.array(w2v_resume)
print(w2v_resume.shape)

with open('w2v_resume.npy', 'wb') as f:
    np.save(f, w2v_resume, allow_pickle=True)

w2v_jd = []

for sentence in tqdm(data_feature2.job_description.values):
    w2v_jd.append(getAverageWord2Vec(sentence))

w2v_jd = np.array(w2v_jd)
print(w2v_jd.shape)

with open('w2v_jd.npy', 'wb') as f:
    np.save(f, w2v_jd, allow_pickle=True)
cosine_euclidean_data = np.array([cosine_euclidean(w2v_jd[i], w2v_resume[i]) for i in range(len(w2v_resume))])
data_feature2[["cosine_similarity", "euclidean_distance"]] = cosine_euclidean_data
data_feature2.to_csv('data_feature2.csv', index=False)
temp = np.array(data_feature['cosine_similarity'])




import nltk
nltk.download('wordnet')