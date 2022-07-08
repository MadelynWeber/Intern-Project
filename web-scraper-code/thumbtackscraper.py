# python3 thumbtackscraper.py links.txt
'''
    A file to run a basic web scraper for collecting contractor reviews
    Site used for this implementation: https://www.thumbtack.com/instant-results/?zip_code=73012&keyword_pk=102906937284094959&project_pk=457294761614598160
    NOTE: This file is specific to the site above, and will need to be altered to work for scraping data from other sites
        (ie. changing links, html class names, Selenium calls, etc.)
        THIS CODE ATTEMPTS TO CLICK THROUGH EVERY PAGE BUT DUE TO THE TIMING OF CLICK EVENTS, RACE CONDITIONS, ETC. IT DOES NOT WORK
        See --> https://www.cloudbees.com/blog/get-selenium-to-wait-for-page-load
'''

# Import Modules
import os
import sys
import math
import csv
import re
import time
from textwrap import indent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
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
# ------------------------------------------ first link constants ------------------------------------------------
# 'Next' button/page XPath
NEXT_PATH = '//button[@aria-label="Next"]'
RATING_CLASS = '_1Wv_Lm7Q0IE3AFEImQTWZ9'
REVIEW_PATH = "//div[contains(@class, 'pv4 bb b-gray')]"
REVIEW_TEXT_PATH = ".//div[@class='_3n1ubgNywOj7LmMk3eLlub mt2']"
REVIEW_CSS = "div[class*='pv4 bb b-gray']"
# ------------------------------------------------------------------------------------------
def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 3:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )

def click_through_to_new_page():
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
    wait = WebDriverWait(driver, 20, ignored_exceptions = ignored_exceptions)
    nextBtn = wait.until(EC.element_to_be_clickable((By.XPATH, NEXT_PATH)))            
    # nextBtn = driver.find_element(By.XPATH, NEXT_PATH)
    driver.execute_script("arguments[0].click();", nextBtn)
    def element_has_gone_stale():
        try:
            # poll the review elements with an arbitrary call
            driver.find_elements(By.CSS_SELECTOR, REVIEW_CSS)
            return False
        except StaleElementReferenceException:
            return True
    wait_for(element_has_gone_stale)

# driver = webdriver.Chrome(executable_path=CHROME_PATH)

s=Service(CHROME_PATH)
driver = webdriver.Chrome(service=s, options=chrome_options)
driver.implicitly_wait(0.5)

# function that finds the reviews on every page, assists in avoiding stale elements when pages are reloaded
def findReviews(driver):
    reviews = driver.find_elements(By.CSS_SELECTOR, REVIEW_CSS)
    if reviews:
        return reviews
    else:
        return False

# function that finds subelements of an element, assists in avoiding stale elements when pages are reloaded
def findSubelement(driver, PATH):
    element = driver.find_element(By.XPATH, PATH)
    if element:
        return element
    else:
        return False

def findRating(driver):
    rating = driver.find_element(By.CLASS_NAME, RATING_CLASS)
    if rating:
        return rating
    else:
        return False



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

                # head = requests.head(url, allow_redirects=True)

                # URL filter: check if link is an HTML page
                # if 'html' in head.headers['content-type']:
                #     response = requests.get(url, headers = headers, timeout=2)
                #     # check if returns a successful status code
                #     if response.status_code == 200:
                        # download page for the link and extract page content and convert to BeautifulSoup object
                        # soup = BeautifulSoup(response.content, 'html.parser')
                # ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
                ignored_exceptions = (StaleElementReferenceException,)
                wait = WebDriverWait(driver, 20, ignored_exceptions = ignored_exceptions)
                # continue clicking the next page until the last page is reached
                while True:                
                    nextBtn = wait.until(EC.presence_of_element_located((By.XPATH, NEXT_PATH)))
                    # nextBtn = driver.find_element(By.XPATH, NEXT_PATH)
                    # get information per review block
                    # last review on first page contains an extra class for some reason, may be similar for other pages
                    # reviews = driver.find_elements(By.CSS_SELECTOR, REVIEW_CSS)
                    reviews = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, REVIEW_CSS)))
                    # reviews = driver.find_elements(By.XPATH, REVIEW_PATH)
                    # grab data from each review on the page
                    for review in reviews:
                        # try:
                            print(review.get_attribute('innerHTML') + '\n')
                            # get star-rating values

                            # ratingBlock = wait.until(EC.presence_of_element_located(By.CLASS_NAME, RATING_CLASS))
                            # rating = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='_1Wv_Lm7Q0IE3AFEImQTWZ9']")))[count]['data-star'].text
                            # rating = review.find_element(By.CLASS_NAME, RATING_CLASS).get_attribute("data-star")
                            # rating = wait.until(review.find_element(By.CLASS_NAME, RATING_CLASS)).get_attribute("data-star")
                            wait1 = WebDriverWait(review, 20, ignored_exceptions = ignored_exceptions)
                            rating = wait1.until(EC.presence_of_element_located((By.CLASS_NAME, RATING_CLASS))).get_attribute("data-star")
                            # adjust for any lag to retrive DOM elements on newly refreshed page
                            
                            # rating = wait1.until(findRating).get_attribute("data-star")
                            # rating = review.find_elements(By.CLASS_NAME, RATING_CLASS)['data-star'].text
                            if rating == "":
                                print("Failed to obtain rating.")
                            # rating = ratingBlock[0]['data-star'].text()
                            
                            # review_text = review.find('div', id=re.compile('^review-text-')).text
                            # review_text = review.find_element(By.XPATH, ".//div[@id='re.compile('^review-text-')']").text
                            ''' replies to reviews have similar class values, main difference is that the original review posted will 
                            have mt2 included as a class while replies will have mt3 included as a class. Code below retrieves the 
                            correct nested element to get the review text '''
                            # review_div1 = review.find_element(By.XPATH, REVIEW_TEXT_PATH)
                            # review_div1 = wait1.until(findSubelement(REVIEW_TEXT_PATH))
                            # review_div1 = wait1.until(lambda d: d.find_element(By.XPATH, REVIEW_TEXT_PATH))
                            review_div1 = wait1.until(EC.presence_of_element_located((By.XPATH, REVIEW_TEXT_PATH)))
                            #review_div2 = review_div1.find_element(By.XPATH, ".//div[starts-with(@id,'review-text-')]")
                            wait2 = WebDriverWait(review_div1, 20, ignored_exceptions = ignored_exceptions)
                            # review_div2 = wait2.until(lambda d: d.find_element(By.XPATH, ".//div[starts-with(@id,'review-text-')]"))
                            review_div2 = wait2.until(EC.presence_of_element_located((By.XPATH, ".//div[starts-with(@id,'review-text-')]")))
                            #review_text = review_div2.find_element(By.TAG_NAME, "span").text
                            # adjust for any lag to retrive DOM elements on newly refreshed page
                            wait3 = WebDriverWait(review_div2, 20, ignored_exceptions = ignored_exceptions)
                            review_text = wait3.until(EC.presence_of_element_located((By.TAG_NAME, "span"))).text

                            if review_text == "":
                                print("Failed to obtain review text.")

                            # print(rating + review_text + '\n')
                            # writing data to csv file
                            writer.writerow([rating] + [review_text.replace('\n', ' ')])
                        # except:
                            # print("failed to retrive review") 
                            # continue
                    
                    # Check that there is a next button on the page
                    if nextBtn.is_enabled():
                        # click on next page through chromedriver (+ synchronize the state between the browser and its DOM and WebDriver script)
                        # wait.until(EC.element_to_be_clickable((By.XPATH, NEXT_PATH))).click() 
                        click_through_to_new_page()      
                        # nextBtn = wait.until(EC.element_to_be_clickable((By.XPATH, NEXT_PATH)))
                        
                        # # nextBtn = driver.find_element(By.XPATH, NEXT_PATH)
                        # driver.execute_script("arguments[0].click();", nextBtn)
                        print("click")
                        driver.implicitly_wait(0.5)   
                    else:   
                        print("No more pages left")
                        break             
            # except:
                print("Error")
        dataf.close()

if __name__ == "__main__":
    main()
                        
                        

