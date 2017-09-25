
import config
from .worker import Worker
from .worker import DieException
import smtplib
import time
from email.message import Message

class Worker_Sender(Worker):

    def __init__(self, model, model_sender, hostid, logger):
        Worker.__init__(self, model, hostid, logger)
        self.model_sender = model_sender
        self.module = 'smtp-sender'
        self.moduleid = self.model.get_module_id(self.module)
        self.log.info('Constructor - Worker Sender (moduleid: %s)'
                      % (self.moduleid,))

    def run(self):
        infinity = True
        while infinity:
            try:

                self.log.info('** SENDER nodeid: %s, moduleid: %s' % (self.nodeid, self.moduleid))
                self.checkid = self.model.start_new_check(self.nodeid, self.moduleid)
                self.log.info('** checkid: %s' % (self.checkid,))

                while True:

                    (sendid, address) = self.model_sender.get_address_to_check(self.checkid)
                    self.log.info('SENDER: checkid: %s, sendid: %s, address: %s' % (self.checkid, sendid, address))
                    if sendid == 0:
                        raise Exception("SENDER: no address to check...")
                    (code, msg, conn_log) = self.send_msg(address, sendid)
                    self.log.info('SENDER: checkid: %s, code: %s' % (self.checkid, code))
                    self.model_sender.update_send_info(sendid, code, msg, conn_log)
                    self.check_msg_queue()

            except DieException:
                self.log.info('dying... bye, bye...');
                infinity = False

            except Exception as e:
                self.log.error(' *** Exception *** WORKER Sender: %s' % (e.__str__(),))
                time.sleep(10)
                infinity = False

    def send_msg(self, address, sendid):

        code = self.generate_code(sendid)
        msg = self.generate_msg(code, sendid)
        conn_log = []

        try:
            smtp = smtplib.SMTP(timeout=config.smtp_timeout)
            conn_log.append(smtp.connect(address))
            conn_log.append(smtp.helo(config.smtp_helo_email_address))
            smtp.send_message(msg)
            smtp.quit()
        except Exception as e:
            self.log.error('SENDER: unable to send email - %s' % (e.__str__(),))

        return (code, msg.__str__(), conn_log)

    def generate_code(self, sendid):
        return 'SendID: %s' % (sendid,)

    def generate_msg(self, code, sendid):
        msg = Message()
        msg.set_payload(code)
        msg['Subject'] = 'Rummager (sendid: %s)' % (sendid,)
        msg['From'] = 'ws@rummager.net'
        msg['To'] = 'rummager@luka.sh'
        return msg
