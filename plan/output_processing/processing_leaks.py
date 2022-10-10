import re

observed_modules = []
occ = {}
svf_sum = {}
fin_svf ={}
with open ("./final_final_leaks.txt","r") as f:
    data = f.read().split('\n')
    for line in data:
        info = re.match(r"(?P<val>\d+.\d+)\s+(?P<signame>.+)",line)
        if not info:
            continue
        else:
            info = info.groupdict()
        sig_heir = info['signame'].split(".")
        for modules in sig_heir[:-1]:
          if not modules in observed_modules:
            observed_modules.append(modules)
        #No of occurance of each module
        for modu in observed_modules:
          if modu in info['signame']:
            if modu in occ:
              svf_sum[modu]+=float(info["val"])
              occ[modu]+=1
            else:
              svf_sum[modu]=float(info["val"])
              occ[modu]=1

for modu in occ:
  fin_svf[modu]=(svf_sum[modu])/(occ[modu])


with open ("final_report.txt","w") as f:
    for modules in fin_svf:
        f.write(f"{modules:<40} = {fin_svf[modules]:<10}\n")

