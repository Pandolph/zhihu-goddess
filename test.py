#!/usr/bin/python
#encoding:utf-8
#author:hackersungl@gmail.com

def testlist(num):
    ll = []
    for i in range(num):
        ll.append(i)
    return ll

if __name__ == '__main__':
    lt = testlist(10)
    print lt
    print lt.index(3)
    print lt.index(10)
