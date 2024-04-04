# import required libraries

import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso, Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error as mse, r2_score, mean_absolute_error as msa
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler
from joblib import dump


csvData = pd.read_csv('dataset/data.csv')
data_feature = pd.read_csv('data_feature.csv')
with open('bow_resume.npy', 'rb') as f:
    bow_resume = np.load(f, allow_pickle=True)

with open('bow_jd.npy', 'rb') as f:
    bow_jd = np.load(f, allow_pickle=True)

y_bow = data_feature.match_percentage
X_bow_1 = data_feature.drop(columns=['job_description', 'processed_resume', 'match_percentage'])
X_bow_2 = pd.DataFrame(bow_jd, columns=['bow_jd_'+str(i) for i in range(1, bow_jd.shape[1]+1)])
X_bow_3 = pd.DataFrame(bow_resume, columns=['bow_resume_'+str(i) for i in range(1, bow_resume.shape[1]+1)])
X_bow = pd.concat([X_bow_1, X_bow_2, X_bow_3], axis=1)

features = X_bow.columns.to_numpy()
y_bow = y_bow.to_numpy()
X_train_bow, X_test_bow, y_train_bow, y_test_bow = train_test_split(X_bow, y_bow, test_size=0.30, random_state=1)

svr_model_linear = SVR(kernel = 'linear', C = 1.429)
svr_model_linear.fit(X_train_bow, y_train_bow)

csvData = pd.read_csv('dataset/data.csv')
data_feature = pd.read_csv('data_feature2.csv')


with open('w2v_resume.npy', 'rb') as f:
    w2v_resume = np.load(f, allow_pickle=True)


with open('w2v_jd.npy', 'rb') as f:
    w2v_jd = np.load(f, allow_pickle=True)


y_w2v = data_feature.match_percentage
X_w2v_1 = data_feature.drop(columns=['job_description', 'processed_resume', 'match_percentage'])
X_w2v_2 = pd.DataFrame(w2v_jd, columns=['w2v_jd_'+str(i) for i in range(1, w2v_jd.shape[1]+1)])
X_w2v_3 = pd.DataFrame(w2v_resume, columns=['w2v_resume_'+str(i) for i in range(1, w2v_resume.shape[1]+1)])

X_w2v = pd.concat([X_w2v_1, X_w2v_2, X_w2v_3], axis=1)
print(X_w2v.shape)
X_w2v.head(3)
y_w2v = y_w2v.to_numpy()

X_train_w2v, X_test_w2v, y_train_w2v, y_test_w2v = train_test_split(X_w2v, y_w2v, test_size=0.30, random_state=1)

lr_model_2 = Ridge(alpha = 8.287, max_iter=3000)
lr_model_2.fit(X_train_w2v, y_train_w2v)
 
X_ensemble_train = pd.DataFrame({'svr_linear_bow':svr_model_linear.predict(X_train_bow), 

                                'linear_reg_w2v':lr_model_2.predict(X_train_w2v)})
X_ensemble_test = pd.DataFrame({'svr_linear_bow':svr_model_linear.predict(X_test_bow), 

                                'linear_reg_w2v':lr_model_2.predict(X_test_w2v)})


y_ensemble_train = y_train_bow
y_ensemble_test = y_test_bow

knn_model_meta = KNeighborsRegressor(n_neighbors=2)
knn_model_meta.fit(X_ensemble_train, y_ensemble_train)

dump(knn_model_meta,"knn_model")


