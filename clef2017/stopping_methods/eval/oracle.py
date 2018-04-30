import operator
import matplotlib.pyplot as plt
import math
import numpy as np
import sys, getopt
import random
import os
import re
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

def loadTestResults(file):
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



opts, args = getopt.getopt(sys.argv[1:],"hc:q:r:")
qrel = None
rankingFile = None

for opt, arg in opts:
	if opt == '-h':
		usage()
	elif opt in ("-q"):
		qrel = arg
	elif opt in ('-r'):
		rankingFile = arg
        

content = readQrel(qrel)
records = loadTestResults(rankingFile)

thre = 70


totalEffort = 0


for key in content:


	rel = len([x for x in content[key] if x[1] == '1'])
	total = len(content[key])
	keyPoint = int((rel / 100) * thre)
	topic = records[key]
	
	count = 0
	indexPoint = 0
	for id in content[key]:
		if id[0] in topic.docsReturned and id[1] == '1':
			count = count + 1
			index = findIn(id[0], topic.docsReturned)
			if count == keyPoint:
				indexPoint = index
				
	
	effort = indexPoint / total
	totalEffort+=effort
	print("Effort:{0}\tRecall:{1}\tReliability{2}".format(effort, 0.7, 1.0))
	

print("")
print("Effort:{0}\tRecall:{1}\tReliability{2}".format(totalEffort / len(content), 0.7, 1.0))
	
	
	
	
		
	
	






