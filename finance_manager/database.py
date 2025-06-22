import sqlite3

# make database query like dictionary format
def get_db_connection():
    conn = sqlite3.connect('finance_manager.db')
    conn.row_factory = sqlite3.Row
    return conn

#create transactions table if not exits
def create_transactions_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER NOT NULL,
                   amount REAL NOT NULL,
                   type TEXT NOT NULL,
                   category TEXT NOT NULL,
                   date TEXT DEFAULT (DATE('now'))
                   )
                   ''')
    conn.commit()
    conn.close()


