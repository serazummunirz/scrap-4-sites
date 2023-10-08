import os, time, requests
from bs4 import BeautifulSoup

from selenium import webdriver

# import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

#Chrome profile directory.
chrome_profile = "C:\\Users\\Administrator\\chrome_profile"

if not os.path.exists(chrome_profile):
    os.mkdir(chrome_profile)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--user-data-dir={chrome_profile}')
chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 30)

# Import program functions
import SetEnviron
import GetLinks
import ScrapArticles
import AwsFunctions
import ReWriter


# Setup Environments
SetEnviron.SetEnviron()


keyword = os.environ["KEYWORD"]
search_date = os.environ["DATE"]
search_month = os.environ["MONTH"]
search_year = os.environ["YEAR"]
total_articles = int(os.environ["TOTAL_ATICLES"])
page_range = int(os.environ['MAX_PAGE'])
tinq_api_key = os.environ['TINQ_API_KEY']


# Hard coded values
pagesize = 50
file_name = f"{search_year}{search_month}{search_date}-{keyword}.txt"
folder_name = f"{search_year}{search_month}{search_date}/{keyword}"

# scraped_article_s3_path = f"scraped_articles/{folder_name}"

scraped_articles_folder_name = f"scraped_articles/{folder_name}"
rewritten_articles_folder_name = f"rewritten_articles/{folder_name}"
source_list_folder_name = "source_lists"

source_list_local_path = f"{source_list_folder_name}/{file_name}"
source_list_s3_path = f"{source_list_folder_name}/{file_name}"



# Defining main function 
def main():

    AwsFunctions.create_bucket()
    

    def setup_proxy():
        user_command = input("Do you need to set up proxy? (y/n):")
        if user_command.lower() == 'y':
            driver.get("https://chrome.google.com/webstore/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif")
            proxy_is_set = input("Are you done setting up the proxy? (y/n):")
            if proxy_is_set.lower() == 'y':
                pass
            else:
                exit()
        else:
            pass


    def create_initial_files_structure():
        if not os.path.exists(source_list_folder_name):
            os.mkdir(source_list_folder_name)
        if not os.path.exists(scraped_articles_folder_name):
            os.makedirs(scraped_articles_folder_name)
        if not os.path.exists(rewritten_articles_folder_name):
            os.makedirs(rewritten_articles_folder_name)


    def remove_old_file():
        if os.path.exists(source_list_local_path):
            os.remove(source_list_local_path)
    

    def scrap_links_from_all_sites():

        prnewswire_links = GetLinks.prnewswire_links
        prnewswire_links(driver, wait, keyword, search_date, search_month, search_year, source_list_local_path, pagesize, page_range, total_articles, WebDriverWait)

        sec_links = GetLinks.sec_links
        sec_links(driver, wait, keyword, search_date, search_month, search_year, source_list_local_path, pagesize, page_range, total_articles, WebDriverWait)

        # lseg_links = GetLinks.lseg_links
        # lseg_links(driver, wait, EC, By, keyword, search_date, search_month, search_year, source_list_local_path, pagesize, page_range, total_articles, WebDriverWait)

        businesswire_links = GetLinks.businesswire_links
        businesswire_links(driver, wait, EC, By, keyword, search_date, search_month, search_year, source_list_local_path, pagesize, page_range, total_articles, WebDriverWait)

        AwsFunctions.upload_file_to_s3(source_list_local_path, source_list_s3_path)


    def scrap_articles_from_all_links():
        if os.path.exists(source_list_local_path):
            scrap_articles = ScrapArticles.scrap_articles
            scrap_articles(driver, wait, EC, By, source_list_local_path, scraped_articles_folder_name)
        else:
            print("No Source Links for this prefernce. Please scrap again with from another criteria.")


    def upload_scraped_articles_to_s3():
        scraped_articles = os.listdir(scraped_articles_folder_name)
        for article in scraped_articles:
            source_article_full_path = f"{scraped_articles_folder_name}/{article}"
            AwsFunctions.upload_file_to_s3(source_article_full_path, source_article_full_path)
    
    def rewrite_articles():

        ReWriter.rewrite(tinq_api_key, scraped_articles_folder_name, rewritten_articles_folder_name)


    def upload_rewritted_article_to_s3():

        scraped_articles = os.listdir(rewritten_articles_folder_name)
        for article_file in scraped_articles:
            rewritten_article_full_path = f"{rewritten_articles_folder_name}/{article_file}"
            AwsFunctions.upload_file_to_s3(rewritten_article_full_path, rewritten_article_full_path)
            

    setup_proxy()
    create_initial_files_structure()
    remove_old_file()
    scrap_links_from_all_sites()
    scrap_articles_from_all_links()
    upload_scraped_articles_to_s3()
    # rewrite_articles()
    # upload_rewritted_article_to_s3()
    driver.close()


if __name__=="__main__":
    main()
