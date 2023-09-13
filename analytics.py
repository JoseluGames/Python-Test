import storage


def setup():
    storage.run_query(
        "CREATE TABLE IF NOT EXISTS analytics (timestamp TEXT, ip TEXT, action TEXT, user_token TEXT, url TEXT)"
    )


def track_register(ip, user_token):
    storage.run_query(
        "INSERT INTO analytics (timestamp, ip, action, user_token, url) VALUES (datetime('now'), ?, 'register', ?, NULL)",
        (ip, user_token),
    )


def track_shortening(ip, user_token, url):
    storage.run_query(
        "INSERT INTO analytics (timestamp, ip, action, user_token, url) VALUES (datetime('now'), ?, 'shorten', ?, ?)",
        (ip, user_token, url),
    )


def track_redirect(ip, url):
    storage.run_query(
        "INSERT INTO analytics (timestamp, ip, action, user_token, url) VALUES (datetime('now'), ?, 'redirect', NULL, ?)",
        (ip, url),
    )
