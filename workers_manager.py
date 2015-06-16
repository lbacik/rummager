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
 Main logic  
 
 @note: python 2.7
 @version: 0.2
 @author: Lukasz Bacik <mail@luka.sh>
"""

import config
import worker_model_soap, worker_smtp
import time, threading, os, logging, socket

class Workers_Manager:
    
    def __init__(self, hostname, logger):
        self.model = worker_model_soap.Worker_Model_SOAP()
        self.hostname = hostname
        self.hostid = self.model.get_host_id(self.hostname)
        self.max_threads = 0 #self.model.get_max_threads(self.hostid)
        self.log = logger
        self.log.info('Constructor - Workers Manager, hostname: %s' 
                      % (self.hostname,))
        # structure that is containing list of thread and worker objects 
        self.threads = []
                    
    def print_threads_status(self):
        for t in threading.enumerate():
            self.log.warning('--- %s : %s' 
                             % (t.getName(), t.is_alive().__str__()))    
            
    def run(self):
        """ Main loop """
        nodes_running = 0
        old_nodes_running = 0
        while True:
            try:
                self.max_threads = self.model.get_max_threads(self.hostid)
                if self.model.get_nodes_running(self.hostid) != nodes_running \
                        or nodes_running != old_nodes_running:
                    # some threads are probably suspended 
                    self.log.warning(' * nodes running %s ' % (nodes_running,))
                    old_nodes_running = nodes_running
                    nodes_running = self.model.get_nodes_running(self.hostid)
                    
                activeT = threading.activeCount()    
                if activeT != int(self.max_threads)+1 :
                    self.log.info(' * active thread %d / %d' 
                              % (activeT-1, int(self.max_threads)))
                for i in range(activeT, int(self.max_threads)+1):
                    self.log.info(' * Starting thread %d' % (i,))
                    w = worker_smtp.Worker_SMTP(self.model, self.hostid, self.log)
                    w.start()
                    time.sleep(2)
            except Exception as e:
                #print("Error: unable to start thread")
                self.log.error(' *** Exception *** MAIN *** ')
                self.log.exception(e)
            time.sleep(10)

if __name__ == "__main__":
    
    logging.basicConfig(format='%(asctime)s T:%(thread)d %(levelname)s: %(message)s',
                    filename='%s/%s' % (config.log_dir, config.log_file), 
                    #'%s/T-%s-%s.log' % (config.log_dir, PID, TIME),
                    level=config.log_level) #logging.INFO)

    PID = os.getpid()
    hostname = socket.gethostname()
    logging.info('MANAGER START - hostname: %s, pid: %s' % (hostname,PID))
    wm = Workers_Manager(hostname, logging)
    wm.run()
