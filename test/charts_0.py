import json
import time
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
            numeric_values.append(float(value))
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
    # one , two = sorting(list_one, list_two) # --> Werte müssen nicht sortiert werden (wie dumm von mir)
    one, two = clean(list_one, list_two)
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
    filtered_list = [tup for tup in list_of_tuples if tup[0] != -100 and tup[1] != -100]
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
    file_name = f"{x_label}_{y_label}"

    # Werte sortieren und -100 Werte entfernen
    ax, ay = sorting_clean(ax, ay)

    sorted_indices = np.argsort(ax)
    ax = np.array(ax)[sorted_indices]
    ay = np.array(ay)[sorted_indices]

    # min und max Werte für die Achsen berechnen
    min_width , max_width = min(ax) - prozentwert(max(ax),5), max(ax) + prozentwert(max(ax),5)
    min_height, max_height = min(ay) - prozentwert(max(ay),5), max(ay) + prozentwert(max(ay),5)

    

    # Graph erstellen
    plt.figure(figsize=(10, 10))

    #! Erstellen Sie einen Graphen mit einer linearen Regression
    # lineare Regression
    # coef = np.polyfit(ax,ay,1)
    # poly1d_fn = np.poly1d(coef)
    # plt.plot(ax,ay, 'b.')
    # plt.plot(ax, poly1d_fn(ax), '--r', label='Lineare Regression') 
    
    # #! Erstellen des Graphen mit Regression 2. Ordnung
    # Berechnung der Koeffizienten des Polynoms 2. Grades
    coefficients = np.polyfit(ax, ay, 2)
    # Erstellen der Polynomfunktion
    poly2d_fn = np.poly1d([])
    poly2d_fn = np.poly1d(coefficients)
    plt.plot(ax, ay, 'b.')
    plt.plot(ax, poly2d_fn(ax), '--r', label='Quadratische Regression')

    plt.xlim(min_width, max_width)
    plt.ylim(min_height, max_height)
    plt.xticks(rotation=90)  # Drehen Sie die x-Achsenbeschriftungen um 90 Grad
    unit_x = get_unit(x_label)
    unit_y = get_unit(y_label)
    plt.xlabel(f'{x_label} {unit_x}')  # Beschriftung der x-Achse
    plt.ylabel(f'{y_label} {unit_y}')  # Beschriftung der y-Achse
    plt.legend(fontsize='large', loc = 'upper left')  # Legende hinzufügen
    plt.savefig(f"{save_location}/Circle with Regression Quadrat/{x_label}/{file_name}.png") 
    # plt.show()
    plt.close()

def get_unit(key):
    switcher = {
        'Overall Category': '',
        'First Contentful Paint Time': 'in ms',
        'First Contentful Paint Score': '',
        'Largest Contentful Paint Time': 'in ms',
        'Largest Contentful PaintCP Score': '',
        'Total Blocking Time': 'in ms',
        'Cumulative Layout Shift Time': 'in ms',
        'Cumulative Layout Shift Score': '',
        'Layout Shifts': '',
        'Speed Index': 'in ms',
        'Time to Interactive': 'in ms',
        'DOM Size': '',
        'Offscreen Images': '',
        'Total Byte Weight': 'in Bytes',
        'Baymard Score': 'in Punkten',
        'Anzahl a Tags': '',
        'Anzahl p Tags': '',
        'Anzahl div Tags': '',
        'Anzahl IMG Tags': '',
        'Anzahl Button Tags': '',
        'Overall UX Performance': 'in Punkten',
        'Desktop UX Performance': 'in Punkten',
        'Homepage & Navigation UX Performance': 'in Punkten',
        'Homepage UX Performance': 'in Punkten',

    }
    return switcher.get(key, "Invalid Key")


    

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
    file = "/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/merged_data_1.json"
    keys = get_keys(file)
    data = extract(file, keys)
    # for key , value in data.items():
    #     print(f"{key}: {value}\n\n")

    for key in keys:
        if key in unwanted:
            continue
        try:
            create_graphs_one_category(data, key, keys, save_location)
            # time.sleep(10)
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            continue
    # create_graphs_one_category(data, 'Cumulative Layout Shift Time', keys, save_location)

if __name__ == "__main__":
    main()
