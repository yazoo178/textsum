#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
 CLEF2017
 retrive and prepare data 
 retrive abstracts from Pubmed and save into text files
 extract query
 
 by Amal
 
'''
from Bio import Entrez
import os
from Bio import Medline
from itertools import repeat

print('**** CLEF 2017 ****')
print('1. Training Dataset')
print('2. Test Dataset')
data_set = input('Enter the number of Dataset:')
try:
    data_set = int(data_set)
except ValueError:
    print('Invalid number ..')
    exit()
    
print('*******')
print('1. Retrive Dataset from PubMed (titles, abstracts and MeSHs')
print('2. Extract queries from data files.')
choice = input('Enter the number of Dataset:')
try:
    choice = int(choice)
except ValueError:
    print('Invalid number ..')
    exit()
    
    
if data_set == 1: #Training dataset
    folder = 'TrainingData/topics_train/'
    data_folder = '/Users/william/Desktop/Data/CLEF2017/TrainingData/'
    q_folder = '/Users/william/Desktop/Data/CLEF2017/TrainingData/Queries/'
else: #Test dataset
    folder = 'TestData/'
    data_folder = '/Users/william/Desktop/Data/CLEF2017/TestData/'
    q_folder = '/Users/william/Desktop/Data/CLEF2017/TestData/Queries/'
    
   
#AUTOMATICLLY CREATE LIST OF TOICS NAMES AND IDS
#*************************************************
topics = [[0 for x in range(3)] for y in range(len(os.listdir(folder)))]
topics_nums = []
topics_ids = []
topics_titles = []

#read each file and extract topic number, id, and title
for i , file in enumerate(os.listdir(folder)):          
    r_file = open(folder + file ,'r', encoding="ISO-8859-1")
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

#*************************************************
#*************************************************   

if choice == 1:
    # create list of all Pids for each topic
    Pids = [[] for i in repeat(None, len(topics_nums))]
    
    i = 0
    pointer = 0
    for item in (topics_ids): 
         with open(folder + str(topics_nums[i]) , encoding="ISO-8859-1") as input_data:
             pointer = 0
             for line in input_data:
                 if 'Pids:' in line:
                     pointer = 1
                 if pointer == 1 :
                    Pids[i].append(line)  
                    
             for k, x in enumerate(Pids[i]): Pids[i][k] = Pids[i][k].strip()
             Pids[i] = Pids[i][1:]
             i += 1
    
    #*************************************************
    #************************************************* 
    
    # RETRIVE ABSTRACT + MeSH in one file for each PID
    
    abs_folder = data_folder + '/Abstracts/'
    mesh_folder = data_folder + '/MeSHs/original/'
    
    num = 0
    num1 = 0
    i = 0
    
    final_records = []
    
    while num1 < len(topics_nums)  :
    
        handle = Entrez.efetch(db="pubmed", id=[str(p) for p in Pids[num1]], rettype="medline", retmode="text")
        records = Medline.parse(handle)   
        records = list(records) 
        print (len(records))
        
        for ii , rec in enumerate(records):
            final_records.append(records[ii])
    
        for k, record in enumerate(final_records):
        #create folder for each topic to store abstract files
            new_folder_abs = abs_folder  + str(topics_nums[num1]) + '/' 
            if not os.path.exists(new_folder_abs):
                os.makedirs(new_folder_abs)
                
            file_name = final_records[k].get("PMID","?")
            
            if file_name == '?':
                file_name = '22497021'
                
            #create new file to store title + abstract  - file name = pubmed id
            file_name1 = abs_folder + str(topics_nums[num1]) + '/' + file_name + '.txt'
            file1 = open(file_name1,"w", encoding="ISO-8859-1") 
            
            #create folder for each topic to store MeSHs files
            new_folder_MeSH = mesh_folder + str(topics_nums[num1]) + '/' 
            if not os.path.exists(new_folder_MeSH):
                os.makedirs(new_folder_MeSH)
                
            #create new file to store MeSH - file name = pubmed id
            file_name2 = new_folder_MeSH + file_name + '.txt'
            file2 = open(file_name2,"w", encoding="ISO-8859-1") 
            
            #save the title and abstract    
            file1.write(final_records[k].get("TI", "?") + '\n' + final_records[k].get("AB", "?"))
            file2.write(str(final_records[k].get("MH", "?")) )
             
        num1 += 1
        i += 1
        
    handle.close()
    
if choice == 2:
    i = 0
    start = end = 0
    
    if not os.path.exists(q_folder):
        os.makedirs(q_folder)
            
    #retrive query    
    for item in topics_nums :
                
        #create new txt file contain the query
        query_file = q_folder + str(topics_nums[i]) + '.txt'
        file = open(query_file,"w", encoding="utf8") 
        #open the train data file to copy the query from it
        file_name = folder + str(item)
        data = open(file_name ,'r', encoding="ISO-8859-1")
        text = data.readlines()
        for j , line in enumerate(text):
            if line.startswith('Query: '):
                start = j
            if line.startswith('Pids: '):
                end = j
        query = text [start+1 : end-1]
        file.writelines(query)       
        i +=1