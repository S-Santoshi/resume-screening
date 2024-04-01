import re
from sklearn.preprocessing import LabelEncoder
import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from scipy.sparse import hstack
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import re
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics


def preprocess_text(text_to_clean):
    cleaned_text = re.sub('http\S+\s*', ' ', text_to_clean)
    cleaned_text = re.sub('RT|cc', ' ', cleaned_text)
    cleaned_text = re.sub('#\S+', '', cleaned_text)
    cleaned_text = re.sub('@\S+', ' ', cleaned_text)
    cleaned_text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleaned_text)
    cleaned_text = re.sub(r'[^\x00-\x7f]', r' ', cleaned_text)
    cleaned_text = re.sub('\s+', ' ', cleaned_text)
    cleaned_text = cleaned_text.strip()
    return cleaned_text


df = pd.read_csv('UpdatedResumeDataSet.csv')
df['cleaned_text'] = df['Resume'].apply(lambda x:preprocess_text(x))

label = LabelEncoder()
df['encoded_cat'] = label.fit_transform(df['Category'])

text = df['cleaned_text'].values
target = df['encoded_cat'].values
print(df)
word_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    stop_words='english',
    max_features=1500)
word_vectorizer.fit(text)
WordFeatures = word_vectorizer.transform(text)

X_train, X_test, y_train, y_test = train_test_split(WordFeatures, target, random_state=24, test_size=0.2)

model = OneVsRestClassifier(KNeighborsClassifier())
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Training Accuracy   :-", (model.score(X_train, y_train)*100) ,"%")
print("Validation Accuracy :-", (model.score(X_test, y_test)*100),"%")

