import multiprocessing
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

urls = [
"https://baymard.com/ux-benchmark/case-studies/abcam",
"https://baymard.com/ux-benchmark/case-studies/abel-and-cole",
"https://baymard.com/ux-benchmark/case-studies/academy",
"https://baymard.com/ux-benchmark/case-studies/ace-hardware",
"https://baymard.com/ux-benchmark/case-studies/adidas",
"https://baymard.com/ux-benchmark/case-studies/adobe",
"https://baymard.com/ux-benchmark/case-studies/advance-auto-parts",
"https://baymard.com/ux-benchmark/case-studies/airbnb",
"https://baymard.com/ux-benchmark/case-studies/albertsons",
"https://baymard.com/ux-benchmark/case-studies/aldi",
"https://baymard.com/ux-benchmark/case-studies/allegro-medical",
"https://baymard.com/ux-benchmark/case-studies/allstate",
"https://baymard.com/ux-benchmark/case-studies/amazon",
"https://baymard.com/ux-benchmark/case-studies/american-eagle-outfitters",
"https://baymard.com/ux-benchmark/case-studies/anine-bing",
"https://baymard.com/ux-benchmark/case-studies/ann-taylor",
"https://baymard.com/ux-benchmark/case-studies/apple",
"https://baymard.com/ux-benchmark/case-studies/apple-music",
"https://baymard.com/ux-benchmark/case-studies/argos",
"https://baymard.com/ux-benchmark/case-studies/arrow",
"https://baymard.com/ux-benchmark/case-studies/asos",
"https://baymard.com/ux-benchmark/case-studies/att",
"https://baymard.com/ux-benchmark/case-studies/autodoc",
"https://baymard.com/ux-benchmark/case-studies/avast",
"https://baymard.com/ux-benchmark/case-studies/avnet",
"https://baymard.com/ux-benchmark/case-studies/away",
"https://baymard.com/ux-benchmark/case-studies/axa-uk",
"https://baymard.com/ux-benchmark/case-studies/bh-photo",
"https://baymard.com/ux-benchmark/case-studies/b-q",
"https://baymard.com/ux-benchmark/case-studies/backcountry",
"https://baymard.com/ux-benchmark/case-studies/backdrop",
"https://baymard.com/ux-benchmark/case-studies/bang-olufsen",
"https://baymard.com/ux-benchmark/case-studies/barkbox",
"https://baymard.com/ux-benchmark/case-studies/basecamp",
"https://baymard.com/ux-benchmark/case-studies/bass-pro-shops",
"https://baymard.com/ux-benchmark/case-studies/bell",
"https://baymard.com/ux-benchmark/case-studies/berlin-packaging",
"https://baymard.com/ux-benchmark/case-studies/bespoke-post",
"https://baymard.com/ux-benchmark/case-studies/best-buy",
"https://baymard.com/ux-benchmark/case-studies/best-western",
"https://baymard.com/ux-benchmark/case-studies/birchbox",
"https://baymard.com/ux-benchmark/case-studies/blivakker",
"https://baymard.com/ux-benchmark/case-studies/blue-apron",
"https://baymard.com/ux-benchmark/case-studies/bodybuilding",
"https://baymard.com/ux-benchmark/case-studies/bol",
"https://baymard.com/ux-benchmark/case-studies/book-of-the-month",
"https://baymard.com/ux-benchmark/case-studies/booking-com",
"https://baymard.com/ux-benchmark/case-studies/bossard",
"https://baymard.com/ux-benchmark/case-studies/bound-tree-medical",
"https://baymard.com/ux-benchmark/case-studies/box",
"https://baymard.com/ux-benchmark/case-studies/bt",
"https://baymard.com/ux-benchmark/case-studies/build-com",
"https://baymard.com/ux-benchmark/case-studies/burger-king",
"https://baymard.com/ux-benchmark/case-studies/cabelas",
"https://baymard.com/ux-benchmark/case-studies/carparts-com",
"https://baymard.com/ux-benchmark/case-studies/cb2",
"https://baymard.com/ux-benchmark/case-studies/centurylink",
"https://baymard.com/ux-benchmark/case-studies/chanel",
"https://baymard.com/ux-benchmark/case-studies/chewy",
"https://baymard.com/ux-benchmark/case-studies/codecademy",
"https://baymard.com/ux-benchmark/case-studies/cole-parmer",
"https://baymard.com/ux-benchmark/case-studies/costco",
"https://baymard.com/ux-benchmark/case-studies/cox",
"https://baymard.com/ux-benchmark/case-studies/crate-barrel",
"https://baymard.com/ux-benchmark/case-studies/crutchfield",
"https://baymard.com/ux-benchmark/case-studies/cvs",
"https://baymard.com/ux-benchmark/case-studies/debenhams",
"https://baymard.com/ux-benchmark/case-studies/deliveroo",
"https://baymard.com/ux-benchmark/case-studies/dell",
"https://baymard.com/ux-benchmark/case-studies/demon-tweeks",
"https://baymard.com/ux-benchmark/case-studies/dicks-sporting-goods",
"https://baymard.com/ux-benchmark/case-studies/digikey",
"https://baymard.com/ux-benchmark/case-studies/disney-store",
"https://baymard.com/ux-benchmark/case-studies/dollar-shave-club",
"https://baymard.com/ux-benchmark/case-studies/dominos-pizza",
"https://baymard.com/ux-benchmark/case-studies/doordash",
"https://baymard.com/ux-benchmark/case-studies/dropbox",
"https://baymard.com/ux-benchmark/case-studies/dunelm",
"https://baymard.com/ux-benchmark/case-studies/breuninger",
"https://baymard.com/ux-benchmark/case-studies/ecs-tuning",
"https://baymard.com/ux-benchmark/case-studies/ellos",
"https://baymard.com/ux-benchmark/case-studies/esme-hotel",
"https://baymard.com/ux-benchmark/case-studies/etsy",
"https://baymard.com/ux-benchmark/case-studies/everlane",
"https://baymard.com/ux-benchmark/case-studies/evernote",
"https://baymard.com/ux-benchmark/case-studies/evo",
"https://baymard.com/ux-benchmark/case-studies/expedia",
"https://baymard.com/ux-benchmark/case-studies/extranomical-tours",
"https://baymard.com/ux-benchmark/case-studies/farm-to-people",
"https://baymard.com/ux-benchmark/case-studies/fastenal",
"https://baymard.com/ux-benchmark/case-studies/fat-brain-toys",
"https://baymard.com/ux-benchmark/case-studies/firebase",
"https://baymard.com/ux-benchmark/case-studies/fitbit",
"https://baymard.com/ux-benchmark/case-studies/fnac",
"https://baymard.com/ux-benchmark/case-studies/foot-locker",
"https://baymard.com/ux-benchmark/case-studies/fresh-direct",
"https://baymard.com/ux-benchmark/case-studies/gamestop-com",
"https://baymard.com/ux-benchmark/case-studies/gamma",
"https://baymard.com/ux-benchmark/case-studies/gap",
"https://baymard.com/ux-benchmark/case-studies/generali",
"https://baymard.com/ux-benchmark/case-studies/gilt",
"https://baymard.com/ux-benchmark/case-studies/gopro",
"https://baymard.com/ux-benchmark/case-studies/gousto",
"https://baymard.com/ux-benchmark/case-studies/grainger",
"https://baymard.com/ux-benchmark/case-studies/grammarly",
"https://baymard.com/ux-benchmark/case-studies/green-chef",
"https://baymard.com/ux-benchmark/case-studies/gucci",
"https://baymard.com/ux-benchmark/case-studies/guitar-center",
"https://baymard.com/ux-benchmark/case-studies/hm",
"https://baymard.com/ux-benchmark/case-studies/hamleys",
"https://baymard.com/ux-benchmark/case-studies/harrys",
"https://baymard.com/ux-benchmark/case-studies/hayneedle",
"https://baymard.com/ux-benchmark/case-studies/hbo-max",
"https://baymard.com/ux-benchmark/case-studies/heb",
"https://baymard.com/ux-benchmark/case-studies/hellofresh",
"https://baymard.com/ux-benchmark/case-studies/henry-schein",
"https://baymard.com/ux-benchmark/case-studies/hibbett",
"https://baymard.com/ux-benchmark/case-studies/hitachi",
"https://baymard.com/ux-benchmark/case-studies/hollandandbarrett",
"https://baymard.com/ux-benchmark/case-studies/home-depot",
"https://baymard.com/ux-benchmark/case-studies/home-24",
"https://baymard.com/ux-benchmark/case-studies/hp",
"https://baymard.com/ux-benchmark/case-studies/hyatt",
"https://baymard.com/ux-benchmark/case-studies/iherb",
"https://baymard.com/ux-benchmark/case-studies/ikea",
"https://baymard.com/ux-benchmark/case-studies/inter-cars",
"https://baymard.com/ux-benchmark/case-studies/jp-cycles",
"https://baymard.com/ux-benchmark/case-studies/jc-penney",
"https://baymard.com/ux-benchmark/case-studies/jimmy-choo",
"https://baymard.com/ux-benchmark/case-studies/john-lewis",
"https://baymard.com/ux-benchmark/case-studies/just-eat",
"https://baymard.com/ux-benchmark/case-studies/kentucky-fried-chicken",
"https://baymard.com/ux-benchmark/case-studies/kicks",
"https://baymard.com/ux-benchmark/case-studies/kidandcoe",
"https://baymard.com/ux-benchmark/case-studies/kiwico",
"https://baymard.com/ux-benchmark/case-studies/kohls",
"https://baymard.com/ux-benchmark/case-studies/kroger",
"https://baymard.com/ux-benchmark/case-studies/ll-bean",
"https://baymard.com/ux-benchmark/case-studies/la-redoute",
"https://baymard.com/ux-benchmark/case-studies/lego",
"https://baymard.com/ux-benchmark/case-studies/leroy-merlin",
"https://baymard.com/ux-benchmark/case-studies/liberty-mutual",
"https://baymard.com/ux-benchmark/case-studies/lifeextension",
"https://baymard.com/ux-benchmark/case-studies/living-spaces",
"https://baymard.com/ux-benchmark/case-studies/louis-vuitton",
"https://baymard.com/ux-benchmark/case-studies/lowes",
"https://baymard.com/ux-benchmark/case-studies/lululemon",
"https://baymard.com/ux-benchmark/case-studies/lyko",
"https://baymard.com/ux-benchmark/case-studies/macys",
"https://baymard.com/ux-benchmark/case-studies/marks-spencer",
"https://baymard.com/ux-benchmark/case-studies/marley-spoon",
"https://baymard.com/ux-benchmark/case-studies/maxon",
"https://baymard.com/ux-benchmark/case-studies/mcafee",
"https://baymard.com/ux-benchmark/case-studies/mcdonalds",
"https://baymard.com/ux-benchmark/case-studies/mcgee-and-co",
"https://baymard.com/ux-benchmark/case-studies/mckesson",
"https://baymard.com/ux-benchmark/case-studies/mediamarkt",
"https://baymard.com/ux-benchmark/case-studies/medline",
"https://baymard.com/ux-benchmark/case-studies/menards",
"https://baymard.com/ux-benchmark/case-studies/microsoft",
"https://baymard.com/ux-benchmark/case-studies/microsoft-teams",
"https://baymard.com/ux-benchmark/case-studies/morrisons",
"https://baymard.com/ux-benchmark/case-studies/mouser",
"https://baymard.com/ux-benchmark/case-studies/msc-direct",
"https://baymard.com/ux-benchmark/case-studies/much-better-adventures",
"https://baymard.com/ux-benchmark/case-studies/musicians-friend",
"https://baymard.com/ux-benchmark/case-studies/mytoys-de",
"https://baymard.com/ux-benchmark/case-studies/neiman-marcus",
"https://baymard.com/ux-benchmark/case-studies/netflix",
"https://baymard.com/ux-benchmark/case-studies/netonnet",
"https://baymard.com/ux-benchmark/case-studies/newegg",
"https://baymard.com/ux-benchmark/case-studies/nike",
"https://baymard.com/ux-benchmark/case-studies/nordstrom",
"https://baymard.com/ux-benchmark/case-studies/norgren",
"https://baymard.com/ux-benchmark/case-studies/northern-tool",
"https://baymard.com/ux-benchmark/case-studies/norton",
"https://baymard.com/ux-benchmark/case-studies/obi",
"https://baymard.com/ux-benchmark/case-studies/ocado",
"https://baymard.com/ux-benchmark/case-studies/office-depot",
"https://baymard.com/ux-benchmark/case-studies/orange",
"https://baymard.com/ux-benchmark/case-studies/our-place",
"https://baymard.com/ux-benchmark/case-studies/overstock",
"https://baymard.com/ux-benchmark/case-studies/peapod",
"https://baymard.com/ux-benchmark/case-studies/pep-boys",
"https://baymard.com/ux-benchmark/case-studies/prince-akatoki-london",
"https://baymard.com/ux-benchmark/case-studies/progressive",
"https://baymard.com/ux-benchmark/case-studies/purple-carrot",
"https://baymard.com/ux-benchmark/case-studies/rei",
"https://baymard.com/ux-benchmark/case-studies/rent-the-runway",
"https://baymard.com/ux-benchmark/case-studies/reserved",
"https://baymard.com/ux-benchmark/case-studies/rev-zilla",
"https://baymard.com/ux-benchmark/case-studies/rtv-euro-agd",
"https://baymard.com/ux-benchmark/case-studies/safeway",
"https://baymard.com/ux-benchmark/case-studies/sainsburys",
"https://baymard.com/ux-benchmark/case-studies/schneider-electric",
"https://baymard.com/ux-benchmark/case-studies/sea-paradise",
"https://baymard.com/ux-benchmark/case-studies/sea-saffron",
"https://baymard.com/ux-benchmark/case-studies/sears",
"https://baymard.com/ux-benchmark/case-studies/sephora",
"https://baymard.com/ux-benchmark/case-studies/shangri-la",
"https://baymard.com/ux-benchmark/case-studies/shop-apotheke",
"https://baymard.com/ux-benchmark/case-studies/shopify",
"https://baymard.com/ux-benchmark/case-studies/sigma-aldrich",
"https://baymard.com/ux-benchmark/case-studies/slack",
"https://baymard.com/ux-benchmark/case-studies/smyths",
"https://baymard.com/ux-benchmark/case-studies/snowe",
"https://baymard.com/ux-benchmark/case-studies/charter-spectrum",
"https://baymard.com/ux-benchmark/case-studies/sportchek",
"https://baymard.com/ux-benchmark/case-studies/sports-direct",
"https://baymard.com/ux-benchmark/case-studies/staples",
"https://baymard.com/ux-benchmark/case-studies/state-farm",
"https://baymard.com/ux-benchmark/case-studies/sunbasket",
"https://baymard.com/ux-benchmark/case-studies/swansonvitamins",
"https://baymard.com/ux-benchmark/case-studies/tag-heuer",
"https://baymard.com/ux-benchmark/case-studies/take-walks",
"https://baymard.com/ux-benchmark/case-studies/target",
"https://baymard.com/ux-benchmark/case-studies/telekom",
"https://baymard.com/ux-benchmark/case-studies/tesco",
"https://baymard.com/ux-benchmark/case-studies/the-entertainer",
"https://baymard.com/ux-benchmark/case-studies/vitamin-shoppe",
"https://baymard.com/ux-benchmark/case-studies/thermo-fisher",
"https://baymard.com/ux-benchmark/case-studies/thomann",
"https://baymard.com/ux-benchmark/case-studies/tigerdirect",
"https://baymard.com/ux-benchmark/case-studies/tire-rack",
"https://baymard.com/ux-benchmark/case-studies/travelers",
"https://baymard.com/ux-benchmark/case-studies/trip-com",
"https://baymard.com/ux-benchmark/case-studies/tti",
"https://baymard.com/ux-benchmark/case-studies/twice",
"https://baymard.com/ux-benchmark/case-studies/uber-eats",
"https://baymard.com/ux-benchmark/case-studies/ulta",
"https://baymard.com/ux-benchmark/case-studies/urban-outfitters",
"https://baymard.com/ux-benchmark/case-studies/van-cleef-arpels",
"https://baymard.com/ux-benchmark/case-studies/verizon",
"https://baymard.com/ux-benchmark/case-studies/viasat",
"https://baymard.com/ux-benchmark/case-studies/victorias-secret",
"https://baymard.com/ux-benchmark/case-studies/vitamin-world",
"https://baymard.com/ux-benchmark/case-studies/vodafone",
"https://baymard.com/ux-benchmark/case-studies/walgreen-co",
"https://baymard.com/ux-benchmark/case-studies/walmart",
"https://baymard.com/ux-benchmark/case-studies/waters",
"https://baymard.com/ux-benchmark/case-studies/wayfair",
"https://baymard.com/ux-benchmark/case-studies/west-elm",
"https://baymard.com/ux-benchmark/case-studies/wild-rover-tours",
"https://baymard.com/ux-benchmark/case-studies/williams-sonoma",
"https://baymard.com/ux-benchmark/case-studies/xero",
"https://baymard.com/ux-benchmark/case-studies/xfinity",
"https://baymard.com/ux-benchmark/case-studies/zalando",
"https://baymard.com/ux-benchmark/case-studies/zendesk",
"https://baymard.com/ux-benchmark/case-studies/ziptrek-ecotours",
"https://baymard.com/ux-benchmark/case-studies/zoom",
"https://baymard.com/ux-benchmark/case-studies/zooplus"
]

# Funktion zur Extraktion der Daten
def scrape_data(url):
    # Selenium-Webdriver-Setup
    print(f"Scraping {url}")
    op = webdriver.ChromeOptions()
    op.add_argument('--headless')
    driver = webdriver.Chrome(options=op)

    try:
        driver.delete_all_cookies()

        driver.get(url)
        time.sleep(2)
        try:
            cookie_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyButtonAccept")))
            cookie_button.click()
            time.sleep(1)
        except Exception as e:
            print(f'Cookie error {url}')
            print(e)
        # Element 1: Website Name

        website_name = driver.find_element(By.CLASS_NAME, "truncate").text

        # Finden aller relevanten Elemente mit den Klassen _title_hfdxh_10 und _subTitle_hfdxh_23
        titles = driver.find_elements(By.CLASS_NAME, "_title_hfdxh_10")
        


        # Prüfung, ob "Overall UX Performance" existiert
        #! overall_found gibt an ob die Kategorie Overall UX Performance existiert -> dies beeinflusst wo welche Daten in der Liste titles/subtitles stehen -> daher muss eine Verschiebung von 1 eingebaut werden je nachdem ob Overall UX Performance existiert oder nicht
        overall_found = 0 
        
        if titles[0].text.find("Overall") != -1:
            overall_found = 1

        #! hier die anderen 3 Kategorien in das Dict schreiben
        
        try:
            wrapper = driver.find_elements(By.CLASS_NAME, "_wrapper_7m4vv_1")
            # Kein Overall und alles eingeklappt
            if len(wrapper) <= 4 and overall_found == 0:
                # Desktop ausklappen
                wrapper[0].click()
                # Homepage & Category ausklappen --> danach alles sichtbar
                new_wrapper = driver.find_elements(By.CLASS_NAME, "_wrapper_7m4vv_1")
                new_wrapper[1].click()

            # Kein Overall und Desktop ausgeklappt
            elif len(wrapper) > 4 and overall_found == 0:
                # Homepage & Category ausklappen --> danach alles sichtbar
                wrapper[1].click()

            # Overall + Desktop NICHT ausgeklappt
            elif len(wrapper) <= 4 and overall_found == 1:
                # Desktop ausklappen
                wrapper[1].click()
                # Homepage & Category ausklappen --> danach alles sichtbar
                new_wrapper = driver.find_elements(By.CLASS_NAME, "_wrapper_7m4vv_1")
                new_wrapper[2].click()

            # Overall + Desktop ausgeklappt
            elif len(wrapper) > 4 and overall_found == 1:
                # Homepage & Category ausklappen --> danach alles sichtbar
                wrapper[2].click()

            time.sleep(2)

        except Exception as e:
            print(e)

        subtitles = driver.find_elements(By.CLASS_NAME, "_subTitle_hfdxh_23")

        try:
            overall_text = subtitles[0]
            overall = clean_tag(overall_text)
        except:
            overall = -100
        try:
            desktop_text = subtitles[0 + overall_found]
            desktop = clean_tag(desktop_text)
        except:
            desktop = -100
        try:
            homepage_navigation_text = subtitles[1 + overall_found]
            homepage_navigation = clean_tag(homepage_navigation_text)
        except:
            homepage_navigation = -100
        try:
            homepage_text = subtitles[2 + overall_found]
            homepage = clean_tag(homepage_text)
        except:
            homepage = -100
        

        # Daten-Dictionary vorbereiten
        data = {website_name: {}}
        
        data[website_name]["Overall UX Performance"] = overall
        data[website_name]["Desktop"] = desktop
        data[website_name]["Homepage_Navigation"] = homepage_navigation
        data[website_name]["Homepage"] = homepage

        return data
    
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return {
            website_name: {
                "Overall UX Performance": -100,
                "Desktop": -100,
                "Homepage_Navigation": -100,
                "Homepage": -100
            }
        }
    finally:
        driver.quit()

def parallel_scrape(urls):
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(scrape_data, urls)
    all_data = {}
    for result in results:
        all_data.update(result)
    return all_data

def write_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
def clean_tag(tag):
    # Get the text of the tag and all its children
    parent_text = tag.text
    children_text = " ".join([child.text for child in tag.find_elements(By.XPATH, ".//*")])
    # Merge the parent and children text
    merged_text = parent_text + " " + children_text
    # Extract the performance score (clean text so score can be extracted)
    score_text = merged_text.split("Performance:")[1].strip().replace("~", "")
    score = float(score_text.split()[0])

    return score


        


def main():
    print("Start")
    start_time = time.time()
    all_data = {}

    all_data = parallel_scrape(urls)

    write_to_json(all_data, '/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/baymard_scores_3.json')

    end_time = time.time()
    print(f"Time: {int(end_time - start_time)}s")

if __name__ == "__main__":
    main()