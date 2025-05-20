# chat_memory.py
import streamlit as st

import sqlite3
import os
from datetime import datetime

DB_FILE = "./DB/chat_memory.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chatlog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            role TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def init_resume_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            resume_name TEXT,
            resume_text TEXT,
            uploaded_at TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_message(user_id, role, message):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO chatlog (user_id, role, message, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (user_id, role, message, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def get_chat_history(user_id, limit=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    if limit is not None:
        c.execute('''
            SELECT role, message FROM chatlog
            WHERE user_id = ?
            ORDER BY timestamp ASC
            LIMIT ?
        ''', (user_id, limit))
    else:
        c.execute('''
            SELECT role, message FROM chatlog
            WHERE user_id = ?
            ORDER BY timestamp ASC
        ''', (user_id,))
    
    rows = c.fetchall()
    conn.close()
    return rows

def clear_chat_history(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        DELETE FROM chatlog WHERE user_id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()
    st.session_state.confirm_delete = False  # Reset confirmation
    st.success("✅ Chat history has been cleared. Please refresh the page.")
    st.rerun()
if __name__ == "__main__":
    clear_chat_history("demo_user")
    print("Chat history cleared for demo_user.")
    
