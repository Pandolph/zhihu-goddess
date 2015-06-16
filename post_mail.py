#!/usr/bin/python
#coding:utf-8
#Author:hackersungl@gmail.com

import sys
import smtplib
from email.mime.text import MIMEText

def post_mail(mail_from_addr, mail_from_pwd, mail_to_addr, subject, body):
    print '-----------------'
    #validate mail_from_addr
    if(mail_from_addr.find('@') <= 0):
        print  mail_from_addr + ' is an invalid mail address, please check it...'
        return False

    mail_body = body
    mail = MIMEText(mail_body)
    mail['From'] = mail_from_addr
    mail['To'] = ';'.join(mail_to_addr)
    mail['Subject'] = subject

    smtp = smtplib.SMTP()
    server = 'smtp.' + mail_from_addr.split('@')[1]
    print 'connecting mail server '+ server + ' ...'
    smtp.connect(server)
    print 'loging...'
    smtp.login(mail_from_addr, mail_from_pwd)
    print 'sending email...'
    smtp.sendmail(mail_from_addr, mail_to_addr, mail.as_string())
    print 'send email complete.'
    smtp.quit()
    return True

def post_mail(params):
    print '-----------------'
    mail_from_addr = params['mail_from_addr']
    mail_from_pwd = params['mail_from_pwd']
    mail_to_addr = params['mail_to_addr']
    subject = params['subject']
    body = params['body']

    #validate mail_from_addr
    if(mail_from_addr.find('@') <= 0):
        print  mail_from_addr + ' is an invalid mail address, please check it...'
        return False

    mail_body = body
    mail = MIMEText(mail_body)
    mail['From'] = mail_from_addr
    mail['To'] = ';'.join(mail_to_addr)
    mail['Subject'] = subject

    smtp = smtplib.SMTP()
    server = 'smtp.' + mail_from_addr.split('@')[1]
    print 'connecting mail server '+ server + ' ...'
    smtp.connect(server)
    print 'loging...'
    smtp.login(mail_from_addr, mail_from_pwd)
    print 'sending email...'
    smtp.sendmail(mail_from_addr, mail_to_addr, mail.as_string())
    print 'send email complete.'
    smtp.quit()
    return True


if __name__ == '__main__':
    if len(sys.argv) == 2:
        post_mail(sys.argv[1])
