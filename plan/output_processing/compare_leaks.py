import os
import re


#File path for leaks of Non-Obfuscated core
noobs_path="/home/mindgrove/data/rohit/c-class-test/power-side-channel-analysis/plan/output_processing/final_leaks.txt"
#File path for leaks of Obfuscated core
obs_path="/home/mindgrove/data/rohit/c-class-work/power-side-channel-analysis/plan/output_processing/final_leaks.txt"
#File Path for the comparison report
compare_report="/home/mindgrove/data/rohit/c-class-work/power-side-channel-analysis/plan/output_processing/comparison_report.txt"
#Separate file for separate modules
dcache_file="/home/mindgrove/data/rohit/c-class-work/power-side-channel-analysis/plan/output_processing/dcache_sig.txt"
fillbuffer_file="/home/mindgrove/data/rohit/c-class-work/power-side-channel-analysis/plan/output_processing/fillbuffer_sig.txt"
registerfile_file="/home/mindgrove/data/rohit/c-class-work/power-side-channel-analysis/plan/output_processing/registerfile_sig.txt"
# dcache_file="/home/mindgrove/data/rohit/c-class-work/power-side-channel-analysis/plan/output_processing/dcache_sig.txt"


#Opening both result files in read mode
f_obs=open(obs_path,"r")
f_noobs=open(noobs_path,"r")

#Opening comparison report in write mode
wf_comp=open(compare_report,"w")
wf_comp.write("COMPARISON REPORT\n")

#Storing data from both files in two separate varialbles
data_obs=f_obs.read().split("\n")
data_noobs=f_noobs.read().split("\n")



# Printing the signal information in both result files
wf_comp.write("Number of leaked signals in Obfuscated core = "+str(len(data_obs))+"\n")
wf_comp.write("Number of leaked signals in Non-Obfuscated core = "+str(len(data_noobs))+"\n")


#Arranging the data from both in a dictionary for comaprison
#dict_obs holds the result for obfuscated core
dict_obs={}
for line_obs in data_obs:
    info_obs=re.search(r"(?P<val>\d.\d+)\s+(?P<signame>.+)",line_obs) 
    if not(info_obs):
        continue
    else:
        info_obs=info_obs.groupdict()
    dict_obs[info_obs['signame']]=info_obs['val']
    
#dict_noobs holds the result for obfuscated core
dict_noobs={}
for line_noobs in data_noobs:
    info_noobs=re.search(r"(?P<val>\d.\d+)\s+(?P<signame>.+)",line_noobs) 
    if not(info_noobs):
        continue
    else:
        info_noobs=info_noobs.groupdict()
    dict_noobs[info_noobs['signame']]=info_noobs['val']

#Checking Signals which exists in obfuscated core which was not present in the non-obfuscated core
#using sets to find difference between two dictionaries keys
obs_sigs=set(dict_obs.keys())
noobs_sigs=set(dict_noobs.keys())

#extra_obs is the signals which were not leaking in the non-obfuscated core
extra_obs= obs_sigs-noobs_sigs
#extra_noobs are the signals which were not leaking in the non-obfuscated core
extra_noobs= noobs_sigs-obs_sigs
#common_sig holds the signal which are in both the results
common_sig= obs_sigs.intersection(noobs_sigs)


#Using a dictionary to print all the signals in extra_obs
ex_leak_obs={}
for sig_obs in extra_obs:
    ex_leak_obs[sig_obs]=dict_obs[sig_obs]

#Sorting the dictionary according to values
wf_comp.write("Signals which have leaked only in Obfuscated Core\n")
#Printing number of leaks in this category
wf_comp.write("Total Number= "+str(len(ex_leak_obs))+"\n")
count_leaks=0
for sig_values_obs in sorted(ex_leak_obs.items(), key = lambda kv:kv[1],reverse=True):
    #0.6 is the threshold they have set in the PARAM Paper
    #Remove this line if all leaked signals are required
    if (float(sig_values_obs[1])>0.6):
        count_leaks+=1
        wf_comp.write(sig_values_obs[1]+"\t\t"+sig_values_obs[0]+"\n") # Only keep this line if all leaks are needed
wf_comp.write("Number of Leaks with SVF greater than threshold (0.6) = "+str(count_leaks)+"\n")


#Check for difference in value for common signals in both the results
#eq_sig are signals which have same value in both obsfucated and non-obfuscated core
eq_sig=[]
#gr_obs are signals which have greater value in obs
gr_obs=[]
#ls_obs are signals which have lesser value in obs
ls_obs=[]
for sig in common_sig:
    if (dict_obs[sig]==dict_noobs[sig]):
        eq_sig.append(sig)
    elif(dict_obs[sig]>dict_noobs[sig]):
        gr_obs.append(sig)
    else:
        ls_obs.append(sig)

#Printing in the comparison report
wf_comp.write("-------------------------------------------------\n")
wf_comp.write("Signals that have same values in both obfuscated and non obfuscated core\n")
wf_comp.write("Number of leaked signals that have same values in both obfuscated and non obfuscated core = "+str(len(eq_sig))+"\n")
const_eq=0
const_gr=0
const_ls=0
for sig in eq_sig:
    if(float(dict_obs[sig])>0.6):
        const_eq+=1
        wf_comp.write(dict_obs[sig]+"  "+sig+"\n")
wf_comp.write("Number of Leaks in this section with SVF greater than threshold (0.6) = "+str(const_eq)+"\n")

wf_comp.write("-------------------------------------------------\n")
wf_comp.write("Signals that have greater values in obfuscated as compared to non obfuscated core\n")
wf_comp.write("Number of leaked signals that have greater values in obfuscated as compared to non obfuscated core = "+str(len(gr_obs))+"\n")
for sig in gr_obs:
    if(float(dict_obs[sig])>0.6):
        const_gr+=1
        wf_comp.write("OBS = "+dict_obs[sig]+"  Non-OBS = "+dict_noobs[sig]+"  "+sig+"\n")        
wf_comp.write("Number of Leaks in this section with SVF greater than threshold (0.6) = "+str(const_gr)+"\n")    

wf_comp.write("-------------------------------------------------\n")
wf_comp.write("Signals that have have lesser values in obfuscated as compared to non obfuscated core\n")
wf_comp.write("Number of leaked signals that have lesser values in obfuscated as compared to non obfuscated core = "+str(len(ls_obs))+"\n")
for sig in ls_obs:
    wf_comp.write("OBS = "+dict_obs[sig]+"  Non-OBS = "+dict_noobs[sig]+"  "+sig+"\n")        
wf_comp.write("-------------------------------------------------\n")
wf_comp.write("-------------------------------------------------\n")

#Putting the signal is seperate files
#Printing the signals present in dcache
with open(dcache_file,"w") as wf_dcache:
    wf_dcache.write("Signals present in dcache\n")
    wf_dcache.write("All dcache signals\n")
    sig_dcache=0
    dcache_obs_noobs=[]
    dcache_obs=[]
    for sig in dict_obs:
        if(re.search("TOP.mkTbSoc.soc.ccore.dmem.dcache.",sig)):
            # if(float(dict_obs[sig])>0.6):
            sig_dcache+=1
            if sig in dict_noobs:
                dcache_obs_noobs.append("OBS = "+dict_obs[sig]+"  Non-OBS = "+dict_noobs[sig]+"  "+sig+"\n")        
            else:
                dcache_obs.append("OBS = "+dict_obs[sig]+"  "+sig+"\n") 
    wf_dcache.write("Number of leaked signals in dcache = "+str(sig_dcache)+"\n")               
    for i in dcache_obs_noobs:
        wf_dcache.write(f"{i}")
    for i in dcache_obs:
        wf_dcache.write(f"{i}")
    wf_dcache.write("-------------------------------------------------\n")
#Printing the signals present in fillbuffer
with open(fillbuffer_file,"w") as wf_fb:
    wf_fb.write("Signals present in fillbuffer\n")
    wf_fb.write("All fillbuffer signals\n")
    sig_fb=0
    fb_obs_noobs=[]
    fb_obs=[]
    for sig in dict_obs:
        if(re.search("TOP.mkTbSoc.soc.ccore.dmem.dcache.m_fillbuffer.",sig)):
            # if(float(dict_obs[sig])>0.6):
            sig_fb+=1
            if sig in dict_noobs:
                fb_obs_noobs.append("OBS = "+dict_obs[sig]+"  Non-OBS = "+dict_noobs[sig]+"  "+sig+"\n")        
            else:
                fb_obs.append("OBS = "+dict_obs[sig]+"  "+sig+"\n") 
    wf_fb.write("Number of leaked signals in fillbuffer = "+str(sig_fb)+"\n")               
    for i in fb_obs_noobs:
        wf_fb.write(f"{i}")
    for i in fb_obs:
        wf_fb.write(f"{i}")
    wf_fb.write("-------------------------------------------------\n")

# Printing signals in registerfile
with open(registerfile_file,"w") as wf_regfile:
    wf_regfile.write("Signals present in registerfile\n")
    wf_regfile.write("All registerfile signals\n")
    sig_regfile=0
    rf_obs_noobs=[]
    rf_obs=[]
    for sig in dict_obs:
        if(re.search("TOP.mkTbSoc.soc.ccore.riscv.stage2.registerfile.",sig)):
            # if(float(dict_obs[sig])>0.6):
            sig_regfile+=1
            if sig in dict_noobs:
                rf_obs_noobs.append("OBS = "+dict_obs[sig]+"  Non-OBS = "+dict_noobs[sig]+"  "+sig+"\n")        
            else:
                rf_obs.append("OBS = "+dict_obs[sig]+"  "+sig+"\n")       
    for i in rf_obs_noobs:
        wf_regfile.write(f"{i}")
    for i in rf_obs:
        wf_regfile.write(f"{i}")
    wf_regfile.write("Number of leaked signals in registerfile = "+str(sig_regfile)+"\n")
    wf_regfile.write("============================================================================================================\n")
wf_comp.write("============================================================================================================\n")



    



















wf_comp.close()
f_noobs.close()
f_obs.close()

