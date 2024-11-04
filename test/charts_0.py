import json
import numpy as np
import matplotlib.pyplot as plt
import traceback

save_location = "/Users/HugoWienhold/Desktop/Graphen"

unwanted = ["Overall Category", "First Contentful Paint Score", "Largest Contentful PaintCP Score", "Cumulative Layout Shift Score", "Website ID"]

def read_json(file): 
    with open(file, 'r') as f: 
        data = json.load(f)
    return data

#lädt alle keys aus dem subdict
def get_keys(file):
    # Laden Sie das Dictionary aus der JSON-Datei
    with open(file, 'r') as f:
        data = json.load(f)
    first = data["http://dropbox.com"]
    keys = list(first.keys())
    return keys

# gibt ein Dict mit Arrays zurück
def extract(file, keys):
    out = {}
    for key in keys:
        if key in unwanted:
            continue
        extraced = extract_data(file, key)
        out[key] = convert_to_numeric(extraced)  # Konvertieren Sie die Werte in numerische Werte
    return out

# gibt die Werte für EINEN key als Array zurück + ließt die Werte aus der JSON Datei ein
def extract_data(file, location):
    with open(file, 'r') as f:
        data = json.load(f)
    out = []
    for value in data.values():
        try:
            out.append(value[location])
        except KeyError as e:
            print(f"Ein Fehler ist aufgetreten: '{location}' mit Error '{e}'")
            traceback.print_exc()
            continue
    return out

# Konvertiert Werte in numerische Werte
def convert_to_numeric(values):
    numeric_values = []
    for value in values:
        try:
            numeric_values.append(int(value))
        except ValueError:
            print(f"Nicht-numerischer Wert gefunden und ignoriert: {value}")
            continue
    return numeric_values

# "übersetzt" die slow, average und fast werte in Zahlen
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

# sortiert die Werte anhand erster List und sortiert alle -100 aus
def sorting_clean(list_one, list_two):
    one = []
    two = []
    one , two = sorting(list_one, list_two)
    one, two = clean(one, two)
    return one, two

# sortiert die Werte anhand erster List (aufgerufen von sorting_clean)
def sorting(list_one, list_two):
    list_one, list_two = zip(*sorted(zip(list_one, list_two)))
    return list_one, list_two

# sortiert alle -100 aus (aufgerufen von sorting_clean)
def clean(list_one, list_two):
    # Liste von Tupeln erstellen
    list_of_tuples = list(zip(list_one, list_two))
    # Kriterium: Behalte nur Tupel, bei denen beide Elemente >= -100 sind
    filtered_list = [tup for tup in list_of_tuples if tup[0] != -100 and tup[0] != 0 and tup[1] != -100]
    # Listen wieder entpacken
    if filtered_list:  # Überprüfen, ob die gefilterte Liste nicht leer ist
        list_one, list_two = zip(*filtered_list)
    else:
        list_one, list_two = [], []

    return list_one, list_two

# prozentwert für Limits der Graphen berechnen
def prozentwert(gesamtwert, prozentsatz):
    return (gesamtwert * prozentsatz) / 100

#erstellt einen Graphen zwischen 2 Kategorien + lineare Regression
def create_graph(ax, ay, x_label, y_label, save_location):
    # Label für den Graphen erstellen
    label = f"{x_label}{y_label}"

    # Werte sortieren und -100 Werte entfernen
    ax, ay = sorting_clean(ax, ay)

    # min und max Werte für die Achsen berechnen
    min_width , max_width = min(ax) - prozentwert(max(ax),5), max(ax) + prozentwert(max(ax),5)
    min_height, max_height = min(ay) - prozentwert(max(ay),5), max(ay) + prozentwert(max(ay),5)

    

    # Graph erstellen
    plt.figure(figsize=(10, 6))

    #! Erstellen Sie einen Graphen mit einer linearen Regression
    # lineare Regression
    coef = np.polyfit(ax,ay,1)
    poly1d_fn = np.poly1d(coef)
    plt.plot(ax,ay, 'b.', ax, poly1d_fn(ax), '--r') 
    
    # #! Erstellen des Graphen mit Regression 2. Ordnung
    # # Berechnung der Koeffizienten des Polynoms 2. Grades
    # coefficients = np.polyfit(ax, ay, 2)
    # # Erstellen der Polynomfunktion
    # poly2d_fn = np.poly1d(coefficients)
    # plt.plot(ax, ay, 'b.', label='Originaldaten') 
    # plt.plot(ax, poly2d_fn(ax), '--r', label='Quadratische Regression')

    plt.xlim(min_width, max_width)
    plt.ylim(min_height, max_height)
    plt.xticks(rotation=90)  # Drehen Sie die x-Achsenbeschriftungen um 90 Grad
    plt.xlabel(x_label)  # Beschriftung der x-Achse
    plt.ylabel(y_label)  # Beschriftung der y-Achse
    plt.savefig(f"{save_location}/Circle with Regression/{x_label}/{label}.png") 
    plt.close()

def create_graphs_one_category(data, category, keys, save_location):
    ax = data[category]
    for key in keys:
        if key in unwanted:
            continue
        ay = data[key]
        create_graph(ax, ay, category, key, save_location)

# 'Website ID', 'Overall Category', 'First Contentful Paint Time', 'First Contentful Paint Score', 'Largest Contentful Paint Time',
# 'Largest Contentful PaintCP Score', 'Total Blocking Time', 'Cumulative Layout Shift Time', 'Cumulative Layout Shift Score', 
# 'Layout Shifts', 'Speed Index', 'Time to Interactive', 'DOM Size', 'Offscreen Images', 'Total Byte Weight', 'Baymard Score', 
# 'Anzahl a Tags', 'Anzahl p Tags', 'Anzahl div Tags', 'Anzahl IMG Tags', 'Anzahl Button Tags'
def main():
    file = "/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/out_corr.json"
    keys = get_keys(file)
    data = extract(file, keys)
    # for key , value in data.items():
    #     print(f"{key}: {value}\n\n")
    create_graphs_one_category(data, 'Baymard Score', keys, save_location)

if __name__ == "__main__":
    main()
