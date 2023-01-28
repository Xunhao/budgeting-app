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

# Add a line of transaction into DB table
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

class BudgetApp:

	# Class Variables here
	accounts = [] # Store all Accounts here
	income_categories = [] # Store all Income catgories here
	expense_categories = [] # Store all Expense categories here

	# Initialise Account creation and populate it with basic requirements
	def __init__(self, account, description):
		self.account = account  # An account needs to be specified before categories and transactions can be created under it
		self.ledger = [] # Create an ledger array to store various transactions for a given Account
		self.income = 50  # Every account starts with 0 income 
		self.expense = 30  # Every account starts with 0 expense 
		self.balance = self.income - self.expense  # The total amount of an account is the difference between income and expense
		self.description = description  # An short description for the Account created
		self.accounts.append(self.account)

	# Check current balance of an Account
	# def check_balance(self):
	# 	print(f'Current {self.account} Balance: {self.balance}')

	# List all Accounts under the Class
	# @classmethod
	# def list_accounts(cls):
	# 	return f'Accounts: {", ".join(cls.accounts)}'

	# Returns a unique list for further processing under Instances
	# @staticmethod
	# def return_unique_list(non_unique_list):
	# 	return list(set(non_unique_list))

	# Return all transactions between a given date range
	# def list_transactions(self, start_date = None, end_date = None):
		
		# transaction_dates = sorted(list(set([key['date'] for key in self.ledger])), reverse = False)

		# # Check if the user provided any date when calling the method
		# if start_date is None:
		# 	start_date = transaction_dates[0] # We will assign the earliest date if no date is provided
		# if end_date is None:
		# 	end_date = transaction_dates[-1] # We will assign the latest date if no date is provided

		# for count,entry in enumerate(self.ledger):
		# 	if start_date <= entry.get('date') <= end_date: # chain operation to consider only transaction dates within range
		# 		date = entry.get('date')
		# 		account = entry.get('transaction').get('account')
		# 		category = entry.get('transaction').get('category')
		# 		sub_category = entry.get('transaction').get('sub_category')
		# 		description = entry.get('transaction').get('description')
		# 		amount = entry.get('transaction').get('amount')
		# 		print(f'Date: {date}')
		# 		print(f'Account: {account}')
		# 		print(f'Category: {category}')
		# 		print(f'Sub_category: {sub_category}')
		# 		print(f'Description: {description}')
				# print(f'Amount: {amount}\n')

	# Handles all actions pertaining to Adding transaction
	def insert_transaction(self, date, category, sub_category, amount, description = None):
		db_insert_transaction(
			date = date,
			account = self.account,
			category = category,
			sub_category = sub_category,
			amount = amount,
			description = description
			)

	# Handles all actions pertaining to Removing transaction 
	def delete_transaction(self, id):
		db_delete_transaction(self.account, id)

	# Handles all actions pertaining to Modifying transaction
	def update_transaction(self, id):
		db_update_transaction(self.account, id)


# Test section
acc1 = BudgetApp('Bank', 'This is a sample bank account')
BudgetApp.insert_transaction(acc1, date = '2023-01-01', category = 'Income', sub_category = 'Salary', amount = 100) # Test insert function
BudgetApp.delete_transaction(acc1, id = 2) # Test delete function
# BudgetApp.update_transaction(acc1, 1) # Test update function
# BudgetApp.insert_transaction(acc1, date = '2023-01-01', category = 'Income', sub_category = 'Bonus', amount = 30)


# c.execute("SELECT * FROM transactions")
# print(dict(c.fetchone()))

conn.close()
