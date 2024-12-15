import sqlite3
import os

db_file='temp'

def check_and_create_db( db_file= db_file + '.db'):
    if not os.path.exists(db_file):
        conn = sqlite3.connect( db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS conversation_history
            (user_id text, role text, content text)''')
        conn.close()
        return(f"Database { db_file} created.")
    else:
        print(f"Database  { db_file} already exists ")



def write_conversation_history_to_db(conversation_history,  db_file= db_file + '.db'):
    conn = sqlite3.connect( db_file )
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


def read_conversation_history_from_db( db_file= db_file + '.db'):
    conn = sqlite3.connect( db_file)
    c = conn.cursor()
    c.execute("SELECT * FROM conversation_history")
    rows = c.fetchall()
    conn.close()
    return rows


def write_indiviual_entry_to_db(user_id, role, content,  db_file = db_file + '.db'):
    conn = sqlite3.connect( db_file)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversation_history
                (user_id text, role text, content text)''')
    c.execute("INSERT INTO conversation_history VALUES (?, ?, ?)", (user_id, role, content))
    conn.commit()
    conn.close()