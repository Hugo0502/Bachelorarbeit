import json
import time

import requests
from selenium import webdriver


def read_json_extract_sites():
    sites = []
    with open('out_50mbit.json') as f:
        data = json.load(f)
    for key, value in data.items():
        sites.append(key)
    return sites

def speed_test(sites):
    for url in sites:
        speed_test_url(url)

def speed_test_url(url):
    driver = webdriver.Chrome()
    start_time = time.time()
    driver.get(url)
    end_time = time.time()
    load_time = end_time - start_time


def main():
    sites = read_json_extract_sites()
    print(sites)

if __name__ == '__main__':
    main()