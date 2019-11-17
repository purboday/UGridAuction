'''
Created on Oct 12, 2018

@author: purboday
'''
from riaps.run.comp import Component
import logging
import time
import os


class Seller(Component):
    def __init__(self, sellernum):
        super(Seller, self).__init__()
        self.pid = os.getpid()
        now = time.ctime(int(time.time()))
        self.logger.info("(PID %s)-starting seller, %s",str(self.pid),str(now))
        self.sellernum = sellernum
        self.bidamt == 0
        self.assigned = ''
        self.winner = ''
        self.price = 0
        self.active = True
        self.pulse = 0
        
    def on_assignport(self):
        # Receive bid
        msg = self.assignport.recv_pyobj()
        if self.active == True:   
            msg = msg.split(',')
            obj = int(msg[0])
            self.bidamt = float(msg[1])
            buyernum = msg[2]
            if obj == self.sellernum:
                if float(msg[1]) >= self.bidamt:
                    self.bidamt = float(msg[1])
                    self.winner = buyernum
    
    def on_timeout(self):
        now = self.timeout.recv_pyobj()
        if self.active:
            self.pulse += 1
            if self.pulse == 4:   
                self.active = False
                self.logger.info('finalizing bids for seller [PID: %s]' %(self.pid))
                if not self.assigned == '':
                    freed = self.assigned
                    self.assigned = self.winner
                    self.logger.info("seller temporarily assigned to buyer %s" % self.assigned)
                    self.freebuyer.send_pyobj('assigned_'+self.assigned)
                    self.freebuyer.send_pyobj('freed_'+freed)
                    self.price += self.bidamt
                    msg = self.sellernum+'_'+str(self.price)
                    self.logger.info('seller %s sending new price' % self.sellernum)
                    self.sendprice.send_pyobj(msg)
                    self.active = True
                    self.pulse = 0
        
            
    def on_notify(self):
        msg = self.notify.recv_pyobj()
        if msg == 'start':
            self.active == True
            self.logger.info('starting negotiation round')
            msg = self.sellernum+'_'+self.price
            self.sendprice.send_pyobj(msg)
        elif msg == 'stop':
            self.active = False
            self.logger.info('seller %s assigned to buyer %s' % (self.sellernum, self.assigned))

        
    def __destroy__(self):
        now = time.time()
        self.logger.info("%s - stopping TempMonitor, %s",str(self.pid),now)