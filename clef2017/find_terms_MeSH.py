#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 *** CLEF 2017 ***
 this code to extartct MeSH and terms from OVID and PubMed queries
 it ignore lines witch include  Not, adj operators
 the output is a list of text files containe MeSH and Terms for each topic
 
 Author: Amal Alharbi
 Last updated: 24 June 2017

"""
import re
import os

print('**** CLEF 2017 ***')
print('Extract terms and MeSHs from queries.')

#define list of terms and MeSHs tags that appear in queries

Ovid_terms_tags = ['mp' , 'tw' , 'ti,ab' , 'tw,ot' , 'tw,ot,nm']
Ovid_MeSH_tags = ['/' , 'sh' ]

Pub_terms_tags = ['tw' , 'tiab' , 'ti' ]
Pub_MeSH_tags = [ 'mesh' , 'sh' , 'mh' , 'mh:noexp' , 'mesh_terms' , 'mesh terms' ]

Pub_marks = [ '[tw]' , '[tiab]' , '[ti]' ,'[mesh]' , '[sh]' , '[mh]' , '[mh:noexp]' , '[mesh_terms]' ]


def find_terms_Mesh (new_folder_terms,new_folder_MeSH,folder,f_path):
    
    topics_nums = []
    topics_ids = []
    topics_titles = []

    #create new folder to include text files with terms and Mesh
    #Terms:
    if not os.path.exists(new_folder_terms):
        os.makedirs(new_folder_terms)
    
    #MesHs:
    if not os.path.exists(new_folder_MeSH):
        os.makedirs(new_folder_MeSH)
        
    #AUTOMATICLLY CREATE LIST OF TOICS NAMES AND IDS
    #*************************************************
    
    topics = [[0 for x in range(3)] for y in range(len(os.listdir(folder)))]

    #read each topic file and extract topic number, id, and title
    for i , file in enumerate(os.listdir(folder)):          
        r_file = open(folder + file ,'r', encoding = 'ISO-8859-1')
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
    
    size = len(topics_ids)
    num = 0
    #loop for all topics
    while size > 0 :
        path = f_path + str(topics_nums[num]) + '.txt'
        myfile = open( path , 'r' , encoding = 'ISO-8859-1' )   
        query_file = myfile.readlines()
     
        Ovid_terms = []
        Ovid_MeSH = []  
        
        Pub_terms = []
        Pub_MeSH = []  
        
        #replace dot with space, slash with space+/ and remove space from the end of text
        for i , l in enumerate(query_file):
            query_file[i] = query_file[i].replace('.',' ').replace('/',' /')
            query_file[i] = query_file[i].rstrip().lower()
            
        #remove empty list elements   
        query_file = list(filter(None, query_file)) 
      
        temp = str(query_file) 
        
        
        if not(any(ext in temp.lower() for ext in Pub_marks)) : 
            
        #******************************************************
        #************************ OVID ************************
        #******************************************************
                    
           for i , l in enumerate(query_file):
             if (query_file[i].split())[-1] in Ovid_terms_tags :
                 #add term to the terms list
                 Ovid_terms.append(query_file[i])
             if (query_file[i].split())[-1] in Ovid_MeSH_tags :
                 #add MeSH to the MesHs list
                 Ovid_MeSH.append(query_file[i])
             else:
                # MeSH with subheading
                if ('/' in query_file[i] and not('or' in query_file[i]) and not('and' in query_file[i])):
                    temp = query_file[i].split('/')
                    Ovid_MeSH.append(temp[0])
                                                                                        
#             else:
#                 # MeSH with subheading
#                 if (re.findall("^/", query_file[i].split()[-1] , re.I)):
#                     if (query_file[i].split()[0] != 'or' and query_file[i].split()[0] != 'and'):
#                         temp = ' '.join(query_file[i].split()[:-1])
#                         Ovid_MeSH.append(temp)
#                         Ovid_MeSH.append(query_file[i].split()[-1])
#                 else:
#                      if (re.findall("^/", query_file[i].split()[-2] , re.I)):
#                        if (query_file[i].split()[0] != 'or' and query_file[i].split()[0] != 'and'):
#                            temp = ' '.join(query_file[i].split()[:-2])
#                            Ovid_MeSH.append(temp)
#                            Ovid_MeSH.append(query_file[i].split()[-1])                     
           
           #remove duplicate
           #Ovid_MeSH = list(set(Ovid_MeSH))
        
           # (1) OVID terms
           #**************
           
           #remove tags from Terms list   
           tags_1 = ['mp' , 'tw' , 'ti,ab' , 'tw,ot' , 'tw,ot,nm' , ')' , '(' , '"' , '$' , '*'  ]
           big_regex_1 = re.compile('|'.join(map(re.escape, tags_1)))
                  
           for j , l in enumerate(Ovid_terms):
               Ovid_terms[j] = big_regex_1.sub(" ", Ovid_terms[j])
               Ovid_terms[j] = Ovid_terms[j].replace(' or ',' , ')
               Ovid_terms[j] = Ovid_terms[j].rstrip()
            
           #remove adj from Term list
           for i, w in enumerate(Ovid_terms):
               if re.search('(.*)(adj)+[0-9]*', w):
                   Ovid_terms[i] =  re.sub('(adj)+[0-9]*',' , ', Ovid_terms[i])
                   
           #remove emptu list elements
           Ovid_terms = list(filter(None, Ovid_terms)) 
           
           #if list element contains more than 1 term --> seprate
           Ovid_terms = [y  for x in Ovid_terms for y in x.split(',')]
           
           for i, x in enumerate(Ovid_terms): Ovid_terms[i] = Ovid_terms[i].strip()
           
           #write the list of terms into text file
           terms_file = new_folder_terms + str(topics_nums[num]) + '.txt'
           file1 = open(terms_file,"w", encoding="utf-8") 
           file1.write(str(Ovid_terms))      
           file1.close() 
           
           # (2) OVID MeSH
           #**************
           
           #remove tags from Mesh list
           tags_2 = ['/' , 'sh' , 'exp' , ')' , '(' , '"' , '$' , '*' , '[', ']' ]
           big_regex_2 = re.compile('|'.join(map(re.escape, tags_2)))
           
           for j , t in enumerate(Ovid_MeSH):
               Ovid_MeSH[j] = big_regex_2.sub(" ", Ovid_MeSH[j])
               Ovid_MeSH[j] = Ovid_MeSH[j].replace(' or ',' , ').replace(' and ',' , ')
               Ovid_MeSH[j] = Ovid_MeSH[j].rstrip()      
               
           #remove not from MeSH list
           for i, w in enumerate(Ovid_MeSH):
               if re.search('(.*)(not)+', w):
                   Ovid_MeSH[i] = ''
                   
           Ovid_MeSH = list(filter(None, Ovid_MeSH))  
           Ovid_MeSH = [y  for x in Ovid_MeSH for y in x.split(',')] 
           
           for i,x in enumerate(Ovid_MeSH): Ovid_MeSH[i] = Ovid_MeSH[i].strip()
     
           #write the list of MeSHs into text file
           MeSH_file = new_folder_MeSH + str(topics_nums[num]) + '.txt'
           file2 = open(MeSH_file , "w" , encoding = 'utf-8') 
           file2.write(str(Ovid_MeSH))
           file2.close()   
            
        else:
            #******************************************************
            #************************ Pubmed **********************
            #******************************************************
            
            tags_1 = [  ')' , '(' , '"' , '“', '”' ,'$' , '*' , '[' , ']' , 'exp'  ]
            big_regex_1 = re.compile('|'.join(map(re.escape, tags_1)))
            
            for i , l in enumerate(query_file):
                query_file[i] = big_regex_1.sub(" ", query_file[i])
                query_file[i] = query_file[i].replace(' and ',' or ')
                query_file[i] = query_file[i].rstrip()
                if query_file[i][0].isdigit():
                    #Exclusion criteria
                    if 'exclusion' in query_file[i]:
                        query_file[i:-1] = ''
                        break
                    query_file[i] = ''
    
            #remove empty elements                       
            query_file = list(filter(None, query_file)) 
            
            indev = []
            
            #seperate query based on 'OR'
            for i, o in enumerate(query_file):
                temp = query_file[i].split(' or ')
                for j,q in enumerate(temp):
                    indev.append(temp[j])
                    
            #remove not from  list
            for i, w in enumerate(indev):
               if re.search('(.*)(NOT)+', w):
                   indev[i] = ''
                   
            indev = list(filter(None, indev))  
            
            for index, curr in enumerate(indev):
                if curr.split()[-1] in Pub_MeSH_tags:
                    #add MeSH to the terms list
                    Pub_MeSH.append(curr)
                if curr.split()[-1] in Pub_terms_tags:
                    #add term to the terms list
                    Pub_terms.append(curr)
                    
    
            # (1) Pubmed terms
            #******************
            
            #remove tags from Terms list   
            tags_1 = ['tw' , 'tiab']
            big_regex_1 = re.compile('|'.join(map(re.escape, tags_1)))
                  
            for j , l in enumerate(Pub_terms):
                Pub_terms[j] = big_regex_1.sub(" ", Pub_terms[j])
                Pub_terms[j] = Pub_terms[j].rstrip().strip()
           
            #write the list of terms into text file
            terms_file = new_folder_terms + str(topics_nums[num]) + '.txt'
            file1 = open(terms_file , "w", encoding = 'utf-8') 
            file1.write(str(Pub_terms))      
            file1.close()               
            
            # (2) Pubmed MeSH
            #*****************
            
            #remove tags from Mesh list
            tags_2 = ['mesh_terms' , ' mesh terms' , ' mh' , ' mesh' , ' mh:noexp' , ' sh' , '$' , '*' , '[', ']' ]
            big_regex_2 = re.compile('|'.join(map(re.escape, tags_2)))
           
            for j , t in enumerate(Pub_MeSH):
                Pub_MeSH[j] = big_regex_2.sub(" ", Pub_MeSH[j])
                Pub_MeSH[j] = Pub_MeSH[j].replace(' or ',' , ')
                Pub_MeSH[j] = Pub_MeSH[j].rstrip()
                
            Pub_MeSH = list(filter(None, Pub_MeSH))  
            Pub_MeSH = [y  for x in Pub_MeSH for y in x.split(',')] 
           
            for i,x in enumerate(Pub_MeSH): Pub_MeSH[i] = Pub_MeSH[i].strip()
     
            #write the list of terms into text file
            MeSH_file = new_folder_MeSH + str(topics_nums[num]) + '.txt'
            file2 = open(MeSH_file , "w" , encoding = 'utf-8') 
            file2.write(str(Pub_MeSH))
            file2.close()
    
        
        size -= 1
        num += 1

source_folder = '/Users/amal/Desktop/Data/CLEF2017/'

#training data
new_folder_terms = source_folder + 'TrainingDataset/MeSHsTerms/terms/'
new_folder_MeSH = source_folder + 'TrainingDataset/MeSHsTerms/Mesh/'
folder = 'TrainingData/topics_train/'
query_folder = source_folder + 'TrainingDataset/Queries/'
find_terms_Mesh(new_folder_terms,new_folder_MeSH,folder,query_folder)

#test data
new_folder_terms = source_folder + 'TestDataset/MeSHsTerms/terms/'
new_folder_MeSH = source_folder + 'TestDataset/MeSHsTerms/Mesh/'
folder = 'TestData/'
query_folder = source_folder + 'TestDataset/Queries/'
find_terms_Mesh(new_folder_terms,new_folder_MeSH,folder,query_folder)

print('terms and Meshes have been extracted for both training and test dataset.')