
import logging, os, queue, socket, time
import config

import sys
sys.path.append('src')

from worker_model_soap import Worker_Model_SOAP
from worker_model_soap_sender import Worker_Sender_Model_SOAP
from worker_pool_manager import Worker_Pool_Manager
from workers_manager import Workers_Manager

logging.basicConfig(format='%(asctime)s T:%(thread)d %(levelname)s: %(message)s',
                    filename='%s/%s' % (config.log_dir, config.log_file),
                    level=config.log_level)

PID = os.getpid()
hostname = socket.gethostname()
logging.info('MANAGER START - hostname: %s, pid: %s' % (hostname, PID))

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
