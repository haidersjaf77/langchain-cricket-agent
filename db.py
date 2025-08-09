import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            username TEXT,
            message TEXT,
            response TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Optional: handle duplicate user case here
    finally:
        conn.close()


def validate_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result


def save_convo(username, message, response):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (username, message, response) VALUES (?, ?, ?)",
        (username, message, str(response))
    )
    conn.commit()
    conn.close()


def get_user_history(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT message, response FROM history WHERE username=?", (username,))
    rows = cursor.fetchall()
    conn.close()
    return rows
