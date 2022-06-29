'''
    A file to test how to run a basic web scraper
    Site used for this implementation: https://www.houzz.com/proMatch/handyman?m_refid=olm_google_720190069_43199500488_kwd-115160911&pos=&device=c&nw=g&matchtype=b&loc=9029030&loc2=&lsmr=ho_google&lsd=ho_google&gclid=EAIaIQobChMIsPbC0tXG-AIVTD6tBh1niw04EAMYAyAAEgKwivD_BwE
    NOTE: This file is specific to the site above, and will need to be altered to work for scraping data from other sites
        (ie. changing links, html class names, Selenium calls, etc.)
'''

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import requests
import csv

URL = "https://www.houzz.com/professionals#"
URL_TEST = "https://www.houzz.com/professionals/kitchen-and-bath-remodelers/treeium-design-and-build-pfvwus-pf~914865704"
# html class name for finding contractors 
BUTTON_CLASS = "hz-text-clamp__text-node"
# html class name for contractor cards
CARD_CLASS = "hz-pro-search-result__info"
# html class name for contractor reviews
REVIEW_CLASS = ""
# path needs to be changed dpenending on where chromedriver.exe is saved on machine
CHROME_PATH = "/Users/mxw115/Downloads/chromedriver"
CONTRACTOR_CLASS = "hz-pro-search-results__item"

f = open('./data/review_data.csv', 'w')
# NOTE: this will re-write the file each time this file is ran
writer = csv.writer(f)

driver = webdriver.Chrome(executable_path=CHROME_PATH)
driver.implicitly_wait(0.5)
driver.get(URL)
driver.implicitly_wait(10)

# clicks on specific contractor button we wish to look at
driver.find_element(By.CLASS_NAME, BUTTON_CLASS).click()
driver.implicitly_wait(10)

# clicks on the specific contractor company we wish to look at
driver.find_element(By.CLASS_NAME, CARD_CLASS).click()
driver.implicitly_wait(10)

# creating ability to move between open tabs
tab = driver.current_window_handle
parent = driver.window_handles[0]
child = driver.window_handles[1]
driver.switch_to.window(child)
driver.implicitly_wait(10)

# get current url for scraping
current_url = driver.current_url 

# getting html information from url to be used with BeautifulSoup
html_text = requests.get(current_url).text

# gathers all contents from the webpage's html
page_contents = BeautifulSoup(html_text, 'lxml')

# getting information per review block
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
    
    # getting review text
    review_text = item.find('div', class_='review-item__body-string').text

    # writing data to csv file
    writer.writerow([value] + [review_text])

f.close()

print("Finished scraping webpage.")