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
        self.progress = config.getfloat('Task-State', 'Process')
        if self.progress != 0:
            t = self.progress * self.getTotalTileNum() / 100
            plus_x = int(t % (self.max_x - self.min_x))
            plus_y = int(t/(self.max_x - self.min_x))
            self.x = self.min_x + plus_x - 1
            self.y = self.min_y + plus_y
        # Initialize
        if self.x == 0 and self.y == 0:
            self.x = self.min_x
            self.y = self.min_y
        # Breakpoint Resume
        elif self.x-self.min_x+(self.y-self.min_y)*(self.max_x-self.min_x)>2*self.MAX_Threads:
            if self.x - self.min_x > 2*self.MAX_Threads:
                self.x = self.x - 2*self.MAX_Threads
            else:
                self.x = self.max_x - (2*self.MAX_Threads % (self.x - self.min_x))
                self.y = self.y - int((2*self.MAX_Threads % (self.x - self.min_x)))
        else:
            self.x = self.min_x
            self.y = self.min_y
        
        self.resumeProcess()

        print self.x, self.max_x
        print self.y, self.max_y
        cur = (self.y-self.min_y)*(self.max_x-self.min_x)+(self.x-self.min_x)
        print self.getTotalTileNum() - cur
    
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
        process = process + 1/float(total)*100
        config.set('Task-State', 'Process', str(process))
        with open(self.fp, 'wb') as configfile:
            config.write(configfile)
        return process
    def resumeProcess(self):
        config = RawConfigParser()
        config.read(self.fp)
        cur = (self.y-self.min_y)*(self.max_x-self.min_x)+(self.x-self.min_x)
        total = self.getTotalTileNum()
        process = float(cur)/total * 100
        config.set('Task-State', 'Process', str(process))
        with open(self.fp, 'wb') as configfile:
            config.write(configfile)
        return process


if __name__ == '__main__':
    c = BroadFirstConfig('wuhan.cfg')