# python3 thumbtackscraper.py links.txt
'''
    A file to run a basic web scraper for collecting contractor reviews
    Site used for this implementation: https://www.thumbtack.com/instant-results/?zip_code=73012&keyword_pk=102906937284094959&project_pk=457294761614598160
    NOTE: This file is specific to the site above, and will need to be altered to work for scraping data from other sites
        (ie. changing links, html class names, Selenium calls, etc.)
'''

# Import Modules
import os
import sys
import math
import csv
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.parse import urldefrag
from urllib.request import urlopen
from urllib.request import Request

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("user-data-dir=C:\\selenium") 

chrome_options.binary_location = "/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta"
# Chromedriver path
CHROME_PATH = '/Users/arz003/Downloads/chromedriver'
# 'Next' button/page XPath
NEXT_PATH = '//button[@aria-label="Next"]'

# driver = webdriver.Chrome(executable_path=CHROME_PATH)

s=Service(CHROME_PATH)
driver = webdriver.Chrome(service=s, chrome_options=chrome_options)
driver.implicitly_wait(0.5)


def main():
    # get file from command line containing all the urls that need to be scraped
    file = Path(sys.argv[1])
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }



    dataf = open('./data/review_data1.csv', 'w')
    # NOTE: this will re-write the file each time this file is ran
    writer = csv.writer(dataf)
    
    if not os.path.exists(file):
        print("Error: Filepath does not exist")
        exit(1)

    with open(file, 'r', encoding="ISO-8859-1") as f:
        # read through file one URL at a time
        urls = f.read().splitlines()
        for url in urls: 
            # try:    
                # open website through chromedriver
                driver.get(url)
                driver.implicitly_wait(10)

                head = requests.head(url, allow_redirects=True)

                # URL filter: check if link is an HTML page
                if 'html' in head.headers['content-type']:
                    response = requests.get(url, headers = headers, timeout=2)
                    # check if returns a successful status code
                    if response.status_code == 200:
                        # download page for the link and extract page content and convert to BeautifulSoup object
                        soup = BeautifulSoup(response.content, 'html.parser')

                        
                        # continue clicking the next page until the last page is reached
                        while True:
                            nextBtn = driver.find_element(By.XPATH, '//button[@aria-label="Next"]')

                            print(nextBtn)
                            # If the Next button is enabled/available, then enabled_next_page_btn size will be one.
                            # if len(nextBtn) < 1:
                            if not nextBtn.is_enabled():
                                print("No more pages left")
                                break
                            else:
                                # get information per review block
                                reviewBlock = soup.find_all('div', class_='pv4 bb b-gray')

                                # grab data from each review on the page
                                for item in reviewBlock:
                                    try:
                                        # get star-rating values
                                        # review = item.find_all('div', class_="_1Wv_Lm7Q0IE3AFEImQTWZ9")
                                        # rating = review[0]['data-star']

                                        rating = driver.findElement(By.XPATH, "//div[@class='_1Wv_Lm7Q0IE3AFEImQTWZ9']")[0]['data-star'].getText()
                                        
                                        # getting review text
                                        # review_text = item.find('div', id=re.compile('^review-text-')).text
                                        review_text = driver.findElement(By.XPATH, "//div[@id='id=re.compile('^review-text-')']").getText()

                                        # writing data to csv file
                                        writer.writerow([rating] + [review_text.replace('\n', ' ')])
                                    except: 
                                        continue 
                                # click on next page through chromedriver
                                # driver.findElement(By.xpath('//button[@aria-label="Next"]')).click()
                                nextBtn = driver.find_element(By.XPATH, NEXT_PATH)
                                driver.execute_script("arguments[0].click();", nextBtn)              
                                # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Next"]'))).click()


                        
            # except:
                print("Error")
        dataf.close()

if __name__ == "__main__":
    main()
                        
                        

