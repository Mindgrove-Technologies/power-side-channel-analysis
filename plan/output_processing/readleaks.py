#------------------
# from distutils.log import info
# from imp import init_frozen
# from distutils.log import info
import os
import re
# from selectors import EpollSelector
#------------------


filePath = "/home/mindgrove/data/rohit/c-class-work/power-side-channel-analysis/plan/results/trial/cclass_add"

count = 0
# Iterate directory
for path in os.listdir(filePath):
    # check if current path is a file
    if os.path.isfile(os.path.join(filePath, path)):
        count += 1
print('File count:', count)

wf = open('final_leaks.txt','w')

l={}

for i in range(0,(count)):
    with open (filePath+f"/leaks{i}"+".txt","r") as f:
        # print("i",i)
        data=f.read().split('\n')
        for line in data:
            info = re.match(r"(?P<signame>.+),(?P<val>\d+.\d+)",line)
            if not info:
                continue
            else:
                info = info.groupdict()
            if (info['val']=='0.0000'):
                continue
            else:
                # wf.write(f"{info['val']:<10}\t\t{info['signame']:>20}\n")
                if (info['signame'] in l):
                    l[info['signame']].append(info['val'])
                else:
                    l[info['signame']]=[info['val']]
# print(l)

# writing only the max value from all cycles
for data in l:
    print(data)
    print(l[data])
    wf.write(str(max(l[data]))+"\t\t"+data+"\n")

    # wf.write(f"{l[data]:<10}\t\t{data:>20}\n")

# print(l)
print("completed ")
#------------------------------------------------------------------------------------------------------#
