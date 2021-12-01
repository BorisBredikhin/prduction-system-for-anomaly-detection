from collections import deque

from common import Message
from data import database
from io_module import IOModule, CLIIOMddule
from rules import KnowledgeBase, load_kowledge_base, VariableType


class Core:
    db: dict[str, VariableType]
    kb: KnowledgeBase
    io_mod: IOModule
    mq: deque[Message]

    def __init__(self, path_to_knowedge_base: str):
        self.db = database.value
        self.kb = load_kowledge_base(path_to_knowedge_base)
        self.io_mod = CLIIOMddule()
        self.mq = deque()
        self.mq.append(Message(to='io', cmd='LOAD_INITIAL_DATA', params={'input_variables': self.kb['input_variables']}))

    def loop(self):
        while len(self.mq)>0:
            msg = self.mq.popleft()
            if msg['to'] == 'io':
                self.io_mod.send(msg, self.mq)
            elif msg['to'] == 'db':
                self.process_db_message(msg)
            elif msg['to'] == 'core':
                if msg['cmd'] == 'INITIAL_DATA_LOADED':
                    # todo: начать логический вывод
                    pass
            else:
                raise Exception('Wrong message', msg)

    def process_db_message(self, msg):
        if msg['cmd'] == 'UPDATE':
            self.db[msg['params']['name']] = msg['params']['value']
