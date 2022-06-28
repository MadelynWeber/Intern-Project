'''
    A file to test how to run a basic web scraper
    Site used for this implementation: https://www.houzz.com/proMatch/handyman?m_refid=olm_google_720190069_43199500488_kwd-115160911&pos=&device=c&nw=g&matchtype=b&loc=9029030&loc2=&lsmr=ho_google&lsd=ho_google&gclid=EAIaIQobChMIsPbC0tXG-AIVTD6tBh1niw04EAMYAyAAEgKwivD_BwE
'''

# NOTES:
#  1. may have to implement some form of web interaction in order to click on specific contractors, then proceed to scrape data?
#       a. could be done using Selenium? Or see if BeautifulSoup library (or some other) has this functionality

import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import requests
import csv
import os

URL = "https://www.houzz.com/professionals#"
URL_TEST = "https://www.houzz.com/professionals/kitchen-and-bath-remodelers/treeium-design-and-build-pfvwus-pf~914865704"
# html class name for finding contractors 
BUTTON_CLASS = "hz-text-clamp__text-node"
# path needs to be changed dpenending on where chromedriver.exe is saved on machine
CHROME_PATH = "/Users/mxw115/Downloads/chromedriver"

f = open('./data/review_data.csv', 'w')
# NOTE: this will re-write the file each time this file is ran
writer = csv.writer(f)

# getting information from the website that data will be scraped from
html_text = requests.get(URL_TEST).text

# Selenium interactions
driver = webdriver.Chrome(executable_path=CHROME_PATH)
driver.implicitly_wait(0.5)
driver.get(URL)
# clicks on specific contractor button to get to page with list of contractors
driver.find_elements_by_class_name(BUTTON_CLASS).click() # --> THIS METHOD DOES NOT WORK, FIND SOMETHING ELSE TO REPLAFCE
# wait for page load
timeout = 5
try:
    element_present = EC.presence_of_element_located((By.Class, BUTTON_CLASS))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load.")

# TODO: click on individual contractor on page --> might need to get url from each individual page for data scraping step
# TODO: go to 'reviews' tab and scrape data
# TODO: go back to previous contractor page
# TODO: click on next contractor on page and repeat

# gathers all contents from the webpage's html
page_contents = BeautifulSoup(html_text, 'lxml')

# getting information per review block
review_block = page_contents.find_all('div', class_='review-item')
# print(review_block)

for item in review_block:
    # print(item.text)

    # getting star-rating values (formated as: "average rating <number> out of 5")
    rating_value = item.find('span', class_='sr-only').text
    print(rating_value)

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
    print(review_text)
    print()

    # writing data to csv file
    writer.writerow([value] + [review_text])

f.close()

'''
    TODOs and Notes:
        4. implement web automation using Selenium --> for this file's given website, needs to do the following...
            a. enter what kind of contractor we wish to search for on main page
            b. click on the contractor company from the results page
            c. click on 'reviews'
            d. scrape data
'''