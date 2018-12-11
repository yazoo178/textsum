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

folder = None

opts, args = getopt.getopt(sys.argv[1:],"f:")
for opt, arg in opts:
    if opt in ("-f"):
        if os.path.exists(arg):
            folder = arg
        else:
            exit("Folder doesn't exist")


for filename in os.listdir(folder):
    run_file = folder + "\\" + filename
    run_file = run_file.replace('\\', '\\\\')
    print(run_file)

    
    
    if "Sheffield" in filename:
        table = [np.array(["dif(d_1, d_{1+i})", "recall", "reliability", "effort"])]
        for i in [0.8, 0.81, 0.82, 0.83, 0.84, 0.85,0.855, 0.86, 0.87, 0.88, 0.89]:
            #val = float(i / 10.0)
            val = i
            output = proc  = subprocess.check_output('python cutoff_method.py -o {0} -c {1} -m 0 -q C:\\Users\\william\\Documents\\TextSum\\clef2017\\qrel\\qrel_abs_test -s 1'.format(run_file, str(val)),shell=True)
            
            scores = output.decode().split('\t')
            scores[-1] = scores[-1].strip()
            scores = np.array([str((val * 100)) + "%", scores], dtype=object)
            table.append(scores)

        table = np.array(table)
        print(table)
        
