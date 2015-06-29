#!/usr/bin/python
#encoding:utf-8
#author:hackersungl@gmail.com
import sys
import random
import time

def testlist(num):
    for i in range(num):
        j = random.randint(1,10)
        print 'sleep ' + str(j) + '...'
        time.sleep(j)
        print i


if __name__ == '__main__':
    lt = testlist(200)
