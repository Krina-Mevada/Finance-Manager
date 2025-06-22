from finance_manager import auth
from finance_manager.database import create_transactions_table
from finance_manager.tracker import add_transaction, view_transactions,update_transactions,delete_transactions

def main():
    create_transactions_table()
    auth.init_db()

    print("\n---Personal Finance Manager---\n")
    print("1. Register")
    print("2. Login")
    choice = input("Choose an option (1/2): ")

    if choice == "1":
        auth.register()
    elif choice == "2":
        user_id = auth.login()
        if user_id:
            while True:
                print("\n--- Finance Manager Menu ---")
                print("1. Add Income")
                print("2. Add Expense")
                print("3. View Transactions")
                print("4. Update Transaction - (Check id from View trans(press 3))")
                print("5. Delete Transaction")
                print("6. Exit\n")

                choice = input("Enter your choice: ")

                if choice == '1':
                    amount = float(input("Enter Income Amount: "))
                    category = input("Enter category (e.g. Salary, Bonus): ")
                    add_transaction(user_id,amount,"Income",category)
                
                elif choice == '2':
                    amount = float(input("Enter Expense Amount: "))
                    category = input("Enter category (e.g. Grocery, Travel): ")
                    add_transaction(user_id,amount,"Expense",category)
                
                elif choice == '3':
                    view_transactions(user_id)

                elif choice == '4':
                    id = int(input("Enter Transaction ID to update: "))
                    amount = float(input("Enter Income/Expense Amount: "))
                    category = input("Enter category (e.g. Salary, Bonus): ")
                    type = input("Enter type - Income or Expense: ")
                    update_transactions(id,user_id,amount,type,category)

                elif choice == '5':
                    id = int(input("Enter Transaction ID to update: "))
                    delete_transactions(user_id, id)
                
                elif choice == '6':
                    print("Exiting Finance Manager. Goodbye!")
                    break

                else:
                    print("Invalid choice. Please try again")

    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
