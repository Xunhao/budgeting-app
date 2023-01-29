import json
import sqlite3 

# Use an in-memory database for prototyping
conn = sqlite3.connect(':memory:')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# We will simply create a singular table to govern all transactions instead of attempting to normalise the design for simplicity
c.execute("""CREATE TABLE transactions (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	date DATE,
	account TEXT,
	category TEXT,
	sub_category TEXT,
	description TEXT,
	amount REAL
	)""")

# Add a line into the transaction table
def db_insert_transaction(date, account, category, sub_category, amount, description):

	parameter = {
		 'date': date,
		 'account': account,
		 'category': category,
		 'sub_category': sub_category,
		 'description': description,
		 'amount': amount
		 }

	with conn:
		c.execute("""INSERT INTO transactions (date, account, category, sub_category, description, amount) VALUES
		 (:date, :account, :category, :sub_category, :description, :amount)""", parameter)
		row = c.execute('SELECT date, account, category, sub_category, description, amount FROM transactions').fetchone()
		print(f'The following transaction has been added:')
		print(json.dumps(dict(row), indent = 1))

# Remove a line from the transaction table 
def db_delete_transaction(account, transaction_id):

	parameter = {
	'id': transaction_id,
	'account': account
	}

	with conn:
		entry = c.execute('SELECT * FROM transactions WHERE id = :id AND account = :account', parameter).fetchone()
		# No need to check for duplicated IDs since it auto increases for each entry
		if entry is not None:
			c.execute('DELETE FROM transactions WHERE id = :id AND account = :account', parameter)
			print(f'ID = {transaction_id} has been deleted successfully!')
		else:
			print(f'ID = {transaction_id} does not exist in the database!')

# Update a line in the transaction table
def db_update_transaction(account, transaction_id):

	with conn:
		entry = c.execute('SELECT * FROM transactions WHERE id = :id', {'id': transaction_id}).fetchone()
		if entry is not None:
			entry = dict(entry)
			print('Please provide a new value for each column. If you wish to skip a columnm, simply hit "Enter"')
			date = input('Date: ')
			category = input('Category: ')
			sub_category = input('Sub Category: ')
			description = input('Description: ')
			amount = input('Amount: ')

			if date == '':
				date = entry['date']

			if category == '':
				category = entry['category']

			if sub_category == '':
				sub_category = entry['sub_category']

			if description == '':
				description = entry['description']

			if amount == '':
				amount = entry['amount']

			parameter = {
			'id': transaction_id,
			'date':date, 
			'account': account,
			'category': category,
			'sub_category': sub_category,
			'description': description,
			'amount': amount
			}

			c.execute('''UPDATE transactions 
				SET date = :date, category = :category, sub_category = :sub_category, description = :description, amount = :amount 
				WHERE id = :id AND account = :account''',
				parameter)
			entry = c.execute('SELECT * FROM transactions WHERE id = :id', {'id': transaction_id}).fetchone()
			print(f'ID = {transaction_id} has been updated with the new values')
			print(json.dumps(dict(entry), indent = 1))

		else:
			print(f'ID = {transaction_id} does not exist in the database!')

def db_check_balance():

	account = input('Specify an Account or hit "Enter" to return all Accounts: ') # Ask user which account he would like to retrieve the balance for

	with conn:
		if account != '': # return the balance of a specific account
			row = c.execute('SELECT count(distinct account) as count FROM transactions WHERE lower(account) = :account', {'account': account.lower()}).fetchone()

			# Check if there are any transactions pertaining to the specified Account
			if dict(row).get('count') == 0:
				print(f'Account = "{account}" does not exist in the database')
				return None
			
			entries = c.execute(
				'''
				SELECT
				account,
				category,
				SUM(iif(category = 'Expense', -amount, amount)) as amount

				FROM transactions 

				WHERE
				account = :account

				GROUP BY
				account,
				category

				ORDER BY category DESC
				''',
				{'account': account.capitalize()}
				).fetchall()

		else: # Return balance of only all accounts
			entries = c.execute(
				'''
				SELECT 
				account,
				category,
				SUM(iif(category = 'Expense', -amount, amount)) as amount
					
				FROM transactions

				GROUP BY 1,2

				ORDER BY category DESC
				'''
				).fetchall()

		for entry in entries:
			print(json.dumps(dict(entry), indent = 1))

class BudgetApp:

	# Class Variables here

	# Initialise Account creation and populate it with basic requirements
	def __init__(self, account, description):
		self.account = account  # An account needs to be specified before categories and transactions can be created under it
		# self.ledger = [] # Create an ledger array to store various transactions for a given Account
		# self.income = 50  # Every account starts with 0 income 
		# self.expense = 30  # Every account starts with 0 expense 
		# self.balance = self.income - self.expense  # The total amount of an account is the difference between income and expense
		# self.description = description  # A short description for the Account created
		# self.accounts.append(self.account)

	# Check current balance of an Account
	@staticmethod
	def check_balance():
		db_check_balance()

	# Insert transaction
	def insert_transaction(self, date, category, sub_category, amount, description = None):
		db_insert_transaction(
			date = date, account = self.account, category = category,
			sub_category = sub_category, amount = amount, description = description
			)

	# Delete transaction
	def delete_transaction(self, id):
		db_delete_transaction(self.account, id)

	# Update transaction
	def update_transaction(self, id):
		db_update_transaction(self.account, id)


# Test section
acc1 = BudgetApp('Bank', 'This is a sample bank account')
acc2 = BudgetApp('Investment', 'This is a sample bank account')
BudgetApp.insert_transaction(acc1, date = '2023-01-01', category = 'Income', sub_category = 'Salary', amount = 100) # Test insert function
BudgetApp.insert_transaction(acc1, date = '2023-01-30', category = 'Income', sub_category = 'Salary', amount = 30) # Test insert function
BudgetApp.insert_transaction(acc1, date = '2023-01-30', category = 'Expense', sub_category = 'Gas', amount = 10) # Test insert function
BudgetApp.insert_transaction(acc2, date = '2023-01-01', category = 'Expense', sub_category = 'Food', amount = 50) # Test insert function
print('===BREAK===\n')
# BudgetApp.delete_transaction(acc1, id = 2) # Test delete function
# BudgetApp.update_transaction(acc1, 1) # Test update function


BudgetApp.check_balance()

# c.execute("SELECT * FROM transactions")
# print(dict(c.fetchone()))

conn.close()
