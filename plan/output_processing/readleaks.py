#------------------
import os
import re
from tqdm import tqdm
# import numpy as np
#------------------


filePath = "/home/mindgrove/data/rohit/c-class-test/power-side-channel-analysis/plan/results/trial/c_class"

count = 0
# Iterate directory
for path in os.listdir(filePath):
    # check if current path is a file
    if os.path.isfile(os.path.join(filePath, path)):
        count += 1
print('File count:', count)

wf = open('final_leaks.txt','w')

l={}
rfiles=os.listdir(filePath)
# for i in range(0,(count)):
    # with open (filePath+f"/leaks{i}"+".txt","r") as f:
for i in tqdm(rfiles,desc="Processing Leak Files",total=len(rfiles)):
    with open(filePath+f"/{i}") as f:
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

for data in tqdm(l,desc="Printing Leaks",total=len(l)):
    
    #To print only the max value of the signal
    wf.write(str(max(l[data]))+"\t\t"+data+"\n")

#     # Print all the values in array
#     wf.write(f"{l[data]}\t\t{data:>20}\n")

# print(l)

# To print the variance of signals
# l_arr={}
# for data in l:
#     fp_val=[float(x) for x in (l[data])]
#     #creating numpy array
#     np_arr=np.array(fp_val)
#     l_arr[data]=np.var(np_arr)

# for data in tqdm(l_arr,desc="Printing Variance of signals",total=len(l)):
    
#     #To print only the var value of the signal
#     wf.write(str(l_arr[data])+"\t\t"+f"{data:>50}"+"\n")


#------------------------------------------------------------------------------------------------------#
