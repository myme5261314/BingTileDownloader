#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2014年1月22日

@author: peng
@contact: myme5261314@gmail.com
'''

from ConfigParser import RawConfigParser
from transform import lonToTileX, latToTileY

class BroadFirstConfig(object):
    def __init__(self, filepath):
        config = RawConfigParser()
        config.read(filepath)
        self.fp = filepath
        self.name = config.get('Task', 'name')
        self.description = config.get('Task', 'description')
        self.basic_url = config.get('Task', 'Basic_url')
        self.area = map(float, config.get('Task', 'Area').split(','))
        self.max_z = config.getint('Task', 'maxZoom')
        self.min_z = config.getint('Task', 'minZoom')
        
                
        self.debug = config.getboolean('Debug', 'debugmode')
        self.debugTryTimes = config.getint('Debug', 'TryTimes')
        
        self.MAX_Threads = config.getint('Run', 'MAX_Threads')
        self.MAX_QUEUE = config.getint('Run', 'MAX_QUEUE')
        self.image_floder = config.get('File', 'ImageFloder')
        
        self.min_x = int(lonToTileX(self.area[0], self.min_z))
        self.min_y = int(latToTileY(self.area[3], self.min_z))
        self.max_x = int(lonToTileX(self.area[1], self.min_z))
        self.max_y = int(latToTileY(self.area[2], self.min_z))
        self.x = config.getint('Task-State', 'currentX')
        self.y = config.getint('Task-State', 'currentY')
        # Initialize
        if self.x == 0 and self.y == 0:
            self.x = self.min_x
            self.y = self.min_y
        # Breakpoint Resume
        elif self.x-self.min_x+(self.y-self.min_y)*(self.max_x-self.min_x)>3*self.MAX_QUEUE:
            if self.x - self.min_x > 3*self.MAX_QUEUE:
                self.x = self.x - 3*self.MAX_QUEUE
            else:
                self.x = self.max_x - (3*self.MAX_QUEUE - (self.x - self.min_x))
                self.y = self.y - 1
        else:
            self.x = self.min_x
            self.y = self.min_y
        

        print self.x, self.max_x
        print self.y, self.max_y
        print (self.max_x-self.x)*(self.max_y-self.y)
    
    def getTotalTileNum(self):
        return (self.max_x-self.min_x)*(self.max_y-self.min_y)

    def getProcess(self, x, y, qsize):
        cur = (y-self.min_y)*(self.max_x-self.min_x)+(x-self.min_x)-qsize
        total = (self.max_x-self.x)*(self.max_y-self.y)
        return float(cur)/total*100

    def updateState(self, x, y):
        config = RawConfigParser()
        config.read(self.fp)
        config.set('Task-State', 'currentX', str(x))
        config.set('Task-State', 'currentY', str(y))
        with open(self.fp, 'wb') as configfile:
            config.write(configfile)
    def updateProcess(self):
        config = RawConfigParser()
        config.read(self.fp)
        process = config.getfloat('Task-State', 'Process')
        total = self.getTotalTileNum()
        process = process + 1/float(total)
        config.set('Task-State', 'Process', str(process))
        with open(self.fp, 'wb') as configfile:
            config.write(configfile)
        return process


if __name__ == '__main__':
    c = BroadFirstConfig('wuhan.cfg')