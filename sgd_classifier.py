# -*- coding: utf-8 -*-
"""SGD_Classifier.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qf_ZRH0Ajxm1gqMiyR18ezMHIC2w79ch
"""

# Import Section
import csv
import codecs
import sys
import io
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
from nltk.stem.porter import *
!pip install emot
import emot
emot_obj = emot.core.emot()
!pip install langdetect
from langdetect import detect
!pip install unidecode
import unidecode

import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import *

from sklearn.linear_model import SGDClassifier

#Customized Function Definition
def peformStopWordRemoval(text):
  stopWordRemovedText=""
  return stopWordRemovedText

# Data Preprocessing Module
def preProcessingModule(text):
  returnPreProcessedText=""
  getStopWordRemovedText = peformStopWordRemoval(text)
  no_acc = unidecode.unidecode(text)
  text_tokens = word_tokenize(no_acc)
  getStopWordRemovedText = [word for word in text_tokens if not word in stopwords.words()]
  stemmer = PorterStemmer()
  singles = [stemmer.stem(token) for token in getStopWordRemovedText]
  demoticon = emot_obj.emoticons(no_acc)
  filtered_sentence = (" ").join(singles)
  detect(filtered_sentence)
  returnPreProcessedText = filtered_sentence
  return returnPreProcessedText

# Main Function Module
def main():
  tweets = []
  label = []
  csv.field_size_limit(500 * 1024 * 1024)
  with open('/content/IronyDetectionSmall_TrainDataset.txt', 'r') as f:
      next(f) # skip headings
      reader=csv.reader(f, dialect="excel-tab")
      for line in reader:
          #print(line[2])
          #preProcessedTweetText= preProcessingModule(line[2])
          preProcessedTweetText= line[2]
          #print(preProcessedTweetText)
          tweets.append(preProcessedTweetText)
          if(line[1] == '1'):
            label.append('irony')
          else:
            label.append('not irony')
  X_train = np.array(tweets)
  Y_train = np.array(label)
  classifier = Pipeline([
      ('count_vectorizer', CountVectorizer(ngram_range=(1, 3))),
      ('tfidf', TfidfTransformer(norm='l2', use_idf=True, smooth_idf=True)),
      ('clf', SGDClassifier())])
  #train classifier
  classifier.fit(X_train, Y_train)

  testTweets = []
  testLabelGold = []
  with open('/content/IronyDetectionSmall_TestDataset.txt', 'r') as f:
    next(f) # skip headings
    reader=csv.reader(f, dialect="excel-tab")
    for line in reader:
      #print(line[2])
      #preProcessedTweetText= preProcessingModule(line[2])
      preProcessedTweetText= line[2]
      #print(preProcessedTweetText)
      testTweets.append(preProcessedTweetText)
      if(line[1] == '1'):
        testLabelGold.append('irony')
      else:
        testLabelGold.append('not irony')
  #test_label_prediction
  X_test = np.array(testTweets)
  testLabelPredicted = classifier.predict(X_test)
  #print

  #Evaluation
  results = confusion_matrix(testLabelGold, testLabelPredicted)
  print('Confusion Matrix:')
  print(results)
  print('Recall Score:', recall_score(testLabelGold, testLabelPredicted, average=None))
  print('Precision Score:', precision_score(testLabelGold, testLabelPredicted, average=None))
  print('Macro Avg, F1 Score:', f1_score(testLabelGold, testLabelPredicted, average=None))
  print('Accuracy:', accuracy_score(testLabelGold, testLabelPredicted))

  #print('Evaluation report:')
  print(classification_report(testLabelGold, testLabelPredicted))

if __name__ == '__main__':
  main()