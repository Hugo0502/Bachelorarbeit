import pandas as pd
from scipy.stats import pearsonr, spearmanr
import json

def convert_to_dataframes(keys, data):
    daten = {keys[i]: data[i] for i in range(1, len(keys))}
    dataframe = pd.DataFrame(daten)
    return dataframe

def correlate_data(dataframe, key_one, key_two):
    pearson_coeff, pearson_p_value = pearsonr(dataframe[key_one], dataframe[key_two])
    spearman_coeff, spearman_p_value = spearmanr(dataframe[key_one], dataframe[key_two])

    corr = {
        f"{key_one}{key_two}Pearson Coefficient": pearson_coeff,
        f"{key_one}{key_two}Pearson P-Value": pearson_p_value,
        f"{key_one}{key_two}Spearman Coefficient": spearman_coeff,
        f"{key_one}{key_two}Spearman P-Value": spearman_p_value
        }
    correlation_in_json(corr)

def correlation_in_json(data):
    with open('correlation_out.json', 'a') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def correlate_all(dataframe, keys):
    for i in range(14, 15):
        for j in range(1, 14):
            if j != i:
                correlate_data(dataframe, keys[i], keys[j])

def get_keys(data):
    first = data["http://dropbox.com"]
    keys = list(first.keys())
    return keys

def read_json(file_json):
    with open(file_json, 'r') as f:
        data = json.load(f)
    return data

def main():
    file_json = "/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/out_corr.json"
    data = read_json(file_json)
    keys = get_keys(data)
    dataframe = convert_to_dataframes(keys, data)
    correlate_all(dataframe, keys)

if __name__ == "__main__":
    main()