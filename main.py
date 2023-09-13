from flask import Flask, request, redirect, g
import hashlib
import validators
import storage
import auth
import analytics
from threading import Thread

app = Flask(__name__)


def shorten_url(url):
    hash = hashlib.sha256(url.encode())
    digested = hash.hexdigest()
    return digested[:8]


@app.route("/register", methods=["POST"])
def register():
    token = auth.create_token()
    Thread(target=analytics.track_register, args=(request.remote_addr, token)).start()
    return token


@app.route("/shorten/<token>", methods=["POST"])
def shorten(token):
    if auth.validate_token(token) is not True:
        return "Invalid token"

    long_url = request.form["url"]
    if validators.url(long_url) is not True:
        return "Invalid URL"

    short_url = shorten_url(long_url)
    storage.store_shortened(short_url, long_url)
    Thread(
        target=analytics.track_shortening, args=(request.remote_addr, token, short_url)
    ).start()
    return request.host_url + short_url


@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = storage.retrieve_url(short_url)

    if long_url:
        Thread(
            target=analytics.track_redirect, args=(request.remote_addr, short_url)
        ).start()
        return redirect(long_url)
    else:
        return "URL not found"


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "db"):
        g.db.close()


if __name__ == "__main__":
    storage.run_query(
        "CREATE TABLE IF NOT EXISTS urls (short_url TEXT NOT NULL PRIMARY KEY, url TEXT)"
    )
    auth.setup()
    analytics.setup()
    app.debug = True
    app.run()
