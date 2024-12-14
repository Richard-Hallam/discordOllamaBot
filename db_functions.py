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



check_and_create_db(db_path)

def write_conversation_history_to_db(conversation_history, db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversation_history
                 (user_id text, role text, content text)''')
    for user_id, conversation in conversation_history.items():
        for message in conversation:
            c.execute("INSERT INTO conversation_history VALUES (?, ?, ?)", (user_id, message['role'], message['content']))
    conn.commit()
    conn.close()