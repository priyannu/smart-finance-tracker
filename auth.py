import sqlite3
import hashlib
import os

SALT = b"finance_ai_fixed_salt"


def hash_password(password):
    return hashlib.scrypt(password.encode(), salt=SALT, n=16384, r=8, p=1).hex()


def create_db():
    with sqlite3.connect("users.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")


def register(username, password):
    with sqlite3.connect("users.db") as conn:
        existing = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if existing:
            return "Username already exists"
        conn.execute("INSERT INTO users VALUES (?,?)", (username, hash_password(password)))
    return "Registered successfully"


def login(username, password):
    with sqlite3.connect("users.db") as conn:
        data = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, hash_password(password))
        ).fetchone()
    return data is not None


def logout():
    return True
