#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

import pickle
from sklearn.externals import joblib
import psycopg2


def get_train_data():
  try:
      conn = psycopg2.connect("dbname='uzeni' user='postgres' host='192.168.50.170' password='ant'")
  except:
      print ("I am unable to connect to the database")
  
  cur = conn.cursor()
  cur.execute("SELECT body as data \
                      ,CASE WHEN rep = 'Good' THEN 1 \
                            WHEN rep = 'Bad'  THEN 2 \
                       ELSE 0 END as target \
                      ,rep as target_names \
                 FROM water_korea_train;")
  X=[];Y=[]
  for rec in cur:
      x,y,z = rec
      X.append(x)
      Y.append(y) 
  #    Z.append(z)
  
  conn.commit()
  conn.close()
  return X,Y #,Z


if __name__ == "__main__":

  X, Y = get_train_data() 
  #vec = CountVectorizer()
  #tfidf = TfidfTransformer()
  tfidf = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
  mnb = MultinomialNB()

  #pip = Pipeline([('Vectorizer', vec),('TF-IDF',tfidf), ('Classifier', mnb)])
  pip = Pipeline([('Vectorizer', tfidf), ('Classifier', mnb)])
 
  clf = pip.fit(X,Y)
  joblib.dump(clf, './model/rep.pkl') 
  clf_new = joblib.load('./model/rep.pkl') 

  out = clf_new.predict(X[95:120])
  
  for i in range(10):
    key = i + 95
    print (str(out[i]) + "   =>    ")
    print (X[key])
    
