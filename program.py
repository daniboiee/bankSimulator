# Version 1 of the bank program

balance = 0.0
transaction_history = ""

# Function to make an account
def makeAccount():
    balance += 10000.0
    transaction_history = "Deposited 10000."

def bankMenu():
    choice = None
    while choice != "4":
        print("\n--- Bank Menu ---")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Show Transaction History")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")
        match choice:
            case "1":
                updateBalance(False)
            case "2":
                updateBalance(True)
            case "3":
                print(transaction_history)
            case "4":
                break
            case _:
    print("Thank you for using the program.")

def updateBalance(isWithdraw):
    print(f"Your current account balance is {balance}.")
    money = input("Please insert how much money you want to move: ")
    if type(money) not in (int, float) or (isWithdraw and balance < money): # Checks if the insert value is valid
        print("What you input is invalid. Please try again.")
        updateBalance(isWithdraw)

    if isWithdraw:
        balance -= money
        transaction_history += f"\nWithdrew {int(money)}."
    else:
        balance += money
        transaction_history += f"\nDeposited {int(money)}."


def main():
    makeAccount()
    bankMenu()
    

main()

#& C:/Users/daniel.sarruf/AppData/Local/Programs/Python/Python312/python.exe C:\Users\daniel.sarruf\Desktop\school_code\assessment_bank\bankSimulator\program.py