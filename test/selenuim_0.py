import time 
import multiprocessing as mp 
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

out_json = 'out.json'

def scrape_page(url): 
    try:
        result = []
        driver = webdriver.Chrome()
        driver.get(url)
        # Warten Sie, bis der gesamte Body geladen ist
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(5)
        a_tags = driver.find_elements(By.TAG_NAME, "a")
        p_tags = driver.find_elements(By.TAG_NAME, "p")
        div_tags = driver.find_elements(By.TAG_NAME, "div")
        img_tags = driver.find_elements(By.TAG_NAME, "img")
        btn_tags = driver.find_elements(By.TAG_NAME, "button")

        result = [url, len(a_tags), len(p_tags), len(div_tags), len(img_tags), len(btn_tags)]
        return result
    except Exception as e:
        result = [url, -100, -100, -100, -100, -100]
        print(f"Error in scraping {url}: {e}") 

def scrape_pages_mp(urls): 
	with mp.Pool(4) as p: 
		results = p.map(scrape_page, urls) 
	return results 

def read_json(file): 
    with open(file, 'r') as f: 
        data = json.load(f)
    return data
def json_to_list(url): 
    url_list = [] 
    for key, value in url.items(): 
        url_list.append(str(key)) 
    return url_list

def write_json(results): 
    # results = [URL, Anzahl a Tags, Anzahl p Tags, Anzahl div Tags, Anzahl img Tags, Anzahl button Tags]
    data = read_json(out_json)
    for result in results:
        try:
            data[result[0]]['Anzahl a Tags'] = result[1]
            data[result[0]]['Anzahl p Tags'] = result[2]
            data[result[0]]['Anzahl div Tags'] = result[3] 
            data[result[0]]['Anzahl IMG Tags'] = result[4]
            data[result[0]]['Anzahl Button Tags'] = result[5]
        except Exception as e:
            print(f"Error in writing: {e}")
            continue
    with open(out_json, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__": 
    # Test the multithreaded scraper 
    data = read_json('/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/url.json')
    urls = json_to_list(data)	
    # Test the multiprocessed scraper 
    start = time.time() 
    data = scrape_pages_mp(urls)
    write_json(data)
    # print(data) 
    end = time.time() 
    print(f"Time taken for multiprocessed scraper: {(int(end - start))/60} minutes") 



# def get_average_font_size(url):
#     try: 
#         driver = webdriver.Chrome()
#         driver.get(url)
         
#         # Warten Sie, bis die Seite vollständig geladen ist
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
         
#         # Finden Sie alle Text-Elemente
#         text_elements = driver.find_elements(By.XPATH, "//p | //div | //span | //a | //h1 | //h2 | //h3 | //h4 | //h5 | //h6")
        
#         font_sizes = []
        
#         for element in text_elements:
#             font_size = element.value_of_css_property("font-size")
#             if font_size:
#                 # Entfernen Sie "px" und konvertieren Sie in float
#                 font_size = float(font_size.replace("px", ""))
#                 font_sizes.append(font_size)
        
#         driver.quit()
        
#         if font_sizes:
#             average_font_size = sum(font_sizes) / len(font_sizes)
#             return average_font_size
#         else:
#             return 0
#     except Exception as e:
#         print(f"Error in getting average font size for {url}: {e}")
#         return 0