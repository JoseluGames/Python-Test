from flask import Flask, request, redirect
import hashlib
import sqlite3

app = Flask(__name__)


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


def shorten_url(url):
    hash = hashlib.sha256(url.encode())
    digested = hash.hexdigest()
    return digested[:8]


@app.route("/shorten", methods=["POST"])
def shorten():
    url = request.form["url"]
    short_url = shorten_url(url)
    run_query("INSERT OR IGNORE INTO urls (short_url, url) VALUES (?, ?)", (short_url, url))
    return request.host_url + short_url

@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = run_query("SELECT url FROM urls WHERE short_url = ?", (short_url,))

    if long_url:
        return redirect(long_url)
    else:
        return "URL not found"


if __name__ == "__main__":
    run_query(
        "CREATE TABLE IF NOT EXISTS urls (short_url TEXT NOT NULL PRIMARY KEY, url TEXT)"
    )
    app.debug = True
    app.run()
