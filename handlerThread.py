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
from Config import Config

from transform import tileXYZToQuadKey


# z = 13
# MAX_axes = 2**z-1

# basic_url = 'http://h0.ortho.tiles.virtualearth.net/tiles/a%s.jpeg?g=131'
# basic_url = 'http://ecn.t0.tiles.virtualearth.net/tiles/a%s.jpeg?g=2241'

none_img = open('None.png','rb').read()
# floder = 'D://bing/%s'

class BingException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class BingImageDownloader(threading.Thread):
    def __init__(self, ix, iy, config, iz=0):
        threading.Thread.__init__(self)
        self.config = config
        self.x = ix
        self.y = iy
        if iz==0:
            self.z = config.max_z
        else:
            self.z = iz
        self.key = tileXYZToQuadKey(self.x, self.y, self.z)
        self.url = config.basic_url % self.key
        self.file = config.image_floder % (self.key+'.jpg')
    
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
        if not exists(self.file):
            try:
                img = requests.get(self.url)
                if img.content != none_img:
                    _f = open(self.file, 'wb')
                    _f.write(img.content)
                    _f.close()
                else:
                    self.retry_z()
            except Exception as e:
                raise BingException(e)
        else:
            return

    def retry(self):
        h = BingImageDownloader(self.x, self.y, self.config, self.z)
        h.start()
    
    def retry_z(self):
        if self.z > self.config.min_z:
            x = int(self.x/2)
            y = int(self.y/2)
            h = BingImageDownloader(x, y, self.config, self.z-1)
            h.start()
        else:
            return
        
class KeyGenerator(threading.Thread):
    def __init__(self, configpath):
        threading.Thread.__init__(self)
        self.config = Config(configpath)
        self.data = Queue()
        self.x = self.config.x
        self.y = self.config.y
        self.Max_z = self.config.max_z
        self.Min_z = self.config.min_z
        self.MAX_axes = 2**self.Max_z
        self.debug = self.config.debug
        self.debugTryTimes = self.config.debugTryTimes
        if self.config.debug:
            self.count = 0
        self.stop_produce = False
        self.stop_consume = False
    
    def run(self):
        while True:
            dl = self.data.qsize()
            if dl <= self.config.MAX_QUEUE/2 and not self.stop_produce:
                for _ in range(self.config.MAX_QUEUE/10):
                    if not self.getNextXY():
                        self.stop_produce = True
                        break
                    else:
                        self.data.put((self.x, self.y))
            
            tl = len(threading.enumerate())
#             print tl
            if tl < self.config.MAX_Threads+1 and not self.stop_consume:
                for _ in range(self.config.MAX_Threads-tl):
                    if not self.data.empty():
                        (_x, _y) = self.data.get()
                        handler = BingImageDownloader(_x, _y, self.config)
                        handler.start()
                    else:
                        self.stop_consume = True
                        break
            
            if self.stop_produce and self.stop_consume:
                break
                    
    def getNextXY(self):
        if self.debug:
            if self.count >= self.debugTryTimes:
                self.x = None
                self.y = None
                return False
            self.count = self.count + 1
        
        if self.y < self.MAX_axes:
            if self.x < self.MAX_axes:
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
    
    r = KeyGenerator('china.cfg')
    r.start()
            
                    