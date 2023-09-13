from flask import Flask, request, redirect
import hashlib
import validators
import storage
import auth

app = Flask(__name__)


def shorten_url(url):
    hash = hashlib.sha256(url.encode())
    digested = hash.hexdigest()
    return digested[:8]


@app.route("/register", methods=["POST"])
def register():
    return auth.create_token()


@app.route("/shorten/<token>", methods=["POST"])
def shorten(token):
    if auth.validate_token(token) is not True:
        return "Invalid token"

    long_url = request.form["url"]
    if validators.url(long_url) is not True:
        return "Invalid URL"

    short_url = shorten_url(long_url)
    storage.store_shortened(short_url, long_url)
    return request.host_url + short_url


@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = storage.retrieve_url(short_url)

    if long_url:
        return redirect(long_url)
    else:
        return "URL not found"


if __name__ == "__main__":
    storage.run_query(
        "CREATE TABLE IF NOT EXISTS urls (short_url TEXT NOT NULL PRIMARY KEY, url TEXT)"
    )
    auth.setup()
    app.debug = True
    app.run()
