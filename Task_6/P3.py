<<<<<<< HEAD
class BankAccount:
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited: {amount}")
        else:
            print("Deposit amount must be positive")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance")
        else:
            self.balance -= amount
            print(f"Withdrawn: {amount}")

    def show_balance(self):
        print(f"Current balance: {self.balance}")


account = BankAccount()

account.deposit(1000)
account.withdraw(300)
account.withdraw(800) 
=======
class BankAccount:
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited: {amount}")
        else:
            print("Deposit amount must be positive")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance")
        else:
            self.balance -= amount
            print(f"Withdrawn: {amount}")

    def show_balance(self):
        print(f"Current balance: {self.balance}")


account = BankAccount()

account.deposit(1000)
account.withdraw(300)
account.withdraw(800) 
>>>>>>> b424a5e40c93cbecb347dcdcda05a113238ded1d
account.show_balance()