import pickle
from matplotlib.pyplot import axis
import pandas as pd
import numpy as np
from textfill import TextFill

def get_topic_names(n=3):
    topic_names = []
    for topic_idx, topic in enumerate(nmf.components_):
        top_features_ind = topic.argsort()[: -n - 1 : -1]
        top_features = [tfidf_feature_names[i] for i in top_features_ind]
        topic_names.append(top_features)
    return topic_names

def get_topic_names_abstract(n=3):
    topic_names = []
    for _, topic in enumerate(nmf_abstract.components_):
        top_features_ind = topic.argsort()[: -n - 1 : -1]
        top_features = [tfidf_feature_names_abstract[i] for i in top_features_ind]
        topic_names.append(top_features)
    return topic_names

def find_closest_match(topic_embed, n=5):
    # find the closest match
    dist = (topic_vector - topic_embed)**2
    dist = dist.mean(axis=1)
    print(dist.shape)

    # find the best match
    inds = dist.argsort()[0:n]
    print(inds.shape)

    return df.iloc[inds, :]

def find_closest_match_abstract(topic_embed, n=5):
    # find the closest match
    dist = (topic_vector_abstract - topic_embed)**2
    dist = dist.mean(axis=1)
    print(dist.shape)

    # find the best match
    inds = dist.argsort()[0:n]
    print(inds.shape)

    return df.iloc[inds, :]

def get_relevant_papers(input_text, n=5):

    # tfidf vectorizer
    input_tfidf = tfidf_vectorizer.transform([input_text])

    # check at least one word is in the vocab
    if input_tfidf.count_nonzero() == 0:
        return None

    # get topic embedding
    topic_embed = nmf.transform(input_tfidf)
    
    # closest match
    out = find_closest_match(topic_embed, n)

    return out #out["title"].to_json()

def get_relevant_papers_abstract(input_text, n=5):

    # tfidf vectorizer
    input_tfidf = tfidf_vectorizer_abstract.transform([input_text])

    # check at least one word is in the vocab
    if input_tfidf.count_nonzero() == 0:
        return None

    # get topic embedding
    topic_embed = nmf_abstract.transform(input_tfidf)
    
    # closest match
    out = find_closest_match_abstract(topic_embed, n)

    return out

def get_top_by_count(n=5):
    global top_topic_inds
    topic_names = get_topic_names(n=5)
    out = []
    for i in range(n):
        ind = top_topic_inds[i]
        out.append(topic_names[ind])
    return out

def get_top_by_citation(n=5):
    global top_topic_citation_inds
    topic_names = get_topic_names(n=5)
    out = []
    for i in range(n):
        ind = top_topic_citation_inds[i]
        out.append(topic_names[ind])
    return out

def get_top_rising(n=5):
    global top_rising_inds
    topic_names = get_topic_names(n=5)
    out = []
    for i in range(n):
        ind = top_rising_inds[i]
        out.append(topic_names[ind])
    return out

# https://discuss.streamlit.io/t/display-urls-in-dataframe-column-as-a-clickable-hyperlink/743/8
def make_clickable(url, text):
    url = "https://openaccess.thecvf.com/" + url
    return f'<a target="_blank" href="{url}">{text}</a>'


def get_word_suggestions(abs_input, top_k):
    abs_input = abs_input.replace("#", "[MASK]")
    return tf.fill_mask(abs_input, top_k=top_k)

def init_model(model_dir = "..\\model", lm_dir="distilbert-base-uncased-finetuned-cvpr"):
    
    global nmf, nmf_abstract, tfidf_vectorizer, tfidf_vectorizer_abstract, df, tfidf_feature_names, tfidf_feature_names_abstract, topic_vector, topic_vector_abstract
    with open(model_dir + "\\nmf.pickle", "rb") as f:
        nmf = pickle.load(f)
    
    with open(model_dir + "\\nmf_abstract.pickle", "rb") as f:
        nmf_abstract = pickle.load(f)
    
    with open(model_dir + "\\tfidf_vectorizer.pickle", "rb") as f:
        tfidf_vectorizer = pickle.load(f)
    
    with open(model_dir + "\\tfidf_vectorizer_abstract.pickle", "rb") as f:
        tfidf_vectorizer_abstract = pickle.load(f)
    
    with open(model_dir + "\\topic_vector.pickle", "rb") as f:
        topic_vector = pickle.load(f)
    
    with open(model_dir + "\\topic_vector_abstract.pickle", "rb") as f:
        topic_vector_abstract = pickle.load(f)
    
    df = pd.read_csv(model_dir + "\\cvpr_data_with_topics.csv")

    tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
    tfidf_feature_names_abstract = tfidf_vectorizer_abstract.get_feature_names_out()

    df["topic_class"] = topic_vector.argmax(axis=1)

    global topic_stats
    topic_stats = []
    years = df["year"].unique()
    for year in years:
        topic_stats.append(df[df["year"] == year].groupby("topic_class")["citation_count"].describe())

    n_components = nmf.get_params()["n_components"]
    global counts
    counts = np.zeros((n_components, len(years)))
    for i in range(len(years)):
        inds = topic_stats[i].index.values
        counts[inds,i] = topic_stats[i]["count"].to_numpy()
    

    paper_count = counts.sum(axis=1)
    global top_topic_inds
    top_topic_inds = paper_count.argsort()[::-1]

    global top_rising_inds
    top_rising_inds = counts[:,-1].argsort()[::-1]

    global citation_counts
    citation_counts = np.zeros((n_components, len(years)))
    for i in range(len(years)):
        inds = topic_stats[i].index.values
        citation_counts[inds,i] = topic_stats[i]["count"].to_numpy() * topic_stats[i]["mean"].to_numpy()
    
    paper_citation_count = citation_counts.sum(axis=1)
    global top_topic_citation_inds
    top_topic_citation_inds = paper_citation_count.argsort()[::-1]

    global tf
    tf = TextFill(model_checkpoint=lm_dir)