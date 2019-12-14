from tabulate import tabulate
from collections import defaultdict
import pandas as pd
import os
import sys

file_name = sys.argv[1]
f = open(file_name,"r")
c = f.readline()
fun_dict = {}
count = 0
for line in f:
    x = line.split()
    time = float(x[0])
    func_name = x[1][:x[1].find("(")]
    if func_name in fun_dict:
        fun_dict[func_name][0]+=1
        fun_dict[func_name][1]+=time
    else:
        fun_dict[func_name]=[1,time]

for func_name in fun_dict:
    print(func_name + (20-len(func_name))*" " + str(fun_dict[func_name][0]) + (30-len(func_name)-len(str(fun_dict[func_name][0]))-(20-len(func_name)))*" " + str(fun_dict[func_name][1]))
