
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from baymard_selenium import clean_tag as clean_tag
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau

import matplotlib.pyplot as plt

def two():
    data = read_json('/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/merged_data_1.json')
    keys = data['http://dropbox.com'].keys()
    for key in keys:
        ordner_pfad = f'/Users/HugoWienhold/Desktop/Graphen/Circle with Regression Quadrat/{key}'
        os.makedirs(ordner_pfad, exist_ok=True)

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def four():
    all = read_json('/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/out_corr.json')
    baymard = read_json('/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/baymard_scores_3.json')

    for all_key in all.keys():
        for baymard_key in baymard.keys():
            if all_key.find(baymard_key) != -1:
                all[all_key].update(baymard[baymard_key])

    with open('/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/merged_data.json', 'w') as file:
        json.dump(all, file, ensure_ascii=False, indent=4)


def six():
    print("Start")
    start_time = time.time()
    op = webdriver.ChromeOptions()
    op.add_argument('--headless')
    driver = webdriver.Chrome(options=op)
    driver.get('https://baymard.com/ux-benchmark/')
    j = 0
    results = {}
    categories = ['Overall', 'Desktop', 'Homepage_Category','Homepage']
    parent_div = driver.find_elements(By.CLASS_NAME, "_d3Container_1u38f_9")
    for i in range(2):
        for child in parent_div[i].find_elements(By.XPATH, ".//*"):
            if child.get_attribute('data-site-review-id') is None: continue
            j += 1
            website = child.get_attribute('data-site-review-id')
            score = child.get_attribute('data-performance-score')
            if website not in results:
                results[website] = {}
            results[website][categories[i]] = float(score)

        print(f'Anzahl: {j}')
    driver.quit()
    end_time = time.time()
    print(f"Time: {int(end_time - start_time)}s")
    print(results)



def seven():
    driver = webdriver.Chrome()
    driver.delete_all_cookies()

    driver.get("https://baymard.com/ux-benchmark/case-studies/adidas")
    time.sleep(2)
    try:
        cookie_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyButtonAccept")))
        cookie_button.click()
        time.sleep(1)
    except Exception as e:
        print(e)

    try:
        wrapper = driver.find_elements(By.CLASS_NAME, "_wrapper_7m4vv_1")
        if len(wrapper) <= 4:
            wrapper[1].click()
        time.sleep(1)

    except Exception as e:
        print(e)
    
    try:
        new_wrapper = driver.find_elements(By.CLASS_NAME, "_wrapper_7m4vv_1")
        new_wrapper[2].click()
        time.sleep(1)

    except Exception as e:
        print(e)
    

    try:
        subtitles = driver.find_elements(By.CLASS_NAME, "_subTitle_hfdxh_23")
        try:
            print(f'Overall: {clean_tag(subtitles[0])}')
        except:
            print(f'Overall: -100')
        try:
            print(f'Desktop: {clean_tag(subtitles[1])}')
        except:
            print(f'Desktop: -100')
        try:
            print(f'Homepage Category: {clean_tag(subtitles[2])}')
        except:
            print(f'Homepage Category: -100')
        try:
            print(f'Homepage: {clean_tag(subtitles[3])}')
        except:
            print(f'Homepage: -100')
    
    except:
        print("No more subtitles")

    
    while True:
        continue

def extract_data(location):
    file = '/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/merged_data_1.json'
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

def eight():
    removed_size = 0.05
    removed_axis = 0 # 0 = x, 1 = y
    x_axis = 'DOM Size'
    y_axis = 'Time to Interactive'
    x = extract_data(x_axis)
    y = extract_data(y_axis)
    # zip die zwei arrays zusammen und entferne alle -100
    data = list(zip(x, y))
    for i in data:
        if -100 in i:
            data.remove(i)
    #entferne die oberen und unteren 10% der Daten
    data_ = sorted(data, key=lambda x: x[removed_axis])
    data_ = data_[int(len(data_) * removed_size):int(len(data_) * (1 - removed_size))]
    x, y = zip(*data_)
    corr_two_keys(x, y)
    create_graph(data, x_axis, y_axis, removed_size, removed_axis)
    
    


#erstellt einen Graphen zwischen 2 Kategorien + lineare Regression
def create_graph(data, x_label, y_label, removed_size, removed_axis):
    ax_data, ay_data = zip(*data)
    data = sorted(data, key=lambda x: x[removed_axis])
    upper = data[int(len(data) * (1 - removed_size)):]
    x_upper, y_upper = zip(*upper)
    lower = data[:int(len(data) * removed_size)]
    x_lower, y_lower = zip(*lower)
    data = data[int(len(data) * removed_size):int(len(data) * (1 - removed_size))]
    ax, ay = zip(*data)
    
    
    sorted_indices = np.argsort(ax)
    ax = np.array(ax)[sorted_indices]
    ay = np.array(ay)[sorted_indices]

    # min und max Werte für die Achsen berechnen
    min_width , max_width = min(ax_data) - prozentwert(max(ax_data),5), max(ax_data) + prozentwert(max(ax_data),5)
    min_height, max_height = min(ay_data) - prozentwert(max(ay),5), max(ay_data) + prozentwert(max(ay_data),5)

    # Graph erstellen
    plt.figure(figsize=(10, 10))

    #! Erstellen Sie einen Graphen mit einer linearen Regression
    # lineare Regression
    coef = np.polyfit(ax,ay,1)
    poly1d_fn = np.poly1d(coef)
    plt.plot(ax, poly1d_fn(ax), '--r', label='Lineare Regression') 
    plt.plot(ax,ay, 'b.')
    plt.plot(x_upper, y_upper, 'g.')
    plt.plot(x_lower, y_lower, 'g.')
    # #! Erstellen des Graphen mit Regression 2. Ordnung
    # # Berechnung der Koeffizienten des Polynoms 2. Grades
    # coefficients = np.polyfit(ax, ay, 2)
    # # Erstellen der Polynomfunktion
    # poly2d_fn = np.poly1d([])
    # poly2d_fn = np.poly1d(coefficients)
    # plt.plot(ax, ay, 'b.')
    # plt.plot(ax, poly2d_fn(ax), '--r', label='Quadratische Regression')

    plt.xlim(min_width, max_width)
    plt.ylim(min_height, max_height)
    plt.xticks(rotation=90)  # Drehen Sie die x-Achsenbeschriftungen um 90 Grad

    plt.xlabel(f'{x_label}')  # Beschriftung der x-Achse
    plt.ylabel(f'{y_label}')  # Beschriftung der y-Achse
    plt.legend(fontsize='large', loc = 'upper left')  # Legende hinzufügen
    plt.show()

def prozentwert(gesamtwert, prozentsatz):
    return (gesamtwert * prozentsatz) / 100

def corr_two_keys(list_one, list_two):
    pearson_coeff, pearson_p_value = pearsonr(list_one, list_two)
    spearman_coeff, spearman_p_value = spearmanr(list_one, list_two)
    kendall_coeff, kendall_p_value = kendalltau(list_one, list_two)
    print(f'Pearson: {pearson_coeff}, {pearson_p_value}')
    print(f'Spearman: {spearman_coeff}, {spearman_p_value}')
    print(f'Kendall: {kendall_coeff}, {kendall_p_value}')


# write a function that gives me the biggest number of the catagory Total Byte Weight
def nine():
    data = read_json('/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/merged_data_1.json')
    max = 0
    for value in data.values():
        if value['Total Byte Weight'] == -100:
            continue
        if value['Total Byte Weight'] > max:
            max = value['Total Byte Weight']
    # max is the value in Bytes. Convert it to MB
    max = max / 1000000
    print(f'Max: {max} MB')

# schreibe mir eine Funktion, die mir die durchschnittliche Korrelation zwischen allen Werten in der Datei ausgibt
# nehme dafür die werte aus der Datei /Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/corr_sort_pearson.json
def ten():
    data = read_json('/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/corr_sort_pearson.json')
    out = {}
    for x in data:
        #print the first key and value of the dictionary
        keys = list(x.keys())
        name = keys[0].split('Pearson Coefficient')[0]
        total_coef = x[keys[0]]+x[keys[2]]+x[keys[4]]
        total_p_value = x[keys[1]]+x[keys[3]]+x[keys[5]]
        avg_coef = total_coef / 3
        avg_p_value = total_p_value / 3
        #add name as key in dict out and avg_coef as value
        out[name] = [avg_coef, avg_p_value]
    #sortiere die einträge des Dict out nach avg_coef
    out = dict(sorted(out.items(), key=lambda item: item[1]))
    # save out in a json file
    with open('/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/avg_corr.json', 'w') as file:
        json.dump(out, file, ensure_ascii=False, indent=4)

def eleven():
    s = 'Homepage UX PerformanceLayout ShiftsPearson Coefficient'
    print(s.split('Pearson Coefficient')[0])

ten()