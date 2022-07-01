# 2021: 10.1109/CVPR46437.2021.00007
# 2020: 10.1109/CVPR42600.2020.00008
# 2019: 10.1109/CVPR.2019.00009
# 2018: 10.1109/CVPR.2018.00008
# 2017: 10.1109/CVPR.2017.8
# 2016: 10.1109/CVPR.2016.8
# 2015: 10.1109/CVPR.2015.7298594
# 2014: 10.1109/CVPR.2014.8
# 2013: 10.1109/CVPR.2013.8

import requests
import pandas as pd
import numpy as np
import json
import time
from crossref.restful import Works
import os

try:
    os.mkdir("json")
except:
    print("json folder already exists")

works = Works()

years = np.arange(2013,2022)
sinds = np.array([8,8,7298594,8,8,8,9,8,7])

skipped = []
for i in range(7,len(years)):
    data = pd.read_csv("year_"+str(years[i])+".csv")
    if (years[i]==2021):
        year_id = "46437."+str(years[i])+"."
    elif years[i]==2020:
        year_id = "42600."+str(years[i])+"."
    else:
        year_id = "."+str(years[i])+"."
    
    json_data = []
    N = data.shape[0]
    t = 1
    for j in range(N):
        try:
            print(f"iteration: {j} time: {t} seconds")
            # time.sleep(1)
            t1 = time.time()
            if years[i] >= 2018:
                num_id = str(j+sinds[i]).zfill(5)
            else:
                num_id = str(j+sinds[i])
            unique_id = year_id + num_id
            
            page  = requests.get("https://opencitations.net/index/api/v1/metadata/10.1109/CVPR"+unique_id)
            out   = page.json()
            out2  = works.doi("10.1109/CVPR"+unique_id)
            
            t2 = time.time()
            t = t2 - t1
            
            with open("json\\year_"+str(years[i])+"_"+str(j)+"_open_cite.json", 'w') as f:
                json.dump(out, f)
            
            with open("json\\year_"+str(years[i])+"_"+str(j)+"_cross_ref.json", 'w') as f:
                json.dump(out2, f)
        except:
            print(f"{j} didn't work skipping")
            skipped.append([years[i], j])

skipped = pd.DataFrame(skipped)
print(skipped)

skipped.to_csv("skipped.csv")

for i in range(len(skipped)):
    year = skipped.iloc[i,0]
    j    = skipped.iloc[i,1]
    data = pd.read_csv("year_"+str(year)+".csv")
    if (year==2021):
        year_id = "46437."+str(year)+"."
    elif year==2020:
        year_id = "42600."+str(year)+"."
    else:
        year_id = "."+str(year)+"."
    
    json_data = []
    N = data.shape[0]
    t = 1
    try:
        print(f"iteration: {j} time: {t} seconds")
        # time.sleep(1)
        t1 = time.time()
        if year >= 2018:
            num_id = str(j+sinds[i]).zfill(5)
        else:
            num_id = str(j+sinds[i])
        unique_id = year_id + num_id
        
        page  = requests.get("https://opencitations.net/index/api/v1/metadata/10.1109/CVPR"+unique_id)
        out   = page.json()
        out2  = works.doi("10.1109/CVPR"+unique_id)
        
        t2 = time.time()
        t = t2 - t1
        
        # with open("json\\year_"+str(year)+"_"+str(j)+"_open_cite.json", 'w') as f:
        #     json.dump(out, f)
        
        with open("json\\year_"+str(year)+"_"+str(j)+"_cross_ref.json", 'w') as f:
            json.dump(out2, f)
    except:
        print(f"{i} didn't work skipping")