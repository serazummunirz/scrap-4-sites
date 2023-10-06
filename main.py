import os, time, requests
from bs4 import BeautifulSoup

from selenium import webdriver

import SetEnviron

# import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--remote-debugging-port=8989')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
wait = WebDriverWait(driver, 10)



# Import program functions
import GetLinks


# Setup Environments
SetEnviron.SetEnviron()

keyword = os.environ["KEYWORD"]
search_date = os.environ["DATE"]
search_month = os.environ["MONTH"]
search_year = os.environ["YEAR"]
total_articles = int(os.environ["TOTAL_ATICLES"])
page_range = int(os.environ['MAX_PAGE'])


# Hard coded values
pagesize = 100
file_name = f"{search_month}{search_date}{search_year}.txt"

# Defining main function 
def main():

    def remove_old_file():
        if os.path.exists(file_name):
            os.remove(file_name)
    

    def scrap_links_from_all_sites():

        prnewswire_links = GetLinks.prnewswire_links
        prnewswire_links(driver, wait, keyword, search_date, search_month, search_year, file_name, pagesize, page_range, total_articles)

        sec_links = GetLinks.sec_links
        sec_links(driver, wait, keyword, search_date, search_month, search_year, file_name, pagesize, page_range, total_articles)

        lseg_links = GetLinks.lseg_links
        lseg_links(driver, wait, EC, By, keyword, search_date, search_month, search_year, file_name, pagesize, page_range, total_articles)

        businesswire_links = GetLinks.businesswire_links
        businesswire_links(driver, wait, EC, By, keyword, search_date, search_month, search_year, file_name, pagesize, page_range, total_articles)
    
    remove_old_file()
    scrap_links_from_all_sites()

    driver.close()


# Using the special variable
# __name__
if __name__=="__main__": 
    main()