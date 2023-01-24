import json
import sqlite3 

# Use an in-memory database for prototyping
conn = sqlite3.connect(':memory:')

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
def insert_transaction(date, account, category, sub_category, amount, description):
	with conn:
		c.execute("""INSERT INTO transactions (date, account, category, sub_category, description, amount) VALUES
		 (:date, :account, :category, :sub_category, :description, :amount)""", 
		 {
		 'date': date,
		 'account': account,
		 'category': category,
		 'sub_category': sub_category,
		 'description': description,
		 'amount': amount
		 }
		 )

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
	def check_balance(self):
		print(f'Current {self.account} Balance: {self.balance}')

	# List all Accounts under the Class
	@classmethod
	def list_accounts(cls):
		return f'Accounts: {", ".join(cls.accounts)}'

	# Returns a unique list for further processing under Instances
	@staticmethod
	def return_unique_list(non_unique_list):
		return list(set(non_unique_list))

	# List existing categories under each Account
	def list_categories(self, category):
		if category.capitalize() == 'Income':
			categories = '\n'.join(sorted(self.return_unique_list(self.income_categories)))
		else:
			categories = '\n'.join(sorted(self.return_unique_list(self.expense_categories)))

		return f'{self.account.capitalize()} Acount {category.capitalize()} categories:\n{categories}'

	# Allows adding of a new category to a specified Account
	def add_sub_category(self, category, sub_category):
		if category.capitalize() == 'Income':
			if sub_category not in self.income_categories:
				self.income_categories.append(sub_category.capitalize())
		elif category.capitalize() == 'Expense':
			if sub_category not in self.expense_categories:
				self.expense_categories.append(sub_category.capitalize())
		
		return f'"{sub_category.capitalize()}" added to {category.capitalize()} under {self.account.capitalize()} Account'


	# Allows removing of a new category to a specified Account
	# Also need to remove all transactions under the sub_category
	def remove_sub_category(self):
		pass

	# Allows modifying of a new category to a specified Account
	def modify_sub_category(self):
		pass

	# Return all transactions between a given date range
	def list_transactions(self, start_date = None, end_date = None):
		
		transaction_dates = sorted(list(set([key['date'] for key in self.ledger])), reverse = False)

		# Check if the user provided any date when calling the method
		if start_date is None:
			start_date = transaction_dates[0] # We will assign the earliest date if no date is provided
		if end_date is None:
			end_date = transaction_dates[-1] # We will assign the latest date if no date is provided

		for count,entry in enumerate(self.ledger):
			if start_date <= entry.get('date') <= end_date: # chain operation to consider only transaction dates within range
				date = entry.get('date')
				account = entry.get('transaction').get('account')
				category = entry.get('transaction').get('category')
				sub_category = entry.get('transaction').get('sub_category')
				description = entry.get('transaction').get('description')
				amount = entry.get('transaction').get('amount')
				print(f'Date: {date}')
				print(f'Account: {account}')
				print(f'Category: {category}')
				print(f'Sub_category: {sub_category}')
				print(f'Description: {description}')
				print(f'Amount: {amount}\n')

	# Handles all actions pertaining to Adding transaction
	def add_transaction(self, date, category, sub_category, amount, description = None):
		insert_transaction(
			date = date,
			account = self.account,
			category = category,
			sub_category = sub_category,
			amount = amount,
			description = description
			)

	# Handles all actions pertaining to Removing transaction 
	def remove_transaction(self):
		pass

	# Handles all actions pertaining to Modifying transaction
	def modify_transaction(self):
		pass


# Test section
acc1 = BudgetApp('Bank', 'This is a sample bank account')
BudgetApp.add_transaction(acc1, date = '2023-01-01', category = 'Income', sub_category = 'Salary', amount = 100)

c.execute("SELECT * FROM transactions")
print(c.fetchone())

conn.close()