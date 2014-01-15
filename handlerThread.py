#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2014年1月15日

@author: peng
@contact: myme5261314@gmail.com
This is the file for handlerThread which extends from Thread to handle with the
job for each tile image download stuff.
'''

import threading
import requests
from transform import *
from requests.exceptions import ConnectionError

debug = True
z = 19
MAX = 2**z-1
x = 0
y = 0
print y
count = 0
threads_num = 20
current_keys = []

lock = threading.RLock()

class handlerThread(threading.Thread):
    def __init__(self, QuadKey):
        threading.Thread.__init__(self)
        self.key = QuadKey
        self.basic_url = 'http://h0.ortho.tiles.virtualearth.net/tiles/a%s.jpeg?g=131'
        self.basic_path = 'D://bing/%s.jpg'
    
    def run(self):
        img_url = self.basic_url % self.key
        try:
            img = requests.get(img_url)
        except ConnectionError as e:
            print e
            print 'Retry %s' % self.key
            self.stop(self.key)
            
        f = open(self.basic_path % self.key, 'wb')
        f.write(img.content)
        f.close()
        self.stop()
#         print self.key
    
    def stop(self, next_key=None):
        lock.acquire()
        if next_key == None:
            next_key = getNextQuadKey()
        lock.release()
        if next_key != None:
            lock.acquire()
            global current_keys
            current_keys.remove(self.key)
            current_keys.append(next_key)
            lock.release()
            print 'finish %s -> %s' % (self.key,next_key)
            next_handler = handlerThread(next_key)
            next_handler.start()


def getNextQuadKey():
    global count, x, y, MAX, debug
    count = count + 1
    if debug and count >= 201:
        return None
    
    if x<MAX:
        if y<MAX:
            y = y + 1
        else:
            y= 0
            x= x + 1;
        print x,y
        return tileXYZToQuadKey(x, y, z)
    else:
        return None
    
    

        
if __name__ == '__main__':
    for i in xrange(threads_num):
        current_keys.append(getNextQuadKey())
    print current_keys
         
    for i in xrange(threads_num):
        th = handlerThread(current_keys[i])
        th.start()
        