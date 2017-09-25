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

import config
from .worker import Worker
from .worker import DieException
import smtplib
import netaddr
import time

class Worker_SMTP(Worker):
    """
    This worker checks if a SMTP server is available on the given ip:port address.  
    The helo/ehlo and greeting msg/code, plus some time statistics are written in DB.    
    """
    
    def __init__(self, model, hostid, logger):
        Worker.__init__(self, model, hostid, logger)
        self.module = 'smtp'
        self.moduleid = self.model.get_module_id(self.module)
        self.port = config.smtp_port
        self.log.info('Constructor - Worker SMTP (moduleid: %s)' 
                      % (self.moduleid,))
        
    def _check_host(self, ip, port):
        SMTPResult = {
            'checkid' : self.checkid,
            'ipv4' : ip.__str__(),
            'port' : port,
            'connectionResult' : '',
            'server-helo' : '',
            'server-ehlo' : '',
            'time_start' : None,
            'time_con' : None,
            'time_end' : None
            }
    
        try:
            smtp = smtplib.SMTP(timeout=config.smtp_timeout)
            SMTPResult['time_start'] = time.strftime('%H:%M:%S') 
            SMTPResult['connectionResult'] = smtp.connect(ip.__str__(),port)
            SMTPResult['time_con'] = time.strftime('%H:%M:%S')
            SMTPResult['server-helo'] = smtp.helo(config.smtp_helo_email_address)
            SMTPResult['server-ehlo'] = smtp.ehlo(config.smtp_helo_email_address)
            smtp.quit()
            SMTPResult['time_end'] = time.strftime('%H:%M:%S')
        except Exception:
            self.log.debug('SMTP Error!')
        
        return SMTPResult 
       
    def _check_network(self):
        pass   

    def run(self):
        infinity = True
        while infinity:
            try:
                self.log.info('** nodeid: %s' % (self.nodeid,))
                self.checkid = self.model.start_new_check(self.nodeid, self.moduleid)
                self.log.info('** checkid: %s' % (self.checkid,))
                ipclass = self.get_network()
                startip = self.get_start_ip(ipclass.ip, ipclass.broadcast) 
                self.log.info('wsmtp: %s, *START* - ip: %s (%s/%s), port: %s' 
                              % (self.nodeid, startip, ipclass.ip, ipclass.prefixlen,
                                 self.port))
                if startip < ipclass.broadcast:
                    IPRange = netaddr.IPRange(startip, ipclass.broadcast)
                    for ip in list(IPRange):
                        self.log.debug('...connecting to %s:%s' % (ip, self.port))
                        result = self._check_host(ip, self.port)
                        self.log.debug(result)
                        self.model.db_save(self.nodeid, result)
                        self.check_msg_queue()

                self.model.update_network_status(ipclass.ip, ipclass.prefixlen, 'FINISHED')
                self.log.info('FINISHED: %s/%s' %(ipclass.ip, ipclass.prefixlen))
                self.check_msg_queue()

            except DieException:
                self.log.info('dying... bye, bye...');
                infinity = False
            except Exception as e:
                self.log.error(' *** Exception *** WORKER SMTP *** ')
                self.log.exception(e)
                time.sleep(5)
                infinity = False
