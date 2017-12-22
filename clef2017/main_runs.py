"""
 ***** CLEF2017 *****
 Find similarity between title and documents based on cosine similarity
 using NLTL and Lancaster stemmer for preprocessing
 using sklearn to calculate the tf-idf 
 by Amal Alharbi and Mark Stevenson
 
"""
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import os
import timeit
import operator
import re
import numpy as np
from scipy.sparse import csr_matrix

queryIdToRelvDocs = {}
queryIdToNonRelDocs = {}

def genRelevantDocs(testFiles):
    found = False
    header = True
    qId = ""
    lastId = "Start"

    with open(testFiles, encoding='utf-8') as content:
        for line in content:
            tabbed = re.split('\s+', line)

            if tabbed[0] not in queryIdToRelvDocs:
                queryIdToRelvDocs[tabbed[0]] = []
                queryIdToNonRelDocs[tabbed[0]] = []

            if '1' in tabbed[3].rstrip().strip():
                queryIdToRelvDocs[tabbed[0]].append(tabbed[2].rstrip().strip())

            elif '0' in tabbed[3].rstrip().strip():
                queryIdToNonRelDocs[tabbed[0]].append(tabbed[2].rstrip().strip())

    

def eval(dSet, id, num):
    subset = dSet[0:num]
    x = float(len([x for x in subset if x.replace('.txt', '') in queryIdToRelvDocs[id]]) / num)
    return x

genRelevantDocs('qrel/qrel_abs_train.txt')


alpha = 1.0
beta = 0.5
print('**** CLEF 2017 ***')
print('1. Training Dataset')
print('2. Test Dataset')
data_set = 1
try:
    data_set = int(data_set)
except ValueError:
    print('Invalid number ..')
    exit()
    
print('\n**** RUNS ****')
print('1. Sheffeild run 1')
print('2. Sheffeild run 2')
print('3. Sheffeild run 3')
print('4. Sheffeild run 4')
print('5. Sheffeild run 5')
choice = 1
try:
    choice = int(choice)
except ValueError:
    print('Invalid number ..')
    exit()

source_folder = 'C:\\Users\\william\\Desktop\\Data\\CLEF2017\\'

if data_set == 1: #Training dataset
    RUNID = "Sheffield-run-" + str(choice)
    folder = 'TrainingData/topics_train/'
    #create qrel file
    qrel_abstract = open("output/Sheffield-run-"+str(choice),"w+") 
    
    if choice == 1 or choice == 5:
        abs_path = source_folder + 'TrainingDataset/Abstracts/'        

    if choice == 2 or choice == 4:
        abs_path = source_folder + 'TrainingDataset/AbstractsMeSH/'
        query_terms_path = source_folder + 'TrainingDataset/MeSHsTerms/terms/'

    if choice == 3:
        abs_path = source_folder + 'TrainingDataset/Abstracts/'        
        mesh_path = source_folder + 'TrainingDataset/MeSHs/encoded/'        
        query_mesh_path = source_folder + 'TrainingDataset/MeSHsTerms/encodedMeSH/'
        query_terms_path = source_folder + 'TrainingDataset/MeSHsTerms/terms/'
    
    if choice == 5:
        query_mesh_path = source_folder + 'TrainingDataset/MeSHsTerms/encodedMeSH/'

else: #Test dataset
    RUNID = "Test_Data_Sheffield-run-" + str(choice)
    folder = 'Test Data/'
    #create qrel file
    qrel_abstract = open("output/Test_Data_Sheffield-run-"+str(choice),"w+") 

    if choice == 1:
        abs_path = source_folder + 'TestDataset/Abstracts/'        

    if choice == 2 or choice == 4:
        abs_path = source_folder +  'TestDataset/AbstractsMeSH/'
        query_terms_path = source_folder + 'TestDataset/MeSHsTerms/terms/'
    
    if choice == 3:
        abs_path = source_folder + 'TestDataset/Abstracts/'        
        mesh_path = source_folder + 'TestDataset/MeSHs/encoded/'        
        query_mesh_path = source_folder + 'TestDataset/MeSHsTerms/encodedMeSH/'
        query_terms_path = source_folder + 'TestDataset/MeSHsTerms/terms/'
        
    if choice == 5:
        query_mesh_path = source_folder + 'TestDataset/MeSHsTerms/encodedMeSH/'


start = 0
end = 0

#to calculate run time
start = timeit.default_timer()

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

#preprocessing
if choice == 4 : #use PubMed stop words
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
    
else: #use nltk english stopwords
    #using lancaster stemmer
    stemmer = nltk.stem.lancaster.LancasterStemmer()
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    
    def stem_tokens(tokens):
        return [stemmer.stem(item) for item in tokens]
    
    def normalize(text):
        return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))
    
    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

   
#loop for all topics
for i in range(0, 1):
    print('processing topic .. ' + str(i+1))
    
    path = abs_path + str(topics_nums[i]) +'/'  
        
    # Make a list of files in the directory then read these documents in for later processing
    # (just make this list once so don't need to call the OS more than needed)
    doc_ids = os.listdir(path)
    documents = [open(path+f,'r',encoding="ISO-8859-1").read() for f in doc_ids]

    if choice == 3 or choice == 5:
        path2 = mesh_path+ str(topics_nums[i]) +'/'
        #path2 = 'Data/Test Data Set/MeSHs/encoded/' + str(topics_nums[i]) +'/'

        #read MeSH heading for all abstract
        mesh_ids = os.listdir(path2)
        Meshs_abs = [open(path2+f,'r',encoding="ISO-8859-1").read() for f in mesh_ids]
    
        #add decoded MeSH to abstract
        for j, d in enumerate(documents):
            documents[j] = documents[j].replace('-',' ').replace('/',' ').replace('(',' ').replace(')',' ').replace('[',' ').replace(']',' ').replace("'",' ')
            documents[j] = documents[j] + ' ' + Meshs_abs[j]

    tfidf = vectorizer.fit_transform(documents)
    
    if choice == 1:     
        t = topics_titles[i]
               
    if choice == 2 or choice == 4:
        #read topic title + terms
        terms = open(query_terms_path + str(topics_nums[i]) + '.txt').read()
        t = topics_titles[i] + ' ' + terms
        
    if choice == 3:
        MeSHs = open(query_mesh_path + str(topics_nums[i]) + '.txt').read()    
        terms = open(query_terms_path + str(topics_nums[i]) + '.txt').read()
        t = topics_titles[i] + ' ' + MeSHs + ' ' + terms
        
    if choice == 5:
        MeSHs = open(query_mesh_path + str(topics_nums[i]) + '.txt').read()
        t = topics_titles[i] + ' ' + MeSHs 
    
    title = vectorizer.transform([t])
    
    cosine_sim = linear_kernel(title, tfidf).flatten()   

    # Create a dictionary with the filenames as keys and cosine similarity scores as values
    # then print it out in order (sorted by the cosine similarity score)
    doc_sim_values = dict(zip(doc_ids, cosine_sim))


    #set the relevance/non-relevance weights

    #nonRelevanceWeighting = beta / (count - len(doc_sim_values))

    numberToTake = 3
    tmpTest = open("record.txt", "w+")
    while True:
        
        print("query:"  + t)
        for top_doc in sorted(doc_sim_values.items(), key=operator.itemgetter(1), reverse=True):
            pass
            #print(top_doc[0])

        #chosen = input("Input documents, "'N'" to stop\r\n").rstrip().split(',')

      #  if chosen == "N":
         #   break

        tmpVec = [0] * len(title.toarray()[0])
        tmpVecNonRel = [0] * len(title.toarray()[0])

        relevantDocs = [x + ".txt" for x in queryIdToRelvDocs[topics_ids[i]]][0:5]
        numberToTake+=1
        nonRelDocs = [x + ".txt" for x in queryIdToNonRelDocs[topics_ids[i]]]

        indices = [i for i, ii in enumerate(doc_ids) if ii in relevantDocs]
        indicesNonRel = [i for i, ii in enumerate(doc_ids) if ii in nonRelDocs]

        selectedDocuments = list(map(documents.__getitem__, indices))
        selectedNonRel = list(map(documents.__getitem__, indicesNonRel))

        relevanceWeighting = alpha * (1 / float(len(selectedDocuments)))
        nonRelevanceWeighting = beta * (1 / float(len(selectedNonRel)))

        termIndicies = []
        nontermInd = []
        topic_mod = title.toarray()[0]

        for doc in selectedDocuments:
            re_vec_doc = vectorizer.transform([doc])
            termIndicies.append([i for i, x in enumerate(re_vec_doc.toarray()[0]) if x > 0])

        for doc in selectedNonRel:
            re_vec_doc = vectorizer.transform([doc])
            nontermInd.append([i for i, x in enumerate(re_vec_doc.toarray()[0]) if x > 0])

        for ind in list((sum(termIndicies, []))):
            if topic_mod[ind] == 0:
                tmpVec[ind] = relevanceWeighting
            else:
                tmpVec[ind] += (topic_mod[ind]  * relevanceWeighting)

        for ind in set((sum(nontermInd, []))):
            if topic_mod[ind] == 0:
                tmpVecNonRel[ind] = nonRelevanceWeighting
            else:
                tmpVecNonRel[ind] += (topic_mod[ind]  * nonRelevanceWeighting)


        for element in topic_mod:
            tmpTest.write(str(element) + ",")

        tmpTest.write("\n")
        tmpTest.flush()

        topic_mod = np.subtract(np.add(topic_mod, tmpVec), tmpVecNonRel)
        title = csr_matrix(topic_mod)
        cosine_sim = linear_kernel(title, tfidf).flatten()   
        doc_sim_values = dict(zip(doc_ids, cosine_sim))
        docIdsSorted = [doc[0] for doc in sorted(doc_sim_values.items(), reverse=True, key= lambda x :x[1])]
        print(str(eval(docIdsSorted, topics_ids[i], 39)))

    topic_id = topics_ids[i]
    docRanks = []
    rank = 1

    

    for doc, score in sorted(doc_sim_values.items(), key=operator.itemgetter(1), reverse=True):
        doc_id = doc.split('.')[0] # Remove suffix from filename (to leve PID)
        # Print out sorted results in this format: 
        # TOPIC-ID INTERACTION PID RANK SCORE RUN-ID
        qrel_abstract.writelines('{t} NF {d} {r} {s} {i} \n'.format(t=topic_id, d=doc_id, r=rank, s=score, i=RUNID))
        rank = rank + 1

    

qrel_abstract.close()   
     
end = timeit.default_timer()
print('Run Time: ' + str((end - start)/60))
print('The qrel file: ' + RUNID + ' in output folder.')