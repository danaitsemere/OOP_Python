import datetime


class Transaction:
    def __init__(self, amount, transaction_type, narration="", date_time=None):
        self.amount = amount
        self.transaction_type = transaction_type  
        self.narration = narration
        self.date_time = date_time if date_time else datetime.datetime.now()


    def __str__(self):
        return f"{self.date_time}: {self.transaction_type.title()} - ${self.amount:.2f} ({self.narration})"

class Account:
    def __init__(self, owner, account_number, minimum_balance=0):
        self.__owner = owner 
        self.__account_number = account_number  
        self.__transactions = [] 
        self.__loan_balance = 0  
        self.__is_frozen = False
        self.__minimum_balance = minimum_balance  
        self.__closed = False 

    def __get_current_balance(self):
       
        balance = 0
        for transaction in self.__transactions:
            if transaction.transaction_type == 'deposit' or transaction.transaction_type == 'interest' or transaction.transaction_type == 'transfer_in':
                balance += transaction.amount
            elif transaction.transaction_type == 'withdrawal' or transaction.transaction_type == 'transfer_out':
                balance -= transaction.amount
        balance -= self.__loan_balance
        return balance

    def account_status(self):
        if self.__closed:
            return "Alert: Account is closed."
        if self.__is_frozen:
            return "Alert: Account is frozen."
        return None

    def deposit(self, amount, narration=""):
        alert = self.account_status()
        if alert:
            return alert
        if amount > 0:
            transaction = Transaction(amount, 'deposit', narration)
            self.__transactions.append(transaction)
            return f"Deposited ${amount:.2f}. New balance: ${self.get_balance():.2f}"
        else:
            return "Deposit amount must be positive."

    def withdraw(self, amount, narration=""):
        alert = self.account_status()
        if alert:
            return alert
        if amount <= 0:
            return "Withdrawal amount must be positive."
        balance = self.__get_current_balance() 
        if balance - amount < self.__minimum_balance:
            return f"Insufficient withdrawal. Minimum balance requirement of ${self.__minimum_balance:.2f} not met."
        transaction = Transaction(amount, 'withdrawal', narration)
        self.__transactions.append(transaction)
        return f"Withdrew ${amount:.2f}. New balance: ${self.get_balance():.2f}"

    def transfer_funds(self, other_account, amount):
        alert = self.account_status()
        if alert:
            return alert
        if not isinstance(other_account, Account):
            return "Invalid target account."

        result = self.withdraw(amount, narration=f"Transfer to {other_account.get_account_number()}")
        if "Withdrew" in result:
            other_account.deposit(amount, narration=f"Transfer from {self.get_account_number()}")
            return f"Transferred ${amount:.2f} to account {other_account.get_account_number()}. New balance: ${self.get_balance():.2f}"
        return result

    def get_balance(self):
        return self.__get_current_balance()

    def request_loan(self, amount, narration=""):
        alert = self.account_status()
        if alert:
            return alert
        if amount > 0:
            self.__loan_balance += amount
            transaction = Transaction(amount, 'loan_request', narration)
            self.__transactions.append(transaction) 
            return f"Loan of ${amount:.2f} approved. Total loan: ${self.__loan_balance:.2f}"
        return "Loan amount must be positive."

    def repay_loan(self, amount, narration=""):
        alert = self.account_status()
        if alert:
            return alert
        if amount > 0:
            repayment = min(amount, self.__loan_balance)
            self.__loan_balance -= repayment
            transaction = Transaction(repayment, 'loan_repay', narration)
            self.__transactions.append(transaction)
            return f"Repaid ${repayment:.2f}. Remaining loan: ${self.__loan_balance:.2f}"
        return "Repayment must be positive."

    def view_account_details(self):
        return f"Owner: {self.__owner}, Account Number: {self.__account_number}, Balance: ${self.get_balance():.2f}, Loan: ${self.__loan_balance:.2f}"

    def change_account_owner(self, new_owner):
        alert = self.account_status()
        if alert:
            return alert
        self.__owner = new_owner
        return f"Account owner changed to {self.__owner}"

    def bank_statement(self):
        print(f"Transaction Statement for Account {self.__account_number} ({self.__owner}):")
        for transaction in self.__transactions:
            print(transaction)
        print(f"Current Loan Balance: ${self.__loan_balance:.2f}")
        print(f"Current Account Balance: ${self.get_balance():.2f}")
   
    def interest(self, rate=0.05):
        alert = self.account_status()
        if alert:
            return alert
        balance = self.__get_current_balance()
        if balance > 0:
            interest_amount = balance * rate
            transaction = Transaction(interest_amount, 'interest', narration=f"Interest applied at {rate*100}%")
            self.__transactions.append(transaction)
            return f"Interest of ${interest_amount:.2f} applied. New balance: ${self.get_balance():.2f}"
        return "No interest applied to non-positive balance."

    def freeze_account(self):
        self.__is_frozen = True
        return "Account has been frozen."

    def unfreeze_account(self):
        self.__is_frozen = False
        return "Account has been unfrozen."

    def set_minimum_balance(self, amount): 
        if amount >= 0:
            self.__minimum_balance = amount
            return f"Minimum balance set to ${amount:.2f}"
        return "Minimum balance must be non-negative."

    def close_account(self):
        alert = self.account_status()
        if alert:
            return alert
  
        self.__transactions.clear()
        self.__loan_balance = 0
        self.__closed = True
        self.__is_frozen = False
        return "Account closed and all data cleared."

    def get_owner(self):
        return self.__owner

    def get_account_number(self):
        return self.__account_number

    def get_loan_balance(self):
        return self.__loan_balance

    def is_account_frozen(self):
        return self.__is_frozen

    def get_minimum_balance(self):
        return self.__minimum_balance

    def is_account_closed(self):
        return self.__closed
