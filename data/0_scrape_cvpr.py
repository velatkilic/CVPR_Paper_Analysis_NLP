# %%
"""
Scrape CVPR paper information (abstract, author names, abstract)
"""

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
import numpy as np

# %% Functions for extracting information

# Get list of paper urls for a given year
def get_paper_urls(year, verbose=False):
    page = requests.get("https://openaccess.thecvf.com/CVPR"+year)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # get all the paper list
    urls = []
    for dt in soup.find_all("dl"):
        for title in dt.find_all("dt", {"class":"ptitle"}):
            for href in title.find_all("a", href=True):
                urls.append(href["href"])
    
    if verbose:
        print("Number of papers found: " + str(len(urls)))
    return urls

# Extract paper information from a given url
# Web page format is different for 2021 and after
# so let's wrap content extraction in different functions
def extract_pre2021(url, verbose=False):
    page = requests.get("https://openaccess.thecvf.com/"+url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    for dd in soup.find_all("dd"):
        for div in dd.find_all("div", id="papertitle"):
            title = div.get_text().strip()
        for div in dd.find_all("div", id="authors"):
            author = div.get_text().strip().split(";")[0]
        for div in dd.find_all("div", id="abstract"):
            abstract = div.get_text().strip()
        
        pdf_link = ""
        for href in dd.find_all("a", href=True):
            link = href["href"]
            if link.split(".")[-1] == 'pdf' and link.split("/")[3] == "papers":
                pdf_link = link
    if verbose:
        print(title)
    return title, author, abstract, pdf_link

def extract_post2021(url, verbose=False):
    page = requests.get("https://openaccess.thecvf.com/"+url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    for div in soup.find_all("div", id="papertitle"):
        title = div.get_text().strip()
    
    for div in soup.find_all("div", id="authors"):
        author = div.get_text().strip().split(";")[0]
    
    for div in soup.find_all("div", id="abstract"):
        abstract = div.get_text().strip()
    
    pdf_link = ""
    for dd in soup.find_all("dd"):
        for href in dd.find_all("a", href=True):
            link = href["href"]
            if link.split(".")[-1] == 'pdf' and link.split("/")[3] == "papers":
                pdf_link = link
    if verbose:
        print(title)
    return title, author, abstract, pdf_link
                

# %%

try:
    os.mkdir("data")
except:
    print("Folder already exists")

years = list(map(str, np.arange(2013,2018,1)))
years += ["2018?day=2018-06-19",
          "2018?day=2018-06-20",
          "2018?day=2018-06-21",
          "2019?day=2019-06-18",
          "2019?day=2019-06-19",
          "2019?day=2019-06-20",
          "2020?day=2020-06-16",
          "2020?day=2020-06-17",
          "2020?day=2020-06-18",
          "2021?day=all",
          "2022?day=all"
        ]
t = 2 # initial time to sleep 
xf = 1 # wait time multiplication factor

# %%
for year in years:
    urls = get_paper_urls(year)

    # visit each url to parse title, author names and the abstract
    titles    = []
    authors   = []
    abstracts = []
    pdf_links = []
    
    for url in urls:
        time.sleep(t)
        t1 = time.time()
        if year in ["2021?day=all", "2022?day=all"]:
            title, author, abstract, pdf_link = extract_post2021(url)
            pdf_link = "content/" + "/".join(pdf_link.split("/")[-3:])
        else:
            title, author, abstract, pdf_link = extract_pre2021(url)
            pdf_link = "/".join(pdf_link.split("/")[-3:])
        titles.append(title)
        authors.append(author)
        abstracts.append(abstract)
        pdf_links.append(pdf_link)
        t2 = time.time()
        t = xf*(t2-t1)
        print("Wait time: " + str(t))
        if (t > 20): break
    
    df = pd.DataFrame(
            {"title":titles, "authors":authors, "abstract":abstracts, "link":pdf_links}
        )
    filename = year.replace("?","").replace("=","")
    df.to_csv("data\\year_"+filename+".csv")

# %% Concat all dataframes into one

# in the previous step we write to file in case the script fails midway
# so now we read from the file and concat
df = []
for year in years:
    filename = year.replace("?","").replace("=","")
    df_year = pd.read_csv("data\\year_"+filename+".csv")[["title", "authors", "abstract", "link"]]
    df_year["year"] = int(year[0:4])
    df.append(df_year)

df = pd.concat(df)
df.head(1)
# %%
df.to_csv("data\\cvpr_web.csv", index=False)
# %%
