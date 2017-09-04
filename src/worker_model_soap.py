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

from suds.client import Client
import config

class Worker_Model_SOAP:
    """
    The model layer. 
    In this case there is no direct connection to DB, but the remote SOAP service was used. 
    """
    def __init__(self):
        self.c = Client(config.soapurl)

    def get_host_id(self, hostname):
        hostid = self.c.service.getHostID(hostname)
        return hostid

    def get_max_threads(self, hostid, workerType):
        max_threads = self.c.service.getHostMaxThreads(hostid, workerType)
        return max_threads

    def get_node_id(self, hostid):
        nodeid = self.c.service.getNewNodeId(hostid)
        return nodeid
    
    def get_network_id(self, checkid):
        netid = self.c.service.getNetworkId(checkid)
        return netid

    def get_network(self, netid):
        net = self.c.service.getNetwork(netid)
        return net
    
    def get_last_ip(self, ip, broadcast):
        lastip = self.c.service.getLastIP(ip, broadcast)
        return lastip
    
    def check_node_is_running(self, nodeid):
        status = self.c.service.checkNodeIsRunning(nodeid)
        return status
    
    def db_save(self, nodeid, rec):
        
        if self.check_node_is_running(nodeid):
            
            data = self.c.factory.create('struct1')
            
            if len(rec['connectionResult']) > 1:
                data.gcode = rec['connectionResult'][0]
                data.gtext = rec['connectionResult'][1]

            if len(rec['server-helo']) > 1:
                data.hcode = rec['server-helo'][0]
                data.htext = rec['server-helo'][1]

            if len(rec['server-ehlo']) > 1:
                data.ecode = rec['server-ehlo'][0]
                data.etext = rec['server-ehlo'][1]
                
            data['time_start'] = rec['time_start']
            data['time_con'] = rec['time_con']
            data['time_end'] = rec['time_end']
            
            data.ip = rec['ipv4']
            data.port = rec['port']
            data.checkid = rec['checkid']
            
            self.c.service.addHostInfo(data)
            
        else:
            raise Exception('hmmm... nodeid != running?...') 
    
    def update_network_status(self, ip, prefixlen, status):
        self.c.service.updateNetworkStatus(ip, prefixlen, status)

    def get_module_id(self, module):
        id = self.c.service.getModuleId(module)
        return id

    def start_new_check(self, nodeid, moduleid):
        '''  '''
        checkid = self.c.service.startNewCheck(nodeid, moduleid)
        return checkid 
    
    def get_nodes_running(self, hostid):
        nodes = self.c.service.getNodesRunning(hostid)
        return nodes
     