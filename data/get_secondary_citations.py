import glob
import json
import os
from crossref.restful import Works
import numpy as np
import pandas as pd
import string
import random

def gen_random_string(k=50):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=k))

works = Works()

fnames = glob.glob("json\\*_open_cite.json")

try:
    os.mkdir("secondary")
except:
    print("Folder already exists")

try:
    os.mkdir("processed")
except:
    print("Folder already exists")

def get_json(filename):
    with open(filename) as f:
        data = json.load(f)
    if len(data) == 1:
        return data[0]
    else:
        return data

restart = True
if restart:
    i_start  = 2860
    doi_hmap = {}
    uid_set  = set()
    hmap_new = pd.read_csv("secondary\\doi_hmap.csv")
    for i in range(len(hmap_new)):
        doi_hmap[hmap_new.iloc[i,0]] = hmap_new.iloc[i,1]
        uid_set.add(hmap_new.iloc[i,1])
    no_dates = pd.read_csv("secondary\\no_dates.csv").values.tolist()
    full_fail = []
else:
    i_start  = 0
    doi_hmap = {}
    uid_set  = set()
    no_dates = []
    full_fail = []

for i in range(i_start, len(fnames)):
    try:
        fname = fnames[i]
        print(f"Iteration {i}, filename: {fname}")
        
        data = get_json(fname)
        
        # augment with dates
        cita = data["citation"].split(";")
        data["citation_date"] = []
        for j in range(len(cita)):
            # read from file if in the set else get
            if cita[j] in doi_hmap:
                try:
                    out = get_json("secondary\\"+doi_hmap[cita[j]]+".json")
                except:
                    data["citation_date"].append(None)
                try:
                    data["citation_date"].append(out["created"]["date-parts"][0])
                except:
                    no_dates.append(doi_hmap[cita[j]])
            else:
                print(cita[j])
                try:
                    out = works.doi(cita[j])
                    # generate unique id to save
                    rstr = gen_random_string()
                    while rstr in uid_set:
                        rstr = gen_random_string()
                    uid_set.add(rstr)
                    
                    # save unique id to hashmap
                    doi_hmap[cita[j]] = rstr
                    
                    # save to file
                    with open("secondary\\"+doi_hmap[cita[j]]+".json", 'w') as f:
                        json.dump(out, f)
                    try:
                        data["citation_date"].append(out["created"]["date-parts"][0])
                    except:
                        no_dates.append(doi_hmap[cita[j]])
                except:
                    data["citation_date"].append(None)
            
            if j%10 == 0:
                temp = pd.Series(doi_hmap).to_frame().to_csv("secondary\\doi_hmap.csv")
        
        # save augmented version
        fname = fname.split("\\")[1]
        with open("processed\\"+fname, "w") as f:
            json.dump(data, f)
    except:
        full_fail.append(fname)

df = pd.Series(doi_hmap).to_frame()
df.to_csv("secondary\\doi_hmap.csv")

df2 = pd.DataFrame(no_dates).to_csv("secondary\\no_dates.csv")

df3 = pd.Series(full_fail).to_frame()
df3.to_csv("secondary\\full_fail.csv")