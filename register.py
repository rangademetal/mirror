from Model.Secret import SERVER, USERNAME, PASSWORD, DATABASE
from Model.Database import Database
from send import sendemail
import random

connection = Database(SERVER, USERNAME, PASSWORD, DATABASE)
db = connection.connect()

email = input('Enter your email: ')
username = input('Enter your username: ')
password = input('Enter your password: ')
code = random.randint(100000, 999999)
connection.set_register(db, email, username, password, str(code))
send = sendemail(email, code)

