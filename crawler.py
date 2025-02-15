from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from collections import deque
from db import save_links_to_db
from config import MAX_DEPTH, BASE_URL, CHROME_DRIVER_PATH

def get_driver():
    chrome_coptions = Options()
    chrome_coptions.add_argument("--headless")
    service = Service(CHROME_DRIVER_PATH)
    return webdriver.Chrome(service=service, options=chrome_coptions)

# A function to normalize urls
def normalize(url):
    parsed = urlparse(url)
    normal_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return normal_url.rstrip('/')

# A function to get links of page
def get_links(driver, url):
    links = set()
    driver.get(url)
    elements = driver.find_elements(By.TAG_NAME, "a")
    for elem in elements:
        link = elem.get_attribute("href")
        if link and urlparse(link).netloc.startswith("www.isna.ir"):
            links.add(normalize(link))
    return links

def crawler():
    driver = get_driver()
    
    collected_links = set()
    visited_links = set()
    queue = deque([(BASE_URL, 1)])

    while queue:
        url, depth = queue.popleft()

        if url in visited_links or depth > MAX_DEPTH:
            continue

        visited_links.add(url)
        new_links = get_links(driver, url)
        new_links -= collected_links

        collected_links.update(new_links)
        save_links_to_db(new_links)

        print(f"{len(new_links)} links added to db")

        for link in new_links:
            queue.append((link, depth + 1))

    print(f"Total links collected: {len(collected_links)}")
    driver.quit()