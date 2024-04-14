import json
import datetime

# Global dictionary to store transactions
transactions = {}


def validate_date(date_string):
    try:
        datetime.datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# Improved file handling with the 'with' statement
def load_transactions():
    try:
        with open("transactions.json", "r") as file:
            return json.load(file)
    except:
        return {}


def save_transactions():
    with open("Transactions.json","w") as file:
        json.dump(transactions, file)


def add_transaction():
    try:
        type = input("Enter transaction type (e.g., Groceries, Salary): ")
        amount = input("Enter amount: ")
        try:
            amount = float(amount)
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return
        category = input("Enter transaction category (income/expense): ")
        while category.lower() not in ["income", "expense"]:
            print("Invalid category. Please enter either 'income' or 'expense'.")
            category = input("Enter transaction category (income/expense): ")
        date = input("Enter date (YYYY-MM-DD): ")
        while not validate_date(date):
            print("Invalid date format. Please enter date in YYYY-MM-DD format.")
            date = input("Enter date (YYYY-MM-DD): ")
        
        if type in transactions:
            transactions[type].append({"amount": amount, "category": category.lower(), "date": date})
        else:
            transactions[type] = [{"amount": amount, "category": category.lower(), "date": date}]
        
        print("Transaction added successfully")
        save_transactions()
    except Exception as e:
        print(f"An error occurred: {e}")


def bulk_add_transactions():
    try:
        file_name = input("Enter the file name containing bulk transactions: ")
        with open(file_name, 'r') as f:
            bulk_transactions = json.load(f)
            if isinstance(bulk_transactions, dict):
                for transaction in bulk_transactions:
                    if 'type' in transaction and 'amount' in transaction and 'category' in transaction and 'date' in transaction:
                        add_transaction(transaction['type'], transaction['amount'], transaction['category'], transaction['date'])
                    else:
                        print("Invalid transaction format. Each transaction should have 'type', 'amount', 'category', and 'date' fields.")
                save_transactions()
                print("Transactions added successfully!")
            else:
                print("Invalid data format. Expecting a dictionary of transactions.")
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data in file '{file_name}': {e}")
    except Exception as e:
        print(f"An error occurred while adding transactions: {e}")



def view_transactions():
    load_transactions()
    for type, trans in transactions.items():
        print(f"{type}:")
        for t in trans:
            print(f"  Amount: {t['amount']}, Category: {t['category']}, Date: {t['date']}")


def update_transaction():
    global transactions
    load_transactions()
    try:
        for types in transactions:
            print("Type: ", types)

            chosen_type = input("Enter the type you want to update from above: ")
            if chosen_type not in transactions:
                print(f"Type '{chosen_type}' not found. Please enter a valid type.")
            else:
                for index, transaction in enumerate(transactions[chosen_type]):
                    print(index, '.', transaction)
                choice = int(input("Enter the index to update: "))
                if choice >= len(transactions[chosen_type]) or choice < 0:
                    print("Invalid index selected.")
                    return

                new_amount = input("Enter new amount: ")
                try:
                    new_amount = float(new_amount)
                except ValueError:
                    print("Invalid amount. Please enter a numeric value.")
                    return

                new_category = input("Enter new category (income/expense): ")
                while new_category.lower() not in ["income", "expense"]:
                    print("Invalid category. Please enter either 'income' or 'expense'.")
                    new_category = input("Enter new transaction category (income/expense): ")

                new_date = input("Enter new date (YYYY-MM-DD): ")
                while not validate_date(new_date):
                    print("Invalid date format. Please enter date in YYYY-MM-DD format.")
                    new_date = input("Enter date (YYYY-MM-DD): ")

                transactions[chosen_type][choice] = {"amount": new_amount, "category": new_category.lower(), "date": new_date}
        save_transactions()  # Moved the save_transactions() call outside the loop
        print("Transaction updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def delete_transaction():
    load_transactions()
    if not transactions:
        print("No transactions to delete")
    else:
        try:
            for types in transactions:
                print("Type: ", types)
            chosen_type = input("Enter the type you want to delete from above: ")
            if chosen_type not in transactions:
                print(f"Type '{chosen_type}' not found. Please enter a valid type.")
                return
            for index, transaction in enumerate(transactions[chosen_type]):
                print(index, '.', transaction)
            choice = int(input("Enter the index to delete: "))
            del transactions[chosen_type][choice]
            if not transactions[chosen_type]:  # Checking if the list is empty and then deleting the key
                del transactions[chosen_type]
            save_transactions()
            print("Transaction deleted successfully. ")
        except Exception as e:
            print(f"An error occurred: {e}")


def display_summary():
    load_transactions()
    total_income = 0.0
    total_expense = 0.0
    try:
        for trans in transactions.values():
            for t in trans:
                try:
                    if t['category'] == 'income':
                        total_income += t['amount']
                    elif t['category'] == 'expense':
                        total_expense += t['amount']
                    else:
                        print("Invalid category")

                except Exception as e:
                    print(f"An error occurred: {e} ")
        print("Total income: ", total_income)
        print("Total expense : ", total_expense)
        print("Balance: ", total_income - total_expense)
    except Exception as e:
        print(f"An error occurred: {e}")


def main_menu():
    while True:
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. View Summary")
        print("6. Bulk Add Transaction") 
        print("7. Exit")
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                add_transaction()
            elif choice == "2":
                view_transactions()
            elif choice == "3":
                update_transaction()
            elif choice == "4":
                delete_transaction()
            elif choice == "5":
                display_summary()
            elif choice == "6":
                bulk_add_transactions()
            elif choice == "7":
                print("Thank you!")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main_menu()