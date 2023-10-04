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


search_month = "September"


keyword = "car"
page_range = 5

search_date = "29"
search_month = search_month[:3].upper()
search_year = "2023"


file_name = f"businesswire{search_month}{search_date}{search_year}.txt"
if os.path.exists(file_name):
    os.remove(file_name)


page = 1

for _ in range(page_range):
        url = f"https://www.businesswire.com/portal/site/home/search/?searchType={keyword}&searchTerm=car&searchPage={page}"
        driver.get(url)

        while True:
                news_section = driver.find_elements(By.XPATH, "//ul[contains(@class,'bw-news-list')and not(contains(@id,'bw-more-news-list'))]//li")
                page_source = driver.page_source
                # page_source = driver.execute_script("return document.body.innerHTML;")
                soup = BeautifulSoup(page_source, "html.parser")
                inner_tables = soup.findAll('ul', {'class': 'bw-news-list'})
                if len(inner_tables) > 0:
                        for inner_table in inner_tables:
                                tables = inner_table.findAll('li')
                                for table in tables:
                                        searched_date = f"{search_month} {search_date} {search_year}"
                                        date_posted = table.find('time').text
                                        splited_date_posted = date_posted.split(",")
                                        month_date_splitted = splited_date_posted[0].split()[0]
                                        month_formatted = splited_date_posted[0].split()[0]
                                        date_formatted = splited_date_posted[0].split()[1]
                                        actual_date_posted = f"{month_formatted[:3].upper()} {date_formatted} {splited_date_posted[1].strip()}"
                                        if actual_date_posted == searched_date:
                                                print("Matched:", actual_date_posted)
                                                article_url = table.find('a').get('href')
                                                print(article_url)
                                                with open(file_name, "a") as f:
                                                        f.write(article_url + '\n')
                        break
        page += 1