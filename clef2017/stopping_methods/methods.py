import re


rankedDocsDoL = {}
ranked_docs = {}
rel_count = {}
docsFoundDoL = {}
judgements = {}


def loadrun(run_file, qrel_file):


    f = open(qrel_file, "r") 
    for line in f: 
        items = line.split()
        topic = items[0]
        pid = items[2]
        qrel = items[3]

        if topic not in judgements:
            judgements[topic] = {}
        if(qrel is "1"): 
             judgements[topic][pid] = qrel

    f.close()


    # Dict containing relevance counts 

    # Read through run output and create lists of pmids found
    f = open(run_file, "r")

    last_topic = "null"
    topic_count = 0

    for line in f:
        items = line.split()
        topic = items[0]
        pid = items[2]
        rank = items[3]
        score = items[4]

        if(topic != last_topic):
            rel_count = 0
            docsFoundDoL[topic] = []
            rankedDocsDoL[topic] = []
            last_topic = topic

        # Code to create graph of output - might as well keep this here for now
        if(pid in judgements[topic]):
            rel_count = rel_count + 1

        # Store in list of running total of found documents
        docsFoundDoL[topic].append(rel_count)
        # Store in list of ranked documents
        rankedDocsDoL[topic].append({'pid' : pid, 'score' : score})




def eval(topic, cutoffPoint):

    relieability = 0

    recall = cutoffPoint / len(judgements[topic])

    effort = cutoffPoint / len(rankedDocsDoL[topic])
        
    if recall > 0.7:
        relieability = 1

    return [recall, effort, relieability]




def run_on_topic(topic, cutoff, starPoint = 1, min = 0):
    recall_stats = {}
    effort_stats = {}

    cutPoint = 0


    lastScore = 0

        #min docus to look at for this topic
    minDocs = int(float(len(rankedDocsDoL[topic])) * min)

    for x, study in enumerate(rankedDocsDoL[topic]):
        score = study['score']

        if cutoff == 0:
            if x >= minDocs:
                cutoffs[topic] = x
                break

        else:
                #always look at one document
            if x == 0:
                lastScore = score
                continue

                #if our simularity score has reached 0 then end
            if float(lastScore) == 0.0:
                cutPoint = len(rankedDocsDoL[topic])
                break

            if starPoint is not None:
                topDoc = (float(rankedDocsDoL[topic][starPoint]['score']))
                decrase = topDoc - float(lastScore)
                dif  = decrase / topDoc 

                    

            else:
                #calculate the dif between current score and last score
                decrase = (float(lastScore)  - float(score))
                dif  = decrase / (float(lastScore))


                #if difference is greater than cut off then break. 
            if dif >= cutoff and x >= minDocs:
                cutPoint = x
                break

            if x + 1 == len(rankedDocsDoL[topic]):
                cutPoint = len(rankedDocsDoL[topic])
                break

            lastScore = score
        
        
    return cutPoint


#Class for reprsenting a topic
class record:
    def __init__(self, qId):
        self.queryId = qId
        self.docsReturned = []

    def addDoc(self, doc):
        self.docsReturned.append(doc)



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


def calcMovingAverage(window, testFiles, records):

    queryIdToRelvDocs = {}
    distb = {}
    relIndexs = {}


    ##Load Qrel
    with open(testFiles, encoding='utf-8') as content:
        for i, line in enumerate(content):
            tabbed = re.split('\s+', line)

            if tabbed[0] not in queryIdToRelvDocs:
                queryIdToRelvDocs[tabbed[0]] = []
                

            if '1' in tabbed[3].rstrip().strip():
                queryIdToRelvDocs[tabbed[0]].append(tabbed[2].rstrip().strip())


    #Loop topics
    for record in records:
        distb[record] = []
        relIndexs[record] = []

        for x in range(0, len(records[record].docsReturned)):

            if records[record].docsReturned[x] in queryIdToRelvDocs[record]:
                relIndexs[record].append(x)

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

        
            #extraMass = 1 / len(windowSet)
            extraMass = 1

            distb[record].append( (relCount / len(windowSet)) * extraMass)


    return distb, relIndexs