import datetime
from ast import literal_eval
import numpy as np
import matplotlib.pyplot as plt

# convert citation date to datetime object
def convert_to_datetime(date_array):
    date_array = literal_eval(date_array)
    out = []
    for d in date_array:
        if d is not None:
            out.append(datetime.date(d[0], d[1], d[2]))
        else:
            out.append(None)
    return out

# sort dates and impute missing values randomly
def impute_and_sort_citation(datetime_array):
    N = len(datetime_array)
    # data imputation for missing dates
    for i in range(N):
        if datetime_array[i] == None:
            # pick a random date from the list
            random_date = None
            while random_date is None:
                random_date = datetime_array[np.random.randint(0, N-1)]
            datetime_array[i] = random_date + datetime.timedelta(days=np.random.randint(50, 100))
    
    # sort
    return sorted(datetime_array)

# plot top words from topic analysis
# modified from: https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-plot-topics-extraction-with-nmf-lda-py
def plot_top_words(model, feature_names, n_top_words, title, figsize=(30, 15)):
    length = model.get_params()["n_components"]
    nrow = length // 5
    if length % 5 != 0: nrow += 1

    fig, axes = plt.subplots(nrow, 5, figsize=figsize, sharex=True, facecolor='w', constrained_layout=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[: -n_top_words - 1 : -1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]

        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f"Topic {topic_idx}", fontdict={"fontsize": 30})
        ax.invert_yaxis()
        ax.tick_params(axis="both", which="major", labelsize=20)
        for i in "top right left".split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=40)

    #plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
    plt.show()
    plt.draw()
    return fig