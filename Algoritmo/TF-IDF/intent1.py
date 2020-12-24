# Python program to read
import os
import re
import sqlite3 
import nltk
import num2words as nw
import numpy as np
import math as mt

def get_data():
  conn = sqlite3.connect("minhouse.db") #Connect to database
  cr = conn.cursor() #Get cursor
  dataset = [ tupla[0] for tupla in cr.execute("SELECT descripcion FROM sjug_juego")] #Obtain the string for each tuple from the query
  conn.close()
  return dataset 

def lower_case(data):
  minus = [desc.lower() for desc in data] #A list of strings
  return minus

#Version using nltk
def tokenize1(texts):
  data = []  #List to keep each string coverted to list 
  for desc in texts:
    tokens = nltk.word_tokenize(desc,"spanish")
    data.append(tokens) 
  return data

def remove_punctuation(texts):
  data = []
  for desc in texts:
    data.append(re.sub(r'[^\w\s]','', desc))
  return data

def single_character(texts):
  data = []
  for desc in texts: ## Could it be for 2 characters?
    no_single = [word for word in desc if len(word) > 2]
    data.append(no_single)
  return data

def convert_number(texts):
  data = []
  for desc in texts:
    data.append([nw.num2words(word,lang="es") if word.isnumeric() \
    		 else word for word in desc])
  return data

def stop_words(texts):
  from nltk.corpus import stopwords
  data = []
  sw = stopwords.words("spanish")
  for desc in texts:
    data.append([word for word in desc if word not in sw])
  return data

def lemmatize(texts):
  from pickle import load
  dt = open("extern/lemmas.pkl","rb")
  lemmas = load(dt)
  dt.close()
  lemmatized = []
  for desc in texts:
    lemmatized.append([lemmas[word] if word in lemmas else \
		  word[:-2] for word in desc])
  return lemmatized

def tag_sentences(texts):
  from pickle import load
  dt = open("extern/tagger.pkl","rb")
  tagger = load(dt)
  dt.close()
  tagged = []
  for desc in texts:
    desc_tagged = tagger.tag(desc) #List of tuples (word,tag) for each description
    desc_tagged = [pair[0]+" "+pair[1][0] for pair in desc_tagged] #Simple 'string tag' instead of a tuple
    desc_tagged = [wordtag.lower() for wordtag in desc_tagged] #Lower each word+tag
    tagged.append(desc_tagged)
  return tagged

def get_vocabulary(texts):
  voc = set()
  for desc in texts:
    voc.update(set(desc))
  voc = sorted(voc) #Comment for a set type
  return voc

def preprocess(data):
    data = lower_case(data) #Lowercase each string
    data = remove_punctuation(data) #Remove dots and punctuation on each string
    data = tokenize1(data) #Convert each string to a list of words
    data = convert_number(data) #Convert numbers to its word's representation
    data = single_character(data) #Remove words of len 1
    data = stop_words(data) #Remove stopwords
    data = tag_sentences(data)
    data = lemmatize(data) #Lemmatize the data
    return data

def get_dict(voc):
  dict = {word:0 for word in voc}
  return dict


def tf_idf(texts,voc):
  N = len(texts)
  voc = sorted(voc)
  dimension = len(voc)
  """ Create a dictionary of positions """
  positions = {}
  for i in range(dimension):
    positions[voc[i]] = i
  """ Getting the DF """
  DF = {}
  for i in range(N):
    desc = texts[i] #Take each description
    for word in desc:
        try:
            DF[word].add(i) #Makes a set of ids from descriptions the word is in
        except:
            DF[word] = {i}  #If have not been seen create a new entry
  for word in DF:
    DF[word] = len(DF[word]) # Replace the set with its length
  #Make DF vector
  df_vect = np.zeros(dimension,dtype=float)
  """ Change later"""
  for word in DF:
     index = positions[word]
     df_vect[index] = DF[word]
  df_vect = df_vect + 1
  """
  print("DF vector + 1:",df_vect)
  dim_vect = np.full(dimension,N,dtype=float)
  print("N vector:",dim_vect)
  idf_vect = np.log(np.divide(dim_vect,df_vect))
  print(idf_vect)
  """
  idf_vect = np.log(N/df_vect)
  """ Getting the TF """
  tf = [] #This list has a size of len(texts), each position is a vector
  for i in range(N):
    desc_vect = np.zeros(dimension,dtype=int)
    desc = texts[i]
    for word in desc:
      index = positions[word]
      desc_vect[index] += 1
    desc_vect = desc_vect / len(desc) ## Divide by description length
    tf.append(desc_vect)
  tf_idf = []
  print(len(tf))
  for i in range(N):
    tfidf_vect = np.multiply(tf[i],idf_vect)
    tf_idf.append(tfidf_vect) 
  print(tf_idf[2])
  return tf_idf 

if __name__ == "__main__":
  texts = get_data()
  min_texts = texts[0:11]
  min_texts = preprocess(min_texts)
  voc = get_vocabulary(min_texts)
  print("El vocabulario tiene longitud de:",len(voc))
  vec_tfidf = tf_idf(min_texts,voc)
  print(type(vec_tfidf[2]))
  print(vec_tfidf[2])
  #coseno = np.dot(vec_1,vec_2) / \
  #     ( ( np.sqrt(np.sum(vec_1**2)) ) * ( np.sqrt(np.sum(vec_2**2)) ) )
