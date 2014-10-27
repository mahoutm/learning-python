#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB

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

  vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5) 
  
  X_train = vectorizer.fit_transform(X)
  X_test  = vectorizer.transform(X[95:120])
  
  gnb = GaussianNB()
  clf = gnb.fit(X_train.toarray(),Y)
  
  joblib.dump(clf, './model/rep.pkl') 
  clf2 = joblib.load('./model/rep.pkl') 
  
  out = clf2.predict(X_test.toarray())
  
  for i in range(10):
    key = i + 95
    print (str(out[i]) + "   =>    ")
    print (X[key])

