import sqlite3

DB_NAME = "queries.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            article TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

def save_query_log(user_id, article):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO query_logs (user_id, article) VALUES (?, ?)", (user_id, article))
        conn.commit()