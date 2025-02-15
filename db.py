import psycopg2

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
