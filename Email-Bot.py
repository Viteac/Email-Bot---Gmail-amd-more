import getpass
import imaplib
import email
from email.header import decode_header
import os
import codecs
from time import sleep
import smtplib, ssl
import re
import time

sender_email = input('Enter your Gmail account\n> ')
password = input('Enter the password\n> ')
u = sender_email
p = password
pat = input('Enter the Subject you want to answer to: > ')

while True:
    file = input('Enter file name containing text you want to send.\n>>> ')
    o = os.getcwd()
    if os.path.isfile(o + '//' + file) is True:
        break
    print(f' There\'s no a {file} in your directory\n Try again')


def menu():
    print('* Vimart Mail bot v1.0')
    print('1. Answer for emails.\n')
    choice = False
    while choice not in ['1']:
        choice = input('\n>>>')
        if choice == '1':
            mai_load(1)

        else:
            print('Try again. Enter option 1')


def send_mail(n):

    with open(file) as f:
        read = f.readlines()


    sub = read[0].rstrip('\n')
    con = ''.join(read)
    email = n
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"

    receiver_email = email

    message = f"""\
    Subject: {sub}

{con}"""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    print(f'{read}\n Emails sent to:', n)
    time.sleep(2)


def mai_load(s):
    global u, p

    while True:
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(u, p)

        except imaplib.IMAP4.error:
            print(' Wrong login or password')
            sleep(3)
            mai_load(s)
        break

    mail.select()
    status, messages = mail.select("INBOX")
    n = int(str(messages[0], 'utf-8'))
    messages = int(messages[0])
    for i in range(messages, messages-n,-1):
        res, msg = mail.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                Sub, encoding = decode_header(msg.get("Subject"))[0]
                if isinstance(Sub, bytes): # check the subject
                    Sub=Sub.decode((encoding))
                if Sub == pat:
                    fro, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(fro, bytes):
                        fro = fro.decode(encoding)

                    print("From:", fro)
                    send_mail(fro)
                    mail.copy(str(i), 'answered')
                    mail.store(str(i), '+FLAGS', '\\Deleted')

                print("=" * 100)


    # close the connection and logout
    mail.close()
    mail.logout()

    # return u, p
    mai_load(0)
    time.sleep(180)


while True:
    menu()
