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

import config, subprocess, logging

logging.basicConfig(format='%(asctime)s P:%(process)d %(levelname)s: %(message)s',
                    filename='%s/%s' % (config.log_dir, config.watch_log_file), 
                    level=config.watch_log_level)

logging.info('** Watchdog START')
p = subprocess.Popen(["ps", "ax"], stdout=subprocess.PIPE)
out, err = p.communicate()

if ( config.watchdog_search_str in out.__str__()):
    logging.info('OK!')
    proc = [f for f in out.split('\n') if config.watchdog_search_str in f ]
    for i in proc:
        logging.info(i)
else:
    args = ['python', config.watchdog_search_str ]
    p = subprocess.Popen(args)
    logging.info('NOT FOUND - STARTED with pid: %s' %(p.pid,))

    


