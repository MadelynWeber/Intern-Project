'''
    A file to test how to run a basic web scraper
    Site used for this implementation: https://trustedpros.ca/write-a-review
        (ie. changing links, html class names, Selenium calls, etc.)
    NOTE: If when running the error message "unknown error: cannot determine loading status" is given, just re-run the code
        (this may be due to the web pages loading too slowly/slow internet connection -- but re-running the code 1-2 more
        times results in the code running correctly)
'''


from unittest import expectedFailure
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import csv

# constant variables
URL = "https://trustedpros.ca/write-a-review"
# CHROME_PATH needs to be changed depending on where chromedriver.exe is located on machine
CHROME_PATH = "/Users/mxw115/Downloads/chromedriver"

# setting up webdriver options
options = Options()
options.page_load_strategy = 'normal'

f = open('./data/review_data2.csv')
# NOTE: this will re-write the csv file each time this file is ran
writer = csv.writer(f)

# initializing an instance of webdriver
driver = webdriver.Chrome(options=options, executable_path=CHROME_PATH)
driver.implicitly_wait(0.5)
driver.get(URL)
driver.implicitly_wait(10)

# want data contents from the following indexes
index_list = [0, 1, 2, 6, 7, 10, 20, 22]
driver.find_elements(By.CLASS_NAME, 'c_name')[index_list[0]].click()
driver.implicitly_wait(10)

current_url = driver.current_url

html_text = requests.get(current_url).text

page_contents = BeautifulSoup(html_text, 'lxml')

review_block = page_contents.find_all('div', class_='feedback-sec')

for item in review_block:
    # getting star-rating values (formated as: <number>)
    rating_value = item.find('span', itemprop='ratingValue').text

    review_text = item.find('div', itempeek='description').text

    print(rating_value + review_text)

driver.quit()

print("Web scraping completed.")

f.close()

print("Completed writing to file.")