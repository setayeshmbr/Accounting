import logging
import os
import pandas as pd


class Account:
    # there are two class variable that are type of incomes and costs
    # cost = ["Housing", "Food", "Clothing"]
    # income = ["Salary", "Stock market","Inheritance" ]
    dict_income = {1: 'Other', 2: 'Stock market', 3: 'Inheritance', 4: 'Salary'}
    dict_cost = {1: 'Other', 2: 'clothing', 3: 'Housing', 4: 'Food' }

    def __init__(self, account_number, initial_amount, bank_name, cart_number, directory):
        """for each account init it`s attributes then create .log and .csv for it """
        self.account_number = account_number
        self.bank_name = bank_name
        self.cart_number = cart_number
        self.balance = initial_amount

        # make log file for each account
        self.logger = logging.getLogger(self.account_number)
        f_handler = logging.FileHandler(os.path.join(r"users\{}".format(directory), '{}.log'.format(account_number)))
        f_handler.setLevel(logging.INFO)
        f_format = logging.Formatter('%(message)s in %(asctime)s')
        f_handler.setFormatter(f_format)
        self.logger.addHandler(f_handler)

        # make csv file for each account
        if os.path.exists('./users/{}/{}.csv'.format(directory, account_number)):
            with open('./users/{}/{}.csv'.format(directory, account_number)) as f:
                len_of_lines = f.readlines()
                self.csv_file_index = len(len_of_lines)
        else:
            df = pd.DataFrame(list(), columns=['row', 'account_number', 'value', "category", "balance", "type"])
            df.to_csv(os.path.join(r"users\{}".format(directory), '{}.csv'.format(account_number)), index=False)
            self.csv_file_index = 1
        self.csv_file = os.path.join(r"users\{}".format(directory), '{}.csv'.format(account_number))

    @classmethod
    def new_income(cls, new_income):
        """add new in come type"""
        new_income.lower()
        cls.dict_income[len(cls.dict_income)+1] = new_income

    @classmethod
    def new_cost(cls, new_cost):
        """add new cost"""
        new_cost.lower()
        cls.dict_cost[len(cls.dict_cost)+1] = new_cost

    def spend_account_balance(self, amount):
        """check for spend if possible return True and change balance else return false"""
        if self.balance < amount:
            return False
        else:
            self.balance -= amount
            return True

    def earn_income(self, amount):
        """update balance after earn """
        self.balance += amount

    def __str__(self):
        """print for account"""
        return " Balance: {} \n Bank_name: {} \n cart_number: {}".format(str(self.balance), self.bank_name, self.cart_number)
