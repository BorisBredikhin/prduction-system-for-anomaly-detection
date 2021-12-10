import abc
import typing
from collections import deque
import enum

@enum.unique
class Command(enum.Enum):
    BEGIN_INFERENCE = enum.auto()
    CHOOSE_INTERFACE = enum.auto()
    LOAD_INITIAL_DATA = enum.auto()
    INITIAL_DATA_LOADED = enum.auto()
    READ = enum.auto()
    UPDATE = enum.auto()


@enum.unique
class InterfaceType(enum.Enum):
    EXPERT = enum.auto()
    USER = enum.auto()


class Message(typing.TypedDict):
    to: str
    cmd: Command
    params: typing.Optional[dict]

class ReceiverMixin(abc.ABC):
    @abc.abstractmethod
    def send(self, msg: Message, mq: deque[Message]):
        pass
