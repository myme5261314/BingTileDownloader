#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2014年1月15日

@author: peng
@contact: myme5261314@gmail.com
'''

import requests
import os
from handlerThread import none_img

# with open('None.png','rb') as f:
#     none_img = f.rea

def downloadTile(key, url_t, path_t):
    path = path_t % (str(len(key))+'/'+key+'.jpg')
    floderpath = path_t % (str(len(key))+'/')
    if os.path.exists(path):
        return True
    url = url_t % key
    success = False
    while not success:
        try:
            img = requests.get(url)
            success = True
        except requests.exceptions.RequestException as e:
            print e
    if len(img.content) > 1033:
        if not os.path.exists(floderpath):
            os.makedirs(floderpath)
        _f = open(path, 'wb')
        _f.write(img.content)
        _f.close()
        return True
    else:
        return False
        
    
