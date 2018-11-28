import re


def LoadTestFile(testFiles):

    queryIdToRelvDocs = {}

    with open(testFiles, encoding='utf-8') as content:
        for line in content:
            tabbed = re.split('\s+', line)

            if tabbed[0] not in queryIdToRelvDocs:
                queryIdToRelvDocs[tabbed[0]] = []

            if '1' in tabbed[3].rstrip().strip():
                queryIdToRelvDocs[tabbed[0]].append(tabbed[2].rstrip().strip())

        return queryIdToRelvDocs




def DistanceBetween(testFiles, records):
    queryIdToRelvDocs = LoadTestFile(testFiles)
    distb = {}

    for record in records:
        distb[record] = []
        windowSet = records[record].docsReturned
        docsBetween = 0

        for x in range(0, len(records[record].docsReturned)):
            for element in windowSet:
                docsBetween += 1
                if element in queryIdToRelvDocs[record]:
                    docsBetween = 0

            distb[record].append(docsBetween)


    



def MovingAverage(window, testFiles, records):

    queryIdToRelvDocs = LoadTestFile(testFiles)
    distb = {}

    for record in records:
        distb[record] = []
        
        for x in range(0, len(records[record].docsReturned)):

            start = x - window
            end = x + window
            relCount = 0

            if start < 0:
                windowSet = records[record].docsReturned[0:end]

            elif end >= len(records[record].docsReturned):
                windowSet = records[record].docsReturned[start:len(records[record].docsReturned) -1]

            else:
                windowSet = records[record].docsReturned[start:end]


            for element in windowSet:
                if element in queryIdToRelvDocs[record]:
                    relCount += 1

        
            extraMass = 1 / len(windowSet)

            distb[record].append( (relCount / len(windowSet)) + extraMass)


    return distb
