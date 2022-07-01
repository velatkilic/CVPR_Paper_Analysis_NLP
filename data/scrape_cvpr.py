# %%
"""
Scrape CVPR paper information (abstract, author names, abstract)
"""

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
# %%
years = ["2021?day=all",
         "2022?day=all"
         ]

for year in years:
    # get list of paper urls for a given year
    page = requests.get("https://openaccess.thecvf.com/CVPR"+year)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # get all the paper list
    urls = []
    for dt in soup.find_all("dl"):
        for title in dt.find_all("dt", {"class":"ptitle"}):
            for href in title.find_all("a", href=True):
                urls.append(href["href"])
    
    print("Number of papers found: " + str(len(urls)))
    
    # visit each url to parse title, author names and the abstract
    titles    = []
    authors   = []
    abstracts = []
    pdf_links = []
    
    t = 2 # initial time to sleep 
    
    for url in urls:
        time.sleep(t)
        t1 = time.time()
        page = requests.get("https://openaccess.thecvf.com/"+url)
        soup = BeautifulSoup(page.content, "html.parser")
        
        for div in soup.find_all("div", id="papertitle"):
            title = div.get_text().strip()
            print(title)
            titles.append(title)
        
        for div in soup.find_all("div", id="authors"):
            authors.append(div.get_text().strip().split(";")[0])
        
        for div in soup.find_all("div", id="abstract"):
            abstracts.append(div.get_text().strip())
        
        for dd in soup.find_all("dd"):
            for href in dd.find_all("a", href=True):
                link = href["href"]
                if link.split(".")[-1] == 'pdf' and link.split("/")[3] == "papers":
                    pdf_links.append(link)
        t2 = time.time()
        t = 10*(t2-t1)
        print("Wait time: " + str(t))
        if (t > 20): break
    
    df = pd.DataFrame(
            {"title":titles, "authors":authors, "abstract":abstracts, "link":pdf_links}
        )
    
    df.to_csv("data\\year_"+year[0:4]+str(np.random.rand())+".csv")
    


# years = ["2018?day=2018-06-19",
#           "2018?day=2018-06-20",
#           "2018?day=2018-06-21",
#           "2019?day=2019-06-18",
#           "2019?day=2019-06-19",
#           "2019?day=2019-06-20",
#           "2020?day=2020-06-16",
#           "2020?day=2020-06-17",
#           "2020?day=2020-06-18"
#          ]

# for year in years:
#     # get list of paper urls for a given year
#     page = requests.get("https://openaccess.thecvf.com/CVPR"+year)
#     soup = BeautifulSoup(page.content, "html.parser")
    
#     # get all the paper list
#     urls = []
#     for dt in soup.find_all("dl"):
#         for title in dt.find_all("dt", {"class":"ptitle"}):
#             for href in title.find_all("a", href=True):
#                 urls.append(href["href"])
    
#     print("Number of papers found: " + str(len(urls)))
    
#     # visit each url to parse title, author names and the abstract
#     titles    = []
#     authors   = []
#     abstracts = []
#     pdf_links = []
    
#     t = 2 # initial time to sleep 
    
#     for url in urls:
#         time.sleep(t+1)
#         t1 = time.time()
#         page = requests.get("https://openaccess.thecvf.com/"+url)
#         soup = BeautifulSoup(page.content, "html.parser")
        
#         for dd in soup.find_all("dd"):
#             for div in dd.find_all("div", id="papertitle"):
#                 title = div.get_text().strip()
#                 titles.append(title)
#                 print(title)
#             for div in dd.find_all("div", id="authors"):
#                 authors.append(div.get_text().strip().split(";")[0])
#             for div in dd.find_all("div", id="abstract"):
#                 abstracts.append(div.get_text().strip())
#             for href in dd.find_all("a", href=True):
#                 link = href["href"]
#                 if link.split(".")[-1] == 'pdf' and link.split("/")[3] == "papers":
#                     pdf_links.append(link)
#         t2 = time.time()
#         t = 10*(t2-t1)
#         print("Wait time: " + str(t))
#         if (t > 20): break
    
#     df = pd.DataFrame(
#             {"title":titles, "authors":authors, "abstract":abstracts, "link":pdf_links}
#         )
    
#     df.to_csv("data\\year_"+year[0:4]+str(np.random.rand())+".csv")