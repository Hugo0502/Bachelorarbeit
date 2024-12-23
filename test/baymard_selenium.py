from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Funktion zur Extraktion der Daten
def scrape_abcam_data(url):
    # Selenium-Webdriver-Setup
    driver = webdriver.Chrome()

    try:
        driver.get(url)

        # Element 1: Website Name
        website_name = driver.find_element(By.CLASS_NAME, "truncate").text

        # Daten-Dictionary vorbereiten
        data = {website_name: {}}

        # Finden aller relevanten Elemente mit den Klassen _title_hfdxh_10 und _subTitle_hfdxh_23
        titles = driver.find_elements(By.CLASS_NAME, "_title_hfdxh_10")
        subtitles = driver.find_elements(By.CLASS_NAME, "_subTitle_hfdxh_23")


        # Prüfung, ob "Overall UX Performance" existiert
        #! overall_found gibt an ob die Kategorie Overall UX Performance existiert -> dies beeinflusst wo welche Daten in der Liste titles/subtitles stehen -> daher muss eine Verschiebung von 1 eingebaut werden je nachdem ob Overall UX Performance existiert oder nicht
        overall_found = 0 
        
        if "Overall UX Performance" in titles[0].text:
            overall_found = 1
            performance_value = float(subtitles[0].text.split("Performance:")[1].strip())
            data[website_name]["Overall UX Performance"] = performance_value
        else:
            data[website_name]["Overall UX Performance"] = -100

        #! hier die anderen 3 Kategorien in das Dict schreiben
        desktop = float(subtitles[0 + overall_found].text.split("Performance:")[1].strip())
        homepage_navigation = float(subtitles[1 + overall_found].text.split("Performance:")[1].strip())

        homepage = float(subtitles[2 + overall_found].text.split("Performance:")[1].strip())

        data[website_name]["Desktop"] = desktop
        data[website_name]["Homepage_Navigation"] = homepage_navigation
        data[website_name]["Homepage"] = homepage

        return data

    finally:
        driver.quit()

# URL zur Abcam-Seite
url = "https://baymard.com/ux-benchmark/case-studies/abcam"
result = scrape_abcam_data(url)
print(result)
