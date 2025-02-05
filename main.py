import psycopg2
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urlparse

load_dotenv()

# Postgres config
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

# A function to save links into database
def save_links_to_db(links):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.executemany(
            "INSERT INTO links (url) VALUES (%s) ON CONFLICT (url) DO NOTHING;",
            [(link,) for link in links],
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error saving links: {e}")

# Setup chrom web driver
PATH = "./chromedriver"
chrom_options = Options()
service = Service(PATH)
chrom_options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=chrom_options)

base_url = "https://www.isna.ir/"
collected_links = set()

# A function to get links of page
def get_links(url):
    links = set()
    driver.get(url)
    elements = driver.find_elements(By.TAG_NAME, "a")
    for elem in elements:
        link = elem.get_attribute("href")
        if link and urlparse(link).netloc.endswith("isna.ir"):
            links.add(link)
    return links

# Get all links of first depth
depth_1_links = list(get_links(base_url))[:120]
collected_links.update(depth_1_links)
save_links_to_db(depth_1_links)

# Get links of second depth
if len(collected_links) < 120:
    for link in depth_1_links:
        if len(collected_links) >= 120:
            break
        new_links = list(get_links(link))[:120 - len(collected_links)]
        collected_links.update(new_links)
        save_links_to_db(new_links)

print(f"Total links collected: {len(collected_links)}")

driver.quit()