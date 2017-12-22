#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Find similarity between title and documents based on cosine similarity
 using NLTL and Lancaster stemmer for preprocessing
 using sklearn to calculate the tf-idf 
 
 RUN 4 Log-Likelihood - Threshold 5
 
"""
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import os
import timeit
import operator

RUNID = "Sheffield-run-4-LL"
#RUNID = 'Test_Data_Sheffield-run-4'

start = 0
end = 0

#to calculate run time
start = timeit.default_timer()


#AUTOMATICLLY CREATE LIST OF TOICS NAMES AND IDS
#*************************************************

folder = 'Training Data/topics_train/'
#folder = 'Test Data/'

topics = [[0 for x in range(3)] for y in range(len(os.listdir(folder)))]
topics_nums = []
topics_ids = []
topics_titles = []

#read each file and extract topic number, id, and title
for i , file in enumerate(os.listdir(folder)):          
    r_file = open(folder + file ,'r', encoding="utf-8")
    lines = r_file.readlines()
    topics[i][0] = (os.path.splitext(file)[0])
    topics[i][1] = (lines[0][7:-2])
    topics[i][2] = (lines[2][7:-2])
    
for j , x in enumerate(topics):
    topics[j][0]=int(x[0])

topics.sort()
   
for x in topics:
    topics_nums.append(x[0])
    topics_ids.append(x[1])
    topics_titles.append(x[2])
    
#read the top words for each topic based on log-likelihood
ll_words = list()
for l in topics_ids:
    ll_path = 'Log_likelihood/Topics - Individual/All words (Thershold 0) without encoded/Training Data/'+ l +'_Threshold_0_without encoded'
    ll_file = open(ll_path,'r').readlines()
    top_words = []
    counter = 0
    for line in ll_file:
        top_words.append(line.split()[0])
        counter += 1
        if counter == 10:
            break
    ll_words.append((l,top_words))
#*************************************************
#*************************************************   

#use PubMed stop words
s_file = open('PubMed_stopwords.txt','r')
PubMed_stopwords = s_file.readlines()
for i, item in enumerate(PubMed_stopwords):
    PubMed_stopwords[i] = PubMed_stopwords[i].strip()
stop_words = set(PubMed_stopwords)

#using lancaster stemmer
stemmer = nltk.stem.lancaster.LancasterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    #remove stop words
    filtered = [w for w in tokens if not w in stop_words]
    #stemmer
    return [stemmer.stem(item) for item in filtered]

def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize)

#create qrel file
qrel_abstract = open("Evaluation/tar-master/training/results/Sheffield-run-4-LL-top-10-thr-0","w+") 
#qrel_abstract = open("output/Test_Data_Sheffield-run-4.4","w+") 


i = 0
size = len(topics_nums)

#loop for all topics
for i in range(0, len(topics_nums)):
    print (i)
    path = '/Users/amal/Desktop/CLEF2017 Data/Training Data Set/Abstracts + MeSH/'+ str(topics_nums[i]) +'/' 
#    path = 'Data/Test Data Set/Abstracts + MeSH/'+ str(topics_nums[i]) +'/' 
    
    # Make a list of files in the directory then read these documents in for later processing
    # (just make this list once so don't need to call the OS more than needed)
    doc_ids = os.listdir(path)
    documents = [open(path+f,'r',encoding="utf-8").read() for f in doc_ids]

    tfidf = vectorizer.fit_transform(documents)
 
    f = open("/Users/amal/Desktop/CLEF2017 Data/Training Data Set/MeSH and terms/terms/" + str(topics_nums[i]) + ".txt")
#    f = open("Data/Test Data Set/MeSH and terms/terms/" + str(topics_nums[i]) + ".txt",encoding="utf-8")
    terms = f.read()
    
    for w in ll_words:
        if w[0] == topics_ids[i]:
            ll_word = w[1]
            break
    ll_word = ' '.join(ll_word)
    
    t = topics_titles[i] + ' ' + terms + ' ' + ll_word
    
    title = vectorizer.transform([t])
    #print(title)
    
    cosine_sim = linear_kernel(title, tfidf).flatten()   

    # Create a dictionary with the filenames as keys and cosine similarity scores as values
    # then print it out in order (sorted by the cosine similarity score)
    doc_sim_values = dict(zip(doc_ids, cosine_sim))

    topic_id = topics_ids[i]
    rank = 1
    for doc, score in sorted(doc_sim_values.items(), key=operator.itemgetter(1), reverse=True):
        doc_id = doc.split('.')[0] # Remove suffix from filename (to leve PID)
        # Print out sorted results in this format: 
        # TOPIC-ID INTERACTION PID RANK SCORE RUN-ID
        qrel_abstract.writelines('{t} NF {d} {r} {s} {i} \n'.format(t=topic_id, d=doc_id, r=rank, s=score, i=RUNID))
        rank = rank + 1


qrel_abstract.close()   
     
end = timeit.default_timer()
print ( (end - start)/60 )
