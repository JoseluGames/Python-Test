import storage
import secrets


def setup():
    storage.run_query(
        "CREATE TABLE IF NOT EXISTS users (token TEXT NOT NULL PRIMARY KEY)"
    )


def create_token():
    token = secrets.token_urlsafe(4)
    storage.run_pooled_query("INSERT OR IGNORE INTO users (token) VALUES (?)", (token,))
    return token


def validate_token(token):
    return (
        storage.run_pooled_query("SELECT token FROM users WHERE token = ?", (token,))
        is not None
    )
