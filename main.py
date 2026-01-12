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