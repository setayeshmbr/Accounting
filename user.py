import logging
import os
import pandas as pd
import matplotlib.pyplot as plt
from account import Account


class User:
    def __init__(self, user_name, password, account_csv_file=None):
        """for each user make directory that has info of accounts"""
        self.user_name = user_name
        self.password = password
        self.accounts = []

        # create folder for each user
        if os.path.exists('./users/{}'.format(user_name)):
            pass
        else:
            os.system(r"mkdir users\{}".format(user_name))

        # make log file for each user to see log of crate new account
        self.logger = logging.getLogger(user_name)
        f_handler = logging.FileHandler(os.path.join(r"users\{}".format(user_name), "accounts.log"))
        f_handler.setLevel(logging.DEBUG)
        f_format = logging.Formatter('%(message)s in  %(asctime)s  ')
        f_handler.setFormatter(f_format)
        self.logger.addHandler(f_handler)

        # make csv file for each user to see detail of crate accounts
        if account_csv_file is None:
            df = pd.DataFrame(list(), columns=['row', 'account_number', 'bank_name', "cart_number", "balance"])
            df.to_csv(os.path.join(r"users\{}".format(user_name), 'accounts.csv'), index=False)
            self.csv_file_index = 1
        else:
            with open("users/{}/{}".format(user_name, account_csv_file), "r") as f:
                len_of_lines = f.readlines()
                self.csv_file_index = len(len_of_lines)

        self.csv_file = os.path.join(r"users\{}".format(user_name), 'accounts.csv')

    def new_account(self, account_number, initial_amount, bank_name, cart_number):
        """create new account for user in his directory and make log to know account create"""
        with open(self.csv_file, "r") as f:
            for account_info in f:
                account_number_in_file = account_info.strip().split(",")
                if account_number_in_file[1] == account_number:
                    print("this account_number already exit")
                    return
        self.accounts.append(Account(account_number, initial_amount, bank_name, cart_number, self.user_name))
        # make log for each account that create
        self.logger.warning(
            "{} account with {} account_number added successfully".format(self.user_name, account_number))

        # add row in csv file for accounts
        csv_file_of_accounts = pd.read_csv(self.csv_file)
        new_transactions = {'row': self.csv_file_index, 'account_number': account_number,
                            'bank_name': bank_name, "cart_number": cart_number, "balance": initial_amount}
        self.csv_file_index += 1
        csv_file_of_accounts.loc[len(csv_file_of_accounts)] = new_transactions

        csv_file_of_accounts.to_csv(self.csv_file, index=False)

    def spend(self, unique, value, category):
        """give account_number or card_number as unique then find account and do spend code
        if account exist return true else return false"""
        for account in self.accounts:
            if account.account_number == unique or account.cart_number == unique:
                if account.spend_account_balance(value):
                    account.logger.warning("{} toman spend for {} ".format(value, category))
                    csv_file_of_account = pd.read_csv(account.csv_file)
                    new_transactions = {"row": account.csv_file_index, "account_number": account.account_number,
                                        "value": value, "category": category, "balance": account.balance,
                                        "type": "spend"}
                    account.csv_file_index += 1
                    csv_file_of_account.loc[len(csv_file_of_account)] = new_transactions

                    csv_file_of_account.to_csv(account.csv_file, index=False)
                    self.update_user_csv_file(account.account_number, account.balance)
                    return True

                else:
                    account.logger.warning("your balance is not enough for to spend money for {} ".format(category))
                    return False
        else:
            return False

    def earn(self, unique, value, category):
        """give account_number or card_number as unique then find account and do earn code
                if account exist return true else return false"""
        for account in self.accounts:
            if account.account_number == unique or account.cart_number == unique:
                account.earn_income(value)
                account.logger.warning("{} toman earn form {} ".format(value, category))
                csv_file_of_account = pd.read_csv(account.csv_file)
                new_transactions = {"row": account.csv_file_index, "account_number": account.account_number,
                                    "value": value, "category": category, "balance": account.balance, "type": "earn"}
                account.csv_file_index += 1
                csv_file_of_account.loc[len(csv_file_of_account)] = new_transactions
                csv_file_of_account.to_csv(account.csv_file, index=False)

                self.update_user_csv_file(account.account_number, account.balance)
                return True
        else:
            return False

    def show_account(self, unique):
        """give account_number or card_number as unique then show detail about account
        if account exist return true else return false"""
        for account in self.accounts:
            if account.account_number == unique or account.cart_number == unique:
                print(account)
                return True
        else:
            return False

    def list_of_transactions(self, unique):
        """give account number or card number and show transactions that save in log file
        if account exist return true else return false"""
        for account in self.accounts:
            if account.account_number == unique or account.cart_number == unique:
                path = 'users/{}/{}.csv'.format(self.user_name, account.account_number)
                log_file = open(path)
                transactions = pd.read_csv(log_file)
                print (transactions.to_string(index=False))
                return True
        else:
            return False

    def update_user_csv_file(self, account_number, balance):

        csv_file_of_accounts = pd.read_csv(self.csv_file)
        csv_file_of_accounts.loc[csv_file_of_accounts["account_number"] == account_number, "balance"] = balance
        csv_file_of_accounts.to_csv(self.csv_file, index=False)

    def display_account_turnover_with_charts(self, unique):
        for account in self.accounts:
            if account.account_number == unique or account.cart_number == unique:
                csv_file_of_account = pd.read_csv(account.csv_file)
                data_for_chart = csv_file_of_account["balance"]
                plt.plot(range(1, len(csv_file_of_account) + 1), data_for_chart, '-p')
                plt.xticks(range(1, len(csv_file_of_account) + 1))
                plt.xlabel("number of transactions")
                plt.ylabel("toman")
                plt.show()

    def pie_chart(self, unique):
        for account in self.accounts:
            if account.account_number == unique or account.cart_number == unique:
                plt.subplot(2, 1, 1)
                csv_file_of_account = pd.read_csv(account.csv_file)
                data_for_chart = csv_file_of_account[csv_file_of_account["type"] == "spend"]
                data_for_chart.category.value_counts().plot.pie(autopct='%1.1f%%')
                plt.title("costs")

                plt.subplot(2, 1, 2)
                data_for_chart = csv_file_of_account[csv_file_of_account["type"] == "earn"]
                data_for_chart.category.value_counts().plot.pie(autopct='%1.1f%%')
                plt.title("incomes")

                plt.show()
