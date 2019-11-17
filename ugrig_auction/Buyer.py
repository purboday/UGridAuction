'''
Created on Oct 12, 2018

@author: purboday
'''
from riaps.run.comp import Component
import logging
import time
import os


class Buyer(Component):
    def __init__(self, buyernum):
        super(Buyer, self).__init__()
        self.pid = os.getpid()
        now = time.ctime(int(time.time()))
        self.logger.info("(PID %s)-starting buyer, %s",str(self.pid),str(now))
        self.benefit = [2,2,0]
        self.increment = 0.4
        self.buyernum = buyernum
        self.assigned = ''
        self.price = []
        self.pulse = 0
        self.started = False
    
    def on_collect(self):
        msg = self.collect.recv_pyobj()
        msg= msg.split('_')
    	self.logger.info('received from seller %s price %s: %s' %(msg[0], msg[1]))
        if not self.started:
            self.started = True
    	self.price.append(int(msg[1]))
        
    def on_waitbid(self):
        now = self.waitbid.recv_pyobj()
        if self.started:
            self.pulse += 1
            if self.pulse == 4:
                self.logger.info('calculating bids')
                for i in range(len(price)):
                    cost[i] = self.benefit[i] - self.price[i]       
                max_value = max(cost)
                max_index = my_list.index(cost)
                cost.pop(max_index)
                second_max = max(cost)
                bidamt = max_value - second_max + self.increment
                msg = str(max_index)+','+str(bidamt)+','+self.buyernum
                self.logger.info('buyer (PID %s) bid %f for object %d' %(self.pid,bidamt,max_index))
                self.bidport.send_pyobj(bidamt)
                self.started = False
            
        
    def on_freebuyer(self):
        msg = self.freebuyer.recv_pyobj()
        msg = msg.split('_')
        if msg[0] == 'assigned':
            self.logger.info('buyer %s assigned object %s' %(self.buyernum, self.assigned))
            self.assigned = msg[1]
            pair = self.buyernum+'_'+self.assigned
        elif msg[0] == 'freed':
            self.assigned = ''
            self.logger.info('buyer %s freed' % self.buyernum)
            pair = self.buyernum+'_free'
        self.statusport.send_pyobj(pair)
                       
    def __destroy__(self):
        now = time.time()
        self.logger.info("%s - stopping buyer, %s",str(self.pid),now)         

