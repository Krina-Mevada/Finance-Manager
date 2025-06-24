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

#Create budget table
def create_budget_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER NOT NULL,
                   category TEXT NOT NULL,
                   month TEXT NOT NULL,
                   amount REAL NOT NULL,
                   UNIQUE(user_id, category, month)
                   )
                   ''')
    conn.commit()
    conn.close()

def set_budget(user_id, category, month, amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute('''
                INSERT INTO budgets (user_id, category, month, amount)
                    VALUES (?,?,?,?)
                    ON CONFLICT(user_id, category, month) 
                    DO UPDATE SET amount =  excluded.amount
                    ''',(user_id, category, month, amount))
        conn.commit()

    except Exception as e:
        print("Error setting budget:", e)

    finally:
        conn.close()

def get_budget(user_id, category, month):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
            SELECT amount FROM budgets
                WHERE user_id = ? AND category = ? AND month = ?
                ''',(user_id, category, month))
    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None

def get_total_expense_for_category(user_id, category, month):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    start_date = f"{month}-01"
    end_date = f"{month}-31"
    cursor.execute('''
            SELECT SUM(amount) FROM transactions
                WHERE user_id = ? AND category = ? AND type = "Expense"
                   AND date >= ? AND date <= ?
                ''',(user_id, category, start_date, end_date))
    row = cursor.fetchone()
    conn.close()

    return row[0] if row[0] else 0

def delete_budget(user_id,category,month,amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
            DELETE FROM budgets
            WHERE user_id = ? AND category = ? AND month = ? AND amount = ?
                   ''',(user_id, category,month,amount))
    
    conn.commit()
    conn.close()
