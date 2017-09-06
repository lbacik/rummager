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
 Config file. 
 
 @author: Lukasz Bacik <mail@luka.sh>
"""

# imported to get access to const defined in logging module
import logging

mainloop_delay = 30

soapurl = 'http://__HOST__/soap.php?wsdl'

log_dir = 'logs'
log_file = 'rum.log'
log_level = logging.INFO

watch_log_file = 'watchdog.log'
watch_log_level = logging.INFO
watchdog_search_str = 'rummager.py'

smtp_helo_email_address = 'rum@luka.sh'

smtp_port = 25
smtp_timeout = 6

'''
Local configuration
Add your all local configuration changes to the config_local.py file
'''
import os.path
if os.path.isfile('config_local.py'):
    from config_local import *

from config_env import *
