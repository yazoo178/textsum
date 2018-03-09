import sys, getopt
import nltk
import rake
import re
from Bio import Entrez

STOPS = "stops.txt"
refs = r'\([\&\.\,\-\'\s\dA-Ȣ]*?\s[0-9]{4}|([A-Z,ÖÄÅ][\.\,\-\'\dA-Ȣ]+[\s\&|et al.|m.fl.|och|and]*){1,7}\([0-9]{4}'


def search(query):
    Entrez.email = 'wbriggs2@sheffield.ac.uk'
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance',
                            retmax='100000',
                            term=query)
    results = Entrez.read(handle)
    return results


def RemoveRefs(content):
    return re.sub(refs, '', content)




def ProtocolToQuery(protocol):
    protocol = RemoveRefs(protocol.lower())

    query = ""
    rake_object = rake.Rake(STOPS, min_keyword_frequency=1)
    
    keywords = rake_object.run(protocol)

    for keyword in keywords[0:int(len(keywords) / 20)]:

        query += keyword[0] + " OR "

    query = query[:-4]    

    results = search(query)
    print(results['IdList'])
    #print(keywords)



def usage():
    print("-p specifiy a protocol file")



pFile = ""
pFile = sys.argv[1:][0]

content = open(pFile, 'r')
ProtocolToQuery(content.read().replace('\n', ''))



