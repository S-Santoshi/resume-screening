from joblib import load
from helper import *
import numpy as np

# jd_processed = load('ml/models/jd_processed.joblib')
bow_jd = load('models/bow_jd.joblib')
vectorizer = load('models/vectorizer.joblib')
with open('models/selected_features1.npy', 'rb') as f:
    features1 = np.load(f, allow_pickle=True)
w2v_jd = load('models/w2v_jd.joblib')
with open('models/selected_features2.npy', 'rb') as f:
    features2 = np.load(f, allow_pickle=True)
scaler1 = load('models/scaler1.joblib')
scaler2 = load('models/scaler2.joblib')
svr_model_linear_1 = load('models/svr_model_linear_1.joblib')
lr_model_2 = load('models/lr_model_2.joblib')
# knn_model_meta = load('models/knn_model_meta.joblib')

print("**1")
res = pdf2Text("candidate_134.pdf")
res_processed = preprocess_text(res, removeStopWords=True)
data = pd.DataFrame({'job_description': [jd_processed], 'processed_resume': [res_processed]})
data_feature = feature_extract(data)
data_feature1 = data_feature.copy()
data_feature2 = data_feature.copy()
print("**1")
bow_resume = vectorizer.transform(data_feature.processed_resume.values).toarray()
cosine_euclidean_data = np.array([cosine_euclidean(bow_jd[i], bow_resume[i]) for i in range(len(bow_resume))])
data_feature1[["cosine_similarity", "euclidean_distance"]] = cosine_euclidean_data
X_bow_1 = data_feature1.drop(columns=['job_description', 'processed_resume'])
X_bow_2 = pd.DataFrame(bow_jd, columns=['bow_jd_'+str(i) for i in range(1, bow_jd.shape[1]+1)])
X_bow_3 = pd.DataFrame(bow_resume, columns=['bow_resume_'+str(i) for i in range(1, bow_resume.shape[1]+1)])
X_bow = pd.concat([X_bow_1, X_bow_2, X_bow_3], axis=1)
X_bow = X_bow[features1]
w2v_resume = np.array([getAverageWord2Vec(data_feature2.processed_resume.values[0])])
cosine_euclidean_data = np.array([cosine_euclidean(w2v_jd[i], w2v_resume[i]) for i in range(len(w2v_resume))])
data_feature2[["cosine_similarity", "euclidean_distance"]] = cosine_euclidean_data
print("**1")
X_w2v_1 = data_feature2.drop(columns=['job_description', 'processed_resume'])
X_w2v_2 = pd.DataFrame(w2v_jd, columns=['w2v_jd_'+str(i) for i in range(1, w2v_jd.shape[1]+1)])
X_w2v_3 = pd.DataFrame(w2v_resume, columns=['w2v_resume_'+str(i) for i in range(1, w2v_resume.shape[1]+1)])
X_w2v = pd.concat([X_w2v_1, X_w2v_2, X_w2v_3], axis=1)
print("**1")
X_w2v = X_w2v[features2]
X_bow = scaler1.transform(X_bow)
prediction1 = np.round(svr_model_linear_1.predict(X_bow), 2)
prediction2 = np.round(lr_model_2.predict(X_w2v), 2)
X_w2v = scaler2.transform(X_w2v)
X_ensemble = pd.DataFrame({'svr_linear_bow':svr_model_linear_1.predict(X_bow), 
                            'linear_reg_w2v':lr_model_2.predict(X_w2v)})
# scaler3 = load('ml/models/scaler3.joblib')
# X_ensemble = scaler3.transform(X_ensemble)
print("**1")
# prediction = np.round(knn_model_meta.predict(X_ensemble), 2)
# ans=prediction[0]
print(prediction1,prediction2)