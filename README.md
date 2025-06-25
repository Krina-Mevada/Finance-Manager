# FINANCE_MANAGER 🧾

A command-line based finance tracking tool built with Python + SQLite.

---

## 📦 Features
- User registration & login
- Add/edit/delete/view transactions
- Category & date-wise summaries
- Set monthly budgets by category
- Automatic database backup & restore
- Generate monthly/yearly reports

---

## 🛠 Installation

1. **Clone this repo:**
   git clone cd FINANCE_MANAGER

2. **Run the app:**
   python main.py

---

## ▶️ Usage

### Menu Options:
1. Register/Login  
2. Add new transaction  
3. View all transactions  
4. Update/Delete transactions
5. Generate monthly/yearly report  
6. Set/Delete budget by category  
7. Exit (auto-backup triggered)

> All data is stored locally in `finance_manager.db` and backed up in the `backup/` folder.

---

## ✅ Running Tests

To run all unit tests:

"python -m unittest discover tests"

---

## 📁 Folder Structure

backup/
finance_manager/ 
    ├── auth.py 
    ├── tracker.py 
    ├── budget.py 
    ├── report.py 
    ├── database.py 
    ├── backup.py 
    ├── utils.py 
main.py 
finance_manager.db 
tests/ 
    └── test_core.py
    └── test_transaction.py
---

## 🙋 Support
Feel free to raise an issue or contribute to improvements!

