import abc
import typing
from collections import deque
import enum
from dataclasses import dataclass, field


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


@dataclass(order=True)
class Message:
    priority: int
    to: str = field(compare=False)
    cmd: Command = field(compare=False)
    params: typing.Optional[dict] = field(compare=False)

class ReceiverMixin(abc.ABC):
    @abc.abstractmethod
    def send(self, msg: Message, mq: deque[Message]):
        pass
