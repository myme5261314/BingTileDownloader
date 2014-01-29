#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2014年1月22日

@author: peng
@contact: myme5261314@gmail.com
'''
import multiprocessing
import Queue
from transform import tileXYZToQuadKey
from downloader import downloadTile
from BroadFirstConfig import BroadFirstConfig
import time

lock = multiprocessing.Lock()

class BroadFirstDownloader(multiprocessing.Process):
    def __init__(self, q, config):
        multiprocessing.Process.__init__(self)
        self.tasks = q
        self.config = config
    
    def run(self):
        Finish = False
        logger = multiprocessing.log_to_stderr(multiprocessing.SUBDEBUG)
        while not Finish:
            try:
                if self.tasks.empty():
                    Finish = True
                    break
                job = self.tasks.get()
            except Queue.Empty as e:
#                 logger.error(e)
                Finish = True
                break
            (x, y, z) = job
#             logger.debug("Start %d, %d, %d" % (x, y, z))
            quadkey = tileXYZToQuadKey(x, y, z)
            if self.config.isFinish(x, y, z) or self.broadFirst(quadkey):
                lock.acquire()
                process = self.config.updateProcess()
                self.config.recordFinish(x, y, z)
                lock.release()
                logger.debug('%s: %f/100' % (time.ctime(), process))
#             if not self.broadFirst(quadkey):
#                 logger.debug("not Finished. %d, %d, %d" % (x, y, z))
#             else:
#                 logger.debug("Finished. %d, %d, %d" % (x, y, z))
                
    def broadFirst(self, key):
        ''' True means no need to dig more
        False means need to dig to next level
        '''
        count = 0
        logger = multiprocessing.log_to_stderr(multiprocessing.SUBDEBUG)
        state = downloadTile(key, self.config.basic_url, self.config.image_floder)
        count = count + 1
        bottom = 0
        l = self.moveToNextLevel(key)
        q = Queue.Queue()
        for i in l:
            q.put(i)
        while not q.empty():
            tl = []
            for _ in range(4):
                tl.append(q.get())
                count = count + 1
            for t in tl:
                state = downloadTile(t, self.config.basic_url, self.config.image_floder)
#                 state = True
                if state and len(t)< self.config.max_z:
                    l = self.moveToNextLevel(t)
                    for _ in l:
                        q.put(_)
            if count - bottom >= 1000:
                logger.debug('%s: Roughly Process: %d/21845' % (time.ctime(), count))
                bottom = count
#             logger.debug('%d' % count)
        return True
        

                
    
    def moveToNextLevel(self, key):
        kl = []
        for i in range(4):
            kl.append(key + str(i))
        return kl
        
if __name__ == '__main__':
    config = BroadFirstConfig('wuhan.cfg')
    q = multiprocessing.Queue()
    q.put((6684,3344,13))
    p = BroadFirstDownloader(q,config)
    p.start()
            