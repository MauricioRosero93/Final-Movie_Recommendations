import pandas as pd
from scipy import stats

def detect_drift(old_data, new_data, column='rating', threshold=0.05):
    ks_stat, p_value = stats.ks_2samp(old_data[column], new_data[column])
    return p_value < threshold