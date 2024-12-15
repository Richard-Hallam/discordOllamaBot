import sqlite3
import os

db_path = 'ollamaDCBot.db'


def check_and_create_db(db_path):
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        conn.close()
        print(f"Database created at {db_path}")
    else:
        print(f"Database already exists at {db_path}")


def write_conversation_history_to_db(conversation_history, db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversation_history
                 (user_id text, role text, content text)''')
    for entry in conversation_history:
        user_id = entry['user_id']
        role = entry['role']
        content = entry['content']
        c.execute("INSERT INTO conversation_history VALUES (?, ?, ?)", (user_id, role, content))
    conn.commit()
    conn.close()


def read_conversation_history_from_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM conversation_history")
    rows = c.fetchall()
    conn.close()
    return rows


def write_indiviual_entry_to_db(user_id, role, content, db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO conversation_history VALUES (?, ?, ?)", (user_id, role, content))
    conn.commit()
    conn.close()