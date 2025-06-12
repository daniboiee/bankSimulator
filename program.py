# Version 3 of the bank program

# Imports neccesary libraries
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# A base frame class that contains helper methods for UI consistency (convenience)
class ThemedFrame(ttk.Frame):
    # Creates a label and entry pair and returns the Entry widget
    def labeled_entry(self, label_text, **entry_kwargs):
        ttk.Label(self, text=label_text).pack(pady=2)
        entry = ttk.Entry(self, **entry_kwargs)     # entry_kwargs allows passing extra keyword args such as show="*", avoiding hardcoding
        entry.pack(pady=2, fill="x")
        return entry

# Function that resizes the current frame 
def smooth_resize(window, target_width, target_height, steps=10, delay=20):
    current_width = window.winfo_width()
    current_height = window.winfo_height()

    delta_w = (target_width - current_width) / steps
    delta_h = (target_height - current_height) / steps

    def step(i=0):
        if i < steps:
            new_w = int(current_width + delta_w * i)
            new_h = int(current_height + delta_h * i)
            window.geometry(f"{new_w}x{new_h}")
            window.after(delay, lambda: step(i + 1))
        else:
            window.geometry(f"{target_width}x{target_height}")  # Snap to final when all steps are done

    step()

# User class to facilitate containing the information of the person using the program
class User:
    # Initialises values
    def __init__(self, username, password, balance=0.0, history=None, dark_mode=False):
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
        history_str = ";".join(self.transaction_history)

        lines = []
        if os.path.exists("accounts.txt"):
            with open("accounts.txt", "r") as f:
                lines = f.readlines()

        updated = False
        for i, line in enumerate(lines):    # If accounts.txt does not exist, lines is empty, and this does not run
            parts = line.strip().split(", ")
            if parts[0] == self.username:   # If the username is already in accounts, basically edits it
                lines[i] = f"{self.username}, {self.password}, {self.balance}, {history_str}\n"
                updated = True
                break   # Quits for loop early once username is found.

        if not updated:     # If accounts.txt does not exist or the username is new, basically creates the account within the file
            lines.append(f"{self.username}, {self.password}, {self.balance}, {history_str}\n")

        with open("accounts.txt", "w") as f:
            f.writelines(lines)

    # Function that loads the users information from the file
    @staticmethod   # "load_user" doesn't rely on "self", so I declared it as a static method
    def load_user(username):
        if not os.path.exists("accounts.txt"):  # If the file doesn't exist, there's no user to load, so return None
            return None
        with open("accounts.txt", "r") as f:    # Opens the accounts file and searches for the user line-by-line
            for line in f:
                parts = line.strip().split(", ")
                if parts[0] == username:    # If the username matches, extracts and converts the data
                    password = parts[1]
                    balance = float(parts[2])
                    history = parts[3].split(";") if len(parts) > 3 else []
                    return User(username, password, balance, history)   # Returns a new User instance with the extracted data
        return None # If no match is found, also returns None

# -------------------- GUI part starts here --------------------

def configure_styles(style: ttk.Style, theme: str):
    style.theme_use("clam")
    if theme == "dark":     # Apply dark theme to all ttk widgets
        style.configure("TFrame", background="#2e2e2e")
        style.configure("TLabel", background="#2e2e2e", foreground="white")
        style.configure("TButton", background="#333333", foreground="white")
        style.configure("TEntry",  fieldbackground="#333333", foreground="white")
    else:   # Light theme
        style.configure("TFrame", background="SystemButtonFace")
        style.configure("TLabel", background="SystemButtonFace", foreground="black")
        style.configure("TButton", background="SystemButtonFace", foreground="black")
        style.configure("TEntry",  fieldbackground="white", foreground="black")

# Main application class that manages the GUI and frame switches
class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()  # Basically makes self.tk exist and allows methods relying on it to work without breaking
        self.title("Bank")  # Sets starting title, but does not set a starting geometry, as this is done within the frames individually
        self.user = None

        self.style = ttk.Style()
        self.theme = "light"    # Start with light theme
        self.apply_theme()

        self.switch_frame(LoginFrame)   # Switches to the login frame as soon as possible

    # Function that sets the theme of the program
    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"   # Toggles the general theme as a fallback
        self.apply_theme()

    # Function that applies the theme of the program
    def apply_theme(self):
        bg = "#2e2e2e" if self.theme == "dark" else "SystemButtonFace"
        self.configure(bg=bg)
        # Delegates all the ttk styling
        configure_styles(self.style, self.theme)

        # Re-apply background on the current frame and its children
        if hasattr(self, "_frame"):
            self._frame.configure(bg=bg)
            for w in self._frame.winfo_children():
                # Only tk widgets will accept bg; ttk ones use style
                try:
                    w.configure(background=bg)
                except tk.TclError:
                    pass

    # Function that destroys the current frame and replaces it with a new one
    def switch_frame(self, frame_class):
        new_frame = frame_class(self) if callable(frame_class) else frame_class(self)  # Properly instantiate frame with "self" as master
        if hasattr(self, '_frame'):
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)  # Replaces with a new frame right after destruction

# First frame, handles logging into an account
class LoginFrame(ThemedFrame):
    def __init__(self, master):
        super().__init__(master)    # Calls the tk.Frame constructor so ThemedFrame works
        smooth_resize(self.master, 220, 220)    # Resizes window
        self.username = self.labeled_entry("Username")      # Sets up username label
        self.password = self.labeled_entry("Password", show="*")    # Sets up password label, hiding the actual password behind "*"s

        ttk.Button(self, text="Login", command=self.login).pack(pady=5)      # Buttons to progress the program
        ttk.Button(self, text="Create Account", command=lambda: master.switch_frame(RegisterFrame)).pack()
        ttk.Button(self, text="Toggle Dark Mode", command=master.toggle_theme).pack(pady=10)


    def login(self):
        user = User.load_user(self.username.get().strip())
        if user and user.password == self.password.get().strip():   # If the user exists and the password is the same
            self.master.user = user
            messagebox.showinfo("Login", "Login successful!")   # Informs user that the login was a success
            self.master.switch_frame(BankMenuFrame)
        else:
            messagebox.showerror("Error", "Invalid username or password.")  # Informs user that the login was unsuccessful

# Second frame, handles registering new accounts
class RegisterFrame(ThemedFrame):
    def __init__(self, master): 
        super().__init__(master)    # Calls the tk.Frame constructor again
        smooth_resize(self.master, 220, 180)    # Resizes window to something else
        self.username = self.labeled_entry("Choose Username")
        self.password = self.labeled_entry("Choose Password", show="*")

        ttk.Button(self, text="Create Account", command=self.register).pack(pady=5)
        ttk.Button(self, text="Back to Login", command=lambda: master.switch_frame(LoginFrame)).pack()
    
    def register(self):
        username = self.username.get().strip()  # Gets user input
        password = self.password.get().strip()

        if not username or not password:    # Validates user input to make sure no fields are empty
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return

        if User.load_user(username):    # Checks if the username already exists in the file
            messagebox.showerror("Error", "Username already exists.")
            return

        new_user = User(username, password) # Creates a new user with the given credentials
        new_user.deposit(10000.0)           # Gives the new user some sarting balance
        new_user.save_to_file()             # Saves the new user's data to the file 
        messagebox.showinfo("Success", "Account created successfully!")
        self.master.user = new_user # Log the new user in
        self.master.switch_frame(BankMenuFrame) # Switch to the main bank menu screen

# Third frame, handles most of the user's actions
class BankMenuFrame(ThemedFrame):
    def __init__(self, master):
        super().__init__(master)    # Calls the tk.Frame constructor
        smooth_resize(self.master, 220, 262)    # Weirdly specific height to make up for the padding 
        user = master.user
        self.balance_label = ttk.Label(self, text=f"Balance: ${user.balance:.2f}")
        self.balance_label.pack(pady=5)

        ttk.Label(self, text=f"Welcome, {user.username}").pack(pady=10)

        ttk.Button(self, text="Deposit", command=lambda: master.switch_frame(lambda m: TransactionFrame(m, False))).pack(pady=2)
        ttk.Button(self, text="Withdraw", command=lambda: master.switch_frame(lambda m: TransactionFrame(m, True))).pack(pady=2)

        ttk.Button(self, text="Show Transaction History", command=self.show_history).pack(pady=2)
        ttk.Button(self, text="Logout", command=self.logout).pack(pady=2)
        ttk.Button(self, text="Toggle Dark Mode", command=master.toggle_theme).pack(pady=10)


    def show_history(self):
        history = "\n".join(self.master.user.transaction_history)   # Retrieves the transaction historyand balance of the current user
        balance = self.master.user.balance
        messagebox.showinfo("Transaction History", f"{history}\n\nBalance: {balance}")  # Displays history and balance in a message box

    def logout(self):
        self.master.user.save_to_file()         # Saves current user's data to the file before logging out
        self.master.user = None                 # Clears the user session
        self.master.switch_frame(LoginFrame)    # Returns to the login screen

# Fourth frame, handles deposits and withdrawals
class TransactionFrame(ThemedFrame):
    def __init__(self, master, is_withdraw):
        super().__init__(master)
        smooth_resize(self.master, 220, 130)    # Smaller window for a more compact UI
        self.master = master
        self.is_withdraw = is_withdraw
        action = "Withdraw" if is_withdraw else "Deposit"   # Label changes based on transaction type

        self.amount_entry = self.labeled_entry(f"{action} Amount")  # Input field is labeled appropriately based on transaction type too

        ttk.Button(self, text=action, command=self.do_transaction).pack(pady=5)
        ttk.Button(self, text="Back", command=lambda: master.switch_frame(BankMenuFrame)).pack()
    
    def do_transaction(self):
        try:    # Tries to convert the entered amount to a valid float
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError()
        except ValueError:  # If the input is invalid, shows an error and returns
            messagebox.showerror("Error", "Please enter a valid positive number.")
            return

        user = self.master.user
        if self.is_withdraw:
            if user.balance < amount:   # If withdrawing, checks if the user has sufficient balance first
                messagebox.showerror("Error", "Insufficient funds.")
                return
            user.withdraw(amount)   # Performs withdrawal and confirms success
            messagebox.showinfo("Success", f"Withdrew {amount}")
        else:
            user.deposit(amount)    # Performs deposit and confirms success
            messagebox.showinfo("Success", f"Deposited {amount}")

        self.master.switch_frame(BankMenuFrame)     # After transaction, returns to the main menu

def start_gui():
    app = BankApp()
    app.mainloop()

if __name__ == "__main__":
    start_gui()  # Runs the program

#& C:/Users/daniel.sarruf/AppData/Local/Programs/Python/Python312/python.exe C:\Users\daniel.sarruf\Desktop\school_code\assessment_bank\bankSimulator\program.py