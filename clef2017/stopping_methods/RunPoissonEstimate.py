#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 17:35:09 2019

@author: william
"""

from PoissonEstimateMethod import setQrel, setDocsNeeded, setRunData, runPEM

lineResults = []
#-q /Users/william/Documents/textsum/clef2017/qrel/qrel_abs_test -r /Users/william/Documents/textsum/clef2017/participant-runs/Sheffield/Test_Data_Sheffield-run-2 -i 70
line = ""
desieredRecalls = [70, 80, 90, 95, 100]
runs =  ['/Users/william/Documents/textsum/clef2017/participant-runs/Sheffield/Test_Data_Sheffield-run-2',
         '/Users/william/Documents/textsum/clef2017/participant-runs/Waterloo/A-rank-cost.txt',
         '/Users/william/Documents/textsum/clef2017/participant-runs/Waterloo/B-rank-cost.txt',
         '/Users/william/Documents/textsum/clef2017/participant-runs/AUTH/simple-eval/run-1',
         '/Users/william/Documents/textsum/clef2017/participant-runs/AUTH/simple-eval/run-2',
         '/Users/william/Documents/textsum/clef2017/participant-runs/NTU/test_ranked_run_1.txt',
         '/Users/william/Documents/textsum/clef2017/participant-runs/UCL/run_fulltext_test.txt']


runsTest = ['/Users/william/Documents/textsum/clef2017/paricpant-runs-test/SHEF/sheffield-feedback.task2',
            '/Users/william/Documents/textsum/clef2017/paricpant-runs-test/UWaterloo/UWA.task2',
'/Users/william/Documents/textsum/clef2017/paricpant-runs-test/UWaterloo/UWB.task2',
'/Users/william/Documents/textsum/clef2017/paricpant-runs-test/AUTh/auth_run2_1000.task2',
'/Users/william/Documents/textsum/clef2017/paricpant-runs-test/AUTh/auth_run3_1000.task2',
'/Users/william/Documents/textsum/clef2017/paricpant-runs-test/UIC/uci_model8.task2',
'/Users/william/Documents/textsum/clef2017/paricpant-runs-test/IMS/ims_unipd_t1500.task2']

for run in runsTest:
    for x in desieredRecalls:
        docs = setDocsNeeded(x)
        data =  setRunData(run)
        results = runPEM(data, docs,'/Users/william/Documents/textsum/clef2017/qrel/qrel_abs_test_2018')
        line += "{0:.3f}".format(results[0]) + "&" + "{0:.3f}".format(results[2]) + "&"
        
    lineResults.append(line)
    line = ""
    
print(lineResults)