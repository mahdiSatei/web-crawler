import psycopg2
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from collections import deque

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
MAX_DEPTH = 2

collected_links = set()
visited_links = set()
queue = deque([(base_url, 1)])

# A function to normalize urls
def normalize(url):
    parsed = urlparse(url)
    normal_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return normal_url.rstrip('/')

# A function to get links of page
def get_links(url):
    links = set()
    driver.get(url)
    elements = driver.find_elements(By.TAG_NAME, "a")
    for elem in elements:
        link = elem.get_attribute("href")
        if link and urlparse(link).netloc.startswith("www.isna.ir"):
            new_link = normalize(link)
            links.add(normalize(new_link))
    return links

# BFS algorithem for collecting links
while queue:

    url, depth = queue.popleft()

    if url in visited_links or depth > MAX_DEPTH:
        continue

    visited_links.add(url)
    new_links = get_links(url)
    new_links -= collected_links

    collected_links.update(new_links)
    save_links_to_db(new_links)

    print(f"{len(new_links)} links added to db")

    for link in new_links:
        queue.append((link, depth + 1))

print(f"Total links collected: {len(collected_links)}")

driver.quit()