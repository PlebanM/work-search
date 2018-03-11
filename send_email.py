import smtplib
import db_init


def create_msg():
    if db_init.find_new() != []:

        msgtext = 'Hello, \n\n'

        for id, newrecord in enumerate(db_init.find_new(),1):

            msgtext += "{}. Title: {}\nDate: {}\nSalary: " \
                           "{}\nAdvertisement: {}...\nLink: {}\n\n\n".format(id, newrecord[1], newrecord[2],
                                                                                newrecord[3],newrecord[4][0:60],
                                                                                newrecord[5])
        return send_email(msgtext)



def send_email(fullMsg):
    subject = "New job offers"

    message = 'Subject: {}\n\n{}'.format(subject, fullMsg).encode('utf-8')

    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()
    mail.starttls()

    mail.login(user='::login::@gmail.com', password='::password::')  # email and password to account

    mail.sendmail('::login:@gmail.com', '::login::@gmail.com',
                  message)

    mail.close()

