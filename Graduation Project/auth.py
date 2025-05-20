# auth.py
import sqlite3
import hashlib

DB_PATH = "./DB/users.db"

def init_users_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            gender TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(name, email, password, gender):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (name, email, password_hash, gender) VALUES (?, ?, ?, ?)', 
                (name, email, hash_password(password), gender))
        conn.commit()
        return True, "User registered successfully!"
    except sqlite3.IntegrityError:
        return False, "Email already registered."
    finally:
        conn.close()

def login_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, name, password_hash, gender FROM users WHERE email = ?', (email,))
    result = c.fetchone()
    conn.close()
    if result:
        user_id, name, stored_hash, gender = result
        if stored_hash == hash_password(password):
            return True, {"user_id": user_id, "name": name, "email": email, "gender": gender}
    return False, None
