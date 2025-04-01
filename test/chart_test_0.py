import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import json

def convert_values(input):
    output = []
    for value in input:
        if value == 'SLOW':
            output.append(1)
        elif value == 'AVERAGE':
            output.append(2)
        elif value == 'FAST':
            output.append(3)
        else:
            output.append(0)
    return output

def extract_data(file, location):
    # Laden Sie das Dictionary aus der JSON-Datei
    with open(file, 'r') as f:
        data = json.load(f)
    out = []
    for value in data.values():
        try:
            out.append(value[location])
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            continue
    return out

def extract(locations):
    out = []
    for location in locations:
        extraced = []
        extraced = extract_data("output.json", location)
        if location in ["Overall Category", "FCP Score", "LCP Score", "CLS Score"]:
            extraced = convert_values(extraced)
        out.append(extraced)
    return out

def get_keys(file):
    # Laden Sie das Dictionary aus der JSON-Datei
    with open(file, 'r') as f:
        data = json.load(f)
    first = data["http://dropbox.com"]
    keys = list(first.keys())
    return keys

def create_graph(ax, ay, x_label, y_label):
    location = "/Users/HugoWienhold/Desktop/Graphen"
    label = f"{x_label}{y_label}"
    ax, ay = sorting(ax, ay) 
    # Erstellen Sie den Graphen
    plt.figure(figsize=(30, 6))  # Größe des Graphen
    plt.plot(ax, ay)  # Erstellen Sie einen Balkendiagramm
    plt.xticks(rotation=90)  # Drehen Sie die x-Achsenbeschriftungen um 90 Grad
    plt.xlabel(x_label)  # Beschriftung der x-Achse
    plt.ylabel(y_label)  # Beschriftung der y-Achse
    plt.savefig(f"{location}/Line/Categories/A Tags/{label}.png")  # Speichern Sie den Graphen als PNG-Datei
    plt.close()  # Schließen Sie den Graphen

def sorting(list_one, list_two):
    # Sortieren Sie die beiden Listen
    list_one, list_two = zip(*sorted(zip(list_one, list_two)))
    return list_one, list_two

def all_graphs_one_catagory(data, keys, category):
    for i in range(1, len(keys)):
        #tags auf der X-Achse und die Kategorie auf der Y-Achse
        # create_graph(data[category], data[i], keys[category], keys[i])

        #Kategorie auf der X-Achse und die Tags auf der Y-Achse
        create_graph(data[i], data[category], keys[i], keys[category])

def all_graphs_all_catagories(data, keys):
    for i in range(1, len(keys)):
        all_graphs_one_catagory(data, keys, i)

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
    with open('correlation_speed.json', 'a') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def correlate_all(dataframe, keys):
    for i in range(14, 15):
        for j in range(1, 14):
            if j != i:
                correlate_data(dataframe, keys[i], keys[j])

# 0 Website ID, 1 Overall Category, 2 FCP Time, 3 FCP Score, 4 LCP Time, 5 LCP Score, 6 TBT, 
# 7 CLS Time, 8 CLS Score, 9 Layout Shifts, 10 Speed Index, 11 Time to Interactive, 12 FMP Time, 
# 13 DOM Size, 14 A Tags, 15 P Tags, 16 Div Tags, 17 IMG Tags, 18 Button Tags
def __main__():
    keys = get_keys("output.json")
    data = extract(keys)
    # all_graphs(data, keys)
    dataframe = convert_to_dataframes(keys, data)
    correlate_all(dataframe, keys)

if __name__ == "__main__":
    __main__()