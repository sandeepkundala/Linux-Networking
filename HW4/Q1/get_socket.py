import sys

file_name = sys.argv[1]
f = open(file_name,"r")
c = f.readline()
ls = []
res = []
for line in f:
    ls.append(line)

for lineNum in range(len(ls)):
    if "socket" in ls[lineNum].split()[1]:
        res.append(ls[lineNum].replace("\n",""))
        if "socket" not in ls[lineNum+1].split()[1]:
            res.append(ls[lineNum+1].replace("\n",""))

for line in res:
    print(line)
