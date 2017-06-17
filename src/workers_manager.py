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

class Workers_Manager:
    
    def __init__(self, hostname, logger, model):
        self.model = model
        self.hostname = hostname
        self.hostid = self.model.get_host_id(self.hostname)
        self.max_threads = 0
        self.log = logger
        self.log.info('Constructor - Workers Manager, hostname: %s' 
                      % (self.hostname,))
        self.pool_manager = []

    # def print_threads_status(self):
    #     for t in threading.enumerate():
    #         self.log.warning('--- %s : %s'
    #                          % (t.getName(), t.is_alive().__str__()))
    #

    def add_pool_manager(self, pool):
        self.pool_manager.append(pool)

    def run(self):
        try:
            for pool in self.pool_manager:
                size = self.model.get_max_threads(self.hostid, pool.worker_type_name)
                size = int(size)
                self.log.debug('%s pool size - get_max_threads: %d' % (pool.worker_type_name, size))
                pool.adjust_pool_size(size)

        except Exception as e:
            self.log.error(' *** Exception *** MAIN *** ')
            self.log.exception(e)
