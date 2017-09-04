
from worker_smtp import Worker_SMTP as SMTP
from worker_sender import Worker_Sender as SENDER

class Worker_Factory:

    def create(self, worker_type_name, models, hostid, logger):

        if worker_type_name == 'smtp':
            worker = SMTP(models.get('model'), hostid, logger)
        elif worker_type_name == 'smtp-sender':
            worker = SENDER(models['model'], models['model_sender'], hostid, logger)
        else:
            raise Exception('Unknow worker type: %s' % (worker_type_name,))

        return worker
