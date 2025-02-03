from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

# Setup chrom web driver
PATH = "./chromedriver"
chrom_options = Options()
service = Service(PATH)
chrom_options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=chrom_options)

base_url = "https://www.isna.ir"

collected_links = set()

# A function to get links of page
def get_links(url):
    links = set()
    driver.get(url)

    elements = driver.find_elements(By.TAG_NAME, "a")
    for elem in elements:
        link = elem.get_attribute("href")
        if link:
            links.add(link)
    
    return links