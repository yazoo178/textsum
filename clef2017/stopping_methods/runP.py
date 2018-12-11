import operator
import matplotlib.pyplot as plt
import math
import numpy as np
import sys, getopt
import random
import os
from subprocess import call
import subprocess
import re




files = []
files.append('C:\\Users\\william\\Documents\\TextSum\\clef2017\\paricpant-runs-test\\AUTh\\auth_run2_1000.task2')
files.append('C:\\Users\\william\\Documents\\TextSum\\clef2017\\paricpant-runs-test\\AUTh\\auth_run3_1000.task2')
files.append('C:\\Users\\william\\Documents\\TextSum\\clef2017\\paricpant-runs-test\\UWaterloo\\UWA.task2')
files.append('C:\\Users\\william\\Documents\\TextSum\\clef2017\\paricpant-runs-test\\UWaterloo\\UWB.task2')
subprocess.Popen("pwd")
    
exit()
for run_file in files:
    run_file = run_file.replace('\\', '\\\\')

    
    for i in [70, 80, 90, 95, 100]:
        #output = proc  = subprocess.check_output('python PoissonEstimateMethod.py -q C:\\Users\\william\\Documents\\TextSum\\clef2017\\qrel\\qrel_abs_test_2018 -r {0} -i {1}'.format(run_file, str(i)), shell=True)
        try:
            subprocess.check_output(['python', 'PoissonEstimateMethod.py'])     
        except subprocess.CalledProcessError as e:
            print(e)

        scores = output.decode().split('\t')
        scores[-1] = scores[-1].strip()
        scores = np.array([str((val * 100)) + "%", scores], dtype=object)
        table.append(scores)

    table = np.array(table)
    print(table)
        

