# %%
import numpy as np
import pandas as pd
import glob
import json
import os
from leven import levenshtein
from soupsieve import match  

def get_json(fname):
    with open(fname,"r") as f:
        data = json.load(f)
    if len(data) == 1:
        return data[0]
    else:
        return data

def get_authors(auth_list):
    auth_list = auth_list.split(';')
    out = []
    for auth in auth_list:
        name = auth.split(',')
        out_name = []
        for n in name: out_name.append(n.strip().lower())
        out.append(out_name)
    return out


# %%

try:
    os.mkdir("merged")
except:
    print("Folder already exists")

fnames = glob.glob("processed\\*_open_cite.json")
years  = np.arange(2013,2022)
dfs    = {}

for year in years:
    dfs[year] = pd.read_csv("year_"+str(year)+".csv")
    dfs[year]['title'] = dfs[year]['title'].apply(lambda x: x.lower())

# %%
missed = [] # neither authors nor title match
author_matched = [] # title match not perfect but authors match
for i, fname in enumerate(fnames):
    if i % 100 == 0: print(i)

    fyear = int(fname.split("_")[1])

    data = get_json(fname)
    title = data["title"].lower()

    df   = dfs[fyear]
    scores = df["title"].apply(lambda x: levenshtein(x, title))
    match_idx = scores.argmin()
    match_score = scores.iloc[match_idx]
    match_title = df["title"].iloc[match_idx]

    if match_score == 0:
        save = True
    else:
        matched_authors = df.iloc[match_idx,:]['authors'].lower()
        authors = get_authors(data['author'])
        
        for auth in authors:
            for name in auth:
                if not(name in matched_authors):
                    print(f"Non-zero levenshtein distance \n" \
                        f"Scraped title: {match_title} \n" \
                        f"Json title: {title}")
                    
                    missed.append({"fname":fname, "scraped title":match_title, "json title": title })
                    save = False
                    break_ = True
                    break
                else:
                    break_ = False
            if break_: break

        if not(break_):    
            save = True
            author_matched.append({"fname":fname, "scraped title":match_title, "json title": title })
        
    if save:
        data["abstract"] = df.iloc[match_idx,:]["abstract"]
        data["pdf_link"] = df.iloc[match_idx,:]["link"]
        data['title'] = df.iloc[match_idx,:]["title"] # scraped titles are cleaner
        
        sname = fname.split("\\")[1]
        with open("merged\\"+sname, "w") as f:
            json.dump(data, f)

df_missed = pd.DataFrame(missed)
df_missed.to_csv("merged\\missed.csv")

df_auth = pd.DataFrame(author_matched)
df_auth.to_csv("merged\\author_matched.csv")

print("Done.")
# %%
