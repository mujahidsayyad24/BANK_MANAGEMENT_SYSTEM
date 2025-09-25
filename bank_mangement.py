import mysql.connector as db
import random


def get_connection():
    return db.connect(user='root', password='Mysql@123', host='localhost', database='BANK_MANAGEMENT')


def generate_account_number():
    """Generate a 12-digit random account number"""
    return random.randint(10**11, 10**12 - 1)


def create_account():
    conn = get_connection()
    cursor = conn.cursor()
    name = input('Enter the name: ')
    account_type = input("Enter Account Type (SAVINGS/CURRENT): ")
    while True:
        pin = input('Set your pin: ')
        if len(pin) == 4 and pin.isdigit():
            break
        else:
            print("Pin must be exactly 4 digits")

    # generate random account number
    account_no = generate_account_number()

    cursor.execute(
        "INSERT INTO users(account_no, name, pin, account_type, balance) VALUES (%s,%s,%s,%s,%s)",
        (account_no, name, pin, account_type, 0)
    )
    conn.commit()

    print("Account created successfully!")
    print(f"Your Bank Account Number is: {account_no}")

    cursor.close()
    conn.close()


def user_login():
    conn = get_connection()
    cursor = conn.cursor()

    acc = input("Enter account number: ")
    pin = input("Enter PIN: ")

    cursor.execute("SELECT * FROM users WHERE account_no = %s AND pin = %s", (acc, pin))
    user = cursor.fetchone()

    if user:
        print("Login successful!")
        while True:
            print("\n1. Deposit\n2. Withdraw\n3. Balance\n4. Transactions\n5. Logout")
            choice = input("Enter choice: ")
            if choice == "1":
                deposit_money(acc)
            elif choice == "2":
                withdraw_money(acc)
            elif choice == "3":
                view_balance(acc)
            elif choice == "4":
                view_transactions(acc)
            elif choice == "5":
                break
            else:
                print("Invalid choice!")
    else:
        print("Invalid account number or PIN!")

    cursor.close()
    conn.close()


def deposit_money(account_no):
    conn = get_connection()
    cursor = conn.cursor()

    amount = int(input("Enter amount to deposit: "))
    cursor.execute("UPDATE users SET balance = balance + %s WHERE account_no = %s", (amount, account_no))
    cursor.execute(
        "INSERT INTO transactions (account_no, trans_type, amount) VALUES (%s, %s, %s)",
        (account_no, "DEPOSIT", amount)
    )
    conn.commit()
    print("Deposit successful")

    cursor.close()
    conn.close()


def withdraw_money(account_no):
    conn = get_connection()
    cursor = conn.cursor()

    amount = int(input("Enter amount to withdraw: "))
    cursor.execute("SELECT balance FROM users WHERE account_no = %s", (account_no,))
    balance = cursor.fetchone()[0]

    if amount > balance:
        print("Insufficient balance!")
    else:
        cursor.execute("UPDATE users SET balance = balance - %s WHERE account_no = %s", (amount, account_no))
        cursor.execute(
            "INSERT INTO transactions (account_no, trans_type, amount) VALUES (%s, %s, %s)",
            (account_no, "WITHDRAW", amount)
        )
        conn.commit()
        print("Withdrawal successful")

    cursor.close()
    conn.close()


def view_balance(account_no):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM users WHERE account_no = %s", (account_no,))
    balance = cursor.fetchone()[0]
    print(f"Your balance is: {balance}")

    cursor.close()
    conn.close()


def view_transactions(account_no):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT trans_id, trans_type, amount, trans_date FROM transactions WHERE account_no = %s",
        (account_no,)
    )
    rows = cursor.fetchall()

    print("Transaction History:")
    for row in rows:
        print(row)

    cursor.close()
    conn.close()


def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. View All Users")
        print("2. View Transactions of a Particular User")
        print("3. View Account Details of a Particular User")
        print("4. View Transactions of Particular Day")
        print("5. Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == "1":
            admin_view_all_users()
        elif choice == "2":
            admin_view_user_transactions()
        elif choice == "3":
            admin_view_user_details()
        elif choice == "4":
            admin_view_transactions()
        elif choice == "5":
            break
        else:
            print("Invalid choice!")


def admin_view_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT account_no, name, account_type, balance FROM users")
    rows = cursor.fetchall()

    print("\nAll Users:")
    for row in rows:
        print(f"Account No: {row[0]}, Name: {row[1]}, Type: {row[2]}, Balance: {row[3]}")

    cursor.close()
    conn.close()


def admin_view_user_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    acc_no = input("Enter Account Number: ")
    cursor.execute("SELECT trans_id, trans_type, amount, trans_date FROM transactions WHERE account_no = %s", (acc_no,))
    rows = cursor.fetchall()

    print(f"\nTransactions for Account {acc_no}:")
    for row in rows:
        print(row)

    cursor.close()
    conn.close()


def admin_view_user_details():
    conn = get_connection()
    cursor = conn.cursor()

    acc_no = input("Enter Account Number: ")
    cursor.execute("SELECT account_no, name, account_type, balance FROM users WHERE account_no = %s", (acc_no,))
    row = cursor.fetchone()

    if row:
        print(f"\nAccount Details:\nAccount No: {row[0]}, Name: {row[1]}, Type: {row[2]}, Balance: {row[3]}")
    else:
        print("User not found!")

    cursor.close()
    conn.close()


def admin_view_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    date = input("Enter date (YYYY-MM-DD): ")
    cursor.execute("SELECT * FROM transactions WHERE DATE(trans_date) = %s", (date,))
    rows = cursor.fetchall()

    print(f"Transactions on {date}:")
    for row in rows:
        print(row)

    cursor.close()
    conn.close()


# ---------------- MAIN PROGRAM ----------------
def main():
    while True:
        print("\n Welcome to Bank System")
        print("1. Create Account\n2. User Login\n3. Admin Login\n4. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            user_login()
        elif choice == "3":
            admin_password = input("Enter admin password: ")
            if admin_password == "Mysql@123":
                admin_menu()
            else:
                print("Wrong admin password!")
        elif choice == "4":
            print("Thank you for using our system")
            break
        else:
            print("Invalid choice!")


main()
