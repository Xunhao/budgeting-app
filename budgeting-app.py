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
		return f'Current {self.account} Balance: {self.balance}'

	# Handles all actions pertaining to Adding
	def add_transaction(self, date, account, category, sub_category, description, amount):

		# Add category if it does not exist yet
		if category.capitalize() == 'Income' and category not in self.income_categories:
			self.income_categories.append(category.capitalize())
			amount = abs(amount)
		else: 
			self.expense_categories.append(category.capitalize())
			amount = -abs(amount)  # We will cast a negative absolute so that users do not have explicitly include the minus sign

		transaction_dict = {
			'date': date,
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
		print(json.dumps(self.ledger, indent = 2))
		return f'Transaction added!\nCurrent Balance: {self.balance}'  # return something to indicate success

	# Handles all actions pertaining to Removing
	def remove_transaction(self):
		pass

	# Handles all actions pertaining to Modifying
	def modify_transaction(self):
		pass

	# Can consider adding an optional date argument 
	def list_transaction(self):
		pass


# Test section
acc1 = BudgetApp('Bank', 'This is a sample bank account')
# acc2 = BudgetApp('Investment', 'This is a sample investment account')
print(acc1.account)
print(BudgetApp.check_balance(acc1))

BudgetApp.add_transaction(acc1, '2023-01-01', 'Bank', 'Income', 'Salary', 'Salary for the month', 100)
BudgetApp.add_transaction(acc1, '2023-01-01', 'Bank', 'Expense', 'Food', 'Macs', 10)

print(BudgetApp.check_balance(acc1))


