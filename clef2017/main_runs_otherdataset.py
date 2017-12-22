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


print('**** CLEF 2017 ****')
print('\n**** Datasets ****')
print('1. COPD')
print('2. Proton')
#print('3. Drugs')
#print('4. Biomarkers')
dataset = input('Enter the number of dataset:')
try:
    dataset = int(dataset)
except ValueError:
    print('Invalid number ..')
    exit()
    
print('\n**** RUNS ****')
print('1. run 1')
print('2. run 2')
print('3. run 3')
print('4. run 4')
print('5. run 5')
choice = input('Enter the number of run:')
try:
    choice = int(choice)
except ValueError:
    print('Invalid number ..')
    exit()

start = 0
end = 0

print('Processing ..')
 
if dataset == 1: #COPD dataset
    path = '/Users/amal/Desktop/Data/COPD/AbstractsMeSH/' 
    t = 'genetic determinants of COPD susceptibility '
    data = 'COPD'
     
else: #PROTON dataset
    path = '/Users/amal/Desktop/Data/Proton/AbstractsMeSH/' 
    data = 'Proton'
    

#create qrel file
qrel_abstract = open('output/' + data + '-run-' + str(choice) ,'w+') 

RUNID = data + '-run-' + str(choice)

doc_ids = os.listdir(path)
for ind, topic in enumerate(doc_ids):
    if topic == '.DS_Store':
        del doc_ids[ind]

#to calculate run time
start = timeit.default_timer()

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


# Make a list of files in the directory then read these documents in for later processing
# (just make this list once so don't need to call the OS more than needed)
documents = [open(path+f,'r',encoding="ISO-8859-1").read() for f in doc_ids]

if choice == 3 or choice == 5:
    path2 = '/Users/amal/Desktop/Data/' + data + '/MeSHs/encoded/'

    #read MeSH heading for all abstract
    mesh_ids = os.listdir(path2)
    Meshs_abs = [open(path2+f,'r',encoding="ISO-8859-1").read() for f in mesh_ids]

    #add decoded MeSH to abstract
    for j, d in enumerate(documents):
        documents[j] = documents[j].replace('-',' ').replace('/',' ').replace('(',' ').replace(')',' ').replace('[',' ').replace(']',' ').replace("'",' ')
        documents[j] = documents[j] + ' ' + Meshs_abs[j]

tfidf = vectorizer.fit_transform(documents)

           
if choice == 2 or choice == 4:
    terms = open('/Users/amal/Desktop/Data/' + data + '/MeSHsTerms/Terms/' + data).read()
    #read topic title + terms
    t = t + ' ' + terms
    
if choice == 3:
    terms = open('/Users/amal/Desktop/Data/' + data + '/MeSHsTerms/Terms/' + data).read()
    mesh = open('/Users/amal/Desktop/Data/' + data + '/MeSHsTerms/encodedMeSH/' + data + '.txt').read()
    t = t + ' ' + terms + ' ' + mesh
        
if choice == 5:
    mesh = open('/Users/amal/Desktop/Data/' + data + '/MeSH and Terms/encodedMeSH/' + data + '.txt').read()
    t = t + ' '  + mesh

title = vectorizer.transform([t])

cosine_sim = linear_kernel(title, tfidf).flatten()   

# Create a dictionary with the filenames as keys and cosine similarity scores as values
# then print it out in order (sorted by the cosine similarity score)
doc_sim_values = dict(zip(doc_ids, cosine_sim))

rank = 1
for doc, score in sorted(doc_sim_values.items(), key=operator.itemgetter(1), reverse=True):
    doc_id = doc.split('.')[0] # Remove suffix from filename (to leve PID)
    # Print out sorted results in this format: 
    # TOPIC-ID INTERACTION PID RANK SCORE RUN-ID
    qrel_abstract.writelines('{t} NF {d} {r} {s} {i} \n'.format(t=data, d=doc_id, r=rank, s=score, i=RUNID))
    rank = rank + 1

qrel_abstract.close()   
     
end = timeit.default_timer()
print('Run Time: ' +  str("%.2f" % ((end - start)/60)))
print('The qrel file: ' + RUNID + ' in output folder.')