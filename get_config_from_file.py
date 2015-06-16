#!/usr/bin/python
#coding:utf-8
#Author:hackersungl@gmail.com

import sys
import os

def main(file_name):
    if not os.path.isfile(file_name):
        print 'config file not exist!!!'
        return
    
    config_dic = {}
    f = open(file_name, 'r')
    lines = f.readlines()
    for line in lines:
        #print line, len(line)
        if(len(line) <= 1 or line.find('#') >= 0):
            continue
        else:
            config = line.strip().split('=')
            config_dic[config[0]] = config[1]
    f.close()

    #print config_dic
    return config_dic

#test case
#main('config.txt')

if __name__ == '__main__':
    main(sys.argv[1])

