# Version 2 of the bank program

# Imports neccesary libraries
import os

# Initialise global variables for account balance and transaction history
balance = 0.0
transaction_history = ""

# Function that handles logins and account creation
def loginMenu():
    choice = input("Would you like to login to an existing account? (y/n): ").strip().lower()
    if choice == "y":
        makeAccount()   # If user doesn't want to log in to an account, make a new one
        return
    elif choice == "n":
        login()         # If user wants to log in to an account, let them
        return
    print("Invalid input. Please pick either 'y' or 'n'.")
    loginMenu()         # If user did not enter y or n, re-enter login menu

def login():
    global float(balance)
    accounts = loadData()
    tries = 5
    exists = False

    name = input("Please enter the name of your account: ")
    for i, line in enumerate(accounts):
        if line.startswith(f"{name}"):
            exists = True
            parts = line.strip().split(", ")
            truePassword = parts[1]     # Finds the password
            balance = parts[-1]         # Enters the balance early
            break

    if exists:
        while True: # If the username exists, enter a loop where the program continuosly asks for a password
            inputPassword = input("Please enter your password: ")
            if inputPassword != truePassword:
                tries -= 1
                print(f"The password you have input is incorrect. You have {tries} tries left.")
            else:
                print("Your password is correct. Login succesful.")
                break
            if tries == 0:
                print("You have entered the wrong password too many times. Returning to login menu...") # NEEDS FIXING
                loginMenu()
    else:
        print("An account with that name does not exist.")
        login()     #If the name is does not exist, try to log in again


# Function to make an account
def makeAccount():
    global balance, transaction_history
    name = input("Please pick a name for your account: ")   # Prompt user for name and password
    password = input("Please pick a password for your account: ")
    balance += 10000.0                          # Add initial funds to balance
    transaction_history = "Deposited 10000.0."  # Records initial transaction
    with open("accounts.txt", "a") as file:
        file.write(f"{name}, {password}, {balance}\n")

# Function that handles the bank menu and its options
def bankMenu():
    choice = None
    while choice != "4":
        print("\n--- Bank Menu ---")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Show Transaction History")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        match choice:   # Handles user's choice using a match case statement
            case "1":
                updateBalance(False)        # Deposit
            case "2":
                updateBalance(True)         # Withdraw
            case "3":
                print(transaction_history)  # Show history
            case "4":
                break   # Exit loop
            case _:
                print("Please enter a valid number.")
    updateData()
    print("Thank you for using the program.")

# Function that handles depositing and withdrawing money from the account
def updateBalance(isWithdraw):
    global balance, transaction_history
    print(f"Your current account balance is {balance}.")
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
        return updateBalance(isWithdraw)  # Retry
    
    # If withdrawing, checks for insufficient balance
    if isWithdraw and balance < money:
        print("Insufficient funds.")
        return updateBalance(isWithdraw)
    
    # Performs the transaction and updates history
    if isWithdraw:
        balance -= money
        transaction_history += f"\nWithdrew {money}."
    else:
        balance += money
        transaction_history += f"\nDeposited {money}."
    print("Transaction complete. Returning to bank menu.")

# Function that updates the user's balance in the file (not currently used in main flow)
def updateData(name, money):
    with open("accounts.txt", "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith(f"{name}"):
            parts = line.strip().split(", ")
            parts[-1] = str(money)  # Updates the balance
            lines[i] = ", ".join(parts)
            break

# Function that loads a user's info from the file
def loadData():
    if not os.path.exists("accounts.txt"):
        with open("accounts.txt", "x") as f:
            pass    # Creates file if it doesn't exist yet
    with open("accounts.txt", "r") as f:
        return f.readlines()

# Entry point for the program
def main():
    loginMenu() # Login or create account
    bankMenu()  # Start bank menu interaction
    
if __name__ == "__main__":
    main()  # Runs the program

#& C:/Users/daniel.sarruf/AppData/Local/Programs/Python/Python312/python.exe C:\Users\daniel.sarruf\Desktop\school_code\assessment_bank\bankSimulator\program.py