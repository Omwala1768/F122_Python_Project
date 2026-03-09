# db_manager.py

import sqlite3


DB = "portal.db"
import os
print("DB Location:", os.path.abspath(DB))


def connect():

    return sqlite3.connect(DB)


# ---------------- CREATE TABLE ----------------

def create_table():

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    """)

    con.commit()
    con.close()


# ---------------- REGISTER ----------------

def register_user(username, password):

    try:

        con = connect()
        cur = con.cursor()

        cur.execute(
            "INSERT INTO users VALUES (?, ?)",
            (username, password)
        )

        con.commit()
        con.close()

        return True

    except sqlite3.IntegrityError:
        return False


# ---------------- LOGIN ----------------

def login_user(username, password):

    username = username.strip().lower()
    password = password.strip()

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    row = cur.fetchone()
    con.close()

    if row is None:
        return "no_user"

    if row[0] != password:
        return "wrong_pass"

    return "success"


# ---------------- UPDATE PASSWORD ----------------

def update_password(username, new_pass):

    username = username.strip().lower()
    new_pass = new_pass.strip()

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute(
        "UPDATE users SET password=? WHERE username=?",
        (new_pass, username)
    )

    con.commit()

    # Check rows updated
    if cur.rowcount == 0:
        print("UPDATE FAILED: No matching username found")

    else:
        print("Password updated in DB")

    con.close()


    
def get_password(username):

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    row = cur.fetchone()

    con.close()

    if row:
        return row[0]

    return None
