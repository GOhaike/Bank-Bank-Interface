## BANK ATM USER INTERFACE PROGRAM USING PYTHON

### PROBLEM STATEMENT

The aim of this project is to simulate a Bank ATM user interface relationship using the power of the object oriented Programming that runs on command line interface in Python3.

### Program features:
This program is intended for high-level applications to give an insight on banking system with some of the key features listed below:

- Create an account(checking/savings) and password that meets criteria, this information would be stored  using pickle to keep   a memory of your login details so you don't have yto create new account anytime you logout. (Please ensure you meet the     password criteria eg AAaa#11 to proceed)

- Login - If more than 3 attempts, your account would be frozen for security reasons

- View account information and transactions with timestamps 

- Withdraw/Deposit - You're only allowed for maximum of 3 withdrawals from your savings account - If there is an emergency/errors, we have a counter to reset your savings account.

- Transfer between accounts- This is limited to work between checking and savings accounts.

### How to run this code
This code runs on the command line interface, you would need to have python3 installed on your computer with your favorite text editor. Then proceed with the steps below

1. Open a command line bash/terminal

2. Choose a directory 
  pwd -to check the present working directory
  cd Desktop - to change directory to desktop
  
3. `git clone https://github.com/GOhaike/bank-atm-Interface.git`
   Wait till you see the folder on your desktop
   
4. Change directory to the path eg cd Desktop/bank-atm-Interface
    type ls to see the file contents
5. Type - `python3 bank_atm_interface.py` to run the code.
