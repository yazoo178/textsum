import os

folder = 'Training Data/topics_train/'
#folder = 'Test Data/'

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

abs_qrel = open('qrel/qrel_abs_train','r').readlines()
content_qrel = open('qrel/qrel_content_train','r').readlines()

#abs_qrel = open('qrel/qrel_abs_test','r').readlines()
#content_qrel = open('qrel/qrel_content_test','r').readlines()

for i,topic in enumerate(topics_ids):
    counter = 0
    print('***********')
    print(topic)

    for j,l in enumerate(abs_qrel):
        line = abs_qrel[j].split()
        if line[0] == topic:
            if line[3] == '1':
                counter += 1
                if line[0] == 'CD008643':
                    print(line[2])
    print('relevant abs:')
    print(counter)
    print()

#for i,topic in enumerate(topics_ids):
#    counter = 0
#    for j,l in enumerate(content_qrel):
#        line = content_qrel[j].split()
#        if line[0] == topic:
#            if line[3] == '1':
#                counter += 1
#    print(topic)
#    print('relevant content:')
#    print(counter)
#    print()
