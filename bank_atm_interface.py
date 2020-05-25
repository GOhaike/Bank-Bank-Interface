import re
import sys
import time
import datetime

import pickle

class Bank:
    """ Returns bank. Bank enables you open a new account and delete account"""

  #initialize dictionary and assign a reference to enable you store and retrieve account
    def __init__(self):
        self.bank_account ={}
        self.frozen_account = {}

    def create_account(self, name, pin):
        """Create new account. Returns True on success or False if the name already
           has an account.
        """
        if name in self.bank_account.keys():
            return False
        else:
            account = Account(name, pin)
            self.bank_account[name] = account
            return True

    def delete_account(self, name):
        """Delete or close account"""
        del self.bank_account[name]

    def freeze_account(self, name):
        """Freeze the named account.
           Return True on success False on failure.
        """
        if name in self.bank_account:
            self.frozen_account[name] = self.bank_account[name]
            del self.bank_account[name]
            return True
        else:
            return False

    def checking_withdraw(self, name, amount):
        """Withdraw from checking. Returns True on success False on failure."""
        account = self.bank_account[name]
        if account.checking_balance < amount:
            print ('You Insufficient balance in checking account.')
            return False
        else:
            account.checking_balance -= amount
            print("Thank you for banking with us, your new checking balance is: {}".format(account.checking_balance))
            return True

    def savings_withdraw(self,name,amount):
        "Withdraw money from savings account. Return True on success False on failure."
        maximum_withdraw = 3
        account = self.bank_account[name]
        if account.counter == maximum_withdraw:
            print("Sorry!Maximum limit for this month reached")
            return False
        elif account.savings_balance < amount:
            print('You have insufficient balance in your savings account')
            return False
        else:
            account.savings_balance -= amount
            account.counter +=1
            print("Thank you for banking with us, your new savings balance is: {}".format(account.savings_balance))
            return True

    def reset_counter(self, name):
        self.bank_account[name].counter =0

    def get_savings_balance(self, name):
        return self.bank_account[name].savings_balance

    def get_checking_balance(self, name):
        return self.bank_account[name].checking_balance

    def deposit_savings(self, name, amount):
        """Deposit to savings. Return True on success or False on failure."""
        self.bank_account[name].savings_balance += amount
        return True

    def deposit_checking(self, name, amount):
        """Deposit to checking. Return True on success or False on failure."""
        self.bank_account[name].checking_balance += amount
        return True

    def validate_login(self, name, pin):
        """ validate during login and confirm from the bank that the customer exist"""
        if name in self.bank_account:
            if pin == self.bank_account[name].pin:
                return True
            else:
                print("Incorrect name or pin: Please enter the correct pin to proceed")
        elif name in self.frozen_account:
            print("Sorry, your account has been frozen due to suspected terrorist activity.")
            return False
        else:
            print("Sorry!, account does not exist")
            return False

    def new_pin(self):
        """Get the user to input a new valid PIN. Returns the new PIN if successful,
           None otherewise.
        """
        count=0
        while True:
            pin = input("Enter a PIN to use with this account" "\n"
                         + "Conditions for a valid password are:" "\n"
                         + "Should have at least one number" "\n"
                         + "Should have at least one uppercase and one lowercase character." "\n"
                         + "Should have at least one special symbol." "\n"
                         + "Should be between 6 to 20 characters long.")
            reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"

            comp = re.compile(reg) # compiling regular expression
            match_pin = re.search(comp,pin)  # searching regular expression
            if match_pin!=None:
                print("Successful!, please remember to keep your pin secured, we'll never ask for your pin")
                return pin
                break
            else:
                count=count+1
                print("Sorry! Pin did not meet requirements, please review the criteria and try again")

                print("You have {} trials left:".format(5-count))
                if(count==5):
                    print("Too many tries: PIN entry attempt aborted.")
                    return None

    def pin_check(self,name):
        """prompt user for password and return counts. After three incorrect password,account is blocked"""
        attempts = 3
        while attempts > 0:
            pin = input("Please enter your password to continue with the transaction:" + "\n")
            if pin == self.bank_account[name].pin:
                return True
            else:
                attempts -= 1
                print ("{} more attempt(s) remaining".format(attempts))
        #Block account
        assert self.freeze_account(name)
        return False

class Account:
    """Class for each person's bank accounts. Stores:
          pin: password
          checking_balance
          savings_balance
          counter: Savings withdrawal counter.
    """
    def __init__(self, name, pin, checking_balance = 0, savings_balance = 0):
        self.pin = pin
        self.checking_balance = checking_balance
        self.savings_balance = savings_balance
        self.counter = 0 #Savings withdrawal counter starts at 0 for new accounts

class ATM:
    """ An ATM for user interactions """

    def __init__(self, bank):
        """Initialize an ATM bound to the given bank"""
        self.bank = bank

    def create_account(self,name,pin):
        return self.bank.create_account(name,pin)

      #show checking once user is logged in!
    def show_checking(self,name):
        date = datetime.date.today().strftime('%d-%B-%Y')
        print("Your checking account bal. as at {} is {}".format(date,self.bank.get_checking_balance(name)))

         #show savings once user is logged in!
    def show_savings(self,name):
        date = datetime.date.today().strftime('%d-%B-%Y')
        print("Your savings account bal. as at {} is {}".format(date,self.bank.get_savings_balance(name)))

          #only when you logged in can you delete the account. If not, must raise error!
    def delete(self, name):
        return self.bank.delete_account(name)

        # if pin fails, it will give three trials and block if not correct
    def login(self, name, pin):
        return self.bank.validate_login(name, pin)

    def deposit_savings(self,name, amount):
        return self.bank.deposit_savings(name, amount)

    def deposit_checking(self, name,amount):
        return self.bank.deposit_checking(name, amount)

    def withdraw_saving(self, name, amount):
        ret = self.bank.savings_withdraw(name, amount)
        self.show_savings(name)
        return ret

    def withdraw_checking(self,name,amount):
        ret = self.bank.checking_withdraw(name, amount)
        self.show_checking(name)
        return ret

        #confirm login pin and blocked user afer attempting password mor than 3 times
    def pin_security(self,name):
        return self.bank.pin_check(name)

        #Use to ensure that password requirements are met
    def create_new_pin(self,name):
        return self.bank.new_pin()

        #User interface to perform account functions
    def interface(self, name):
        while True:
            print("Welcome back {}!".format(name))
            action= input("What would you like to do today? :" + "\n"
                  + "Deposit          press, :d" + "\n"
                  + "Withdraw         press  :w" + "\n"
                  + "Tranfer          press  :t" + "\n"
                  + "Account balance  press  :s" + "\n"
                  + "Delete account   press  :q" + "\n"
                  + "Exit             press  :e "+ "\n"
                  + "View all accounts press :v " + "\n"
                  + "Reset savings withdrawal counter :r " + "\n"
                  ).lower()

            if action in "dwqsetvr":
                if action == "d":
                    account_type =input("Please select :\n.1 for checking Account\n.2 For savings Account:")
                    amount = float(input("How much would you like to deposit: "))
                    if account_type=="1":
                        self.deposit_checking(name,amount)
                        print("Successfully deposited ${:.2f} into your checking account.".format(amount))

                    elif account_type == "2":
                        self.deposit_savings(name,amount)
                        print("You have successfully deposited ${:.2f} into your savings account.".format(amount))
                    else:
                        print("Wrong selection: Please select the correct account type")

                elif action == "w":
                    account_type =input("Please select :1 for checking Acount :2 for saving Account")
                    amount = float(input("How much would you like to withdrawal: "))
                    if account_type == "1":
                        if self.withdraw_checking(name, amount):
                            print("You withdraw: ${:.2f} from your checking account.".format(amount))

                    elif account_type =="2":
                        if self.withdraw_saving(name, amount):
                            print("You withdraw: ${:.2f} from your savings account.".format(amount))
                    else:
                        print("Wrong selection: Please select correct account type")

                elif action == "s":
                    self.show_savings(name)
                    self.show_checking(name)

                elif action == "q":
                    print("YOU ARE DELETING YOUR ACCOUNT")
                    confirm = input("  Type 'yes' to continue. ").lower()
                    if confirm == "yes":
                        print("Deleting acount ...")
                        self.delete(name)
                        break

                    #Transfers between accounts
                elif action == "t":
                    print("1.From checking account TO saving account\n2.From Saving account  checking account")
                    ch = input("choice 1 or 2:")
                    if ch=="1":
                        amount=float(input("amount to withraw from checking account:"))
                        if self.withdraw_checking(name,amount):
                            #Deposit must succeed!!
                            assert self.deposit_savings(name,amount)
                        else:
                            print("Transfer failed.")
                        print(" ")
                        self.show_checking(name)
                        self.show_savings(name)
                    elif ch=="2":
                        amount=float(input("amount to withraw from saving account:"))
                        if self.withdraw_saving(name,amount):
                            #Deposit must succeed!!
                            assert self.deposit_checking(name,amount)
                        else:
                            print("Transfer failed.")
                        print(" ")
                        self.show_savings(name)
                        self.show_checking(name)
                    else:
                        #Invalid options

                        print("You have entered invalid transfer options")

                elif action == 'v':
                    print("Active accounts:")
                    for a_name, acct in self.bank.bank_account.items():
                        print("     Name: {}   PIN: {}  Savings: {}   Checking: {}".format(
                              a_name, acct.pin, acct.savings_balance, acct.checking_balance)
                             )
                    print("Frozen accounts:")
                    for a_name, acct in self.bank.frozen_account.items():
                        print("    Name: {}   PIN: {}  Savings: {}   Checking: {}".format(
                              a_name, acct.pin, acct.savings_balance, acct.checking_balance)
                             )
                    print("\n")
                    
                elif action == 'r':
                    self.bank.reset_counter(name)
                    print("Savings withdrawal counter reset! Get your money now!")
                    
                elif action == "e":
                    print("Exiting ...")
                    print('Thank you {} for banking with us. See you soon!'.format(name))
                    break

def main():
    """Retain method to interact with user"""
    
    #Try to find saved bank info.
    file_name = "bank.pkl"
    try:
      with open(file_name, "rb") as f:
        bank = pickle.load(f)
    except:
      bank = Bank()

    atm = ATM(bank)
    print("Welcome to the ATM machine!")
    while True:
        prompt= input("Please enter a command:"   + "\n"
                  + "Log in              press l" + "\n"
                  + "Create new account  press c" + "\n"
                  + "Exit                press e" + "\n"
                  + "Help                press h" + "\n"
                  ).lower()

        #helps user to go back to the menu
        if prompt == "h":
            print("For:" + "\n"
                + "Log in,        ----> l" +  "\n"
                + "Create account ----> c" + "\n"
                + "Exit           ----> e" + "\n")

        elif prompt == 'c':
            while True:
                name = input("Enter your name: ").capitalize()
                if name in atm.bank.bank_account:
                    #Give user chance to login or try to create account with different name
                    print("Account with name {} already exists!".format(name))
                    question = input("Are you an ACCOUNT holder?: y/n").lower()
                    if question == "y":
                        #User already has account, get pin and log him in.
                        pin = input("Enter your PIN: ")
                        if (atm.login(name,pin)== True):
                            atm.interface(name)
                            #This would take the user back and give him option to login or exit
                            break

                    elif question == "n":
                        #User does not have account, try again with different name
                        print("Please try creating your account with a different name.")
                    else:
                        #Invalid option.
                        print("That was not one of the choices, choose :y/n to continue ")

                else:
                    #Get user to enter a valid PIN and create the new account
                    pin = atm.create_new_pin(name)
                    if pin is not None:
                        result = atm.create_account(name, pin)
                        if result:
                            #Yes! user has successfully created a new account and he would have to login to continue
                            print("Account successfully created!")
                            break

                        else:
                            #Oops ! Account creation failed.
                            print("Account creation failed for unknown reason.")
                            #Let's give him another chance to try again
                            again = input("Would you like to try again? y/n: ").lower()
                            if again == "y":
                                atm.pin_security(name)
                            #go back to start of loop
                            else:
                                #The user is probably frustated and have decided to quit.
                                print("Thank you and good bye!")
                                break
                                #sys.exit()

        elif prompt== 'l':
            name = input("Enter your name: ").capitalize()
            pin = input("Enter your pin: ")

            # Try to login. This can fail if the credentials are wrong or the account
            #   is frozen.`
            if(atm.login(name, pin)==True):
                atm.interface(name)
            elif name in atm.bank.frozen_account:
                print("Please contact the bank for assistence.")
            else:
                login_question = input("Login details does not exist, would you wish to try again?: y/n").lower()
                if login_question == "y":
                    name = input("Enter your name again: ").capitalize()
                    if name in atm.bank.bank_account:
                        if atm.pin_security(name) == True:
                            print("Login successful!")
                            atm.interface(name)
                        else:
                            print ("Account has been frozen due to three wrong password attempts," + "\n"
                                    + "Contact your bank if you need assistance.")
                    #Go back to main menu.
                else:
                    print("No action required! Thank and have a nice day")
        elif prompt == 'e':
            break

        else:
            print("Unrecognized choice: '{}'".format(prompt))

    with open(file_name, "wb") as f:
        pickle.dump(bank, f)

main()