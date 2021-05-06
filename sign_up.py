import csv
import hashlib
import logging
import os
from pathlib import Path


class SignUp:  # ثبت نام
    """class for making a new user and check whether the user already exists or not"""

    def __init__(self):
        if not os.path.exists('users_info'):  # if users directory does not exists make it
            os.makedirs('users_info')
        user_accounts = Path(
            'users_info/user_information.csv')

        if user_accounts.is_file():  # check if the user_information.csv file exists
            pass
        else:
            # make user_accounts.csv file which has all user's user name and password
            with open(
                    'users_info/user_information.csv',
                    'w', newline='') as users_info:
                fieldnames = ['User Name', 'Password']
                headers = csv.DictWriter(users_info, fieldnames=fieldnames)
                headers.writeheader()

        self.logger = logging.getLogger("SignUp")
        f_handler = logging.FileHandler("users_info/accounts.log")
        f_handler.setLevel(logging.WARNING)
        f_format = logging.Formatter(' %(levelname)s - %(message)s-%(asctime)s', datefmt='%d-%b-%y %H:%M:%S')
        f_handler.setFormatter(f_format)
        # Add handlers to the logger
        self.logger.addHandler(f_handler)

    def new_user_info(self, new_username, new_password):
        var = new_password.encode('utf-8')
        new_password = hashlib.md5(var).hexdigest()

        fieldnames = ['User Name', 'Password']

        f = open('users_info/user_information.csv', 'r')
        for line in f:
            details = line.strip().split(",")
            if new_username == details[0]:
                self.logger.error("{} already exists".format(new_username))
                break
            # add the user's username and pass to the main csv file

        else:

            with open('users_info/user_information.csv', 'a') as check_account_existence:

                writer = csv.DictWriter(check_account_existence, fieldnames=fieldnames)
                writer.writerow({'User Name': new_username, 'Password': new_password})
            self.logger.warning("{} added ".format(new_username))

        # add the user's username and pass added to the user_accounts.csv


# signup = SignUp()
# signup.new_user_info("fateme", 123)
