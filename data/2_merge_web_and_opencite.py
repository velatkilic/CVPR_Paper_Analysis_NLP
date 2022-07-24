# %%
import numpy as np
import pandas as pd
import glob
from leven import levenshtein
from tqdm import tqdm

# %%

def get_authors(auth_list):
    auth_list = auth_list.split(';')
    out = []
    for auth in auth_list:
        name = auth.split(',')
        out_name = []
        for n in name: out_name.append(n.strip().lower())
        out.append(out_name)
    return out


# %% Collect all open cite json files into a dataframe
fnames = glob.glob("json\\*_open_cite.json")

df_json = []
for fname in tqdm(fnames):
    df_json.append(pd.read_json(fname))

df_json = pd.concat(df_json)

df_json.head(1)
# %% discard unnec information
df_json = df_json[["author", "title", "year", "citation_count", "doi", "citation"]]
df_json[["author","title"]] = df_json[["author","title"]].apply(lambda x: x.str.lower())

df_json.head(1)

# %% load cvpr web data
df = pd.read_csv("data\\cvpr_web.csv")
df.head(1)

# %%
missed = [] # neither authors nor title match
author_matched = [] # title match not perfect but authors match
df_match = []
dummy = pd.Series({"title":"", "citation_count":-1, "doi":0, "citation":""})
verbose = False
for i in tqdm(range(df.shape[0])):
    if df.iloc[i,:]["year"] != 2022: # we don't have citations for 2022
        # attempt matching based on title
        title = df.iloc[i,:]["title"].lower()
        
        # calculate levenshtein distance
        scores = df_json["title"].apply(lambda x: levenshtein(x, title))
        
        # get index with min levenshetein distance
        match_idx = scores.argmin()
        match_score = scores.iloc[match_idx]
        match_title = df_json["title"].iloc[match_idx]
        if verbose:
            print(title)
            print(f"Match score: {match_score}, title: {match_title}")

        # if distance is zero, then use the match else check authors
        if match_score == 0:
            df_match.append(df_json.iloc[match_idx,:][["title","citation_count","doi","citation"]])
        else:
            matched_authors = get_authors(df_json.iloc[match_idx,:]['author'])
            authors = df.iloc[i,:]["authors"].lower()
            if matched_authors[0][0] in authors:
                df_match.append(df_json.iloc[match_idx,:][["title","citation_count","doi","citation"]])
                author_matched.append([title, match_title])
            else:
                missed.append(i)
                df_match.append(dummy)
    else:
        df_match.append(dummy)

# %% save matches to file
df_match = pd.DataFrame(df_match)
df_match.head(1)
df_match.to_csv("data\\cvpr_open_cite.csv", index=False)
# %% merge cvpr web data with open cite data
df_match.reset_index(inplace=True, drop=True)
df_augmented = pd.concat([df,df_match[["citation_count","doi","citation"]]], axis=1)
# %% keep open-cite title for comparison and debugging
df_augmented["title_open_cite"] = df_match["title"]
# %% save to file
df_augmented.to_csv("data\\cvpr_data.csv", index=False)