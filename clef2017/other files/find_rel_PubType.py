#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Find the type of publication for relevant abstracts and save the result in excel sheet
last updated: 7 July 2017
@author: amal
"""

import xlsxwriter
from Bio import Entrez
from Bio import Medline

abs_qrel = open('Training Data/qrel_abs_train','r').readlines()

abs_rel = []

for j,doc in enumerate(abs_qrel):
    line = abs_qrel[j].split()
    if line[3] == '1':
        abs_rel.append(line[2])


workbook = xlsxwriter.Workbook('pub_type.xlsx')
worksheet = workbook.add_worksheet()

row = 0  
counter = 0
final_records =  []

handle = Entrez.efetch(db="pubmed", id=[str(p) for p in abs_rel], rettype="medline", retmode="text")
records = Medline.parse(handle)  
records = list(records) 
for ii , rec in enumerate(records):
    final_records.append(records[ii]) 
    
for k, record in enumerate(final_records):
    worksheet.write(row, 0, final_records[k].get("PMID","?"))
    worksheet.write(row, 1, str(final_records[k].get("PT", "?")))
    row += 1
    counter +=1

print (counter)   
print (row)
handle.close()
workbook.close()        