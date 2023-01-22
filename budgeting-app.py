import json

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
		if category == 'Income':
			categories = '\n'.join(sorted(self.return_unique_list(self.income_categories)))
		else:
			categories = '\n'.join(sorted(self.return_unique_list(self.expense_categories)))

		return f'{self.account} Acount {category} categories:\n{categories}'

	# Handles all actions pertaining to Adding
	# Need to consider if there is a need to validate if a transaction already exist before adding
	def add_transaction(self, date, account, category, sub_category, description, amount):

		# Add category if it does not exist yet
		if category.capitalize() == 'Income':
			amount = abs(amount)
			if sub_category not in self.income_categories:  # Check if category exists. If not, add it in
				self.income_categories.append(sub_category.capitalize())
			
		elif category.capitalize() == 'Expense':
			amount = -abs(amount)  # We will cast a negative absolute so that users do not have to explicitly include the minus sign
			if sub_category not in self.expense_categories:
				self.expense_categories.append(sub_category.capitalize())
			

		transaction_dict = {
			'date': date,  # Will store as str as date is not JSON serializable
			'transaction': {
				'account': account,
				'category': category,
				'sub_category': sub_category,
				'description': description,
				'amount': amount
				}
		}
		self.ledger.append(transaction_dict)
		self.balance += amount
		return f'Transaction added!\nCurrent Balance: {self.balance}'  # Return something to indicate success

	# Handles all actions pertaining to Removing
	# Use .update()?
	def remove_transaction(self):
		pass

	# Handles all actions pertaining to Modifying
	# Use .pop()?
	def modify_transaction(self):
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


# Test section

acc1 = BudgetApp('Bank', 'This is a sample bank account')
acc2 = BudgetApp('Investment', 'This is a sample investment account')
# print(acc1.account)
# print(BudgetApp.check_balance(acc1))

BudgetApp.add_transaction(acc1, '2023-01-01', 'Bank', 'Income', 'Salary', 'Salary for the month', 100)
BudgetApp.add_transaction(acc1, '2023-01-02', 'Bank', 'Income', 'Bonus', 'Bonus for good performance', 30)
BudgetApp.add_transaction(acc1, '2023-01-05', 'Bank', 'Expense', 'Food', 'Macs', 10)
BudgetApp.add_transaction(acc1, '2023-01-10', 'Bank', 'Expense', 'Transport', 'Bus', 3)

print(BudgetApp.list_accounts())
BudgetApp.check_balance(acc1)
BudgetApp.list_transactions(acc1)
print(BudgetApp.list_categories(acc1, 'Income'))
print(BudgetApp.list_categories(acc1, 'Expense'))
