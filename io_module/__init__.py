import abc
from collections import deque
from typing import Optional

from common import Message
from rules import VariableInputType, VariableType


#todo: разделить с интерфейсом пользователя

class IOModule(abc.ABC):
    @abc.abstractmethod
    def read_variable(self, name: str, var_type: VariableInputType) -> Optional[VariableType]:
        pass

    def send(self, msg: Message, mq: deque[Message]):
        if msg['cmd'] == 'LOAD_INITIAL_DATA':
            for i in msg['params']['input_variables']:
                mq.append({
                    'to': 'db',
                    'cmd': 'UPDATE',
                    'params': {
                        'name': i['name'],
                        'value': self.read_variable(i['name'], i['type'])
                    }
                })
            mq.append(Message(to='cpre', cmd='INITIAL_DATA_LOADED', params=None))


class CLIIOMddule(IOModule):

    def read_variable(self, name: str, var_type: VariableInputType) -> Optional[VariableType]:
        value = input(f'Ввеите значение переменной {name} или None, если значение не известно: ')
        # todo
        if value == 'None':
            return None
        if var_type == 'bool':
            return bool(value)
        if var_type == 'float':
            return float(value)
        if var_type == 'int':
            return int(value)
        if var_type == 'str':
            return value
        raise TypeError(f"Недопустимое значение {var_type=}.")
