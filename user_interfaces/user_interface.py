from queue import PriorityQueue

from common import ReceiverMixin, Message, Command
from io_module import IOModule


class CLIUserInterface(ReceiverMixin):
    iom: IOModule

    def __init__(self, iom):
        self.iom = iom

    def send(self, msg: Message, mq: PriorityQueue[Message]):
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
        if msg.cmd == Command.LOAD_INITIAL_DATA:
            self.iom.send(msg, mq)

