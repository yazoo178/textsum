
NUMBEROFDOCSMIN = 100
RELDOCSMIN = 10

def HasMoreThanNDocuments(topic):
    return len(topic) >= NUMBEROFDOCSMIN


def HasMoreThanNRelDocuments(topic):
    return len(topic) > RELDOCSMIN