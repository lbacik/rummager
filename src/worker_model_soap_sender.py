
from suds.client import Client
import config

class Worker_Sender_Model_SOAP:

    def __init__(self):
        self.c = Client(config.soapurl_sender)

    def get_address_to_check(self, checkId):
        result = self.c.service.getAddressToCheck(checkId)
        return [ result.sendId, result.addr ]

    def update_send_info(self, sendid, code, msg, conn_log):
        conn_log_srt = '|'.join(str(e) for e in conn_log)
        self.c.service.updateSendInfo(sendid, msg, conn_log_srt)
