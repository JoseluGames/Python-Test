import sqlite3
from flask import g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("database.db")
    return g.db


def __internal_run_query(conn, query, params=()):
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    if result:
        return result[0]
    else:
        return None


def run_query(query, params=()):
    conn = sqlite3.connect("database.db")
    result = __internal_run_query(conn, query, params)
    conn.close()
    return result


def run_pooled_query(query, params=()):
    result = __internal_run_query(get_db(), query, params)
    return result


def store_shortened(short_url, long_url):
    run_pooled_query(
        "INSERT OR IGNORE INTO urls (short_url, url) VALUES (?, ?)",
        (short_url, long_url),
    )


def retrieve_url(short_url):
    return run_pooled_query("SELECT url FROM urls WHERE short_url = ?", (short_url,))
