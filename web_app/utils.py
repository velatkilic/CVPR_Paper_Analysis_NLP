from nbformat import read
import pandas as pd

cvpr_data = pd.read_csv("data\cvpr_web.csv")

def predict(papers):
    papers = papers.split(";")
    papers = [p.strip() for p in papers]
    
    return "loyloy"