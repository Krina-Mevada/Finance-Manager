from finance_manager.database import get_db_connection
from finance_manager.database import get_budget, get_total_expense_for_category

#to add income/expense transactions
def add_transaction(user_id,amount,type,category):

    #check budget if expense
    if type == "Expense":
        date = input("Enter date (YYYY-MM-DD): ")
        month = date[:7]
        budget = get_budget(user_id, category, month)
        spent = get_total_expense_for_category(user_id, category, month)
        projected_total = amount + spent

        if budget is not None and projected_total > budget:
            print("warning: This will exceed your budget!")
            print(f"Budget: {budget:.2f}\nSpent so far: {spent:.2f}\nNow total is: {projected_total:.2f}")

    #insert the transaction
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
            INSERT INTO transactions(user_id, amount, type,category) 
                   VALUES(?,?,?,?)
                   ''',(user_id,amount, type, category))
    
    conn.commit()
    conn.close()
    print(f"\n{type} of ₹{amount} added successfully under category '{category}'.")

#to view all transactions
def view_transactions(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
            SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC
                   ''',(user_id,))

    rows = cursor.fetchall()
    conn.close()

    if rows:
        print("\n--- Transaction History ---")
        for row in rows:
            print(f"ID: {row['id']} | {row['type']} | ₹{row['amount']} | {row['category']} | {row['date']}")
    else:
        print("\nNo Transactions found!!")

#to update transactions
def update_transactions(id,user_id,amount,type,category):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
            UPDATE transactions 
            SET amount = COALESCE(?,amount), category = COALESCE(?,category), type = COALESCE(?,type)
            WHERE user_id = ? AND id = ?
                   ''',(amount, category, type, user_id, id))
    
    if cursor.rowcount == 0:
        print("Transaction not found or not authorized.")
    else:
        print("Transaction updated successfully.")
    
    conn.commit()
    conn.close()

#to delete transaction
def delete_transactions(user_id, id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
            DELETE FROM transactions
            WHERE user_id = ? AND id = ?
                   ''',(user_id, id))
    
    if cursor.rowcount == 0:
        print("Transaction not found or not authorized.")
    else:
        print("Transaction deleted successfully.")
    
    conn.commit()
    conn.close()

