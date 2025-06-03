# Version 2 of the bank program

# Imports neccesary libraries
import os

# User class so facilitate containing the information of the person using the program
class User:
    # Initialises values
    def __init__(self, username, password, balance=0.0, history=None):
        self.username = username
        self.password = password
        self.balance = float(balance)
        self.transaction_history = history if history else []   # If there is no transaciton history, use a blank table
    
    # Function that deposits money into the account
    def deposit(self, amount):  
        self.balance += amount
        self.transaction_history.append(f"Deposited {amount}.")
    
    # Function that withdraws money from the account
    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
            return False
        self.balance -= amount
        self.transaction_history.append(f"Withdrew {amount}.")
        return True
    
    # Function that diplays the trnsaction history of the user
    def display_history(self):
        i = 0
        if not self.transaction_history:
            print("No transactions yet.")
        else:
            for entry in self.transaction_history:
                i += 1
                print(f"{i}. {entry}")  # Prints all the entries in a list from 1 to however many entries there are
            print(f"Current balance: {self.balance}")
    
    # Function that saves the users information to the file
    def save_to_file(self):
        lines = []
        if os.path.exists("accounts.txt"):
            with open("accounts.txt", "r") as f:
                lines = f.readlines()

        updated = False
        for i, line in enumerate(lines):
            parts = line.strip().split(", ")
            if parts[0] == self.username:
                history_str = ";".join(self.transaction_history)
                lines[i] = f"{self.username}, {self.password}, {self.balance}, {history_str}\n"
                updated = True
                break

        if not updated:
            history_str = ";".join(self.transaction_history)
            lines.append(f"{self.username}, {self.password}, {self.balance}, {history_str}\n")

        with open("accounts.txt", "w") as f:
            f.writelines(lines)

    # Function that loads the users information from the file
    @staticmethod   # "load_user" doesn't rely on "self", so I declared it as a static method
    def load_user(username):
        if not os.path.exists("accounts.txt"):
            return None
        with open("accounts.txt", "r") as f:
            for line in f:
                parts = line.strip().split(", ")
                if parts[0] == username:
                    password = parts[1]
                    balance = float(parts[2])
                    history = parts[3].split(";") if len(parts) > 3 else []
                    return User(username, password, balance, history)
        return None


# Initialise global variables for account balance and transaction history
balance = 0.0
transaction_history = ""

# Function that handles logins and account creation
def login_menu():
    while True:
        choice = input("Would you like to login to an existing account? (y/n): ").strip().lower()
        if choice == "y":
            return login()  # If user wants to log in to an account, let them
        elif choice == "n":
            return make_account()   # If user doesn't want to log in to an account, make a new one
        else:
            print("Invalid input. Please pick either 'y' or 'n'.")  # If user does not enter y or n, re-enter login menu     

def login():
    while True:
        username = input("Enter your account name (or type 'cancel' to return to menu): ").strip()
        if username == "cancel":
            return login_menu()  # Return to menu
        user = User.load_user(username) # Loads the username
        if not user:
            print("Account not found. Try again.\n")    # If the user does not exist, asks for username again
            continue

        tries = 5
        while tries > 0:
            password = input("Enter your password: ").strip()
            if password == user.password:
                print("Login successful.")  # If the password is right
                return user
            else:
                tries -= 1
                print(f"Incorrect password. {tries} tries remaining.\n")    # If the password is wrong, asks for the password again

        print("Too many failed attempts. Returning to login menu.") # If user fails to enter the password too many times, return to menu
        return login_menu()


# Function to make an account
def make_account():
    username = input("Please pick a username for your account: ").strip()   # Prompt user for name and password
    password = input("Please pick a password for your account: ").strip()
    user = User(username, password)
    user.deposit(10000.0)   # Add initial funds to balance and records initial transaction
    print("Account created with initial deposit of 10000.0")
    user.save_to_file() # Saves the user to the file
    return user

# Function that handles the bank menu and its options
def bank_menu(user):
    choice = None
    while choice != "4":
        print("\n--- Bank Menu ---")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Show Transaction History")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()

        match choice:   # Handles user's choice using a match case statement
            case "1":
                update_balance(user, isWithdraw=False)     # Deposit
            case "2":
                update_balance(user, isWithdraw=True)      # Withdraw
            case "3":
                user.display_history()  # Show history
            case "4":
                user.save_to_file()
                print("Thank you for using the program.")
                break   # Exit loop
            case _:
                print("Please enter a valid number from 1 to 4.")

# Function that handles depositing and withdrawing money from the account
def update_balance(user, isWithdraw):
    print(f"Your current account balance is {user.balance}.")
    user_input = input("Please insert how much money you want to move (or type 'cancel' to return to menu): ").strip().lower()

    if user_input == "cancel":
        print("Transaction cancelled. Returning to bank menu.")
        return

    # Tries to convert user input to float and makes sure it's a positive value
    try:
        money = float(user_input)
        if money <= 0:
            raise ValueError("Amount must be positive.")
    except ValueError:
        print("Invalid input. Please enter a number greater than 0.")
        return update_balance(user, isWithdraw)  # Retry
    
    # If withdrawing, checks for insufficient balance
    if isWithdraw and user.balance < money:
        print("Insufficient funds.")
        return update_balance(user, isWithdraw)  # Retry
    
    # Performs the transaction and updates history
    if isWithdraw:
        if user.withdraw(money):
            print("Withdrawal successful.")
    else:
        user.deposit(money)
        print("Deposit successful.")

# Entry point for the program
def main():
    user = login_menu() # Login or create account
    bank_menu(user)  # Start bank menu interaction
    
if __name__ == "__main__":
    main()  # Runs the program

#& C:/Users/daniel.sarruf/AppData/Local/Programs/Python/Python312/python.exe C:\Users\daniel.sarruf\Desktop\school_code\assessment_bank\bankSimulator\program.py