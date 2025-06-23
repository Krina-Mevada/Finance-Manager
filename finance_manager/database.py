import sqlite3
from datetime import datetime

DB_NAME = "finance_manager.db"

# make database query like dictionary format
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
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

# get all transactions made within specified period
def fetch_transactions(user_id,start_date=None,end_date=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    query = """

        SELECT date, category, amount, type 
        FROM transactions
        WHERE user_id = ?
    """
    params = [user_id]

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    cursor.execute(query,params)
    results = cursor.fetchall()
    conn.close()
    return results


