import sqlite3
from datetime import datetime

# Connect to the database
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create the expenses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    amount REAL NOT NULL
)
""")

conn.commit()


# Add a new expense
def add_expense():
    name = input("Enter expense name: ")
    category = input("Enter category (Food/Travel/Shopping): ")

    date = input("Enter date (YYYY-MM-DD), or press Enter for today: ")

    if date == "":
        date = datetime.now().strftime("%Y-%m-%d")

    try:
        datetime.strptime(date, "%Y-%m-%d")
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        cursor.execute("""
        INSERT INTO expenses (name, category, date, amount)
        VALUES (?, ?, ?, ?)
        """, (name, category, date, amount))

        conn.commit()
        print("Expense added successfully!")

    except ValueError:
        print("Invalid date or amount. Please try again.")


# View all expenses
def view_expenses():
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = cursor.fetchall()

    if not expenses:
        print("No expenses found.")
        return

    print("\n--- YOUR EXPENSES ---")

    for expense in expenses:
        print(
            f"ID: {expense[0]} | "
            f"Name: {expense[1]} | "
            f"Category: {expense[2]} | "
            f"Date: {expense[3]} | "
            f"Amount: ₹{expense[4]:.2f}"
        )


# Calculate total expenses
def calculate_total():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    print(f"\nTotal expenses: ₹{total:.2f}")


# Main menu
while True:
    print("\n===== EXPENSE TRACKER =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Calculate Total")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        view_expenses()

    elif choice == "3":
        calculate_total()

    elif choice == "4":
        print("Thank you for using Expense Tracker!")
        break

    else:
        print("Invalid choice. Please select 1, 2, 3, or 4.")

conn.close()