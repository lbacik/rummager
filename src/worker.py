# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Lukasz Bacik <mail@luka.sh>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

"""
 @note: python 2.7
 @version: 0.2
 @author: Lukasz Bacik <mail@luka.sh>
"""

from abc import abstractmethod
from abc import ABCMeta
# from _pyio import __metaclass__
import netaddr, threading, queue

class Worker (threading.Thread):
    "Base class for all kind of Workers"
        
    __metaclass__ = ABCMeta
    
    def __init__(self, model, hostid, logger):
        """
        model - for now only Worker_Model_SOAP
        
        All arguments are automatically set up in Workers_Manager class
        """
        self.model = model
        self.hostid = hostid
        self.nodeid = self.model.get_node_id(self.hostid)
        self.log = logger
        self.checkid = 0
        self.netid = 0
        self.ipclass = 0
        self.log.info('Constructor - Worker, hostid: %s, nodeid: %s' 
                      % (self.hostid, self.nodeid))
        threading.Thread.__init__(self)
    
    def start_new_check(self):
        """
        checkid is one of the most important values - should be determined 
        at the very beginning in the run method     
        """
        self.checkid = self.model.start_new_check(self.nodeid, self.moduleid)
     
    def get_network(self):
        """
        Get network on which the worker will work

        @todo: concerns only SMTP worker (?)
        """
        self.netid = self.model.get_network_id(self.checkid)
        [ip,mask] = self.model.get_network(self.netid).split('/')
        self.log.info('GET NETWORK: %s/%s - netid: %s, checkid: %s' 
                      % (ip, mask, self.netid, self.checkid))
        self.ipclass = netaddr.IPNetwork(ip + '/' + mask)
        return self.ipclass    
    
    def get_start_ip(self, ip, broadcast):
        """
        Get ip address from which to start
        
        @todo: This method should return a set (list) of addresses that has not 
        been checked rather than just a start point (to avoid holes in ip classes)

        @todo: concerns only SMTP worker (?)
        """
        lastip = self.model.get_last_ip(ip, broadcast)
        if lastip == None:
            startip = ip
        else:
            startip = netaddr.IPAddress(lastip) + 1
        return startip

    def set_msg_queue(self, msg_queue):
        self.msg_queue = msg_queue

    def check_msg_queue(self):
        try:
            msg = self.msg_queue.get_nowait()
            if msg == 'DIE':
                raise DieException()
                    #Exception("...diying...bye...")
        except queue.Empty as e:
            pass

    @abstractmethod
    def run(self):
        """
        All workers should implements this method 
        """
        pass

class DieException(Exception):
    pass