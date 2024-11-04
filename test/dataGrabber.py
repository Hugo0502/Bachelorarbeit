import asyncio
import concurrent.futures
from PythonPSI.api import PSI
import time
import json
from tqdm import tqdm
import subprocess
import traceback

out_json = 'out.json'

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
    out = {} 
    
    i = 0
    # results = [URL, ID, Overall Category, FCP Time, FCP Score, LCP Time, LCP Score, TBT,
    #           CLS Time, CLS Score, Layout Shifts, Speed Index, Time to Interactive, FMP Time, DOM Size Baymard Score]
    for result in results:
        sub_dict = {}
        if result == None:
            i=+1
            print(f"json_write Fehler: None")
            continue
        try:
            sub_dict = {
                'Website ID': result[1],                            # URL
                'Overall Category': result[2],                      # Overall Category in words
                'First Contentful Paint Time': result[3],           # in ms
                'First Contentful Paint Score': result[4],          # in words
                'Largest Contentful Paint Time': result[5],         # in ms 
                'Largest Contentful PaintCP Score': result[6],      # in words
                'Total Blocking Time': result[7],                   # in ms
                'Cumulative Layout Shift Time': result[8],          # in ms
                'Cumulative Layout Shift Score': result[9],         # in words
                'Layout Shifts': result[10],                        # number of
                'Speed Index': result[11],                          # in ms 
                'Time to Interactive': result[12],                  # in ms
                'DOM Size': result[13],                             # number of
                'Offscreen Images': result[14],                     # number of
                'Total Blocking Time': result[15],                  # in ms
                'Total Byte Weight': result[16],                    # in bytes
                'Baymard Score': result[17]                         # Baymard Score
            }
            out[result[0]] = sub_dict 
        except Exception as e:
            print(f"json_write Fehler: {e}")
            continue
    # with open('output_psi.json', 'w') as f:
    #     json.dump(out, f, indent=4)
    
    with open(out_json, 'w') as f:
        json.dump(out, f, indent=4)
    
    print(f"Anzahl der NONE Fehler: {i}")
    return
    

async def get_metrics(url):
    for i in range(2):
        
            # print(f'process started {url[0]}')
            # metrics = 
        data = {}
        metrics = []
        try:
            data =  PSI(url[0], api_key='AIzaSyBuX1dCHH9wbWuGXwo14LvadstFbtLz6cE')
        except Exception as e:
            print(f"PSI Fehler: {e} at {url[0]}")
        try:
            metrics.append(url[0])
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending URL: {e} at {url[0]}")

        try:
            metrics.append(data['id'])
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending ID: {e} at {url[0]}")

        try:
            metrics.append(data['loadingExperience']['overall_category']) # words
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending overall category: {e} at {url[0]}")

        try:
            metrics.append(data['lighthouseResult']['audits']['first-contentful-paint']['numericValue']) # in ms
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending first contentful paint time: {e} at {url[0]}")

        try:
            metrics.append(data['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['category']) # words
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending first contentful paint score: {e} at {url[0]}")

        try:
            metrics.append(data['lighthouseResult']['audits']['largest-contentful-paint']['numericValue']) # in ms
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending largest contentful paint time: {e} at {url[0]}")

        try:
            metrics.append(data['loadingExperience']['metrics']['LARGEST_CONTENTFUL_PAINT_MS']['category']) # words
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending largest contentful paint score: {e} at {url[0]}")

        try:
            metrics.append(data['lighthouseResult']['audits']['total-blocking-time']['numericValue']) # in ms
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending total blocking time: {e} at {url[0]}")

        try:
            metrics.append(data['lighthouseResult']['audits']['cumulative-layout-shift']['numericValue']) # number of
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending cumulative layout shift time: {e} at {url[0]}")

        try:
            metrics.append(data['loadingExperience']['metrics']['CUMULATIVE_LAYOUT_SHIFT_SCORE']['category']) # words
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending cumulative layout shift score: {e} at {url[0]}")

        try:
            metrics.append(data['lighthouseResult']['audits']['layout-shifts']['displayValue']) # number of
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending layout shifts: {e} at {url[0]}")

        try:
            metrics.append(data['lighthouseResult']['audits']['speed-index']['numericValue']) # in ms
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending speed index: {e} at {url[0]}")

        try:
            metrics.append(data['lighthouseResult']['audits']['interactive']['numericValue']) # in ms
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending time to interactive: {e} at {url[0]}")

        try:
            metrics.append(data['lighthouseResult']['audits']['dom-size']['displayValue']) # number of
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending DOM size: {e} at {url[0]}")

        try:
            metrics.append(data['lighthouseResult']['audits']['offscreen-images']['numericValue']) # number of
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending offscreen images: {e} at {url[0]}")

        try:
            metrics.append(data['lighthouseResult']['audits']['total-blocking-time']['numericValue']) # in ms
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending total blocking time: {e} at {url[0]}")

        try:
            metrics.append(data['lighthouseResult']['audits']['total-byte-weight']['numericValue']) # in bytes
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending total byte weight: {e} at {url[0]}")

        try:
            metrics.append(url[1]) # Baymard Score
        except Exception as e:
            metrics.append(-100)
            print(f"Error appending Baymard Score: {e} at {url[0]}")
        print(f'process ended {url[0]}')
        return metrics

def run(url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(get_metrics(url))
    finally:
        loop.close()

def main():
    print("Starte PSI und Selenium")
    psi_start_time = time.time()
    url = json_read('/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/url.json')
    url_list = json_to_list(url)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(run, url_list), total=len(url_list)))
        # for result in results:
        #     print(result)
    json_write(results)
    psi_end_time = time.time()
    psi_runtime = psi_end_time - psi_start_time
    print(f"Laufzeit PSI: {round(psi_runtime, 3)} Sekunden")

    selenium_start_time = time.time()
    # starte hier das Programm selenium_0.py
    subprocess.run(["python3", "/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/selenuim_0.py"])
    

    selenium_end_time = time.time()
    selenium_runtime = selenium_end_time - selenium_start_time
    print(f"Laufzeit Selenium: {round(selenium_runtime, 3)} Sekunden")
    print(f"Laufzeit gesamt: {round(psi_runtime + selenium_runtime, 3)} Sekunden")

if __name__ == "__main__":
    main()