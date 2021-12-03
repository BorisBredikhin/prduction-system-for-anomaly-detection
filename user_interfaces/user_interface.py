from collections import deque

from common import ReceiverMixin, Message
from io_module import IOModule


class CLIUserInterface(ReceiverMixin):
    iom: IOModule

    def __init__(self, iom):
        self.iom = iom

    def send(self, msg: Message, mq: deque[Message]):
        """
        msg:
        {
            "cmd': "READ",
            "params": {
                "name": "string',
                "type': "string'
            }
        }
        cmd='LOAD_INITIAL_DATA', params={'input_variables': self.kb['input_variables'
        """
        if msg['cmd'] == 'LOAD_INITIAL_DATA':
            self.iom.send(msg, mq)

