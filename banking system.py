import pickle
import os

# Custom exception classes
class InsufficientBalanceError(Exception):
    pass

class AccountNotFoundError(Exception):
    pass

class InvalidAmountError(Exception):
    pass

# BankAccount class to manage customer accounts
class BankAccount:
    account_counter = 1000  # Starting point for unique account numbers

    def __init__(self, name, initial_deposit):
        if initial_deposit < 0:
            raise InvalidAmountError("Initial deposit cannot be negative.")
        
        self.account_number = BankAccount.account_counter
        BankAccount.account_counter += 1
        self.name = name
        self.balance = initial_deposit

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be greater than zero.")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be greater than zero.")
        if amount > self.balance:
            raise InsufficientBalanceError("Insufficient funds.")
        self.balance -= amount

    def get_balance(self):
        return self.balance

    def __str__(self):
        return f"Account Number: {self.account_number}, Name: {self.name}, Balance: ${self.balance:.2f}"

# Bank system to manage accounts
class BankSystem:
    def __init__(self, filename='bank_data.pkl'):
        self.filename = filename
        self.accounts = self.load_accounts()

    def save_accounts(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.accounts, file)

    def load_accounts(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as file:
                return pickle.load(file)
        return {}

    def create_account(self, name, initial_deposit):
        account = BankAccount(name, initial_deposit)
        self.accounts[account.account_number] = account
        self.save_accounts()
        return account.account_number

    def deposit(self, account_number, amount):
        if account_number not in self.accounts:
            raise AccountNotFoundError("Account number not found.")
        self.accounts[account_number].deposit(amount)
        self.save_accounts()

    def withdraw(self, account_number, amount):
        if account_number not in self.accounts:
            raise AccountNotFoundError("Account number not found.")
        self.accounts[account_number].withdraw(amount)
        self.save_accounts()

    def check_balance(self, account_number):
        if account_number not in self.accounts:
            raise AccountNotFoundError("Account number not found.")
        return self.accounts[account_number].get_balance()

    def display_account(self, account_number):
        if account_number not in self.accounts:
            raise AccountNotFoundError("Account number not found.")
        return str(self.accounts[account_number])

# Main function to interact with the banking system
def main():
    bank = BankSystem()

    while True:
        print("\n===== BANKING SYSTEM MENU =====")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Show Account Details")
        print("6. Exit")
        
        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                name = input("Enter account holder's name: ")
                deposit = float(input("Enter initial deposit amount: "))
                account_number = bank.create_account(name, deposit)
                print(f"Account created successfully! Your account number is: {account_number}")

            elif choice == '2':
                acc_num = int(input("Enter account number: "))
                amount = float(input("Enter amount to deposit: "))
                bank.deposit(acc_num, amount)
                print("Deposit successful.")

            elif choice == '3':
                acc_num = int(input("Enter account number: "))
                amount = float(input("Enter amount to withdraw: "))
                bank.withdraw(acc_num, amount)
                print("Withdrawal successful.")

            elif choice == '4':
                acc_num = int(input("Enter account number: "))
                balance = bank.check_balance(acc_num)
                print(f"Current balance: ${balance:.2f}")

            elif choice == '5':
                acc_num = int(input("Enter account number: "))
                print(bank.display_account(acc_num))

            elif choice == '6':
                print("Thank you for using our banking system!")
                break

            else:
                print("Invalid choice. Please try again.")

        except ValueError:
            print("Invalid input. Please enter valid details.")
        except AccountNotFoundError as e:
            print(e)
        except InsufficientBalanceError as e:
            print(e)
        except InvalidAmountError as e:
            print(e)

if __name__ == "__main__":
    main()
