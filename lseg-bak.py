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
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--remote-debugging-port=8989')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
wait = WebDriverWait(driver, 60)

search_month = "Aug"
keyword = "car"
page_range = 5

search_date = "31"
search_month = search_month[:3].upper()
search_year = "2023"

# url = f"https://www.lseg.com/en/media-centre/press-releases?q={keyword}"
url = f"https://www.lseg.com/en/media-centre/press-releases"

driver.get(url)


count_page = 1

while count_page <= 5:
    page_source = driver.execute_script("return document.body.innerHTML;")
    soup = BeautifulSoup(page_source, "lxml")
    result_section = soup.find("div", {"class": "tr-SearchResults-results"})
    all_results = result_section.findAll("div", {"class": "tr-SearchResults-result"})

    for result in all_results:
        searched_date = f"{search_month} {search_date} {search_year}"
        date_posted = result.find('span', {'class': 'tr-SearchResults-articleInfoFooterDate'}).text
        splited_date_posted = date_posted.split(",")
        actual_date_posted = splited_date_posted[0].upper() + splited_date_posted[1]

        if actual_date_posted == searched_date:
            article_url = result.find('a', {'class': 'tr-SearchResults-resultTitle track-custom-clicks'}).get('href')

            print(searched_date)
            print(actual_date_posted)
            print(article_url)
    
    time.sleep(5)

    if count_page >= 5:
        break
    else:
        print(count_page)
        next_click_buttons = driver.find_elements(By.XPATH, '//button[@data-testid="navItemRight"]')
        for button in next_click_buttons:
            try:
                button.click()
                break
            except:
                pass
    time.sleep(5)
    
    count_page += 1