from Model.Account import Account
from Model.Database import Database
from Model.Secret import DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_DATABASE
import sys

class login:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.connection = Database(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
        self.db = self.connection.connect()

    def login(self):
        try:
            account = self.connection.get_account(self.db, self.username, self.password)
            account = Account(account[0], account[1], account[2], account[3], account[4], account[5])
            if account.verificatio_status == 0:
                code = input('please enter the activation code:')
                if code == account.verification_code:
                    self.connection.set_code(self.db, account.username)
                    print('Activation Succesfull')
            
        except TypeError as e:
            sys.exit()



