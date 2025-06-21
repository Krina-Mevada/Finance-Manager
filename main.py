from finance_manager import auth

def main():
    auth.init_db()

    print("\n---Personal Finance Manager---\n")
    print("1. Register")
    print("2. Login")
    choice = input("Choose an option (1/2): ")

    if choice == "1":
        auth.register()
    elif choice == "2":
        success = auth.login()
        if success:
            print("Now you can add transactions...")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
