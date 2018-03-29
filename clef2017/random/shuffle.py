
import random
import re

lines = []
records = {}
with open("Output/Test_Data_Sheffield-run-2", encoding='utf-8') as content:
    
   lastId = "Start"

   for line in content:
       tabbed = re.split("\s", line)

       if tabbed[0] not in records:
           records[tabbed[0]] = []

       records[tabbed[0]].append(line)


   for record in records:
       random.shuffle(records[record])
       
       for line in records[record]:
           lines.append(line)
    


with open("Output/Test_Data_Sheffield-run-2_rand", "w") as content:
    for line in lines:
        content.write(line)