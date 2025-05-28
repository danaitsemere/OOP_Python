class BankAccount:
    def __init__(self, owner, minimum_balance=0):
        self.owner = owner
        self.deposits = []
        self.withdrawals = []
        self.loan_balance = 0
        self.is_frozen = False
        self.minimum_balance = minimum_balance
        self.closed = False

    def account_status(self):
        if self.closed:
            return "Error: Account is closed."
        if self.is_frozen:
            return "Error: Account is frozen."
        return None

    def deposit(self, amount):
        alert = self._check_account_status()
        if alert:
            return alert
        if amount > 0:
            self.deposits.append(amount)
            return f"Deposited ${amount:.2f}. New balance: ${self.get_balance():.2f}"
        else:
            return "Deposit amount must be positive."

    def withdraw(self, amount):
        alert = self._check_account_status()
        if alert:
            return alert
        if amount <= 0:
            return "Withdrawal amount must be positive."
        balance = self.get_balance()
        if balance - amount < self.minimum_balance:
            return f"Insufficient funds. Minimum balance requirement of ${self.minimum_balance:.2f} not met."
        self.withdrawals.append(amount)
        return f"Withdrew ${amount:.2f}. New balance: ${self.get_balance():.2f}"

    def transfer_funds(self, other_account, amount):
        alert= self._check_account_status()
        if alert:
            return error
        if isinstance(other_account, BankAccount):
            result = self.withdraw(amount)
            if "Withdrew" in result:
                return other_account.deposit(amount)
            return result
        return "Invalid target account."

    def get_balance(self):
        return sum(self.deposits) - sum(self.withdrawals) - self.loan_balance

    def request_loan(self, amount):
        alert = self._check_account_status()
        if alert:
            return error
        if amount > 0:
            self.loan_balance += amount
            return f"Loan of ${amount:.2f} approved. Total loan: ${self.loan_balance:.2f}"
        return "Loan amount must be positive."

    def repay_loan(self, amount):
        alert = self._check_account_status()
        if alert:
            return alert
        if amount > 0:
            repayment = min(amount, self.loan_balance)
            self.loan_balance -= repayment
            return f"Repaid ${repayment:.2f}. Remaining loan: ${self.loan_balance:.2f}"
        return "Repayment must be positive."

    def view_account_details(self):
        return f"Owner: {self.owner}, Balance: ${self.get_balance():.2f}, Loan: ${self.loan_balance:.2f}"

    def change_account_owner(self, new_owner):
        alert = self._check_account_status()
        if alert:
            return alert
        self.owner = new_owner
        return f"Account owner changed to {self.owner}"

  def show_account_summary(self):
    print("Transaction Statement:")
    count = 1
    for deposit in self.deposits:
        print(f"{count}. Deposit: ${deposit:.2f}")
        count += 1
    count = 1
    for withdrawal in self.withdrawals:
        print(f"{count}. Withdrawal: ${withdrawal:.2f}")
        count += 1
    print(f"Loan Balance: ${self.loan_balance:.2f}")

    def apply_interest(self):
        alert = self._check_account_status()
        if alert:
            return alert
        balance = self.get_balance()
        if balance > 0:
            interest = balance * 0.05
            self.deposits.append(interest)
            return f"Interest of ${interest:.2f} applied. New balance: ${self.get_balance():.2f}"
        return "No interest applied to non-positive balance."

    def freeze_account(self):
        self.is_frozen = True
        return "Account has been frozen."

    def unfreeze_account(self):
        self.is_frozen = False
        return "Account has been unfrozen."

    def set_minimum_balance(self, amount):
        if amount >= 0:
            self.minimum_balance = amount
            return f"Minimum balance set to ${amount:.2f}"
        return "Minimum balance must be non-negative."

    def close_account(self):
        alert = self._check_account_status()
        if alert:
            return alert
        self.deposits.clear()
        self.withdrawals.clear()
        self.loan_balance = 0
        self.closed = True
        return "Account closed and all data cleared."
