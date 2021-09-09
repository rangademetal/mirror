import smtplib


class sendemail:
    def __init__(self, rec_email, code):
        sender_email = 'hardytomson3@gmail.com'
        self.rec_email = rec_email
        self.code = code

        password = 'Sad1996.'

        message = f"Your Activation code is {self.code}"

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, self.rec_email, message)
        print('Email has been send')