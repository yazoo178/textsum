#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculate log-likelihood for individual topics (CLEF2017 Dataset)
by Amal
last updated 27 Oct 2017

"""
import os
from collections import Counter
import nltk, string
import math
import xlsxwriter
import timeit


print('**** CLEF 2017 ***')
print('Calculate Log-Likelihood')
print('1. Individual topics.')
print('2. Combined topics.')
print('3. Combined average (encoded).')
print('4. Combined average.')
print('5. Combined Max (encoded).')
print('6. Combined Max.')
choice = input('Enter your choice:')
try:
    choice = int(choice)
except ValueError:
    print('Invalid number ..')
    quit()
    
print('1. MeSH.')
print('2. encoded MeSH.')
m_choice = input('Enter your choice:')
try:
    m_choice = int(m_choice)
except ValueError:
    print('Invalid number ..')
    quit()

#threshold represent the number of word repetetion to exclude those word less than threshold from dictionary when calculate the LL
threshold = input('Enter the threshold (exclude words occur less than the threshold):')
try:
    threshold = int(threshold)
except ValueError:
    print('Invalid number ..')
    quit()

source_folder = '/Users/amal/Desktop/Data/CLEF2017/'    
    
#to calculate run time
start = timeit.default_timer()

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


#AUTOMATICLLY CREATE LIST OF TOICS NAMES AND IDS
#*************************************************

folder = 'TrainingData/topics_train/'
#folder = 'Test Data/'

topics = [[0 for x in range(2)] for y in range(len(os.listdir(folder)))]
topics_nums = []
topics_ids = []
topics_titles = []

#read each file and extract topic number, id, and title
for i , file in enumerate(os.listdir(folder)):          
    r_file = open(folder + file ,'r', encoding="utf-8")
    lines = r_file.readlines()
    topics[i][0] = (os.path.splitext(file)[0])
    topics[i][1] = (lines[0][7:-2])
    
for j , x in enumerate(topics):
    topics[j][0]=int(x[0])

topics.sort()
   
for x in topics:
    topics_nums.append(x[0])
    topics_ids.append(x[1])

#*************************************************
#*************************************************   

if choice == 1: #Individual topics
    LL_all = list()
    limit = 0
    for topic in topics: 
        print('processing topic .. ' + str(topic[0]))
        #list of relevant PMID , list of non-relevant PMID
        rel = []
        non_rel = []
        
        path_ = 'TrainingData/qrel_abs_train.txt'
        file = open(path_,'r').readlines()
    
        for line in file:
            if line.split()[0] == topic[1] :
                if line.split()[3] == '1':
                    rel.append(line.split()[2])
                else:
                    non_rel.append(line.split()[2])
                           
        #content of relevent documnts, content of non-relevent documnts         
        text_rel , text_non_rel = '',''
        
        #for each PMID : abstract + encoded MeSH
        doc_path = source_folder + 'TrainingDataset/Abstracts/' + str(topic[0]) + '/'
        mesh_path = source_folder + 'TrainingDataset/MeSHs/encoded/' + str(topic[0]) + '/'
    
        #craete list contains content of the documents
        rel_documents = [] #[open(doc_path+f+'.txt','r',encoding="ISO-8859-1").read() for f in rel]
        non_rel_documents = [] #[open(doc_path+f+'.txt','r',encoding="ISO-8859-1").read() for f in non_rel]
       
        #read documnts   
        for file in (os.listdir(doc_path)):
            mesh = open(mesh_path + file ,'r').read()
            temp_text = open(doc_path+file,'r').read() + ' ' + mesh + ' '
            if file.split('.')[0] in rel:
                text_rel = text_rel + temp_text
                rel_documents.append(temp_text)
            else:
                text_non_rel = text_non_rel + temp_text
                non_rel_documents.append(temp_text)
        
        #Preprocessing (lowercase - stop word removal - Stemming)
        text_rel = str(normalize(text_rel)).replace('\'','')
        text_non_rel = str(normalize(text_non_rel)).replace('\'','')
        
        #Create Dictionary from relevant text 
        rel_dic = dict(Counter(text_rel.replace(',', '').replace('.', '').split()))
        
        #remove words that appear less than threshold
        rel_dic = { d_word:rep for d_word,rep in rel_dic.items() if rep >= threshold }
        
        #sort the dictionary
        rel_dic_sorted = sorted(rel_dic, key=lambda c:rel_dic[c], reverse=True)

        #Preprocessing (lowercase - stop word removal - Stemming)
        for i , rel_d in enumerate(rel_documents):
            rel_documents[i] = str(normalize(rel_documents[i])).replace('\'','')
            
        for j , non_rel_d in enumerate(non_rel_documents):
            non_rel_documents[j] = str(normalize(non_rel_documents[j])).replace('\'','')
                
        total_rel = len(rel)
        total_non_rel = len(non_rel)
        
        #relevant documents 
        frq_word_rel_doc = list()
        
        #count how many relevant documents conatin the word
        for word in rel_dic_sorted:
            count = 0
            for doc in rel_documents:
                if word in doc:
                    count += 1
            # word, no of relevant documents contain word , no of relevant documents not contin word
            frq_word_rel_doc.append((word,count,len(rel_documents)-count))
            
        #non-relevant documents
        frq_word_non_rel_doc = list()
        
        #count how many non-relevant documents conatin the word
        for word in rel_dic_sorted:
            count = 0
            for doc in non_rel_documents:
                if word in doc:
                    count += 1
            # word, no of non-relevant documents contain word , no of non-relevant documents not contin word
            frq_word_non_rel_doc.append((word,count,len(non_rel_documents)-count))
        
        #calculate the log-likelihood 
        #G2 = 2*((a*ln(a/E1))+(b*ln(b/E2)))
        #E1 = c*(a+b)/(c+d) and E2 = d*(a+b)/(c+d)
        #a = the frequency of word in Corpus 1 (relevent text)
        #b = the frequency of word in Corpus 2 (non-relevent text)
        #c = size of corpus1 (The total number of opportunities for word to coccur in Corpus 1 (i.e. the number of times it occurred, plus the number of times it could have occurred but didn't);
        #d = size of corpus2
        
        log_likelihood = list()
                
        obsereved = list()
        
        for i, word in enumerate(frq_word_rel_doc):
            #E1, E2
            o1 = total_rel * (frq_word_rel_doc[i][1] + frq_word_non_rel_doc[i][1])/(total_rel + total_non_rel)
            o2 = total_non_rel * (frq_word_rel_doc[i][1] + frq_word_non_rel_doc[i][1])/(total_rel + total_non_rel)
            obsereved.append((frq_word_rel_doc[i][0], o1 , o2))
        
        
        for j, word in enumerate(obsereved):
            #if a == 0
            if frq_word_rel_doc[j][1] == 0:
                ln_value1 = 0
            else:
                ln_value1 = (math.log(frq_word_rel_doc[j][1]/obsereved[j][1]))
           
            #if b == 0    
            if frq_word_non_rel_doc[j][1] == 0:
                ln_value2 = 0
            else:
                ln_value2 = (math.log(frq_word_non_rel_doc[j][1]/obsereved[j][2]))
                
            LL =  2 * ( (frq_word_rel_doc[j][1] * ln_value1)  +  (frq_word_non_rel_doc[j][1] * ln_value2 ))
            
            log_likelihood.append((obsereved[j][0],LL))
        
        LL_sorted = sorted(log_likelihood,key=lambda l:l[1], reverse=True)
        LL_all.append((topic[1],LL_sorted))
    
    #write results into txt + xlsx files
    for i, topic in enumerate(LL_all):
        new_folder = 'LogLikelihood/TopicsIndividual/Thershold_' + str(threshold) +'/TrainingData/'
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
            
        file = open(new_folder + LL_all[i][0] + '_Threshold_' + str(threshold) , 'w+')
        workbook = xlsxwriter.Workbook(new_folder + LL_all[i][0] + '_Threshold_' + str(threshold) +'.xlsx')
        worksheet = workbook.add_worksheet()
        
        temp = LL_all[i][1]
        
        row = 0
        col = 0
        
        for w, ll in (temp):
            worksheet.write(row, col,     w)
            worksheet.write(row, col + 1, ll)
            row += 1
        workbook.close()
    
        for j, item in enumerate(temp): 
            #file.writelines('{w} {ll} \n'.format(w=temp[j][0], ll= temp[j][1]))
            file.writelines('{w} {ll} \n'.format(w=temp[j][0], ll= "%.2f" % temp[j][1]))
        file.close()

#***************************************************************************
#***************************************************************************
        
elif choice == 2: #Combined topics
    text_rel , text_non_rel = '',''

    rel_documents = list()
    non_rel_documents = list()
    
    for topic in topics:    
        print('processing topic .. ' + str(topic[0]))
        rel = []
        non_rel = []
        
        path_ = 'TrainingData/qrel_abs_train.txt'        
        file = open(path_,'r').readlines()
    
        for line in file:
            if line.split()[0] == topic[1] :
                if line.split()[3] == '1':
                    rel.append(line.split()[2])
                else:
                    non_rel.append(line.split()[2])
                               
        doc_path = source_folder + 'TrainingDataset/Abstracts/' + str(topic[0]) + '/'            
        mesh_path = source_folder + 'TrainingDataset/MeSHs/encoded/' + str(topic[0]) + '/'
    
        # read documnts   
        for file in (os.listdir(doc_path)):
            mesh = open(mesh_path + file ,'r').read()
            temp_text = open(doc_path+file,'r').read() + ' ' + mesh + ' ' 
            if file.split('.')[0] in rel:
                text_rel = text_rel + temp_text
                rel_documents.append(temp_text)
            else:
                text_non_rel = text_non_rel + temp_text
                non_rel_documents.append(temp_text)
            
    #Create Dictionary
    rel_dic = dict(Counter(text_rel.replace(',', '').replace('.', '').split()))
    
    #remove words that appear less than threshold
    rel_dic = { d_word:rep for d_word,rep in rel_dic.items() if rep >= threshold }
    
    #sort the relevant dic        
    rel_sorted = sorted(rel_dic, key=lambda c:rel_dic[c], reverse=True)
    
    relevent = 0
    non_relevant = 0
    frq = list()
    
    total_rel = len(rel_documents) #no of relevant documents
    total_non_rel = len(non_rel_documents) #no of  non-relevant documents
    
    #relevant documents
    frq_word_rel_doc = list()
    
    #count how many relevant documents conatin the word
    for word in rel_sorted:
        count = 0
        for doc in rel_documents:
            if word in doc:
                count += 1
        # word, no of relevant documents contain word , no of relevant documents not contin word
        frq_word_rel_doc.append((word,count,len(rel_documents)-count))
        
    #non-relevant documents
    frq_word_non_rel_doc = list()
    
    #count how many non-relevant documents conatin the word
    for word in rel_sorted:
        count = 0
        for doc in non_rel_documents:
            if word in doc:
                count += 1
        # word, no of non-relevant documents contain word , no of non-relevant documents not contin word
        frq_word_non_rel_doc.append((word,count,len(non_rel_documents)-count))
    
    
    obsereved = list()
    
    for i, word in enumerate(frq_word_rel_doc):
        o1 = total_rel * (frq_word_rel_doc[i][1] + frq_word_non_rel_doc[i][1])/(total_rel + total_non_rel)
        o2 = total_non_rel * (frq_word_rel_doc[i][1] + frq_word_non_rel_doc[i][1])/(total_rel + total_non_rel)
        obsereved.append((frq_word_rel_doc[i][0], o1 , o2))
    
    
    #calculate the log-likelihood 
    log_likelihood = list()
    j = 0
    for j, word in enumerate(obsereved):
        if frq_word_rel_doc[j][1] == 0 or obsereved[j][1] == 0:
            ln_value1 = 0
        else:
            ln_value1 = (math.log(frq_word_rel_doc[j][1]/obsereved[j][1]))
            
        if frq_word_non_rel_doc[j][1] == 0 or obsereved[j][2] == 0:
            ln_value2 = 0
        else:
            ln_value2 = (math.log(frq_word_non_rel_doc[j][1]/obsereved[j][2]))
            
        LL =  2 * ( (frq_word_rel_doc[j][1] * ln_value1)  +  (frq_word_non_rel_doc[j][1] * ln_value2 ))
        
        log_likelihood.append((obsereved[j][0],LL))
    
    LL_sorted = sorted(log_likelihood,key=lambda l:l[1], reverse=True)
      
    #write the results into txt + xlsx files
    new_folder = 'LogLikelihood/TopicsCombined/' 
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    file = open(new_folder + 'LL_TrainingData (Threshold ' + str(threshold) + ')', 'w+')
    workbook = xlsxwriter.Workbook(new_folder + 'LL_TrainingData (Threshold ' + str(threshold) + ').xlsx')
    worksheet = workbook.add_worksheet()
    
    row = 0
    col = 0
    
    for w, ll in (LL_sorted):
        worksheet.write(row, col,     w)
        worksheet.write(row, col + 1, ll)
        row += 1
    workbook.close()
    
    j = 0
    for j, item in enumerate(LL_sorted): 
        file.writelines('{w} {ll} \n'.format(w=LL_sorted[j][0], ll= "%.2f" % LL_sorted[j][1]))
    
    file.close()
    
#***************************************************************************    
#***************************************************************************

elif choice == 3 : #average
    LL_all = list()
    limit = 0
    for topic in topics: 
        print('processing topic .. ' + str(topic[0]))
        #list of relevant PMID , list of non-relevant PMID
        rel = []
        non_rel = []
        
        path_ = 'TrainingData/qrel_abs_train.txt'
        file = open(path_,'r').readlines()
    
        for line in file:
            if line.split()[0] == topic[1] :
                if line.split()[3] == '1':
                    rel.append(line.split()[2])
                else:
                    non_rel.append(line.split()[2])
                           
        #content of relevent documnts, content of non-relevent documnts         
        text_rel , text_non_rel = '',''
        
        #for each PMID : abstract + encoded MeSH
        doc_path = source_folder + 'TrainingDataset/Abstracts/' + str(topic[0]) + '/'
        mesh_path = source_folder + 'TrainingDataset/MeSHs/encoded/' + str(topic[0]) + '/'
    
        #craete list contains content of the documents
        rel_documents = [] #[open(doc_path+f+'.txt','r',encoding="ISO-8859-1").read() for f in rel]
        non_rel_documents = [] #[open(doc_path+f+'.txt','r',encoding="ISO-8859-1").read() for f in non_rel]
       
        #read documnts   
        for file in (os.listdir(doc_path)):
            mesh = open(mesh_path + file ,'r').read()
            temp_text = open(doc_path+file,'r').read() + ' ' + mesh + ' '
            if file.split('.')[0] in rel:
                text_rel = text_rel + temp_text
                rel_documents.append(temp_text)
            else:
                text_non_rel = text_non_rel + temp_text
                non_rel_documents.append(temp_text)
        
        #Preprocessing (lowercase - stop word removal - Stemming)
        text_rel = str(normalize(text_rel)).replace('\'','')
        text_non_rel = str(normalize(text_non_rel)).replace('\'','')
        
        #Create Dictionary from relevant text 
        rel_dic = dict(Counter(text_rel.replace(',', '').replace('.', '').split()))
        
        #remove words that appear less than threshold
        rel_dic = { d_word:rep for d_word,rep in rel_dic.items() if rep >= threshold }
        
        #sort the dictionary
        rel_dic_sorted = sorted(rel_dic, key=lambda c:rel_dic[c], reverse=True)

        #Preprocessing (lowercase - stop word removal - Stemming)
        for i , rel_d in enumerate(rel_documents):
            rel_documents[i] = str(normalize(rel_documents[i])).replace('\'','')
            
        for j , non_rel_d in enumerate(non_rel_documents):
            non_rel_documents[j] = str(normalize(non_rel_documents[j])).replace('\'','')
                
        total_rel = len(rel)
        total_non_rel = len(non_rel)
        
        #relevant documents 
        frq_word_rel_doc = list()
        
        #count how many relevant documents conatin the word
        for word in rel_dic_sorted:
            count = 0
            for doc in rel_documents:
                if word in doc:
                    count += 1
            # word, no of relevant documents contain word , no of relevant documents not contin word
            frq_word_rel_doc.append((word,count,len(rel_documents)-count))
            
        #non-relevant documents
        frq_word_non_rel_doc = list()
        
        #count how many non-relevant documents conatin the word
        for word in rel_dic_sorted:
            count = 0
            for doc in non_rel_documents:
                if word in doc:
                    count += 1
            # word, no of non-relevant documents contain word , no of non-relevant documents not contin word
            frq_word_non_rel_doc.append((word,count,len(non_rel_documents)-count))
        
        #calculate the log-likelihood 
        #G2 = 2*((a*ln(a/E1))+(b*ln(b/E2)))
        #E1 = c*(a+b)/(c+d) and E2 = d*(a+b)/(c+d)
        #a = the frequency of word in Corpus 1 (relevent text)
        #b = the frequency of word in Corpus 2 (non-relevent text)
        #c = size of corpus1 (The total number of opportunities for word to coccur in Corpus 1 (i.e. the number of times it occurred, plus the number of times it could have occurred but didn't);
        #d = size of corpus2
        
        log_likelihood = list()
                
        obsereved = list()
        
        for i, word in enumerate(frq_word_rel_doc):
            #E1, E2
            o1 = total_rel * (frq_word_rel_doc[i][1] + frq_word_non_rel_doc[i][1])/(total_rel + total_non_rel)
            o2 = total_non_rel * (frq_word_rel_doc[i][1] + frq_word_non_rel_doc[i][1])/(total_rel + total_non_rel)
            obsereved.append((frq_word_rel_doc[i][0], o1 , o2))
        
        
        for j, word in enumerate(obsereved):
            #if a == 0
            if frq_word_rel_doc[j][1] == 0:
                ln_value1 = 0
            else:
                ln_value1 = (math.log(frq_word_rel_doc[j][1]/obsereved[j][1]))
           
            #if b == 0    
            if frq_word_non_rel_doc[j][1] == 0:
                ln_value2 = 0
            else:
                ln_value2 = (math.log(frq_word_non_rel_doc[j][1]/obsereved[j][2]))
                
            LL =  2 * ( (frq_word_rel_doc[j][1] * ln_value1)  +  (frq_word_non_rel_doc[j][1] * ln_value2 ))
            
            log_likelihood.append((obsereved[j][0],LL))
        
        LL_sorted = sorted(log_likelihood,key=lambda l:l[1], reverse=True)
        LL_all.append((topic[1],LL_sorted))
        
        combained_list = list()
        
        for i,record in enumerate(LL_all): 
            for j,t in enumerate(LL_all[i][1]): 
                combained_list.append((t[0],t[1])) 
                
        d = {}
        for tuple in combained_list:
            key,val = tuple
            d.setdefault(key, []).append(val)
         
        #write the results into txt + xlsx files
        new_folder = 'LogLikelihood/TopicsCombined/' 
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        file = open(new_folder + 'Aver_LL_TrainingData (Threshold ' + str(threshold) + ')', 'w+')
        workbook = xlsxwriter.Workbook(new_folder + 'Aver_LL_TrainingData (Threshold ' + str(threshold) + ').xlsx')
        worksheet = workbook.add_worksheet()
        
        row = 0
        col = 0
        
        for word , value in d.items():
            worksheet.write(row, col,  word)
            worksheet.write(row, col + 1, (sum(value)/len(value)))
            row += 1
        workbook.close()
        
        for word, value in d.items():
            v = sum(value)/len(value)
            file.writelines('{w} {avg} \n'.format(w=word, avg= str(v)))
        
        file.close()  

#***************************************************************************    
#***************************************************************************

elif choice == 4 : #average - without encoded
    LL_all = list()
    limit = 0
    for topic in topics: 
        print('processing topic .. ' + str(topic[0]))
        #list of relevant PMID , list of non-relevant PMID
        rel = []
        non_rel = []
        
        path_ = 'TrainingData/qrel_abs_train.txt'
        file = open(path_,'r').readlines()
    
        for line in file:
            if line.split()[0] == topic[1] :
                if line.split()[3] == '1':
                    rel.append(line.split()[2])
                else:
                    non_rel.append(line.split()[2])
                           
        #content of relevent documnts, content of non-relevent documnts         
        text_rel , text_non_rel = '',''
        
        #for each PMID : abstract + encoded MeSH
        doc_path = source_folder + 'TrainingDataset/AbstractsMesh/' + str(topic[0]) + '/'
    
        #craete list contains content of the documents
        rel_documents = [] #[open(doc_path+f+'.txt','r',encoding="ISO-8859-1").read() for f in rel]
        non_rel_documents = [] #[open(doc_path+f+'.txt','r',encoding="ISO-8859-1").read() for f in non_rel]
       
        #read documnts   
        for file in (os.listdir(doc_path)):
            temp_text = open(doc_path+file,'r').read() + ' '
            if file.split('.')[0] in rel:
                text_rel = text_rel + temp_text
                rel_documents.append(temp_text)
            else:
                text_non_rel = text_non_rel + temp_text
                non_rel_documents.append(temp_text)
        
        #Preprocessing (lowercase - stop word removal - Stemming)
        text_rel = str(normalize(text_rel)).replace('\'','')
        text_non_rel = str(normalize(text_non_rel)).replace('\'','')
        
        #Create Dictionary from relevant text 
        rel_dic = dict(Counter(text_rel.replace(',', '').replace('.', '').split()))
        
        #remove words that appear less than threshold
        rel_dic = { d_word:rep for d_word,rep in rel_dic.items() if rep >= threshold }
        
        #sort the dictionary
        rel_dic_sorted = sorted(rel_dic, key=lambda c:rel_dic[c], reverse=True)

        #Preprocessing (lowercase - stop word removal - Stemming)
        for i , rel_d in enumerate(rel_documents):
            rel_documents[i] = str(normalize(rel_documents[i])).replace('\'','')
            
        for j , non_rel_d in enumerate(non_rel_documents):
            non_rel_documents[j] = str(normalize(non_rel_documents[j])).replace('\'','')
                
        total_rel = len(rel)
        total_non_rel = len(non_rel)
        
        #relevant documents 
        frq_word_rel_doc = list()
        
        #count how many relevant documents conatin the word
        for word in rel_dic_sorted:
            count = 0
            for doc in rel_documents:
                if word in doc:
                    count += 1
            # word, no of relevant documents contain word , no of relevant documents not contin word
            frq_word_rel_doc.append((word,count,len(rel_documents)-count))
            
        #non-relevant documents
        frq_word_non_rel_doc = list()
        
        #count how many non-relevant documents conatin the word
        for word in rel_dic_sorted:
            count = 0
            for doc in non_rel_documents:
                if word in doc:
                    count += 1
            # word, no of non-relevant documents contain word , no of non-relevant documents not contin word
            frq_word_non_rel_doc.append((word,count,len(non_rel_documents)-count))
        
        #calculate the log-likelihood 
        #G2 = 2*((a*ln(a/E1))+(b*ln(b/E2)))
        #E1 = c*(a+b)/(c+d) and E2 = d*(a+b)/(c+d)
        #a = the frequency of word in Corpus 1 (relevent text)
        #b = the frequency of word in Corpus 2 (non-relevent text)
        #c = size of corpus1 (The total number of opportunities for word to coccur in Corpus 1 (i.e. the number of times it occurred, plus the number of times it could have occurred but didn't);
        #d = size of corpus2
        
        log_likelihood = list()
                
        obsereved = list()
        
        for i, word in enumerate(frq_word_rel_doc):
            #E1, E2
            o1 = total_rel * (frq_word_rel_doc[i][1] + frq_word_non_rel_doc[i][1])/(total_rel + total_non_rel)
            o2 = total_non_rel * (frq_word_rel_doc[i][1] + frq_word_non_rel_doc[i][1])/(total_rel + total_non_rel)
            obsereved.append((frq_word_rel_doc[i][0], o1 , o2))
        
        
        for j, word in enumerate(obsereved):
            #if a == 0
            if frq_word_rel_doc[j][1] == 0:
                ln_value1 = 0
            else:
                ln_value1 = (math.log(frq_word_rel_doc[j][1]/obsereved[j][1]))
           
            #if b == 0    
            if frq_word_non_rel_doc[j][1] == 0:
                ln_value2 = 0
            else:
                ln_value2 = (math.log(frq_word_non_rel_doc[j][1]/obsereved[j][2]))
                
            LL =  2 * ( (frq_word_rel_doc[j][1] * ln_value1)  +  (frq_word_non_rel_doc[j][1] * ln_value2 ))
            
            log_likelihood.append((obsereved[j][0],LL))
        
        LL_sorted = sorted(log_likelihood,key=lambda l:l[1], reverse=True)
        LL_all.append((topic[1],LL_sorted))
        
        combained_list = list()
        
        for i,record in enumerate(LL_all): 
            for j,t in enumerate(LL_all[i][1]): 
                combained_list.append((t[0],t[1])) 
        #create new dictionary cobmined words from all topics relevant dictionaries         
        d = {}
        for tuple in combained_list:
            key,val = tuple
            d.setdefault(key, []).append(val)
            
        #write the results into txt + xlsx files
        new_folder = 'LogLikelihood/TopicsCombined/' 
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        file = open(new_folder + 'Aver_LL_TrainingData (Threshold ' + str(threshold) + ')', 'w+')
        workbook = xlsxwriter.Workbook(new_folder + 'Aver_LL_TrainingData (Threshold ' + str(threshold) + ').xlsx')
        worksheet = workbook.add_worksheet()
        
        row = 0
        col = 0
       
        #take the average
        for word , value in d.items():
            worksheet.write(row, col,  word)
            worksheet.write(row, col + 1, (sum(value)/len(value)))
            row += 1
        workbook.close()
        
        for word, value in d.items():
            v = sum(value)/len(value)
            file.writelines('{w} {avg} \n'.format(w=word, avg= str(v)))
            
        file.close() 
        
#***************************************************************************    
#***************************************************************************

elif choice == 5 : #Max - encoded
    LL_all = list()
    limit = 0
    for topic in topics: 
        print('processing topic .. ' + str(topic[0]))
        #list of relevant PMID , list of non-relevant PMID
        rel = []
        non_rel = []
        
        path_ = 'TrainingData/qrel_abs_train.txt'
        file = open(path_,'r').readlines()
    
        for line in file:
            if line.split()[0] == topic[1] :
                if line.split()[3] == '1':
                    rel.append(line.split()[2])
                else:
                    non_rel.append(line.split()[2])
                           
        #content of relevent documnts, content of non-relevent documnts         
        text_rel , text_non_rel = '',''
        
        #for each PMID : abstract + encoded MeSH
        doc_path = source_folder + 'TrainingDataset/Abstracts/' + str(topic[0]) + '/'
        mesh_path = source_folder + 'TrainingDataset/MeSHs/encoded/' + str(topic[0]) + '/'
    
        #craete list contains content of the documents
        rel_documents = [] #[open(doc_path+f+'.txt','r',encoding="ISO-8859-1").read() for f in rel]
        non_rel_documents = [] #[open(doc_path+f+'.txt','r',encoding="ISO-8859-1").read() for f in non_rel]
       
        #read documnts   
        for file in (os.listdir(doc_path)):
            mesh = open(mesh_path + file ,'r').read()
            temp_text = open(doc_path+file,'r').read() + ' ' + mesh + ' '
            if file.split('.')[0] in rel:
                text_rel = text_rel + temp_text
                rel_documents.append(temp_text)
            else:
                text_non_rel = text_non_rel + temp_text
                non_rel_documents.append(temp_text)
        
        #Preprocessing (lowercase - stop word removal - Stemming)
        text_rel = str(normalize(text_rel)).replace('\'','')
        text_non_rel = str(normalize(text_non_rel)).replace('\'','')
        
        #Create Dictionary from relevant text 
        rel_dic = dict(Counter(text_rel.replace(',', '').replace('.', '').split()))
        
        #remove words that appear less than threshold
        rel_dic = { d_word:rep for d_word,rep in rel_dic.items() if rep >= threshold }
        
        #sort the dictionary
        rel_dic_sorted = sorted(rel_dic, key=lambda c:rel_dic[c], reverse=True)

        #Preprocessing (lowercase - stop word removal - Stemming)
        for i , rel_d in enumerate(rel_documents):
            rel_documents[i] = str(normalize(rel_documents[i])).replace('\'','')
            
        for j , non_rel_d in enumerate(non_rel_documents):
            non_rel_documents[j] = str(normalize(non_rel_documents[j])).replace('\'','')
                
        total_rel = len(rel)
        total_non_rel = len(non_rel)
        
        #relevant documents 
        frq_word_rel_doc = list()
        
        #count how many relevant documents conatin the word
        for word in rel_dic_sorted:
            count = 0
            for doc in rel_documents:
                if word in doc:
                    count += 1
            # word, no of relevant documents contain word , no of relevant documents not contin word
            frq_word_rel_doc.append((word,count,len(rel_documents)-count))
            
        #non-relevant documents
        frq_word_non_rel_doc = list()
        
        #count how many non-relevant documents conatin the word
        for word in rel_dic_sorted:
            count = 0
            for doc in non_rel_documents:
                if word in doc:
                    count += 1
            # word, no of non-relevant documents contain word , no of non-relevant documents not contin word
            frq_word_non_rel_doc.append((word,count,len(non_rel_documents)-count))
        
        #calculate the log-likelihood 
        #G2 = 2*((a*ln(a/E1))+(b*ln(b/E2)))
        #E1 = c*(a+b)/(c+d) and E2 = d*(a+b)/(c+d)
        #a = the frequency of word in Corpus 1 (relevent text)
        #b = the frequency of word in Corpus 2 (non-relevent text)
        #c = size of corpus1 (The total number of opportunities for word to coccur in Corpus 1 (i.e. the number of times it occurred, plus the number of times it could have occurred but didn't);
        #d = size of corpus2
        
        log_likelihood = list()
                
        obsereved = list()
        
        for i, word in enumerate(frq_word_rel_doc):
            #E1, E2
            o1 = total_rel * (frq_word_rel_doc[i][1] + frq_word_non_rel_doc[i][1])/(total_rel + total_non_rel)
            o2 = total_non_rel * (frq_word_rel_doc[i][1] + frq_word_non_rel_doc[i][1])/(total_rel + total_non_rel)
            obsereved.append((frq_word_rel_doc[i][0], o1 , o2))
        
        
        for j, word in enumerate(obsereved):
            #if a == 0
            if frq_word_rel_doc[j][1] == 0:
                ln_value1 = 0
            else:
                ln_value1 = (math.log(frq_word_rel_doc[j][1]/obsereved[j][1]))
           
            #if b == 0    
            if frq_word_non_rel_doc[j][1] == 0:
                ln_value2 = 0
            else:
                ln_value2 = (math.log(frq_word_non_rel_doc[j][1]/obsereved[j][2]))
                
            LL =  2 * ( (frq_word_rel_doc[j][1] * ln_value1)  +  (frq_word_non_rel_doc[j][1] * ln_value2 ))
            
            log_likelihood.append((obsereved[j][0],LL))
        
        LL_sorted = sorted(log_likelihood,key=lambda l:l[1], reverse=True)
        LL_all.append((topic[1],LL_sorted))
        
        combained_list = list()
        
        for i,record in enumerate(LL_all): 
            for j,t in enumerate(LL_all[i][1]): 
                combained_list.append((t[0],t[1])) 
                
        d = {}
        for tuple in combained_list:
            key,val = tuple
            d.setdefault(key, []).append(val)
            
        #write the results into txt + xlsx files
        new_folder = 'LogLikelihood/TopicsCombined/' 
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        file = open(new_folder + 'max_encoded_LL_TrainingData (Threshold ' + str(threshold) + ')', 'w+')
        workbook = xlsxwriter.Workbook(new_folder + 'max_encoded_LL_TrainingData (Threshold ' + str(threshold) + ').xlsx')
        worksheet = workbook.add_worksheet()
        
        row = 0
        col = 0
        
        for word , value in d.items():
            worksheet.write(row, col,  word)
            worksheet.write(row, col + 1, (sum(value)/len(value)))
            row += 1
        workbook.close()
        
        for word, value in d.items():
            v = max(value)
            file.writelines('{w} {avg} \n'.format(w=word, avg= str(v)))
        
        file.close()  

#***************************************************************************    
#***************************************************************************

elif choice == 6 : #Max - without encoded
    LL_all = list()
    limit = 0
    for topic in topics: 
        print('processing topic .. ' + str(topic[0]))
        #list of relevant PMID , list of non-relevant PMID
        rel = []
        non_rel = []
        
        path_ = 'TrainingData/qrel_abs_train.txt'
        file = open(path_,'r').readlines()
    
        for line in file:
            if line.split()[0] == topic[1] :
                if line.split()[3] == '1':
                    rel.append(line.split()[2])
                else:
                    non_rel.append(line.split()[2])
                           
        #content of relevent documnts, content of non-relevent documnts         
        text_rel , text_non_rel = '',''
        
        #for each PMID : abstract + encoded MeSH
        doc_path = source_folder + 'TrainingDataset/AbstractsMesh/' + str(topic[0]) + '/'
    
        #craete list contains content of the documents
        rel_documents = [] #[open(doc_path+f+'.txt','r',encoding="ISO-8859-1").read() for f in rel]
        non_rel_documents = [] #[open(doc_path+f+'.txt','r',encoding="ISO-8859-1").read() for f in non_rel]
       
        #read documnts   
        for file in (os.listdir(doc_path)):
            temp_text = open(doc_path+file,'r').read() + ' '
            if file.split('.')[0] in rel:
                text_rel = text_rel + temp_text
                rel_documents.append(temp_text)
            else:
                text_non_rel = text_non_rel + temp_text
                non_rel_documents.append(temp_text)
        
        #Preprocessing (lowercase - stop word removal - Stemming)
        text_rel = str(normalize(text_rel)).replace('\'','')
        text_non_rel = str(normalize(text_non_rel)).replace('\'','')
        
        #Create Dictionary from relevant text 
        rel_dic = dict(Counter(text_rel.replace(',', '').replace('.', '').split()))
        
        #remove words that appear less than threshold
        rel_dic = { d_word:rep for d_word,rep in rel_dic.items() if rep >= threshold }
        
        #sort the dictionary
        rel_dic_sorted = sorted(rel_dic, key=lambda c:rel_dic[c], reverse=True)

        #Preprocessing (lowercase - stop word removal - Stemming)
        for i , rel_d in enumerate(rel_documents):
            rel_documents[i] = str(normalize(rel_documents[i])).replace('\'','')
            
        for j , non_rel_d in enumerate(non_rel_documents):
            non_rel_documents[j] = str(normalize(non_rel_documents[j])).replace('\'','')
                
        total_rel = len(rel)
        total_non_rel = len(non_rel)
        
        #relevant documents 
        frq_word_rel_doc = list()
        
        #count how many relevant documents conatin the word
        for word in rel_dic_sorted:
            count = 0
            for doc in rel_documents:
                if word in doc:
                    count += 1
            # word, no of relevant documents contain word , no of relevant documents not contin word
            frq_word_rel_doc.append((word,count,len(rel_documents)-count))
            
        #non-relevant documents
        frq_word_non_rel_doc = list()
        
        #count how many non-relevant documents conatin the word
        for word in rel_dic_sorted:
            count = 0
            for doc in non_rel_documents:
                if word in doc:
                    count += 1
            # word, no of non-relevant documents contain word , no of non-relevant documents not contin word
            frq_word_non_rel_doc.append((word,count,len(non_rel_documents)-count))
        
        #calculate the log-likelihood 
        #G2 = 2*((a*ln(a/E1))+(b*ln(b/E2)))
        #E1 = c*(a+b)/(c+d) and E2 = d*(a+b)/(c+d)
        #a = the frequency of word in Corpus 1 (relevent text)
        #b = the frequency of word in Corpus 2 (non-relevent text)
        #c = size of corpus1 (The total number of opportunities for word to coccur in Corpus 1 (i.e. the number of times it occurred, plus the number of times it could have occurred but didn't);
        #d = size of corpus2
        
        log_likelihood = list()
                
        obsereved = list()
        
        for i, word in enumerate(frq_word_rel_doc):
            #E1, E2
            o1 = total_rel * (frq_word_rel_doc[i][1] + frq_word_non_rel_doc[i][1])/(total_rel + total_non_rel)
            o2 = total_non_rel * (frq_word_rel_doc[i][1] + frq_word_non_rel_doc[i][1])/(total_rel + total_non_rel)
            obsereved.append((frq_word_rel_doc[i][0], o1 , o2))
        
        
        for j, word in enumerate(obsereved):
            #if a == 0
            if frq_word_rel_doc[j][1] == 0:
                ln_value1 = 0
            else:
                ln_value1 = (math.log(frq_word_rel_doc[j][1]/obsereved[j][1]))
           
            #if b == 0    
            if frq_word_non_rel_doc[j][1] == 0:
                ln_value2 = 0
            else:
                ln_value2 = (math.log(frq_word_non_rel_doc[j][1]/obsereved[j][2]))
                
            LL =  2 * ( (frq_word_rel_doc[j][1] * ln_value1)  +  (frq_word_non_rel_doc[j][1] * ln_value2 ))
            
            log_likelihood.append((obsereved[j][0],LL))
        
        LL_sorted = sorted(log_likelihood,key=lambda l:l[1], reverse=True)
        LL_all.append((topic[1],LL_sorted))
        
        combained_list = list()
        
        for i,record in enumerate(LL_all): 
            for j,t in enumerate(LL_all[i][1]): 
                combained_list.append((t[0],t[1])) 
        #create new dictionary cobmined words from all topics relevant dictionaries         
        d = {}
        for tuple in combained_list:
            key,val = tuple
            d.setdefault(key, []).append(val)
            
        #write the results into txt + xlsx files
        new_folder = 'LogLikelihood/TopicsCombined/' 
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        file = open(new_folder + 'max_LL_TrainingData (Threshold ' + str(threshold) + ')', 'w+')
        workbook = xlsxwriter.Workbook(new_folder + 'max_LL_TrainingData (Threshold ' + str(threshold) + ').xlsx')
        worksheet = workbook.add_worksheet()
        
        row = 0
        col = 0
       
        #take the average
        for word , value in d.items():
            worksheet.write(row, col,  word)
            worksheet.write(row, col + 1, (max(value)))
            row += 1
        workbook.close()
        
        for word, value in d.items():
            v = max(value)
            file.writelines('{w} {avg} \n'.format(w=word, avg= str(v)))
            
        file.close()
end = timeit.default_timer()
print ( (end - start)/60 )