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
import random

# session对象,会自动保持cookies
s = requests.session()


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



#获取username(不是自己,登陆id的获取hashid那里不一样)所有关注的人
def get_a_user_all_followees(username):
    all_followees = []
    #准备好加载更多时的rul
    click_url = 'http://www.zhihu.com/people/' + username + '/followees'
    load_more_url = 'http://www.zhihu.com/node/ProfileFolloweesListV2'
    
    header_info = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
        'Host':'www.zhihu.com',
        'Origin':'http://www.zhihu.com',
        'Connection':'keep-alive',
        'Referer':click_url,
        'Content-Type':'application/x-www-form-urlencoded',
        }

    print '----------------'
    print 'get ' + username + "'s all followees..."
    page = s.get(click_url)
    data = page.text.encode('utf-8')

    #get hash_id and xsrf
    raw_hash_id = re.findall('hash_id(.*)',data)
    hash_id = raw_hash_id[0][14:46]
    raw_xsrf = re.findall('xsrf(.*)',data)
    _xsrf = raw_xsrf[0][9:-3]

    load_more_times = int(re.findall('<strong>(.*?)</strong>', data)[2]) / 20

    followee_id = re.compile('zhihu.com/people/(.*?)"').findall(data)
    followee_id = followee_id[1:len(followee_id)]
    all_followees.extend(followee_id)

    for i in range(1, load_more_times + 1):
        print 'page ' + str(i) + '...' 
        offsets = i * 20
        # 由于返回的是json数据,所以用json处理parameters.
        params = json.dumps({"hash_id":hash_id, "order_by":"created", "offset":offsets,})
        payload = {"method":"next", "params": params, "_xsrf":_xsrf,}
        
        try:
            page = s.post(load_more_url, data=payload, headers=header_info, timeout=18)
        except:
            #响应时间过长，可能被封锁了
            t = random.randint(0,20)
            print 'sleep ' + str(t) + '...'
            time.sleep(t)
            page = s.post(load_more_url, data=payload, headers=header_info, timeout=60)
        
        # parse info.
        followee_id = re.findall('href=\\\\"\\\\/people\\\\/(.*?)\\\\', page.text.encode('utf-8'))
        followee_id = followee_id[0:len(followee_id):5]
        #print followee_id
        all_followees.extend(followee_id)
    return all_followees


#获取所有关注username的人
def get_a_user_all_followers(username):
    all_followers = []
    #准备好加载更多时的rul
    click_url = 'http://www.zhihu.com/people/' + username + '/followers'
    load_more_url = 'http://www.zhihu.com/node/ProfileFollowersListV2'
    
    header_info = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
        'Host':'www.zhihu.com',
        'Origin':'http://www.zhihu.com',
        'Connection':'keep-alive',
        'Referer':click_url,
        'Content-Type':'application/x-www-form-urlencoded',
        }

    print '----------------'
    print 'get ' + username + "'s all followers..."
    page = s.get(click_url)
    data = page.text.encode('utf-8')

    #get hash_id and xsrf
    raw_hash_id = re.findall('hash_id(.*)',data)
    hash_id = raw_hash_id[0][14:46]
    raw_xsrf = re.findall('xsrf(.*)',data)
    _xsrf = raw_xsrf[0][9:-3]

    load_more_times = int(re.findall('<strong>(.*?)</strong>', data)[3]) / 20

    follower_id = re.compile('zhihu.com/people/(.*?)"').findall(data)
    follower_id = follower_id[1:len(follower_id)]
    all_followers.extend(follower_id)

    for i in range(1, load_more_times + 1):
        print 'page ' + str(i) + '...' 
        offsets = i * 20
        # 由于返回的是json数据,所以用json处理parameters.
        params = json.dumps({"hash_id":hash_id, "order_by":"created", "offset":offsets,})
        payload = {"method":"next", "params": params, "_xsrf":_xsrf,}
        
        try:
            page = s.post(load_more_url, data=payload, headers=header_info, timeout=18)
        except:
            #响应时间过长，可能被封锁了
            t = random.randint(0,20)
            print 'sleep ' + str(t) + '...'
            time.sleep(t)
            page = s.post(load_more_url, data=payload, headers=header_info, timeout=60)
        
        follower_id = re.findall('href=\\\\"\\\\/people\\\\/(.*?)\\\\', page.text.encode('utf-8'))
        follower_id = follower_id[0:len(follower_id):5]
        all_followers.extend(follower_id)
    return all_followers




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

def get_a_user_all_followees_and_followers(username):
    followee_list = get_a_user_all_followees(username)
    follower_list = get_a_user_all_followers(username)
    follow_list = [followee_list,follower_list]
    return follow_list


#bfs, get all user and their followees and followers
def get_all_user_followees_and_followers(start_user):
    user_list = []
    user_follow_dict={}
    if isinstance(start_user, str):
        user_list.append(start_user)
    elif isinstance(start_user, list):
        user_list.extend(start_user)
    
    while len(user_list) > 0:
        userid = user_list[0]
        del user_list[0]
        if userid in user_follow_dict:
            continue

        follower_list = get_a_user_all_followees_and_followers(userid)
        user_follow_dict[userid] = follower_list

        file_content = str(follower_list[0]) + '\n' + str(follower_list[1]) + '\n'
        write_to_file('user/' + userid + '.txt', file_content)

        user_list.extend(follower_list[0])
        user_list.extend(follower_list[1])




if __name__ == '__main__':
    login_zhihu("mail@163.com", '1234')
    #followerlist = get_a_user_all_followers('hackersun')
    #ll = get_a_user_all_followees('hackersun')
    #print get_a_user_all_followees_and_followers("hackersun")
    get_all_user_followees_and_followers('hackersun')

