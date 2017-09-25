
import logging
import sys
import os
import queue
import socket
import time
import ssl
import config

from src.worker_model_soap import Worker_Model_SOAP
from src.worker_model_soap_sender import Worker_Sender_Model_SOAP
from src.worker_pool_manager import Worker_Pool_Manager
from src.workers_manager import Workers_Manager

if config.allow_unverified_ssl == True:
    ssl._create_default_https_context = ssl._create_unverified_context

log_format='%(asctime)s T:%(thread)d %(levelname)s: %(message)s'
log_level = config.log_level

if config.log_type == 'stdout':
    logging.basicConfig(
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
        level=log_level
    )
else:
    logging.basicConfig(
        format=log_format,
        filename='%s/%s' % (config.log_dir, config.log_file),
        level=log_level
    )

PID = os.getpid()
hostname = socket.gethostname()
logging.info('MANAGER START - hostname: %s, pid: %s' % (hostname, PID))

logging.debug('CONFIG.soapurl: %s' %(config.soapurl,))
logging.debug('CONFIG.soapurl_sender: %s' %(config.soapurl_sender,))
logging.debug('CONFIG.log_dir: %s' %(config.log_dir,))
logging.debug('CONFIG.mainloop_delay: %s' %(config.mainloop_delay,))

model_soap = Worker_Model_SOAP()
model_sender_soap = Worker_Sender_Model_SOAP()

wm = Workers_Manager(hostname, logging, model_soap)

worker_smpt_pool_manager = Worker_Pool_Manager(
    'smtp',
    0,
    queue.Queue(),
    {'model': model_soap},
    wm.hostid,
    logging
)
wm.add_pool_manager(worker_smpt_pool_manager)

worker_sender_pool_manager = Worker_Pool_Manager(
    'smtp-sender',
    0,
    queue.Queue(),
    {'model': model_soap, 'model_sender': model_sender_soap},
    wm.hostid,
    logging)

wm.add_pool_manager(worker_sender_pool_manager)

while True:
    wm.run()
    time.sleep(config.mainloop_delay)
