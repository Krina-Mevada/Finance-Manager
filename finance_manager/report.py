from datetime import datetime
from finance_manager.database import fetch_transactions

def generate_report(user_id, year=None, month=None):

    #prepare date filters
    if year and month:
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-31"
    elif year:
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
    else:
        start_date = None
        end_date = None

    #Fetch data
    transactions = fetch_transactions(user_id, start_date, end_date)
   
    #Initialize totals
    total_income = 0
    total_expense = 0

    #Process transactions
    for date, category, amount, type in transactions:
        if type.lower() == "income":
            total_income += amount
        elif type.lower() == "expense":
            total_expense += amount

    savings = total_income - total_expense

    #Display report
    print("\n=== Financial Report ===\n")
    if year and month:
        print(f"For: {year}-{month:02d}")
    elif year:
        print(f"For year: {year}")
    else:
        print("For All time")
    print("-----------------------------")
    print(f"Total Income : {total_income:.2f}")
    print(f"Total Expense : {total_expense:.2f}")
    print(f"Total Savings : {savings:.2f}")
    print("-----------------------------\n")
