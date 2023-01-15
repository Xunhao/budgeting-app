# test

class BudgetApp:

	# Insert Class Variables here
	accounts = [] # Store all Accounts here

	# Initialise Account creation and populate it with basic requirements
	def __init__(self, account, description):
		self.account = account  # An account needs to be specified before categories and transactions can be created under it
		self.income = 20  # Every account starts with $0 income 
		self.expense = 30  # Every account starts with $0 expense 
		self.balance = self.income - self.expense  # The total amount of an account is the difference between income and expense
		self.description = description  # An short description for the Account created
		self.accounts.append(self.account)

	# Check current balance of an Account
	def check_balance(self):
		return f'Current {self.account} Balance: {self.balance}'

	# Handles all actions pertaining to Adding
	def add_action(self):
		pass

	# Handles all actions pertaining to Removing
	def remove_action(self):
		pass

	# Handles all actions pertaining to Modifying
	def modify_action(self):
		pass



# Test section
acc1 = BudgetApp('Bank', 'This is a sample bank account')
acc2 = BudgetApp('Investment', 'This is a sample investment account')
print(acc1.account)
print(BudgetApp.check_balance(acc1))
print(BudgetApp.accounts)