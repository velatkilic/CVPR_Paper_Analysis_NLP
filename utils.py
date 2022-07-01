import datetime
from ast import literal_eval
import numpy as np

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