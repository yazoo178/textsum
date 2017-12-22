"""
(4) endecode MeSH heading extracted from queries and retrived for each PubMed PIDs

"""
import os

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
#*************************************************   
      
size1 = len(topics_nums)
num = 0

#encoded MeSHs for all PID
#loop for all topics
while size1 > 0 :
    new_folder_MeSH = '/Users/amal/Desktop/Data/CLEF2017/TrainingDataset/MeSHs/encoded/'  + str(topics_nums[num]) + '/' 
    if not os.path.exists(new_folder_MeSH):
        os.makedirs(new_folder_MeSH)
        
    path1 = '/Users/amal/Desktop/Data/CLEF2017/TrainingDataset/MeSHs/original/' + str(topics_nums[num]) +'/'
    path2 = '/Users/amal/Desktop/Data/CLEF2017/TrainingDataset/MeSHs/encoded/' + str(topics_nums[num]) +'/'
    
    #read MeSH heading for all abstract
    mesh_ids = os.listdir(path1)
    
    size2 = len(mesh_ids)
    i = 0
    
    #loop for all PIDs
    while size2 > 0 :
        
        Meshs_abs = open(path1+mesh_ids[i],'r',encoding="ISO-8859-1").read() 
        Meshs_abs = Meshs_abs.replace('[','').replace(']','').replace('*','').replace("'",'')
        temp = Meshs_abs.split(',')
        
        #encode MeSH heading - add MeSH as suffix to each MeSh heading
        for j,n in enumerate(temp):    
            index = temp[j].find('/')
            if index != -1: 
                t = temp[j][0:index-1]
                temp[j] = t        
            temp[j] = temp[j].strip().rstrip()
            temp[j] = temp[j].replace(' ','')
            temp[j] = 'MeSH' + temp[j]

            
        decode_MeSH =  " ".join( x for x in temp)
        
        file_name = path2 + mesh_ids[i]
        file = open(file_name,"w", encoding="utf8") 
        
        #write encoded MeSH 
        file.write(decode_MeSH)
        file.close()
        
        i += 1
        size2 -= 1
    
    num += 1   
    size1 -= 1
    
#encoded MeSHs extracted from querise
while size1 > 0 :
           
    path1 = '/Users/amal/Desktop/Data/CLEF2017/TrainingDataset/MeSHsTerms/Mesh/' + str(topics_nums[num]) +'.txt'
    path2 = '/Users/amal/Desktop/Data/CLEF2017/TrainingDataset/MeSHsTerms/encodedMeSH/' + str(topics_nums[num]) +'.txt'
        
    Meshs = open(path1,'r',encoding="ISO-8859-1").read() 
    Meshs = Meshs.replace('[','').replace(']','').replace('*','').replace("'",'')
    temp = Meshs.split(',')
    
    #encode MeSH heading - add MeSH as suffix to each MeSh heading
    for j,n in enumerate(temp):    
        index = temp[j].find('/')
        if index != -1: 
            t = temp[j][0:index-1]
            temp[j] = t        
        temp[j] = temp[j].strip().rstrip()
        temp[j] = temp[j].replace(' ','')
        temp[j] = 'MeSH' + temp[j]

        
    decode_MeSH =  " ".join( x for x in temp)
    
    file_name = path2 
    file = open(file_name,"w", encoding="utf8") 
    
    #write encoded MeSH 
    file.write(decode_MeSH)
    file.close()
    
    
    num += 1   
    size1 -= 1
    