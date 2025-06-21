import sqlite3
import getpass

DB_NAME = "finance_manager.db"

#create user table if not exists
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT UNIQUE NOT NULL,
                       password TEXT NOT NULL
                       )
                       ''')
        conn.commit()

#Register new user
def register():
    username = input("Enter new username: ")
    password = getpass.getpass("Enter new password: ")
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username,password) VALUES (?,?)
                       ''',(username,password))
            conn.commit()
            print("User registered successfully!")
        except sqlite3.IntegrityError:
            print("Username already exists. Try another.")

#Login user
def login():
    username = input("Enter new username: ")
    password = getpass.getpass("Enter new password: ")

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM users WHERE username= ? AND password=?
                       ''',(username,password))
        user = cursor.fetchone()
        if user:
            print(f"Welcome {username}!")
            return True
        else:
            print("Invalid credentials.")
            return False

