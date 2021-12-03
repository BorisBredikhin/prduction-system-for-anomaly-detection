from collections import deque

from common import ReceiverMixin, Message
from io_module import IOModule
from rules import VariableType, KnowledgeBase
from user_interfaces import CLIUserInterface


class DecisionMaker(ReceiverMixin):
    db: dict[str, VariableType]
    io_mod: IOModule
    kb: KnowledgeBase
    mq: deque[Message]
    ui: CLIUserInterface

    def __init__(self, ui: CLIUserInterface, db: dict[str, VariableType],
                 kb: KnowledgeBase, mq: deque[Message], io_mod: IOModule):
        self.io_mod = io_mod
        self.mq = mq
        self.kb = kb
        self.db = db
        self.ui = ui

    def send(self, msg: Message, mq: deque[Message]):
        pass
