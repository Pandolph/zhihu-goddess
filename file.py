#!usr/bin/python
#coding:utf-8
#Author:hackersungl@gmail.com

import sys

def write(file_name, content):
    #f = open(file_name, 'w')
    #f.write(content)
    with open(file_name, 'w') as f:
        f.write(content.encode("UTF-8"))
    f.close()

def append(file_name, content):
    with open(file_name, 'a') as f:
        f.write(content.encode("UTF-8"))
    f.close()

