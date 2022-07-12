'''
    A file to test how to run a basic web scraper
    Site used for this implementation: https://www.houzz.com/proMatch/handyman?m_refid=olm_google_720190069_43199500488_kwd-115160911&pos=&device=c&nw=g&matchtype=b&loc=9029030&loc2=&lsmr=ho_google&lsd=ho_google&gclid=EAIaIQobChMIsPbC0tXG-AIVTD6tBh1niw04EAMYAyAAEgKwivD_BwE
    NOTE: This file is specific to the site above, and will need to be altered to work for scraping data from other sites
        (ie. changing links, html class names, Selenium calls, etc.)
    NOTE: If when running the error message "unknown error: cannot determine loading status" is given, just re-run the code
        (this may be due to the web pages loading too slowly/slow internet connection -- but re-running the code 1-2 more
        times results in the code running correctly)
'''

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import csv

# constant variables
URL = "https://www.houzz.com/professionals#"
# CHROME_PATH needs to be changed depending on where chromedriver.exe is on machine
CHROME_PATH = "/Users/mxw115/Downloads/chromedriver"
CONTRACTOR_COMPANY_CLASS = "hz-pro-search-result__info"

# setting up webdriver options
options = Options()
options.page_load_strategy = 'normal'

f = open('./data/data.csv', 'w')
# NOTE: this will re-write the file each time this file is ran
writer = csv.writer(f)

# a function to take in an index and gather data from corresponding contractor company in index list from web page
def scrapeData(index, contractor_button_class):

    # starting a new instance of webdriver
    driver = webdriver.Chrome(options=options, executable_path=CHROME_PATH)
    driver.implicitly_wait(0.5)
    driver.get(URL)
    driver.implicitly_wait(10)

    driver.find_elements(By.CLASS_NAME, contractor_button_class)[index].click()
    driver.implicitly_wait(10)

    # the same contractor company may show up under multiple different contractor types, so changing up the index
    # on each call helps keep things more "random"
    driver.find_elements(By.CLASS_NAME, CONTRACTOR_COMPANY_CLASS)[index].click()
    driver.implicitly_wait(10)

    parent = driver.window_handles[0]
    child = driver.window_handles[1]
    driver.switch_to.window(child)
    driver.implicitly_wait(10)

    current_url = driver.current_url

    html_text = requests.get(current_url).text

    page_contents = BeautifulSoup(html_text, 'lxml')

    review_block = page_contents.find_all('div', class_='review-item')

    for item in review_block:
        # getting star-rating values (formated as: "average rating <number> out of 5")
        rating_value = item.find('span', class_='sr-only').text

        # re-formating the rating for entry into csv
        if "1" in rating_value:
            value = "1"
        elif "2" in rating_value:
            value = "2"
        elif "3" in rating_value:
            value = "3"
        elif "4" in rating_value:
            value = "4" 
        else:
            value = "5"

        review_text = item.find('div', class_='review-item__body-string').text

        # writing data to csv file
        writer.writerow([value] + [review_text])

    driver.quit()

print("Implementing web scraping...")

# "Architects and Building Designers" tab is index 0
scrapeData(0, "br-carousel-item__info")
print("Scraping from data source 0 complete...\n")

# "Interior Designers and Decorators" tab is index 1
scrapeData(1, "br-carousel-item__info")
print("Scraping from data source 1 complete...\n")

# "General Contractors" tab is index 2
scrapeData(2, "br-carousel-item__info")
print("Scraping from data source 2 complete...\n")

# "Home Builders" tab is index 3
scrapeData(3, "br-carousel-item__info")
print("Scraping from data source 3 complete...\n")

# "Kitchen and Bathroon Designers" tab is index 4
scrapeData(4, "br-carousel-item__info")
print("Scraping from data source 4 complete...\n")

# "Kitchen and Bathroom Remodelers" tab is index 5
scrapeData(5, "br-carousel-item__info")
print("Scraping from data source 5 complete...\n")

# "Landscape Architects and Landscape Designers" tab is index 6
scrapeData(6, "br-carousel-item__info")
print("Scraping from data source 6 complete...\n")

# "Landscape Contractors" tab is index 7
scrapeData(7, "br-carousel-item__info")
print("Scraping from data source 7 complete...\n")

# "Swimming Pool Builders" tab is index 8
scrapeData(8, "br-carousel-item__info")
print("Scraping from data source 8 complete...\n")

# "Decks, Patios and Outdoor Enclosures" tab is index 9
scrapeData(9, "br-carousel-item__info")
print("Scraping from data source 9 complete...\n")

print("Web scraping completed.")

f.close()

print("Completed writing to file.")