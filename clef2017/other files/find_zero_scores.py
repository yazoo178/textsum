# -*- coding: utf-8 -*-
"""
find numbr of relevants content and abstracts haveing Zero score
@author: Moli
"""

#abs_qrel = open('Training Data/qrel_abs_train','r').readlines()
#content_qrel = open('Training Data/qrel_content_train','r').readlines()

abs_qrel = open('qrel/qrel_abs_test','r').readlines()
content_qrel = open('qrel/qrel_content_test','r').readlines()

abs_rel = []
content_rel = []
doc_with_zero_score = []

for j,doc in enumerate(abs_qrel):
    line = abs_qrel[j].split()
    if line[3] == '1':
        abs_rel.append(line[0] + ' ' +  line[2])
        
for j,doc in enumerate(content_qrel):
    line = content_qrel[j].split()
    if line[3] == '1':
        content_rel.append(line[0] + ' ' +  line[2])        

def find_score (file_name, doc_with_zero_score):
    counter = 0
    file = open(file_name,'r')
    f = file.readlines()
    
    for i,j in enumerate(f):
        curr_line = f[i].split()
        if curr_line[4] == '0.0' :
            counter += 1
            doc_with_zero_score.append(curr_line[0] + ' ' + curr_line[2])
            
    print (file_name)
    print ("Number of score=0 : " + str(counter))
    

#find_score('C:/Users/Moli/PhD Sheffield/CLEF2017/Output/Sheffield-run-5',doc_with_zero_score) 
find_score('C:/Users/Moli/PhD Sheffield/CLEF2017/Output/Test_Data_Sheffield-run-1',doc_with_zero_score) 
        
#for i , output in enumerate(os.listdir(output_path)):
#    find_score(output,doc_with_zero_score,i)        
    
x1 =  []
z1_counter = 0
for k , item in enumerate(abs_rel): 
    for l , curr in enumerate(doc_with_zero_score):
        if item == curr:
            z1_counter +=1
            x1.append(item + ' ' + curr)
            
print ('abs = ' + str(z1_counter))
print 
x2 =  []
z2_counter = 0
for k , item in enumerate(content_rel): 
    for l , curr in enumerate(doc_with_zero_score):
        if item == curr:
            z2_counter +=1
            x2.append(item + ' ' + curr)
            
print ('content = ' + str(z2_counter))
print