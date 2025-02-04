# Web crawler with Selenium 

**Overview**

This project is a simple web crawler that collects links from a specified base URL up to a depth of two. It uses Selenium to scrape links from web pages and stores them in a PostgreSQL database, ensuring no duplicate links are saved.

**Installation**

Install dependencies:
```
pip install selenium dotenv psycopg2
```

Set up environment variables:
Create a `.env` file in the root directory and add your PostgreSQL credentials:
```
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
```
Ensure the PostgreSQL database has a links table:

```
CREATE TABLE IF NOT EXISTS links (
    url TEXT PRIMARY KEY
);
```

Place the Chrome WebDriver (chromedriver) in the project directory or specify its path in the script.

Place the link of the site in `base_url` and run `python main.py` to run the program.
