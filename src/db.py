import sqlite3

def init_db():
    conn = sqlite3.connect('txid.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 cid TEXT,
                 txid TEXT)''')
    conn.commit()
    conn.close()
