import sqlite3
from datetime import datetime
import os

class FinanceTracker:

    def __init__(self, db_name= "finances.bd"):
        self.db_name = db_name
        self. db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()

    def connect(self):
        """Connect to SQLite datebase"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        """Create transactions table of ot doesn't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOY NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT
            )
        ''')
        self.conn.commit() 

    def add_transaction(self, trans_type, category, amount, description=''):
        """add a new transaction"""
        date = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute('''
            INSERT INTO transactions (date, type, category, amount, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, trans_type, category, amount, description))
        self.comm.commit()
        print(f"\n{trans_type.capitalize()} of ${amount:.2f} added successfully!")
    
    def view_transactions(self, limit=None):
        """View all transactions"""
        query = 'SELECT * FROM transactions ORDER BY date DESC'
        if limit:
            query += f' LIMIT {limit}'

        self.cursor.execute(query)
        transactions = self.cursor.fetchall()
        
        if not transactions:
            print("\nNo transactions found.")
            return
        
        print("\n" + "="*80)
        print(f"{'ID':<5} {'Date':<12} {'Type':<10} {'Category':<15} {'Amount':<10} {'Description'}")
        print("="*80)

        for trans in transactions:
            trans_id, date, trans_type, category, amount, description = trans
            print(f"{trans_id:<5} {date:<12} {trans_type:<10} {category:<15} ${amount:<9.2f} {description}")
        print("="*80)

    def get_balance(self):
        """Calculate current balance"""
        self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
        income = self.cursor.fetchone()[0] or 0

        balance = income - expenses

        
        