from flask import Flask, request
import hashlib

app = Flask(__name__)


def shorten_url(url):
    hash = hashlib.sha256(url.encode())
    digested = hash.hexdigest()
    return digested[:8]


@app.route("/shorten", methods=["POST"])
def shorten():
    url = request.form["url"]
    short_url = shorten_url(url)
    return request.host_url + short_url


if __name__ == "__main__":
    app.run()
