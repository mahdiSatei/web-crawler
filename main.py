from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

PATH = "./chromedriver"
chrom_options = Options()
service = Service(PATH)
chrom_options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=chrom_options)

base_url = "https://www.isna.ir"