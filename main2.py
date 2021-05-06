import logging
import os
import sys
import time

import pandas as pd

from account import Account
from sign_in import SignIn
from sign_up import SignUp
from user import User

# list of all user
users = []
current_object = None


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CGREYBG = '\33[37m'
    RED = '\033[31m'
    GREEN = '\033[32m'


def load_old_users():
    if os.path.exists('./users'):
        for user_directory in os.listdir("users"):
            # find password for this user
            users_password_file = pd.read_csv('users_info/user_information.csv')
            hash_password = users_password_file.loc[users_password_file["User Name"] == user_directory, "Password"]
            # reload user
            user = User(user_directory, hash_password, "accounts.csv")
            with open("users/{}/accounts.csv".format(user_directory)) as accounts_file:
                for line in accounts_file:
                    row, account_number, bank_name, cart_number, balance = line.split(",")
                    if row == "row":
                        pass
                    else:

                        user.accounts.append(
                            Account(account_number.strip(), float(balance.strip()), bank_name.strip(),
                                    cart_number.strip(),
                                    user_directory))

            users.append(user)


def get_account_number():
    dict1 = {}
    with open(current_object.csv_file, "r") as f:
        i = 1
        for line in f:
            line = line.split(",")
            if line[1] == "account_number":
                print(Colors.HEADER + "\n" + line[1] + Colors.ENDC)
            else:
                print(Colors.FAIL + str(i) + " . " + line[1] + Colors.ENDC)
                dict1[i] = line[1]
                i += 1
    while True:
        try:
            account_number = 0
            account_number = int(
                input(Colors.HEADER + "Please enter your account number:" + Colors.ENDC))
        except ValueError:
            pass
        if account_number not in dict1.keys():
            print(
                Colors.HEADER +
                "\n please enter correct number you don`t have any account with this input\n"
                + Colors.ENDC)
        else:
            return dict1[account_number]


load_old_users()
sign_up = SignUp()
sign_in = SignIn()

op = 0
while True:
    # Enter a number within range(1-10) if the number was not in range (1-10) or was not integer give error
    print(Colors.FAIL + "\n")
    print("\t   Main menu")
    print("\t1. Sign up")
    print("\t2. login")
    print("\t3. Add new account ")
    print("\t4. Earn")
    print("\t5. Spend")
    print("\t6. Transaction")
    print("\t7. Account Information")
    print("\t8. Display account turnover with Pie Charts")
    print("\t9. Display account turnover with broken Line Chart")
    print("\t10.Log out")
    print("\t11.Exit")
    print("\t Select Your Option (1-11)" + Colors.ENDC)
    try:
        op = int(input(Colors.FAIL + "Enter:" + Colors.ENDC))
        if op in range(1, 12):

            if op == 1:
                user_name = input(Colors.FAIL + "Username:" + Colors.ENDC)
                pass_word = input(Colors.FAIL + "Password:" + Colors.ENDC)
                if len(users) == 0:
                    sign_up.new_user_info(user_name, pass_word)
                    users.append(User(user_name, pass_word))

                    print(Colors.GREEN + "singed up successfully" + Colors.ENDC)
                else:
                    for user in users:
                        if user.user_name == user_name:
                            print(Colors.HEADER + 'Username already exists choose another username' + Colors.ENDC)
                            break
                    else:
                        sign_up.new_user_info(user_name, pass_word)
                        users.append(User(user_name, pass_word))
                        print("\a")
                        print(Colors.GREEN + "singed up successfully" + Colors.ENDC)

            elif op == 2:
                if current_object is not None:
                    print(Colors.HEADER + "{},you already logged in".format(current_object.user_name) + Colors.ENDC)
                else:
                    exi = 0
                    while exi != 1:
                        user_name = input(Colors.FAIL + "Username:" + Colors.ENDC)
                        pass_word = input(Colors.FAIL + "Password:" + Colors.ENDC)
                        if sign_in.check_user_info(user_name, pass_word):
                            for user in users:
                                if user.user_name == user_name:
                                    current_object = user
                                    print("\a")
                                    print(Colors.HEADER + '***Welcome***\n' + Colors.ENDC)
                                    break
                            break
                        #addd?
                        else:
                            print(Colors.RED + "***Wrong Username or Password***" + Colors.ENDC)
                            print(Colors.HEADER + 'Try Again' + Colors.ENDC)

                        exi = input(Colors.HEADER + "Do you want to sign out? Y/N :" + Colors.ENDC)
                        if exi in ["Y", "y"]:
                            exi = 1
                        if exi not in ["y", "Y", "n", "N"]:
                            logging.error(Colors.HEADER + "Enter a valid input\n" + Colors.ENDC)

            elif op == 3:
                if current_object is None:
                    print(Colors.HEADER + "***Please login***" + Colors.ENDC)
                else:
                    while True:
                        try:
                            print(Colors.HEADER + "      ***New account***" + Colors.ENDC)
                            account_number = input(Colors.FAIL + "Account number:").strip().replace(" ", "")
                            initial_amount = float(input("Initial amount:").replace(" ", ""))
                            bank_name = str(input("Bank name:").strip())
                            cart_number = input("Cart number:" + Colors.ENDC).strip().replace(" ", "")
                            current_object.new_account(account_number, initial_amount, bank_name, cart_number)
                            print(Colors.GREEN + "your account add successfully" + Colors.ENDC)
                            break
                        except ValueError:
                            logging.error(Colors.HEADER + "enter a valid input" + Colors.ENDC)

            elif op == 4:
                if current_object is None:
                    print(Colors.HEADER + "***Please login***" + Colors.ENDC)
                else:
                    account_number = get_account_number()
                    value = float(input(Colors.FAIL + "Amount:" + Colors.ENDC))
                    while True:
                        print(Colors.HEADER + "\t  Earning Types" + Colors.ENDC)
                        for key, val in Account.dict_income.items():
                            print(Colors.FAIL + "\t{}. {}".format(key, val) + Colors.ENDC)

                        spend_type = int(input(Colors.FAIL + "type:" + Colors.ENDC))
                        if spend_type == 1:
                            new_income_key = input(Colors.HEADER + "Enter new income type:" + Colors.ENDC)
                            Account.new_income(new_income_key)
                            continue
                        else:
                            spend_type = Account.dict_income[spend_type]

                            if current_object.earn(account_number, value, spend_type):
                                print("\a")
                                print(Colors.GREEN + "Earned successfully" + Colors.ENDC)
                                break

                            else:
                                print(Colors.RED + "Wrong account number" + Colors.ENDC)
                                break
            elif op == 5:
                if current_object is None:
                    print(Colors.HEADER + "***Please login***" + Colors.ENDC)
                else:
                    account_number = get_account_number()
                    value = float(input(Colors.FAIL + "Amount:" + Colors.ENDC))
                    while True:
                        print(Colors.HEADER + "\t  Spend Types" + Colors.ENDC)
                        for key, val in Account.dict_cost.items():
                            print(Colors.FAIL + "\t{}. {}".format(key, val) + Colors.ENDC)

                        spend_type = int(input(Colors.FAIL + "Spend type:" + Colors.ENDC))
                        if spend_type == 1:
                            new_cost_key = input(Colors.FAIL + "Enter new type:" + Colors.ENDC)
                            Account.new_cost(new_cost_key)
                            continue
                        else:
                            spend_type = Account.dict_cost[spend_type]

                            if current_object.spend(account_number, value, spend_type):
                                print("\a")
                                print(Colors.GREEN + "spent successfully" + Colors.ENDC)
                                break
                            else:
                                print(Colors.WARNING + "your balance is not enough" + Colors.ENDC)
                                break

            elif op == 6:
                if current_object is None:
                    print(Colors.HEADER + "***Please login***" + Colors.ENDC)
                else:
                    account_number = get_account_number()
                    current_object.list_of_transactions(account_number)

            elif op == 7:
                if current_object is None:
                    print(Colors.HEADER + "***Please login***" + Colors.ENDC)
                else:
                    account_number = get_account_number()
                    current_object.show_account(account_number)

            elif op == 8:
                if current_object is None:
                    print(Colors.HEADER + "***Please login***" + Colors.ENDC)
                else:
                    account_number = get_account_number()
                    current_object.pie_chart(account_number)

            elif op == 9:
                if current_object is None:
                    print(Colors.HEADER + "***Please login***" + Colors.ENDC)
                else:
                    account_number = get_account_number()
                    current_object.display_account_turnover_with_charts(account_number)

            elif op == 10:
                if current_object is None:
                    print(Colors.HEADER + "***Please login***" + Colors.ENDC)
                else:
                    current_object = None
                    print(Colors.GREEN + "Log out successfully" + Colors.ENDC)

            elif op == 11:
                print(Colors.HEADER + "Hope enjoyed our application" + Colors.ENDC)
                sys.exit()

        else:
            logging.error(Colors.RED + "Enter a number within range (1-10)" + Colors.ENDC)

    except ValueError:
        logging.error(Colors.RED + "Input is not valid,please enter a number" + Colors.ENDC)

    time.sleep(4)
    os.system('cls')
