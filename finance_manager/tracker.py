from finance_manager.database import get_db_connection

def add_transaction(user_id,amount,type,category):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
            INSERT INTO transactions(user_id, amount, type,category) 
                   VALUES(?,?,?,?)
                   ''',(user_id,amount, type, category))
    
    conn.commit()
    conn.close()
    print(f"\n{type} of ₹{amount} added successfully under category '{category}'.")

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

