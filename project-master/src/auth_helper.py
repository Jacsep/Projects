import random
import string
import smtplib

def generate_code():
    letters = string.ascii_letters
    random_num = random.randint(1000, 9999)
    result_str = ''.join(random.choice(letters) for i in range(4))
    code = result_str + str(random_num)
    return code


def sendEmail(rec, msg):
    sender_email = 'mango5comp1531@gmail.com'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, 'callagher')
    server.sendmail(sender_email, rec, msg)
    return
