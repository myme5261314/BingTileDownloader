#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2014年1月15日

@author: peng
@contact: myme5261314@gmail.com
'''

import os

import requests


# from handlerThread import none_img
# with open('None.png','rb') as f:
#     none_img = f.rea
def downloadTile(key, url_t, path_t):
#     path = path_t % (str(len(key))+'/'+key+'.jpg')
    path = path_t % getFilePath(key)
    if os.path.exists(path):
        return True
#     floderpath = path_t % (str(len(key))+'/')
    url = url_t % key
    success = False
    while not success:
        try:
            img = requests.get(url)
            success = True
        except requests.exceptions.RequestException as e:
            continue
        except Exception as e:
            print e
    if len(img.content) > 1033:
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        _f = open(path, 'wb')
        _f.write(img.content)
        _f.close()
        print 'Finish %s success!' % path
        return True
    else:
        return False
    
def getFilePath(key):
    t = int(key, 4)
    st = 10000
    t = t/st
    return '%s/%d_%d/%s.jpg' % (str(len(key)), t, st, key)
        
    
