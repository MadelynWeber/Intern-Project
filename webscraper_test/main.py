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
import requests

# getting information from the website that data will be scraped from
html_text = requests.get('https://www.houzz.com/professionals/kitchen-and-bath-remodelers/treeium-design-and-build-pfvwus-pf~914865704').text
# print(html_text)

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
    
    # getting review text
    review_text = item.find('div', class_='review-item__body-string').text
    print(review_text)
    print()

    # TODO: figure out how to add review_text and rating_value to a csv file for collecting data from this page



'''
    TODOs:
        1. figure out a way to keep the star rating and the review text together for each review
        2. add data to csv spreadsheet
        3. the company itself ~probably~ isn't important for training the model
        4. implement web automation using Selenium --> for this file's given website, needs to do the following...
            a. enter what kind of contractor we wish to search for on main page
            b. click on the contractor company from the results page
            c. click on 'reviews'
            d. scrape data
'''