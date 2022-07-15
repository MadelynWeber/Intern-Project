'''
    A file to test how to run a basic web scraper
    Site used for this implementation: https://www.angi.com/
    NOTE: This file is specific to the site above, and will need to be altered to work for scraping data from other sites
        (ie. changing links, html class names, Selenium calls, etc.)
    NOTE: If when running the error message "unknown error: cannot determine loading status" is given, just re-run the code
        (this may be due to the web pages loading too slowly/slow internet connection -- but re-running the code 1-2 more
        times results in the code running correctly)
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import math
import csv

# CHROME_PATH needs to be changed depending on where chromedriver.exe is on machine
CHROME_PATH = "/Users/mxw115/Downloads/chromedriver"

# reviews shown in format of "Showing 1-<number> of <number> reviews"
def get_num_total_reviews():
    total_reviews = driver.find_element(By.CLASS_NAME, "reviews__filters-clear").text.split()[3]
    driver.implicitly_wait(10)
    return total_reviews

# gets number of reviews shown per page in format of "Showing 1-<number> of <number> reviews"
def get_num_page_reviews():
    page_review_count = driver.find_element(By.CLASS_NAME, "reviews__filters-clear").text.split()[1]
    driver.implicitly_wait(10)
    page_review_count = page_review_count.split("-")[1]
    return page_review_count

# setting up webdriver options
options = Options()
options.page_load_strategy = 'normal'

f = open('./data/review_data2.csv', 'w')
# NOTE: this will re-write the file each time this file is ran
writer = csv.writer(f)

# opening file with list of URLs to scrape from
url_file = open('./review_urls.txt', 'r')
# for url in url_file.readlines():

try:
    for url in url_file:

        # starting a new instance of webdriver
        driver = webdriver.Chrome(options=options, executable_path=CHROME_PATH)
        driver.implicitly_wait(0.5)
        driver.get(url)
        driver.implicitly_wait(10)

        total_reviews = get_num_total_reviews()
        print("\nTotal reviews: " + str(total_reviews))

        reviews_on_page = get_num_page_reviews()
        print("\nNumber reviews on page: " + str(reviews_on_page))

        # counter to keep track of what review on page we are at
        page_review_count = 0
        while page_review_count < int(total_reviews):
            review_cards = driver.find_elements(By.CLASS_NAME, "review-card")
            driver.implicitly_wait(10)
            for card in review_cards:
                review_text = card.find_element(By.CLASS_NAME, "review-card__review-text").text
                driver.implicitly_wait(10)
                
                # checking for the presense of a "... read more" option when review text is too long
                if "Read more" in review_text and "..." in review_text:
                    card.find_element(By.CLASS_NAME, "review-card__show-more").click()
                    driver.implicitly_wait(10)
                    review_text = card.find_element(By.CLASS_NAME, "review-card__review-text").text
                    driver.implicitly_wait(10)

                star_rating = math.trunc(float(card.find_element(By.CLASS_NAME, "rating-number").text))
                driver.implicitly_wait(10)
                print(review_text)
                print(star_rating)
                print()

                # some reviews don't have text associated with them -- separating those out
                if len(review_text) > 2:
                    # writing data to csv file
                    writer.writerow([star_rating] + [review_text])
                page_review_count += 1
            print("\nPage count: " + str(page_review_count) + "\n")

            # clicking "next" button to get to next page
            if page_review_count != int(total_reviews):
                driver.implicitly_wait(10)
                driver.find_element(By.CLASS_NAME, "right-caret").click()
                driver.implicitly_wait(10)
                reviews_on_page = get_num_page_reviews()

        # closing webdriver instance
        driver.quit()
        print("\nFinished scraping data.\n")
        f.close()
        url_file.close()
        print("\nFinished writing data to file.\n")

except WebDriverException as e:
    print("Something went wrong.\n Exception message: " + str(e))
    driver.quit()
    f.close()
    url_file.close()

    if "unknown error: cannot determine loading status" in str(e):
        print("Error occured. Try running code again.\n")