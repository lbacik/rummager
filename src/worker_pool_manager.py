
from .worker_factory import Worker_Factory
import threading

class Worker_Pool_Manager:

    def __init__(self, worker_type_name, pool_size, msg_queue, models, hostid, logger):
        self.worker_type_name = worker_type_name
        self.pool_size = pool_size
        self.msg_queue = msg_queue
        self.models = models
        self.hostid = hostid
        self.log = logger

    def start_worker(self):
        factory = Worker_Factory()
        worker = factory.create(self.worker_type_name, self.models, self.hostid, self.log)
        worker.set_msg_queue(self.msg_queue)
        worker.start()

    def adjust_pool_size(self, new_pool_size):

        self.pool_size = new_pool_size

        # threads that are currently running
        actual_size = self.get_actual_pool_size()

        delta = self.pool_size - actual_size

        if delta > 0:
            # increment
            for i in range(0, delta):
                self.start_worker()

        elif delta < 0:
            # decrement
            for i in range(0, abs(delta)):
                self.log.debug(' * Putting DIE into msg queue...')
                self.msg_queue.put('DIE');


    def get_actual_pool_size(self):
        count = 0
        for w in threading.enumerate():
            if hasattr(w, 'module') and w.module == self.worker_type_name:
                count = count + 1
        self.log.debug('%s pool manager - get_actual_pool_size: %d' % (self.worker_type_name, count))
        return count
