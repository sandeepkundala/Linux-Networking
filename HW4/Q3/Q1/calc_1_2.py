import sys
import operator

file_name = sys.argv[1]
f = open(file_name,"r")
c = f.readline()
fun_dict = {}
count = 0
ucount = 0
sorted_d = {}
tot = 0
for line in f:
    x = line.split()
    try:
        time = float(x[0])
        tot+=time
        func_name = x[1][:x[1].find("(")]
        count+=1
        if func_name in fun_dict:
            fun_dict[func_name]+=time
        else:
            fun_dict[func_name]=time
            ucount+=1
    except:
        continue
sorted_d = sorted(fun_dict.items(), key = operator.itemgetter(1), reverse = True)

for arg in sys.argv:
    if arg=='top5':
        for func_name in sorted_d[:5]:
            print(func_name[0] + (20-len(func_name[0]))*" " + str(func_name[1]*100/tot))
    if arg=='nsys':
        print("\nNo. of system calls:",count)
        print("\nNo. of unique system calls:",ucount)
    if arg=='alltop':
        for func_name in sorted_d:
            print(func_name[0] + (20-len(func_name[0]))*" " + str(func_name[1]*100/tot))
    if arg=='all':
        sorted_d = sorted(fun_dict.items(), key = operator.itemgetter(0))
        for func_name in sorted_d:
            print(func_name[0] + (20-len(func_name[0]))*" " + str(func_name[1]))
        print("Total: ", tot)

