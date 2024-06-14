import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# Initialize SQLite database connection
def create_connection():
    conn = sqlite3.connect('finance_tracker.db')
    return conn

def create_tables(conn):
    with conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        );
        """)

def add_transaction(conn, transaction_type, amount, category, date):
    with conn:
        conn.execute("""
        INSERT INTO transactions (type, amount, category, date)
        VALUES (?, ?, ?, ?)
        """, (transaction_type, amount, category, date))

def view_transactions(conn):
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions ORDER BY date DESC")
        rows = cur.fetchall()
    return rows

def calculate_balance(conn):
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
        total_income = cur.fetchone()[0] or 0
        cur.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
        total_expense = cur.fetchone()[0] or 0
    return total_income - total_expense

# Streamlit interface
conn = create_connection()
create_tables(conn)

st.title("Personal Finance Tracker")

menu = ["Add Transaction", "View Transactions", "View Balance"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Transaction":
    st.subheader("Add New Transaction")
    transaction_type = st.selectbox("Type", ["Income", "Expense"])
    amount = st.number_input("Amount", min_value=0.01, step=0.01)
    category = st.text_input("Category (e.g., Food, Rent)")
    date_input = st.date_input("Date", value=date.today())
    
    if st.button("Add Transaction"):
        add_transaction(conn, transaction_type, amount, category, date_input.strftime("%Y-%m-%d"))
        st.success("Transaction added successfully!")

elif choice == "View Transactions":
    st.subheader("View Transactions")
    transactions = view_transactions(conn)
    if transactions:
        df = pd.DataFrame(transactions, columns=["ID", "Type", "Amount", "Category", "Date"])
        st.dataframe(df)
    else:
        st.info("No transactions found.")

elif choice == "View Balance":
    st.subheader("View Balance")
    balance = calculate_balance(conn)
    st.write(f"Current Balance: ${balance:.2f}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("By: Your Name")
st.sidebar.markdown("[GitHub Repo](https://github.com/yourusername/finance-tracker)")