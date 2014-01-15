#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2014年1月15日

@author: peng
@contact: myme5261314@gmail.com
This is the file for handlerThread which extends from Thread to handle with the
job for each tile image download stuff.
'''


# producer_consumer_queue
from Queue import Queue
import threading
from os.path import exists

import requests

from transform import tileXYZToQuadKey


MAX_Threads = 201
MAX_QUEUE = 2000
z = 13
MAX_axes = 2**z-1

basic_url = 'http://h0.ortho.tiles.virtualearth.net/tiles/a%s.jpeg?g=131'

none_img = open('None.png','rb').read()
floder = 'D://bing/%s'

class BingException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class BingImageDownloader(threading.Thread):
    def __init__(self, ix, iy):
        threading.Thread.__init__(self)
        self.x = ix
        self.y = iy
        self.key = tileXYZToQuadKey(self.x, self.y, z)
        self.url = basic_url % self.key
        self.file = floder % (self.key+'.jpg')

    def run(self):
        threading.Thread.run(self)
        try:
            self.download()
#             print 'Finish: %d %d' % (self.x, self.y) 
        except BingException as e:
            print e
            self.retry()
#         self.stop()
    
    def download(self):
        try:
            img = requests.get(self.url)
            if img.content != none_img and not exists(self.file):
                _f = open(self.file, 'wb')
                _f.write(img.content)
                _f.close()
        except Exception as e:
            raise BingException(e)
    
    def retry(self):
        h = BingImageDownloader(self.x, self.y)
        h.start()
        
#     def stop(self):
#         threading.Thread.stop(self)
        
class KeyGenerator(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.data = queue
        self.x = 0
        self.y = 0
        self.count = 0
        self.stop_produce = False
        self.stop_consume = False

    def run(self):
        while True:
            dl = self.data.qsize()
            if dl <= MAX_QUEUE/2 and not self.stop_produce:
                for _ in range(MAX_QUEUE/10):
                    if not self.getNextXY():
                        self.stop_produce = True
                        break
                    else:
                        self.data.put((self.x, self.y))
            
            tl = len(threading.enumerate())
#             print tl
            if tl < MAX_Threads and not self.stop_consume:
                for _ in range(MAX_Threads-tl):
                    if not self.data.empty():
                        (_x, _y) = self.data.get()
                        handler = BingImageDownloader(_x, _y)
                        handler.start()
                    else:
                        self.stop_consume = True
                        break
            
            if self.stop_produce and self.stop_consume:
                break
                    
    def getNextXY(self):
        if self.count >= 5000:
            self.x = None
            self.y = None
            return False
        self.count = self.count + 1
        if self.y < MAX_axes:
            if self.x < MAX_axes:
                self.x = self.x + 1
            else:
                self.x = 0
                self.y = self.y + 1
            return True
        else:
            self.x = None
            self.y = None
            return False
            
if __name__ == '__main__':
    q = Queue()
    r = KeyGenerator(q)
    r.start()               
                

            
                    