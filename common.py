import abc
import typing
from collections import deque

Command = typing.Literal[
    'LOAD_INITIAL_DATA',
    'INITIAL_DATA_LOADED',
    'READ',
    'UPDATE',
]


class Message(typing.TypedDict):
    to: str
    cmd: Command
    params: typing.Optional[dict]

class ReceiverMixin(abc.ABC):
    @abc.abstractmethod
    def send(self, msg: Message, mq: deque[Message]):
        pass
