import json
from scipy.stats import pearsonr, spearmanr, kendalltau
file_path = '/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/out_corr.json'
unwanted = ["Overall Category", "First Contentful Paint Score", "Largest Contentful PaintCP Score", "Cumulative Layout Shift Score", "Website ID"]

def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Die Datei {file_path} wurde nicht gefunden.")
    except json.JSONDecodeError:
        print(f"Fehler beim Dekodieren der JSON-Datei {file_path}.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

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

def get_keys(file):
    # Laden Sie das Dictionary aus der JSON-Datei
    with open(file, 'r') as f:
        data = json.load(f)
    first = data["http://dropbox.com"]
    temp = list(first.keys())
    
    #unwanted aussortieren
    keys = []
    for key in temp:
        if key not in unwanted:
            keys.append(key)
        else: continue
    return keys

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

def correlate(data, keys):
    for i in range(0, 16):
        for j in range(0,16):
            if j != i:
                corr(data, keys[i], keys[j])



def corr(data, key_one, key_two):
    list_one = []
    list_two = []
    one = data[key_one]
    two = data[key_two]
    list_one, list_two = clean(one, two) 
    
    pearson_coeff, pearson_p_value, spearman_coeff, spearman_p_value, kendall_coeff, kendall_p_value = corr_two_keys(list_one, list_two)
    
    corr = {
        f"{key_one}{key_two}Pearson Coefficient": pearson_coeff,
        f"{key_one}{key_two}Pearson P-Value": pearson_p_value,
        f"{key_one}{key_two}Spearman Coefficient": spearman_coeff,
        f"{key_one}{key_two}Spearman P-Value": spearman_p_value,
        f"{key_one}{key_two}Kendall Coefficient": kendall_coeff,
        f"{key_one}{key_two}Kendall P-Value": kendall_p_value
        }
    correlation_in_json(corr)
    

def corr_two_keys(list_one, list_two):
    pearson_coeff, pearson_p_value = pearsonr(list_one, list_two)
    spearman_coeff, spearman_p_value = spearmanr(list_one, list_two)
    kendall_coeff, kendall_p_value = kendalltau(list_one, list_two)
    return pearson_coeff, pearson_p_value, spearman_coeff, spearman_p_value, kendall_coeff, kendall_p_value

def correlation_in_json(data):
    with open('/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/correlation_out.json', 'a') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    keys = get_keys(file_path)
    data = extract(file_path, keys)
    correlate(data, keys)

if __name__ == "__main__":
    main()

