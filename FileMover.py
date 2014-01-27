#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2014年1月27日

@author: peng
@contact: myme5261314@gmail.com
'''
import os

floder = 'D:/bing/wuhan/'

if __name__ == '__main__':
    for level in os.listdir(floder):
        if level in ('.', '..'):
            continue
        levelpath = floder + level
        for pic in os.listdir(levelpath):
            if pic in ('.', '..') or os.path.isdir(levelpath+'/'+pic):
                print pic
                continue
            key = pic[:-4]
            print pic, pic[:-4]
            i_key = int(key, 4)
            st = 10000
            i_key = i_key/st
            old = '%s/%s' % (levelpath, pic)
            new = '%s/%d_%d/%s.jpg' % (levelpath, i_key, st, key)
            print old, new
            os.renames(old, new)