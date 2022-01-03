from collections import deque
from queue import PriorityQueue

from common import ReceiverMixin, Message, Command
from io_module import WSIOModule, CLIOModule
from starlette.websockets import WebSocket
from utils import ConnectionManager


class CLIUserInterface(ReceiverMixin):
    iom: CLIOModule

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


class WSUserInterface(ReceiverMixin):
    def send(self, msg: Message, mq: deque[Message]):
        raise Exception("NI")

    async def send_async(self, msg, mq, manage: ConnectionManager, websocket: WebSocket, send_msg, receive):
        if msg.cmd == Command.LOAD_INITIAL_DATA:
            await self.iom.send_async(msg, mq, manage, websocket, send_msg, receive)

    iom: WSIOModule

    def __init__(self, iom):
        self.iom = iom

