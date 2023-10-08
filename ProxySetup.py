from selenium import webdriver

driver = webdriver.Chrome()

def main():
    driver.get("https://ifconfig.me/ip")
    driver.refresh()


if __name__=="__main__":
    main()