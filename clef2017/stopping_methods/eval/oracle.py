import operator
import matplotlib.pyplot as plt
import math
import numpy as np
import sys, getopt
import random
import os
import re
from stopping_methods.BaseRules import *

#-k 10 -o Output/Test_Data_Sheffield-run-2 -q qrel/qrel_abs_test


class record:
    def __init__(self, qId):
        self.queryId = qId
        self.docsReturned = []
		

    def addDoc(self, doc):
        self.docsReturned.append(doc)

def usage():
    print("-o output file name [OPTIONAL] -s sample size [DEFAULT 3] -t true score file -r recall rate [DEFAULT 70] -c curve scores path [OPTIONAL, DEFAULT looks in same folder as true scores]")
    sys.exit()


def findIn(score, x):
    for ind, x1 in enumerate(x):
        if score == x1:
            return ind	
	
def readQrel(qrel):
	ids = {}
	file = open(qrel, "r")
	for line in file:
		tabbed = re.split('\s+', line)
		if tabbed[0] not in ids:
			ids[tabbed[0]] = []
		ids[tabbed[0]].append([tabbed[2], tabbed[3].rstrip().strip()])

	return ids

#load test tests from run file
def loadRunFile(file):
    records = {}
    with open(file) as content:
        lastId = "Start"

        for line in content:
            tabbed = re.split("\s", line)

            if lastId == tabbed[0]:
                records[lastId].addDoc(tabbed[2])

            else:
                lastId = tabbed[0]
                records[lastId] = record(lastId)
                records[lastId].addDoc(tabbed[2])

    return records


opts, args = getopt.getopt(sys.argv[1:],"hc:q:r:i:")
qrel = None
rankingFile = None

for opt, arg in opts:
	if opt == '-h':
		usage()
	elif opt in ("-q"):
		qrel = arg
	elif opt in ('-r'):
		rankingFile = arg
	elif opt in ("-i"):
		thre = int(arg)

        
content = readQrel(qrel)
records = loadRunFile(rankingFile)

totalDocuments = 0
effortSumWeighted = 0
effortSum = 0
topicsUsed = 0

for key in content:
    relDocs = [x[0] for x in content[key] if x[1] == '1']

    if not HasMoreThanNDocuments(content[key]):
        print("Skipping")
        continue
    
    topicsUsed +=1
    rel = len([x for x in content[key] if x[1] == '1'])
    numberNeededForRecall = int(rel * (thre / 100))
    lookedAt = 0
    found = 0

    

    for document in records[key].docsReturned:
        lookedAt+=1
        if document in relDocs:
            found+= 1
            if found == numberNeededForRecall:
                break

    print("Effort: ", lookedAt / len(content[key]), "Documents: ", len(records[key].docsReturned))

    effortSumWeighted += (lookedAt / len(content[key])) * len(records[key].docsReturned)
    effortSum += (lookedAt / len(content[key])) 

    totalDocuments += len(records[key].docsReturned)


print("Topics Used: ", topicsUsed)
print("Weighted Average Effort: ", effortSumWeighted / totalDocuments)
print("Average Effort: " ,effortSum / topicsUsed)

	
	
	
	
		
	
	






