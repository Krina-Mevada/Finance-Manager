from finance_manager import database

def set_budget(user_id):
    category = input("Enter category: ")
    month = input("Enter month (YYYY-MM): ")
    amount = float(input("Enter budget amount: "))

    database.set_budget(user_id, category, month, amount)
    print(f"\nBudget set: {category} - {month} - {amount:.2f}")

def view_budget(user_id):
    category = input("Enter category: ")
    month = input("Enter month (YYYY-MM): ")
    budget = database.get_budget(user_id, category, month)
    spent = database.get_total_expense_for_category(user_id, category, month)

    print("\n=== Budget Report===")
    print(f"For category: {category} and month: {month}\n")
    if budget is not None:
        print(f"Budget : {budget:.2f}")
        print(f"Spent : {spent:.2f}")
        print(f"Remaining : {budget-spent:.2f}")
    else:
        print("No budget set for this category/month.")
    print("=====================\n")

def delete_budget(user_id):
    category = input("Enter category: ")
    month = input("Enter month (YYYY-MM): ")
    amount = float(input("Enter budget amount: "))
    database.delete_budget(user_id,category,month,amount)
