#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2014年1月18日

@author: peng
@contact: myme5261314@gmail.com
'''

from ConfigParser import RawConfigParser

class Config(object):
    def __init__(self, filepath):
        config = RawConfigParser()
        config.read(filepath)
        self.name = config.get('Task', 'name')
        self.description = config.get('Task', 'description')
        self.basic_url = config.get('Task', 'Basic_url')
        self.area = map(float, config.get('Task', 'Area').split(','))
        self.max_z = config.getint('Task', 'maxZoom')
        self.min_z = config.getint('Task', 'minZoom')
        
        self.x = config.getint('Task-State', 'currentX')
        self.y = config.getint('Task-State', 'currentY')
        
        self.debug = config.getboolean('Debug', 'debugmode')
        self.debugTryTimes = config.getint('Debug', 'TryTimes')
        
        self.MAX_Threads = config.getint('Run', 'MAX_Threads')
        self.MAX_QUEUE = config.getint('Run', 'MAX_QUEUE')
        self.image_floder = config.get('File', 'ImageFloder')