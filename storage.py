import sqlite3


def run_query(query, params=()):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if result:
        return result[0]
    else:
        return None


def store_shortened(short_url, long_url):
    run_query(
        "INSERT OR IGNORE INTO urls (short_url, url) VALUES (?, ?)",
        (short_url, long_url),
    )


def retrieve_url(short_url):
    return run_query("SELECT url FROM urls WHERE short_url = ?", (short_url,))
