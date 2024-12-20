# -*- coding: utf-8 -*-
"""Sentiment Analysis With SVM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xxGX25q8ou6XYV2rNhsVgTOLb-Ss7YQ4
"""

import pandas as pd

from google.colab import files
uploaded = files.upload()

# Read file
df2 = pd.read_excel('data2.xlsx')

df2

"""##DATA PREPROCESSING

### 1. Data Cleaning
"""

import re
import string

def cleansing(text):
    # Case folding = lower
    text = text.lower()

    # Case folding = remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Case folding = remove whitespace
    text = text.strip()

    # Case folding = remove mention (@username)
    text = re.sub(r'@\w+', '', text)

    # Case folding = remove hashtag (#tag)
    text = re.sub(r'#\w+', '', text)

    # Case folding = remove URL or link
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)

    # Remove ASCII and unicode
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\x00-\x7f]', '', text)

    # Remove newline
    text = text.replace('\n', '')

    return text

df2['Comment'] = df2['Comment'].apply(cleansing)

"""###2. Normalisasi"""

norm = {
    "ok" : "bagus",
    "dgn": "dengan",
    "bgt": "banget",
    "tdk": "tidak",
    "bgmn": "bagaimana",
    "gue" : "saya",
    "gua" : "saya",
    "good" : "bagus",
    "ajah" : "saja",
    "yh" : "ya",
    "dg" : "dengan",
    "keren": "bagus",
    "mantap" : "bagus"
}

def normalisasi(text) :
   for i in norm:
      text = text.replace(i, norm[i])

   return text

df2['Comment'] = df2['Comment'].apply(normalisasi)

"""###3. Filtering (StopWords)"""

pip install 'Sastrawi'

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Create StopWordRemover
factory = StopWordRemoverFactory()
stopwords_remover = factory.create_stop_word_remover()

# Function to remove stopwords
def stopword(text):
    return stopwords_remover.remove(text)

df2['Comment'] = df2['Comment'].apply(stopword)

df2.head()

"""##4. Tokenez"""

def tokenized(text):
    text = text.split()
    return text

tokenized = df2['Comment'].apply(tokenized)

tokenized

"""##5. Stemming"""

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def stemming(Comment):
    stemfactory = StemmerFactory()
    stemmer = stemfactory.create_stemmer()
    stemmed_words = [stemmer.stem(w) for w in Comment]
    d_clean = " ".join(stemmed_words)
    return d_clean

tokenized = tokenized.apply(stemming)

# Save data to csv
tokenized.to_csv('cleandata_1.csv', index=False)

# Download file to laptop
from google.colab import files
files.download('cleandata_1.csv')

# Read file
data_clean = pd.read_csv('cleandata_1.csv')

data_clean

from google.colab import files
uploaded = files.upload()

d1 = pd.read_csv('cleandata_1.csv')
d2 = pd.read_excel('data2.xlsx')
dd2 = d2['label']

result = pd.concat([d1, dd2], axis = 1)

result

"""### The cleansing, stopword and stemming processes can result in empty or missing data."""

missing_values = result['Comment'].isnull().sum()

missing_values

#change the value of missing data to nan
df3 = result.replace('', pd.NA)

#drop the missing value data
df3.dropna(inplace=True)

df3.reset_index(inplace=True)

df3.drop(columns='index', inplace=True)

df3

missing_values_df3 = df3['Comment'].isnull().sum()

missing_values_df3

"""##TF-IDF
Mengukur seberapa sering suatu kata muncul dalam dokumen. Semakin sering kata muncul, semakin tinggi nilai TF-nya.

###split data TF-IDF
"""

from sklearn.model_selection import train_test_split
#Split training and testing data
X_train, X_test, y_train, y_test = train_test_split(df3['Comment'], df3['label'],test_size = 0.2, stratify=df3['label'], random_state = 42)

#For the vctorization, we use the TF-IDF method
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

print(X_train.shape)
print(X_test.shape)

"""##Model SVM"""

#define SVM model
from sklearn import svm
from sklearn.model_selection import cross_val_score

clf = svm.SVC(kernel = 'linear')

#fit and predict model
clf.fit(X_train, y_train)
predict = clf.predict(X_test)

from sklearn.metrics import confusion_matrix, f1_score, recall_score, precision_score, accuracy_score

f1 = f1_score(y_test, predict)
accuracy = accuracy_score(y_test, predict)
precision = precision_score(y_test, predict)
recall = recall_score(y_test, predict)

#Show the classification report
print('f1-score:', f1)
print('Accuracy score:', accuracy)
print('Precision score:', precision)
print('Recall score:', recall)

# results confusion matrix
cm = confusion_matrix(y_test, predict)

cm

tp = cm[1, 1]  # True Positif
fp = cm[0, 1]  # False Positif
fn = cm[1, 0]  # False Negatif
tn = cm[0, 0]  # True Negatif

# Show results
print("True Positif = ", tp, "\nFalse Positif = ", fp, "\nFalse Negatif = ", fn, "\nTrue Negatif = ", tn)

import seaborn as sns
import matplotlib.pyplot as plt

# Show a confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Negatif', 'Positif'], yticklabels=['Negatif', 'Positif'])
plt.ylabel('Aktual')
plt.xlabel('Prediksi')
plt.title('Confusion Matrix')
plt.show()