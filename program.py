# Version 3 of the bank program

# Imports neccesary libraries
import os
import tkinter as tk
from tkinter import messagebox

# User class so facilitate containing the information of the person using the program
class User:
    # Initialises values
    def __init__(self, username, password, balance=0.0, history=None):
        self.username = username
        self.password = password
        self.balance = float(balance)
        self.transaction_history = history if history else []   # If there is no transaction history, use a blank table
    
    # Function that deposits money into the account
    def deposit(self, amount):  
        self.balance += amount
        self.transaction_history.append(f"Deposited {amount}.")
    
    # Function that withdraws money from the account
    def withdraw(self, amount):
        self.balance -= amount
        self.transaction_history.append(f"Withdrew {amount}.")
        return True
    
    # Function that diplays the trnsaction history of the user
    def display_history(self):
        history = "\n".join(self.transaction_history)
        messagebox.showinfo("History", f"{history}\n\nBalance: {self.balance}")

    # Function that saves the users information to the file
    def save_to_file(self):
        lines = []
        if os.path.exists("accounts.txt"):
            with open("accounts.txt", "r") as f:
                lines = f.readlines()

        updated = False
        for i, line in enumerate(lines):    # If accounts.txt does not exist, lines is empty, and this does not run
            parts = line.strip().split(", ")
            if parts[0] == self.username:   # If the username is already in accounts, basically edits it
                history_str = ";".join(self.transaction_history)
                lines[i] = f"{self.username}, {self.password}, {self.balance}, {history_str}\n"
                updated = True
                break   # Quits for loop early once username is found.

        if not updated:     # If accounts.txt does not exist or the username is new, basically creates the account within the file
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

# -------------------- GUI app starts here --------------------

class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()  # Basically makes self.tk exist and allows methods relying on it to work without breaking
        self.title("Bank Program")  # Sets starting title and geometry
        self.geometry("600x400")
        self.user = None
        self.switch_frame(LoginFrame)   # Switches to the login frame  as soon as possible

    def switch_frame(self, frame_class):    # Function that destroys the current frame and replaces it with a new one
        new_frame = frame_class(self) if callable(frame_class) else frame_class(self)  # Properly instantiate frame with `self` as master
        if hasattr(self, '_frame'):
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)  # Replaces with a new frame right after destruction

# First frame
class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)    # Calls the tk.Frame constructor
        tk.Label(self, text="Username").pack()  # Sets up username label
        self.username = tk.Entry(self)
        self.username.pack()

        tk.Label(self, text="Password").pack()  # Sets up password label
        self.password = tk.Entry(self, show="*")
        self.password.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=5)      # Buttons to progress the program
        tk.Button(self, text="Create Account", command=lambda: master.switch_frame(RegisterFrame)).pack()

    def login(self):
        user = User.load_user(self.username.get().strip())
        if user and user.password == self.password.get().strip():   # If the user exists and the password is the same
            self.master.user = user
            messagebox.showinfo("Login", "Login successful!")   # Informs user that the login was a success
            self.master.switch_frame(BankMenuFrame)
        else:
            messagebox.showerror("Error", "Invalid username or password.")  # Informs user that the login was unsuccessful

# Second frame
class RegisterFrame(tk.Frame):
    def __init__(self, master): 
        super().__init__(master)    # Calls the tk.Frame constructor
        tk.Label(self, text="Choose Username").pack()
        self.username = tk.Entry(self)
        self.username.pack()

        tk.Label(self, text="Choose Password").pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()

        tk.Button(self, text="Create Account", command=self.register).pack(pady=5)
        tk.Button(self, text="Back to Login", command=lambda: master.switch_frame(LoginFrame)).pack()
    
    def register(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return

        if User.load_user(username):
            messagebox.showerror("Error", "Username already exists.")
            return

        new_user = User(username, password)
        new_user.deposit(10000.0)
        new_user.save_to_file()
        messagebox.showinfo("Success", "Account created successfully!")
        self.master.switch_frame(LoginFrame)


# Third frame
class BankMenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)    # Calls the tk.Frame constructor
        user = master.user
        self.balance_label = tk.Label(self, text=f"Balance: ${user.balance:.2f}")
        self.balance_label.pack(pady=5)

        tk.Label(self, text=f"Welcome, {user.username}").pack(pady=10)

        tk.Button(self, text="Deposit", command=lambda: master.switch_frame(lambda m: TransactionFrame(m, False))).pack(pady=2)
        tk.Button(self, text="Withdraw", command=lambda: master.switch_frame(lambda m: TransactionFrame(m, True))).pack(pady=2)

        tk.Button(self, text="Show Transaction History", command=self.show_history).pack(pady=2)
        tk.Button(self, text="Logout", command=self.logout).pack(pady=2)

    def show_history(self):
        history = "\n".join(self.master.user.transaction_history)
        balance = self.master.user.balance
        messagebox.showinfo("Transaction History", f"{history}\n\nBalance: {balance}")

    def logout(self):
        self.master.user.save_to_file()
        self.master.user = None
        self.master.switch_frame(LoginFrame)

# Fourth frame
class TransactionFrame(tk.Frame):
    def __init__(self, master, is_withdraw):
        super().__init__(master)
        self.master = master
        self.is_withdraw = is_withdraw
        action = "Withdraw" if is_withdraw else "Deposit"

        tk.Label(self, text=f"{action} Amount").pack()
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack()

        tk.Button(self, text=action, command=self.do_transaction).pack(pady=5)
        tk.Button(self, text="Back", command=lambda: master.switch_frame(BankMenuFrame)).pack()
    
    def do_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number.")
            return

        user = self.master.user
        if self.is_withdraw:
            if user.balance < amount:
                messagebox.showerror("Error", "Insufficient funds.")
                return
            user.withdraw(amount)
            messagebox.showinfo("Success", f"Withdrew {amount}")
        else:
            user.deposit(amount)
            messagebox.showinfo("Success", f"Deposited {amount}")

        self.master.switch_frame(BankMenuFrame)

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
            messagebox.showerror("Invalid input.", "Please pick either 'y' or 'n'.")    # If user does not enter y or n, loops     

def login():
    while True:
        username = input("Enter your account name (or type 'cancel' to return to menu): ").strip()
        if username == "cancel":
            return login_menu()  # Return to menu
        user = User.load_user(username) # Loads the username
        if not user:
            messagebox.showerror("Account not found.", "Anaccount with this username does not exist. Try again.\n")     # If the user does not exist, asks for username again
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
            raise ValueError()
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a number greater than 0.")
        return update_balance(user, isWithdraw)  # Retry
    
    # If withdrawing, checks for insufficient balance
    if isWithdraw and user.balance < money:
        messagebox.showerror("Error", "Insufficient funds.")
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

def start_gui():
    app = BankApp()
    app.mainloop()

if __name__ == "__main__":
    start_gui()  # Runs the program

#& C:/Users/daniel.sarruf/AppData/Local/Programs/Python/Python312/python.exe C:\Users\daniel.sarruf\Desktop\school_code\assessment_bank\bankSimulator\program.py