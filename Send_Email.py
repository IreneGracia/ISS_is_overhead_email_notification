import smtplib
from email.message import EmailMessage
from params import *

# Automatically sends email from my gmail using an app password and using
# gmail's SMTP server

MY_EMAIL = 'irenucagp@gmail.com'
PASSWORD = 'luco eqit lgqc phjh'

def send_email(ADDRESSEE_EMAIL):
    msg = EmailMessage()
    msg.set_content('Look up! The ISS is above you!')
    msg['Subject'] = 'ISS Alert'
    msg['From'] = MY_EMAIL
    msg['To'] = ADDRESSEE_EMAIL

    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()  # Encrypts the connection
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.send_message(msg)
        print('Email sent!')
