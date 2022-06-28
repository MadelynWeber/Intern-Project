'''
    A file to test how to run a basic web scraper
    Site used for this implementation: https://www.houzz.com/proMatch/handyman?m_refid=olm_google_720190069_43199500488_kwd-115160911&pos=&device=c&nw=g&matchtype=b&loc=9029030&loc2=&lsmr=ho_google&lsd=ho_google&gclid=EAIaIQobChMIsPbC0tXG-AIVTD6tBh1niw04EAMYAyAAEgKwivD_BwE
'''

# NOTES:
#  1. may have to implement some form of web interaction in order to click on specific contractors, then proceed to scrape data?
#       a. could be done using Selenium? Or see if BeautifulSoup library (or some other) has this functionality

from bs4 import BeautifulSoup
from selenium import webdriver
import requests

# getting information from the website that data will be scraped from
html_text = requests.get('https://www.houzz.com/professionals/kitchen-and-bath-remodelers/treeium-design-and-build-pfvwus-pf~914865704').text
print(html_text)

page_contents = BeautifulSoup(html_text, 'lxml')

# with open('./home.html', 'r') as html_file:
#     file_contents = html_file.read()
#     # print(file_contents)

# page_contents = BeautifulSoup(file_contents, 'lxml')
# tags = page_contents.find_all('p')
# # print(tags)

# # For contractor website:
# # rating_value = page_contents.find_all('span', class_='sr-only') # ratings look like: "average rating <number> out of 5"
# # review_text = page_contents.find_all('div', class_='review-item_body-string') # is a block of text

# for item in tags:
#     print(item)
    