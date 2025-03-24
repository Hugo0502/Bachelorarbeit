import multiprocessing
from PythonPSI.api import PSI
import time
import json
from tqdm import tqdm
import subprocess

out_json = 'out_new_TEST.json'

def json_read(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data

def json_to_list(url):
    url_list = []
    for key, value in url.items():
        _ = [key, value]
        url_list.append(_)
    return url_list

def json_write(results):
    
    with open(out_json, 'w') as f:
        json.dump(results, f, indent=4)
    
    return
    

def get_metrics(url):
    data = {}
    metrics = {url: {}}
    try:
        data =  PSI(url, api_key='AIzaSyBuX1dCHH9wbWuGXwo14LvadstFbtLz6cE')
    except Exception as e:
        print(f"PSI Fehler: {e} at {url}")

    try:
        metrics[url]['Website ID'] = data['id']
    except Exception as e:
        metrics[url]['Website ID'] = -100
        print(f"Error appending ID: {e} at {url}")

    try:
        metrics[url]['Overall Category'] = data['loadingExperience']['overall_category']
    except Exception as e:
        metrics[url]['Overall Category'] = -100
        print(f"Error appending overall category: {e} at {url}")

    try:
        metrics[url]['First Contentful Paint Time'] = data['lighthouseResult']['audits']['first-contentful-paint']['numericValue']
    except Exception as e:
        metrics[url]['First Contentful Paint Time'] = -100
        print(f"Error appending first contentful paint time: {e} at {url}")

    try:
        metrics[url]['First Contentful Paint Score'] = data['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['category']
    except Exception as e:
        metrics[url]['First Contentful Paint Score'] = -100
        print(f"Error appending first contentful paint score: {e} at {url}")

    try:
        metrics[url]['Largest Contentful Paint Time'] = data['lighthouseResult']['audits']['largest-contentful-paint']['numericValue']
    except Exception as e:
        metrics[url]['Largest Contentful Paint Time'] = -100
        print(f"Error appending largest contentful paint time: {e} at {url}")

    try:
        metrics[url]['Largest Contentful PaintCP Score'] = data['loadingExperience']['metrics']['LARGEST_CONTENTFUL_PAINT_MS']['category']
    except Exception as e:
        metrics[url]['Largest Contentful PaintCP Score'] = -100
        print(f"Error appending largest contentful paint score: {e} at {url}")

    try:
        metrics[url]['Total Blocking Time'] = data['lighthouseResult']['audits']['total-blocking-time']['numericValue']
    except Exception as e:
        metrics[url]['Total Blocking Time'] = -100
        print(f"Error appending total blocking time: {e} at {url}")

    try:
        metrics[url]['Cumulative Layout Shift Time'] = data['lighthouseResult']['audits']['cumulative-layout-shift']['numericValue']
    except Exception as e:
        metrics[url]['Cumulative Layout Shift Time'] = -100
        print(f"Error appending cumulative layout shift time: {e} at {url}")

    try:
        metrics[url]['Cumulative Layout Shift Score'] = data['loadingExperience']['metrics']['CUMULATIVE_LAYOUT_SHIFT_SCORE']['category']
    except Exception as e:
        metrics[url]['Cumulative Layout Shift Score'] = -100
        print(f"Error appending cumulative layout shift score: {e} at {url}")

    try:
        metrics[url]['Layout Shifts'] = data['lighthouseResult']['audits']['layout-shifts']['displayValue']
    except Exception as e:
        metrics[url]['Layout Shifts'] = -100
        print(f"Error appending layout shifts: {e} at {url}")

    try:
        metrics[url]['Speed Index'] = data['lighthouseResult']['audits']['speed-index']['numericValue']
    except Exception as e:
        metrics[url]['Speed Index'] = -100
        print(f"Error appending speed index: {e} at {url}")

    try:
        metrics[url]['Time to Interactive'] = data['lighthouseResult']['audits']['interactive']['numericValue']
    except Exception as e:
        metrics[url]['Time to Interactive'] = -100
        print(f"Error appending time to interactive: {e} at {url}")

    try:
        metrics[url]['DOM Size'] = data['lighthouseResult']['audits']['dom-size']['displayValue']
    except Exception as e:
        metrics[url]['DOM Size'] = -100
        print(f"Error appending DOM size: {e} at {url}")

    try:
        metrics[url]['Offscreen Images'] = data['lighthouseResult']['audits']['offscreen-images']['numericValue']
    except Exception as e:
        metrics[url]['Offscreen Images'] = -100
        print(f"Error appending offscreen images: {e} at {url}")

    try:
        metrics[url]['Total Blocking Time'] = data['lighthouseResult']['audits']['total-blocking-time']['numericValue']
    except Exception as e:
        metrics[url]['Total Blocking Time'] = -100
        print(f"Error appending total blocking time: {e} at {url}")

    try:
        metrics[url]['Total Byte Weight'] = data['lighthouseResult']['audits']['total-byte-weight']['numericValue']
    except Exception as e:
        metrics[url]['Total Byte Weight'] = -100
        print(f"Error appending total byte weight: {e} at {url}")

    print(f'process ended {url}')
    return metrics


def parallel_get_metrics(urls):
    with multiprocessing.Pool(processes=8) as pool:
        results = pool.map(get_metrics, urls)
    all_data = {}
    for result in results:
        all_data.update(result)
    return all_data

def main():
    print("Starte PSI und Selenium")
    psi_start_time = time.time()
    #get URLs
    baymard = json_read('/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/baymard_scores_3.json')
    url_list = list(baymard.keys())

    # url_list = ['ae.com','aninebing.com']

    # getting metrics for all urls --> multiprocessing
    results = parallel_get_metrics(url_list)
    json_write(results)
    psi_end_time = time.time()
    psi_runtime = psi_end_time - psi_start_time
    print(f"Laufzeit PSI: {round(psi_runtime, 3)} Sekunden")

    # selenium_start_time = time.time()
    # # starte hier das Programm selenium_0.py
    # subprocess.run(["python3", "/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/selenuim_0.py"])
    

    # selenium_end_time = time.time()
    # selenium_runtime = selenium_end_time - selenium_start_time
    # print(f"Laufzeit Selenium: {round(selenium_runtime, 3)} Sekunden")
    # print(f"Laufzeit gesamt: {round(psi_runtime + selenium_runtime, 3)} Sekunden")

if __name__ == "__main__":
    main()