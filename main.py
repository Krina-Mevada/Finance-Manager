from finance_manager import auth
from finance_manager.database import create_transactions_table, create_budget_table
from finance_manager.tracker import add_transaction, view_transactions,update_transactions,delete_transactions
from finance_manager.report import generate_report
from finance_manager import budget

def main():

    #auto creates transaction table
    create_transactions_table()
    create_budget_table()
    
    auth.init_db()

    while True:
        print("\n---Personal Finance Manager---\n")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option (1/2): ")

        if choice == "1":
            auth.register()
        elif choice == "2":
            user_id = auth.login()
            if user_id:

                #crud functionality
                while True:
                    print("\n--- Finance Manager Menu ---")
                    print("1. Add Income")
                    print("2. Add Expense")
                    print("3. View Transactions")
                    print("4. Update Transaction - (Check id from View trans(press 3))")
                    print("5. Delete Transaction")
                    print("6. Generate Monthly Report")
                    print("7. Generate Yearly Report")
                    print("8. Set Budget")
                    print("9. View Budget")
                    print("10. Delete Budget")
                    print("11. Exit\n")

                    choice = input("Enter your choice: ")

                    #add income amount
                    if choice == '1':
                        amount = float(input("Enter Income Amount: "))
                        category = input("Enter category (e.g. Salary, Bonus): ")
                        add_transaction(user_id,amount,"Income",category)
                    
                    #add expense amount
                    elif choice == '2':
                        amount = float(input("Enter Expense Amount: "))
                        category = input("Enter category (e.g. Grocery, Travel): ")
                        add_transaction(user_id,amount,"Expense",category)
                    
                    #to view transaction
                    elif choice == '3':
                        view_transactions(user_id)

                    #update transaction
                    elif choice == '4':
                        id = int(input("Enter Transaction ID to update: "))
                        amount = float(input("Enter Income/Expense Amount: "))
                        category = input("Enter category (e.g. Salary, Bonus): ")
                        type = input("Enter type - Income or Expense: ")
                        update_transactions(id,user_id,amount,type,category)

                    #delete transaction
                    elif choice == '5':
                        id = int(input("Enter Transaction ID to update: "))
                        delete_transactions(user_id, id)

                    #Genrate monthly report
                    elif choice == '6':
                        year = int(input("Enter year (YYYY): "))
                        month = int(input("Enter month (1-12): "))
                        generate_report(user_id, year, month)

                    #Generate yearly report
                    elif choice == '7':
                        year = int(input("Enter year (YYYY): "))
                        generate_report(user_id, year)

                    #Set budget
                    elif choice == '8':
                        budget.set_budget(user_id)
                    
                    #Get budget
                    elif choice == '9':
                        budget.view_budget(user_id)
                    
                    elif choice == '10':
                        budget.delete_budget(user_id)
                    
                    elif choice == '11':
                        print("Exiting Finance Manager. Goodbye!")
                        break

                    else:
                        print("Invalid choice. Please try again")

        elif choice == '3':
            print("Exiting from the app!!")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
