#!/usr/bin/python
#coding:utf-8
#Author:hackersungl@gmail.com

import os
import sys
import get_config_from_file
import post_mail
import fuk_goddess

def main(*file_name):
    #get configs from file
    #default config file is config.txt
    config_file_name = 'config.txt'
    #print file_name, len(file_name)
    if len(file_name) == 1:
        config_file_name = file_name[0]
    print '-----------------'
    print "config_file is:", config_file_name
    print 'reading config file...'
    config_dict = get_config_from_file.main(config_file_name)
    print 'there are', len(config_dict.keys()) ,'configs:'
    print config_dict.keys()


    #post email
    mail_config_dic = {}
    mail_config_dic['mail_from_addr'] = config_dict['mail_from_addr']
    mail_config_dic['mail_from_pwd'] = config_dict['mail_from_pwd']
    mail_config_dic['mail_to_addr'] = config_dict['mail_to_addr'].split(';')
    mail_config_dic['subject'] = 'subject'
    mail_config_dic['body'] = 'This is a test mail from python script.'
    if post_mail.post_mail(mail_config_dic):
        print 'send mail success.'
    else:
        print 'send mail failed..'



if __name__ ==  '__main__':
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) == 2:
        config_file = sys.argv[1]
        print "config_file is:", config_file
        if not os.path.isfile(config_file):
            print config_file, 'is not exist!'
            sys.exit(1)
        main(config_file)
    else:
        print 'please check parameters!'
        print 'main.py [config_file_name]'
        sys.exit(1)



