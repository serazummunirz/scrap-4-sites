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

search_month = "Feb"


keyword = "car"
pagesize = 50
page = 1


search_date = "23"
search_month = search_month[:3].upper()
search_year = "2023"


url = f"https://www.sec.gov/news/pressreleases?aId=&combine=car&year=All&month=All"

driver.get(url)
source_code = driver.page_source

# all_tables = driver.find_element(By.XPATH, '//table[@aria-describedby="DataTables_Table_0_info"]/tbody')

soup = BeautifulSoup(source_code)

odd_elements = soup.findAll('tr', {"class":"pr-list-page-row odd"})
even_elements = soup.findAll('tr', {"class":"pr-list-page-row even"})

file_name = f"sec{search_month}{search_date}{search_year}.txt"
if os.path.exists(file_name):
    os.remove(file_name)

for odd_element in odd_elements:
    searched_date = f"{search_month} {search_date} {search_year}"
    date_posted = odd_element.find('time', {"class": "datetime"}).text
    splited_date_posted = date_posted.split(",")
    actual_date_posted = f"{splited_date_posted[0].split()[0][:3].upper()} {splited_date_posted[0].split()[1]} {splited_date_posted[1].strip()}"
    if actual_date_posted == searched_date:
        base_url = "https://www.sec.gov"
        article_url = odd_element.find('a', {"hreflang": "en"}).get('href')
        full_url = base_url + article_url
        print(actual_date_posted)
        print(full_url)

        with open(file_name, "a") as f:
            f.write(article_url + '\n')

for odd_element in even_elements:
    searched_date = f"{search_month} {search_date} {search_year}"
    date_posted = odd_element.find('time', {"class": "datetime"}).text
    splited_date_posted = date_posted.split(",")
    actual_date_posted = f"{splited_date_posted[0].split()[0][:3].upper()} {splited_date_posted[0].split()[1]} {splited_date_posted[1].strip()}"
    if actual_date_posted == searched_date:
        base_url = "https://www.sec.gov"
        article_url = odd_element.find('a', {"hreflang": "en"}).get('href')
        full_url = base_url + article_url
        print(actual_date_posted)
        print(full_url)

        with open(file_name, "a") as f:
            f.write(full_url + '\n')