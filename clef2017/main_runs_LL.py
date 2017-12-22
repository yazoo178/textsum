"""
 ***** CLEF2017 *****
 Main Run with Log Likelihood
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


print('**** CLEF 2017 ***')
print('1. Training Dataset')
print('2. Test Dataset')
data_set = input('Enter the number of Dataset:')
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
choice = input('Enter the number of run:')
try:
    choice = int(choice)
except ValueError:
    print('Invalid number ..')
    exit()

print('\n**** Log Likelihood ****')
counter = input('Enter the number of top words to include in the query:')
try:
    counter = int(counter)
except ValueError:
    print('Invalid number ..')
    exit()

source_folder = '/Users/amal/Desktop/Data/CLEF2017/'

if data_set == 1: #Training dataset
    RUNID = 'Sheffield-run-' + str(choice)
    folder = 'TrainingData/topics_train/'
    #create qrel file
    qrel_abstract = open('output/Sheffield-run-' + str(choice) + '-LL','w+') 
    
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
#read the top words for each topic based on log-likelihood
ll_words = list()
for l in topics_ids:
#    ll_path = 'LogLikelihood/TopicsIndividual/Threshold_0/TrainingData/'+ l +'_Threshold_0'
    ll_path = 'LogLikelihood/TopicsCombined/LL_TrainingData (Threshold 0)'
    ll_file = open(ll_path,'r').readlines()
    top_words = []
    count = 0
    for line in ll_file:
        top_words.append(line.split()[0])
        count += 1
        if count == counter:
            break
    ll_words.append((l,top_words))


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
for i in range(0, len(topics_nums)):
    print('processing topic .. ' + str(topics_nums[i]))
    
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
    
    #take the top word for current topic
    for w in ll_words:
        if w[0] == topics_ids[i]:
            ll_word = w[1]
            break
    ll_word = ' '.join(ll_word)
    ll_word = ' traum injury wound scor admit hospit mort emerg injuriesblood cohort '
    if choice == 1:     
        t = topics_titles[i] + ' ' + ll_word
               
    if choice == 2 or choice == 4:
        #read topic title + terms
        terms = open(query_terms_path + str(topics_nums[i]) + '.txt').read()
        t = topics_titles[i] + ' ' + terms + ' ' + ll_word
        
    if choice == 3:
        MeSHs = open(query_mesh_path + str(topics_nums[i]) + '.txt').read()    
        terms = open(query_terms_path + str(topics_nums[i]) + '.txt').read()
        t = topics_titles[i] + ' ' + MeSHs + ' ' + terms + ' ' + ll_word
        
    if choice == 5:
        MeSHs = open(query_mesh_path + str(topics_nums[i]) + '.txt').read()
        t = topics_titles[i] + ' ' + MeSHs + ' ' + ll_word

    title = vectorizer.transform([t])
    
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
print('Run Time: ' + str((end - start)/60))
print('The qrel file: ' + RUNID + ' in output folder.')