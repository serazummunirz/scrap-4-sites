import os, time, requests
from bs4 import BeautifulSoup

from selenium import webdriver

# import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
# chrome_options.add_argument('--remote-debugging-port=8989')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
wait = WebDriverWait(driver, 60)

# www.prnewswire.com:

search_month = "September"


keyword = "car"
pagesize = 50
page = 1


search_date = "29"
search_month = search_month[:3].upper()
search_year = "2023"


url = f"https://www.prnewswire.com/search/news/?keyword={keyword}&pagesize={pagesize}&page={page}"

driver.get(url)

page_source = driver.page_source
soup = BeautifulSoup(page_source)

full_section_data = soup.find('section', {'class': 'container search-results-text'})
all_results = full_section_data.find('div', {'class': 'col-sm-12 card-list'})

result_list = all_results.findAll('div', {'class': 'row newsCards'})


file_name = f"prnewswire{search_month}{search_date}{search_year}.txt"
if os.path.exists(file_name):
    os.remove(file_name)

for result in result_list:
    date_text = result.find('small').getText().split(",")
    posted_date = date_text[0] + date_text[1]

    searched_date = f"{search_month} {search_date} {search_year}"

    if posted_date.upper() == searched_date:
        rel_url = result.find('a', {'class': 'news-release'}).get('href')
        full_url = "https://www.prnewswire.com" + rel_url
        print(posted_date, full_url)

        with open(file_name, "a") as f:
            f.write(full_url + '\n')