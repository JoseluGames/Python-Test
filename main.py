from flask import Flask, request, redirect
import hashlib
import sqlite3
import validators
import secrets

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


@app.route("/register", methods=["POST"])
def register():
    token = secrets.token_urlsafe(4)
    run_query("INSERT OR IGNORE INTO users (token) VALUES (?)", (token,))
    return token


@app.route("/shorten/<token>", methods=["POST"])
def shorten(token):
    if run_query("SELECT token FROM users WHERE token = ?", (token,)) is None:
        return "Invalid token"

    long_url = request.form["url"]
    if validators.url(long_url) is not True:
        return "Invalid URL"

    short_url = shorten_url(long_url)
    run_query(
        "INSERT OR IGNORE INTO urls (short_url, url) VALUES (?, ?)",
        (short_url, long_url),
    )
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
    run_query("CREATE TABLE IF NOT EXISTS users (token TEXT NOT NULL PRIMARY KEY)")
    app.debug = True
    app.run()
