import os
from dotenv import load_dotenv

load_dotenv()

# Postgres config
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

BASE_URL = "https://www.isna.ir/"
MAX_DEPTH = 2
CHROME_DRIVER_PATH = "./chromedriver"