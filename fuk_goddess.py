#!usr/bin/python
#coding:utf-8
#Author:hackersungl@gmail.com

import sys
import os
import requests
import re
import time
import datetime
import json
from random import *
from bs4 import BeautifulSoup 
import post_mail

# session对象,会自动保持cookies
s = requests.session()

global goddess_latest_activity_time
goddess_latest_activity_time = 0

def login_zhihu(login_email, login_password):
    print 'loging in zhihu...'
    login_url = 'http://www.zhihu.com/login'
    login_data = {'email': login_email, 'password':login_password, 'rememberme':'y'}
    r = s.post(login_url, login_data)
    #print '============'
    #print r.text
    #print '============'
    if r.status_code == 200:
        print 'log in successfully.'
    else:
        print 'log in failed. status_code=' + str(r.status_code)



def get_goddess_skilled_topics(my_goddess):
    file_name = my_goddess + '-skilled_topics' + time.strftime('.%Y.%m.%d')
    if os.path.isfile(file_name):
        os.remove(file_name)

    print '----------------'
    print "get "+ my_goddess +"'s skilled topics..."
    goddess_homepage = 'http://www.zhihu.com/people/' + my_goddess
    page = s.get(goddess_homepage)
    data = page.text

    soup = BeautifulSoup(data)
    skilled_block = soup.find('div', {'class':"zm-profile-section-wrap skilled-topics"})

    if(skilled_block is None):
        print my_goddess + "does not set its skilled topics."
        return
    skilled_list = soup.findAll('a',{'class':'zg-gray-darker'})
    skilled_topics = []

    print my_goddess + "'s skilled topics are:"
    for skill in skilled_list:
        skilled_topics.append(skill.text.strip())
    print ';'.join(skilled_topics)

    #write to file
    write_to_file(file_name, ';'.join(skilled_topics) + '\n')



def get_goddess_all_activities(my_goddess):
    file_name = my_goddess + '-activities' + time.strftime('.%Y.%m.%d')
    if os.path.isfile(file_name):
        os.remove(file_name)

    #准备好加载更多时的rul
    load_more_url = 'http://www.zhihu.com/people/' + my_goddess + '/activities'
    
    #post header info
    header_info = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
        'Host':'www.zhihu.com',
        'Origin':'http://www.zhihu.com',
        'Connection':'keep-alive',
        'Referer':'http://www.zhihu.com/people/' + my_goddess,
        'Content-Type':'application/x-www-form-urlencoded',
        }

    print '----------------'
    print 'get ' + my_goddess + "'s all activities..."
    goddess_homepage = 'http://www.zhihu.com/people/' + my_goddess
    page = s.get(goddess_homepage)
    data = page.text

    raw_xsrf = re.findall('xsrf(.*)', data)
    _xsrf = raw_xsrf[0][9:-3]# _xsrf

    page_index = 0
    while True:
        page_index += 1
        
        #for debug
        #if page_index == 2:
        #    return

        soup = BeautifulSoup(data)
        activity_list = soup.findAll('div', {'class': "zm-profile-section-item zm-item clearfix"})
        if len(activity_list) == 0:
            if page_index == 1:
                print 'there is no activities.'
            else:
                print 'have got all activities, no more.'
            return

        print 'page ' + str(page_index) + '...'

        a_page_activity = ''
        start = 0
        for a_activity in activity_list:
            a_page_activity += '----------------' + '\n'
            
            start = a_activity['data-time']
            activity_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(start)))

            activity = a_activity.find('div', {'class':"zm-profile-section-main zm-profile-section-activity-main zm-profile-activity-page-item-main"})
            subject = activity.text.encode('utf-8').split('\n')
            
            #remove '' from subject
            indx = len(subject) - 1
            while indx >= 0:
                if len(subject[indx].strip('\n\t ')) == 0:
                    subject.remove(subject[indx])
                indx -= 1

            subject = activity_time + " " + unicode(':'.join(subject), 'utf-8')
            
            a_page_activity += subject + '\n'

            a_list = activity.findAll('a')
            focus_activity = a_list[-1]
            a_page_activity += focus_activity.text.strip('\n\r ') + '\n'
            
            href = focus_activity['href']
            if(href.find('http://zh') <> 0):
                href = 'http://www.zhihu.com' + href
            a_page_activity += href + '\n'
        
        #for debug
        #print a_page_activity
        
        #write to file
        append_to_file(file_name, a_page_activity)

        #next page
        params = {"_xsrf":_xsrf, "start":start,}
        try:
            page = s.post(load_more_url, data=params, headers=header_info, timeout=20)
        except:
            # 响应时间过程过长则重试
            print '=================='
            print 'repost...'
            page = s.post(load_more_url, data=params, headers=header_info, timeout=60)
        data = page.json()
        data = data['msg'][1]



def get_goddess_all_answers(my_goddess):
    print '----------------'
    print 'get ' + my_goddess + "'s all answers..."

    answer_url = 'http://www.zhihu.com/people/' + my_goddess + '/answers'
    file_name = my_goddess + '-answers' + time.strftime('.%Y.%m.%d')
    if os.path.isfile(file_name):
        os.remove(file_name)

    #post header info
    header_info = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
        'Host':'www.zhihu.com',
        'Connection':'keep-alive',
        'Referer':answer_url,
        'Content-Type':'text/html; charset=UTF-8',
        }

    html_page = s.get(answer_url)
    data = html_page.text
    page_index = 1

    while True:
        soup = BeautifulSoup(data)
        answer_list = soup.findAll('div', {'class':'zm-item'})
        
        if len(answer_list) == 0:
            if page_index == 1:
                print 'there is no answers.'
            else:
                print 'got all answers, no more.'
            return

        print 'page ' + str(page_index) + '...'
        a_page_answer = ''

        for answer in answer_list:
            a_page_answer += '----------------\n'
            a_page_answer += answer.h2.a.text + '\n'
            a_page_answer += 'http://www.zhihu.com' + answer.h2.a['href'] + '\n'
        
        #write to file
        append_to_file(file_name, a_page_answer)

        #next page
        page_index += 1
        params = {'page': page_index,}
        html_page = s.get(answer_url + "?page=" + str(page_index), data=params, headers=header_info, timeout=20)
        data = html_page.text



def get_goddess_all_asks(my_goddess):
    print '----------------'
    print 'get ' + my_goddess + "'s all asks..."

    ask_url = 'http://www.zhihu.com/people/' + my_goddess + '/asks'
    file_name = my_goddess + '-asks' + time.strftime('.%Y.%m.%d')
    if os.path.isfile(file_name):
        os.remove(file_name)
    page_index = 1
    
    #post header info
    header_info = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
        'Host':'www.zhihu.com',
        'Connection':'keep-alive',
        'Referer':ask_url + '?page=' + str(page_index),
        'Content-Type':'text/html; charset=UTF-8',
        }

    html_page = s.get(ask_url)
    data = html_page.text

    while True:
        soup = BeautifulSoup(data)
        ask_list = soup.findAll('div', {'class':'zm-profile-section-main'})

        if len(ask_list) == 0:
            if page_index == 1:
                print 'there is no asks.'
            else:
                print 'got all asks, no more.'
            return
        
        print 'page ' + str(page_index) + '...'
        a_page_ask = ''

        for ask in ask_list:
            a_page_ask +=  '----------------\n'
            a_page_ask +=  ask.h2.a.text + '\n'
            a_page_ask +=  'http://www.zhihu.com' + ask.h2.a['href'] + '\n'

        #write to file
        append_to_file(file_name, a_page_ask)

        #next page
        page_index += 1
        params = {'page': page_index,}
        html_page = s.get(ask_url + "?page=" + str(page_index), data=params, headers=header_info, timeout=20)
        data = html_page.text



def watch_goddess_latest_activity(my_goddess, mail_config_dic):
    global goddess_latest_activity_time
    while True:
        print '----------------'
        now_time = time.strftime("%Y%m%d-%H:%M:%S")
        print now_time + ' get ' + my_goddess + "'s latest activity..."
        goddess_homepage = 'http://www.zhihu.com/people/' + my_goddess
        page = s.get(goddess_homepage)
        data = page.text
        soup = BeautifulSoup(data)

        activity_list = soup.findAll('div', {'class': "zm-profile-section-item zm-item clearfix"})
        if len(activity_list) == 0:
            print my_goddess + " has no activities."
            return

        for a_activity in reversed(activity_list):
            if goddess_latest_activity_time == 0:
                goddess_latest_activity_time = int(activity_list[0]['data-time']) - 1

            data_time = int(a_activity['data-time'])
            if data_time <= goddess_latest_activity_time:
                continue
            goddess_latest_activity_time = data_time
            activity_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data_time)))

            activity = a_activity.find('div', {'class':"zm-profile-section-main zm-profile-section-activity-main zm-profile-activity-page-item-main"})
            subject = activity.text.encode('utf-8').split('\n')
            
            #remove '' from subject
            indx = len(subject) - 1
            while indx >= 0:
                if len(subject[indx].strip('\n\t ')) == 0:
                    subject.remove(subject[indx])
                indx -= 1
            subject = activity_time + ' ' + unicode(':'.join(subject),'utf-8')

            a_list = activity.findAll('a')
            focus_activity = a_list[-1]
            body = '\n' + focus_activity.text
            href = focus_activity['href']
            if(href.find('http://') < 0):
                href = 'http://www.zhihu.com' + href
            body += '\n' + href
            
            #print
            print '----------------'
            print my_goddess + "'s lastest activity:"
            print subject
            print body
            
            #send email
            #mail_config_dic['subject'] = subject.encode('utf-8')
            #mail_config_dic['body'] = body.encode('utf-8')
            #post_mail.post_mail(mail_config_dic)

        time.sleep(60 + choice(range(120)))



def write_to_file(file_name, content):
    #f = open(file_name, 'w')
    #f.write(content)
    with open(file_name, 'w') as f:
        f.write(content.encode("UTF-8"))
    f.close()



def append_to_file(filename, content):
    with open(filename, 'a') as f:
        f.write(content.encode("UTF-8"))
    f.close()



if __name__ == '__main__':
    my_goddess_id = 'renfish'
    login_zhihu("doc123@163.com", 'password')
    #get_goddess_skilled_topics(my_goddess_id)
    #get_goddess_all_answers(my_goddess_id)
    #get_goddess_all_asks(my_goddess_id)
    #get_goddess_all_activities(my_goddess_id)

    #mail_config_dic = {}
    #mail_config_dic['mail_from_addr'] = 'doc123@163.com'
    #mail_config_dic['mail_from_pwd'] = 'password'
    #mail_config_dic['mail_to_addr'] = ['mail@163.com']
    #watch_goddess_latest_activity('hackersun', mail_config_dic)


