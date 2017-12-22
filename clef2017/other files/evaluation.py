"""
Find minimum number of documents returned to retrieve all R relevant documents
(a measure for optimistic thresholding)

"""
import os

#AUTOMATICLLY CREATE LIST OF TOICS NAMES AND IDS
#*************************************************

folder = 'TrainingData/topics_train/'
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

#*************************************************
#find min. no. of documents according to content qrel
def min_no_content (file_name):

    size = len(topics_nums)
    num = 0

    qrel_result = open(file_name,'r').readlines()
    for i,n in enumerate(qrel_result):
        qrel_result[i] = qrel_result[i].split(' ')
    print()
    print('Cotent')
    print(file_name)
    print('Topic    Min. no. of documnts')  
    print('*****    ********************')  
    while size > 0:
        
        count1 = 0 
        count2 = 0
    
        count_rev = 0
        
        rev_content = []
        list_content = [] 
        topic = topics_ids[num]
        
        for i,n in enumerate(qrel_result):
            if qrel_result[i][0] == topic:
                list_content.append(qrel_result[i])
            
            
        with open('TrainingData/qrel_content_train') as input_data:
            for line in input_data:
                if topic in line :
                    l = line.split()
                    if l[3] == '1':
                        count_rev += 1
                        rev_content.append(l[2])
                        
        
        for i,n in enumerate(list_content):
            for j,m in enumerate(rev_content):
                if rev_content[j] == list_content[i][2]:
                    count1 += 1
            count2 += 1
            if count1 == count_rev:
                break
            
        print ( str(topics_ids[num]) + ' ' + str(count2))
        
        size -=  1
        num += 1

#*************************************************
#find min. no. of documents according to abstract qrel 
def min_no_abs (file_name):

    size = len(topics_nums)
    num = 0

    qrel_result = open(file_name,'r').readlines()
    for i,n in enumerate(qrel_result):
        qrel_result[i] = qrel_result[i].split(' ')
    print()
    print ('Abstract')
    print(file_name)
    print('Topic    Min. no. of documnts')  
    print('*****    ********************')  
    while size > 0:
        
        count1 = 0 
        count2 = 0
    
        count_rev = 0
        
        rev_abs = []
        list_abs = [] 
        topic = topics_ids[num]
        
        for i,n in enumerate(qrel_result):
            if qrel_result[i][0] == topic:
                list_abs.append(qrel_result[i])
            
            
        with open('TrainingData/qrel_abs_train') as input_data:
            for line in input_data:
                if topic in line :
                    l = line.split()
                    if l[3] == '1':
                        count_rev += 1
                        rev_abs.append(l[2])
                        
        
        for i,n in enumerate(list_abs):
            for j,m in enumerate(rev_abs):
                if rev_abs[j] == list_abs[i][2]:
                    count1 += 1
            count2 += 1
            if count1 == count_rev:
                break
            
        print ( str(topics_ids[num]) + ' ' + str(count2))
        
        size -=  1
        num += 1
  
output_path = 'Output/'
for i , output in enumerate(os.listdir(output_path)):
    min_no_content(output_path+output)
    min_no_abs(output_path+output)              
