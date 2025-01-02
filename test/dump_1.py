
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

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
    baymard = read_json('/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/baymard_scores_2.json')

    for all_key in all.keys():
        for baymard_key in baymard.keys():
            if all_key.find(baymard_key) != -1:
                all[all_key].update(baymard[baymard_key])

    with open('/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/merged_data_1.json', 'w') as file:
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

two()

