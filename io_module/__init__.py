import abc
from collections import deque
from typing import Optional

from common import Message, ReceiverMixin, Command
from rules import VariableInputType, VariableType


#todo: разделить с интерфейсом пользователя

class IOModule(ReceiverMixin, abc.ABC):
    @abc.abstractmethod
    def read_variable(self, name: str, var_type: VariableInputType) -> Optional[VariableType]:
        pass

    @abc.abstractmethod
    def choose_interface(self9, mq: deque[Message]):
        pass

    def send(self, msg: Message, mq: deque[Message]):
        '''
        cmd = LOAD_INITIAL_DATA; params: input_variables
        '''
        if msg['cmd'] == Command.LOAD_INITIAL_DATA:
            for i in msg['params']['input_variables']:
                self.send(Message(
                    to='io',
                    cmd=Command.READ,
                    params={
                        'name': i['name'],
                        'type': i['type']
                    }
                ), mq)
            mq.append(Message(to='core', cmd=Command.INITIAL_DATA_LOADED, params=None))
        elif msg['cmd'] == Command.READ:
            mq.append({
                'to': 'db',
                'cmd': Command.UPDATE,
                'params': {
                    'name': msg['params']['name'],
                    'value': self.read_variable(msg['params']['name'], msg['params']['type'])
                }
            })
        elif msg['cmd'] == Command.CHOOSE_INTERFACE:
            self.choose_interface(mq)


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

    def choose_interface(self9, mq: deque[Message]):
        # todo
        pass
