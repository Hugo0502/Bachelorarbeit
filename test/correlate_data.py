import json
import pandas as pd
from scipy.stats import pearsonr, spearmanr

# Laden der Daten aus der JSON-Datei
with open('out_corr.json', 'r') as file:
    data = json.load(file)

# Umwandeln der Daten in ein DataFrame
df = pd.DataFrame(data)

# Berechnung der Pearson-Korrelation
pearson_corr = df.corr(method='pearson')

# Berechnung der Spearman-Korrelation
spearman_corr = df.corr(method='spearman')

# Ausgabe der Ergebnisse
print("Pearson-Korrelation:")
print(pearson_corr)
print("\nSpearman-Korrelation:")
print(spearman_corr)
