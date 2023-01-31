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
		c.execute(
			'''
			INSERT INTO transactions (date, account, category, sub_category, description, amount) VALUES
			(:date, :account, :category, :sub_category, :description, :amount)
			''', parameter
			)
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
		entry = c.execute('''
			SELECT
			*

			FROM transactions

			WHERE
			id = :id AND
			account = :account''', parameter
			).fetchone()
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

			c.execute(
				'''
				UPDATE transactions 
				SET date = :date, category = :category, sub_category = :sub_category, description = :description, amount = :amount 
				
				WHERE
				id = :id AND
				account = :account
				''',
				parameter)
			entry = c.execute('SELECT * FROM transactions WHERE id = :id', {'id': transaction_id}).fetchone()
			
			print(f'ID = {transaction_id} has been updated with the new values')
			print(json.dumps(dict(entry), indent = 1))

		else:
			print(f'ID = {transaction_id} does not exist in the database!')

# Check balances of Account(s)
def db_check_balance():

	account = input('Specify an Account or hit "Enter" to return the balances for all accounts: ') # Ask user which account he would like to retrieve the balance for

	with conn:
		if account != '': # return the balance of a specific account
			row = c.execute(
				'''
				SELECT
				count(distinct account) AS count

				FROM transactions

				WHERE
				lower(account) = :account
				''', {'account': account.lower()}
				).fetchone()

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
				lower(account) = :account

				GROUP BY
				account,
				category

				ORDER BY category DESC
				''',
				{'account': account.lower()}
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

def db_select_transactions(account):

	start_date = input('Enter Start date: ')

	if start_date == '':
		print('Error! No Start date provided')
		return None

	end_date = input('Enter End date: ')

	if end_date == '':
		print('Error! No End date provided')
		return None

	parameter = {
	'start_date': start_date,
	'end_date': end_date,
	'account': account
	}
	with conn:
		entries = c.execute(
			'''
			SELECT
	 		*

	 		FROM transactions

	 		WHERE
	 		lower(account) = :account and
	 		(date BETWEEN :start_date AND :end_date)
	 		''', parameter
	 		).fetchall()

		if len(entries) != 0:
			for entry in entries:
				print(json.dumps(dict(entry), indent = 1))
		else:
			print('No transactions found within the specified dates')


class BudgetApp:

	# Class Variables here

	# Initialise Account creation and populate it with basic requirements
	def __init__(self, account):
		self.account = account

	# Check current balance for a given or all accounts
	@staticmethod
	def check_balance():
		db_check_balance()

	# Retrieve transactions for a given account
	def list_transactions(self):
		db_select_transactions(self.account)

	# Insert transaction for a given account
	def insert_transaction(self, date, category, sub_category, amount, description = None):
		db_insert_transaction(
			date = date, account = self.account, category = category,
			sub_category = sub_category, amount = amount, description = description
			)

	# Delete transaction for a given account
	def delete_transaction(self, id):
		db_delete_transaction(self.account, id)

	# Update transaction for a given account
	def update_transaction(self, id):
		db_update_transaction(self.account, id)

conn.close()
