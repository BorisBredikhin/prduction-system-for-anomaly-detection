from queue import PriorityQueue

from common import Message, InterfaceType, Command
from data import database
from decsion_maker import DecisionMaker
from io_module import IOModule, CLIIOMddule
from rules import KnowledgeBase, load_kowledge_base, VariableType
from user_interfaces import CLIUserInterface


class Core:
    db: dict[str, VariableType]
    kb: KnowledgeBase
    io_mod: IOModule
    mq: PriorityQueue[Message]
    user_interface: CLIUserInterface
    decsion_maker: DecisionMaker
    interface_Type: InterfaceType

    def __init__(self, path_to_knowedge_base: str):
        self.db = database.value
        self.kb = load_kowledge_base(path_to_knowedge_base)
        self.io_mod = CLIIOMddule()
        self.mq = PriorityQueue()
        self.user_interface = CLIUserInterface(self.io_mod)
        self.mq.put(Message(priority=5, to='core', cmd=Command.CHOOSE_INTERFACE, params=None))
        self.mq.put(Message(priority=5, to='ui', cmd=Command.LOAD_INITIAL_DATA,
                            params={'input_variables': self.kb['input_variables']}))

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
