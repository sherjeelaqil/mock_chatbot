import sqlite3

def init_db(db_path='chat.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        created_at TEXT,
        end_time TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        message TEXT,
        response TEXT,
        timestamp TEXT,
        FOREIGN KEY(session_id) REFERENCES sessions(id)
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
