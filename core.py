from queue import PriorityQueue

from common import Message, InterfaceType, Command
from data import database
from decsion_maker import DecisionMaker
from io_module import IOModule, CLIOModule, WSIOModule
from rules import KnowledgeBase, load_kowledge_base, VariableType
from starlette.websockets import WebSocket
from user_interfaces import CLIUserInterface
from user_interfaces.user_interface import WSUserInterface
from utils import ConnectionManager


class Core:
    db: dict[str, VariableType]
    kb: KnowledgeBase
    io_mod: IOModule
    mq: PriorityQueue[Message]
    user_interface: WSUserInterface
    decsion_maker: DecisionMaker
    interface_Type: InterfaceType

    def __init__(self, path_to_knowedge_base: str):
        self.db = database.value
        self.kb = load_kowledge_base(path_to_knowedge_base)
        self.io_mod = WSIOModule()
        self.mq = PriorityQueue()
        self.user_interface = WSUserInterface(self.io_mod)
        self.mq.put(Message(priority=5, to='core', cmd=Command.CHOOSE_INTERFACE, params=None))

        self.decsion_maker = DecisionMaker(self.user_interface, self.db, self.kb, self.mq, self.io_mod)

    def loop(self):
        while self.mq.qsize() > 0:
            msg = self.mq.get()
            if msg.to == 'io':
                self.io_mod.send(msg, self.mq)
            elif msg.to == 'db':
                self.process_db_message(msg)
            elif msg.to == 'core':
                if msg.cmd == Command.INITIAL_DATA_LOADED:
                    self.mq.put(Message(
                        priority=0,
                        to='decision_maker',
                        cmd=Command.BEGIN_INFERENCE,
                        params=None
                    ))
                elif msg.cmd == Command.CHOOSE_INTERFACE:
                    self.io_mod.send(msg, self.mq)
            elif msg.to == "decision_maker":
                self.decsion_maker.send(msg, self.mq)
            elif msg.to == 'ui':
                self.user_interface.send(msg, self.mq)
            else:
                raise Exception('Wrong message', msg)

    def process_db_message(self, msg: Message):
        if msg.cmd == Command.UPDATE:
            self.db[msg.params['name']] = msg.params['value']

    async def loop_async(self, manage: ConnectionManager, websocket: WebSocket, send_msg, receive):
        while self.mq.qsize() > 0:
            msg = self.mq.get()
            if msg.to == 'io':
                await self.io_mod.send_async(msg, self.mq, manage, websocket, send_msg, receive)
            elif msg.to == 'db':
                self.process_db_message(msg)
            elif msg.to == 'core':
                if msg.cmd == Command.INITIAL_DATA_LOADED:
                    self.mq.put(Message(
                        priority=0,
                        to='decision_maker',
                        cmd=Command.BEGIN_INFERENCE,
                        params=None
                    ))
                elif msg.cmd == Command.CHOOSE_INTERFACE:
                    await self.io_mod.send_async(msg, self.mq, manage, websocket, send_msg, receive)
                elif msg.cmd == Command.INTERFACE_CHOSEN:
                    if msg.params['interface'] == 0:
                        self.mq.put(Message(5, 'ui', Command.LOAD_INITIAL_DATA, {'input_variables': self.kb['input_variables']}))
                    else:
                        raise NotImplemented
                elif msg.cmd == Command.LOAD_INITIAL_DATA:
                    await self.io_mod.send_async(msg, self.mq, manage, websocket, send_msg, receive)
            elif msg.to == "decision_maker":
                await self.decsion_maker.send_async(msg, self.mq, manage, websocket, send_msg, receive)
            elif msg.to == 'ui':
                await self.user_interface.send_async(msg, self.mq, manage, websocket, send_msg, receive)
            else:
                raise Exception('Wrong message', msg)

