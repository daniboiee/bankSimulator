# Version 1 of the bank program

balance = 0.0
transaction_history = ""

# Function to make an account
def makeAccount():
    global balance, transaction_history
    balance += 10000.0
    transaction_history = "Deposited 10000.0"

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
                print("Please enter a valid number.")
    print("Thank you for using the program.")

def updateBalance(isWithdraw):
    global balance, transaction_history
    print(f"Your current account balance is {balance}.")

    try:
        money = float(input("Please insert how much money you want to move: "))
        if money <= 0:
            raise ValueError("Amount must be positive.")
    except ValueError:
        print("Invalid input. Please enter a number greater than 0.")
        return updateBalance(isWithdraw)

    if isWithdraw and balance < money:
        print("Insufficient funds.")
        return updateBalance(isWithdraw)

    if isWithdraw:
        balance -= money
        transaction_history += f"\nWithdrew {money}."
    else:
        balance += money
        transaction_history += f"\nDeposited {money}."
    print("Transaction complete. Returning to bank menu.")


def main():
    makeAccount()
    bankMenu()
    

main()

#& C:/Users/daniel.sarruf/AppData/Local/Programs/Python/Python312/python.exe C:\Users\daniel.sarruf\Desktop\school_code\assessment_bank\bankSimulator\program.py