import sqlite3
from datetime import datetime
import os

class FinanceTracker:
    def __init__(self, db_name='finances.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()
    
    def connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def create_table(self):
        """Create transactions table if it doesn't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        ''')
        self.conn.commit()
    
    def add_transaction(self, trans_type, category, amount, description=''):
        """Add a new transaction"""
        date = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute('''
            INSERT INTO transactions (date, type, category, amount, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, trans_type, category, amount, description))
        self.conn.commit()
        print(f"\n✓ {trans_type.capitalize()} of ${amount:.2f} added successfully!")
    
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
        
        self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
        expenses = self.cursor.fetchone()[0] or 0
        
        balance = income - expenses
        
        print("\n" + "="*40)
        print(f"Total Income:   ${income:,.2f}")
        print(f"Total Expenses: ${expenses:,.2f}")
        print(f"Current Balance: ${balance:,.2f}")
        print("="*40)
        
        return balance
    
    def get_summary_by_category(self):
        """Get spending summary by category"""
        self.cursor.execute('''
            SELECT category, type, SUM(amount) as total
            FROM transactions
            GROUP BY category, type
            ORDER BY total DESC
        ''')
        
        results = self.cursor.fetchall()
        
        if not results:
            print("\nNo transactions to summarize.")
            return
        
        print("\n" + "="*50)
        print("Summary by Category")
        print("="*50)
        print(f"{'Category':<20} {'Type':<10} {'Total'}")
        print("-"*50)
        
        for category, trans_type, total in results:
            print(f"{category:<20} {trans_type:<10} ${total:,.2f}")
        
        print("="*50)
    
    def delete_transaction(self, trans_id):
        """Delete a transaction by ID"""
        self.cursor.execute('DELETE FROM transactions WHERE id = ?', (trans_id,))
        self.conn.commit()
        
        if self.cursor.rowcount > 0:
            print(f"\n✓ Transaction {trans_id} deleted successfully!")
        else:
            print(f"\n✗ Transaction {trans_id} not found.")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def display_menu():
    """Display main menu"""
    print("\n" + "="*40)
    print("   PERSONAL FINANCE TRACKER")
    print("="*40)
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View All Transactions")
    print("4. View Recent Transactions")
    print("5. Check Balance")
    print("6. View Summary by Category")
    print("7. Delete Transaction")
    print("8. Exit")
    print("="*40)


def main():
    tracker = FinanceTracker()
    
    # Common categories
    income_categories = ['Salary', 'Freelance', 'Investment', 'Gift', 'Other']
    expense_categories = ['Food', 'Transport', 'Entertainment', 'Bills', 'Shopping', 
                          'Healthcare', 'Education', 'Other']
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            # Add Income
            print("\nIncome Categories:", ', '.join(income_categories))
            category = input("Enter category: ").strip().capitalize()
            amount = float(input("Enter amount: $"))
            description = input("Enter description (optional): ").strip()
            tracker.add_transaction('income', category, amount, description)
        
        elif choice == '2':
            # Add Expense
            print("\nExpense Categories:", ', '.join(expense_categories))
            category = input("Enter category: ").strip().capitalize()
            amount = float(input("Enter amount: $"))
            description = input("Enter description (optional): ").strip()
            tracker.add_transaction('expense', category, amount, description)
        
        elif choice == '3':
            # View All Transactions
            tracker.view_transactions()
        
        elif choice == '4':
            # View Recent Transactions
            limit = int(input("How many recent transactions? "))
            tracker.view_transactions(limit)
        
        elif choice == '5':
            # Check Balance
            tracker.get_balance()
        
        elif choice == '6':
            # View Summary
            tracker.get_summary_by_category()
        
        elif choice == '7':
            # Delete Transaction
            trans_id = int(input("Enter transaction ID to delete: "))
            tracker.delete_transaction(trans_id)
        
        elif choice == '8':
            # Exit
            print("\nThank you for using Personal Finance Tracker!")
            tracker.close()
            break
        
        else:
            print("\n✗ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()