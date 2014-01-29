#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2014年1月20日

@author: peng
@contact: myme5261314@gmail.com
'''

from multiprocessing import Process,Queue
import multiprocessing
from BroadFirstConfig import BroadFirstConfig
from BroadFirstDownloader import BroadFirstDownloader
import time
import logging

class BroadFirstGenerator(Process):
    def __init__(self, config_path):
        Process.__init__(self)
        self.config = BroadFirstConfig(config_path)
        self.data = Queue()
        self.x = self.config.x
        self.y = self.config.y
        self.stop_produce = False
        self.stop_consume = False
        self.total = self.config.getTotalTileNum()
        self.count = 0
        
    def run(self):
        init = True
        while True and not (self.stop_produce):
            dl = self.data.qsize()
            if dl <= self.config.MAX_QUEUE/2 and not self.stop_produce:
                for _ in range(self.config.MAX_QUEUE/4):
                    if not self.getNextXY():
                        self.stop_produce = True
                        break
                    else:
                        self.data.put((self.x, self.y, self.config.min_z))
            if init:
                init = False
                num_consumers = multiprocessing.cpu_count() * 2
#                 num_consumers = 2
                consumers = [BroadFirstDownloader(self.data, self.config) for _ in range(num_consumers)]
                for consumer in consumers:
                    consumer.start()
            if self.data.empty():
                break
            time.sleep(60)
                        
    def getNextXY(self):
#         logger = multiprocessing.get_logger()
        if self.config.debug:
            if self.count >= self.config.debugTryTimes:
                self.x = None
                self.y = None
                return False
        self.count = self.count + 1
        if self.count % 1 == 0 and self.x != None and self.y != None:
#             process = self.config.getProcess(self.x, self.y, self.data.qsize())
#             print '%s: Proceed:%f/100' % (time.ctime(), process)
#             logger.debug('%s: Proceed:%f/100' % (time.ctime(), process))
            self.config.updateState(self.x, self.y)
        if self.y < self.config.max_y:
            if self.x < self.config.max_x:
                self.x = self.x + 1
            else:
                self.x = self.config.min_x
                self.y = self.y + 1
            return True
        else:
            self.x = None
            self.y = None
            return False

if __name__ == '__main__':
    r = BroadFirstGenerator('wuhan.cfg')
    r.start()
                    
            