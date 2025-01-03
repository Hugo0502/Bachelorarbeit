
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from baymard_selenium import clean_tag as clean_tag
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

four()
