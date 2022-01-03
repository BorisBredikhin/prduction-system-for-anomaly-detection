from queue import PriorityQueue
from typing import Optional

from common import Message, ReceiverMixin, Command
from rules import VariableInputType, VariableType

from starlette.websockets import WebSocket
from utils import ConnectionManager


class IOModule(ReceiverMixin):
    def read_variable(self, name: str, var_type: VariableInputType) -> Optional[VariableType]:
        pass

    def choose_interface(self, mq: PriorityQueue[Message]):
        pass

    def send(self, msg: Message, mq: PriorityQueue[Message], ):
        '''
        cmd = LOAD_INITIAL_DATA; params: input_variables
        '''
        if msg.cmd == Command.LOAD_INITIAL_DATA:
            for i in msg.params['input_variables']:
                self.send(Message(
                        to='io',
                        cmd=Command.READ,
                        params={
                            'name': i['name'],
                            'type': i['type']
                        },
                        priority=1
                ), mq)
            mq.put(Message(to='core', cmd=Command.INITIAL_DATA_LOADED, params=None, priority=5))
        elif msg.cmd == Command.READ:
            mq.put(Message(
                    priority=5, to='db', cmd=Command.UPDATE,
                    params={
                        'name':  msg.params['name'],
                        'value': self.read_variable(msg.params['name'], msg.params['type'])
                    }
            ))
        elif msg.cmd == Command.CHOOSE_INTERFACE:
            self.choose_interface(mq)

    async def send_async(
            self, msg: Message, mq: PriorityQueue[Message],
            manage: ConnectionManager, websocket: WebSocket, send_msg, receive
    ):
        if msg.cmd == Command.LOAD_INITIAL_DATA:
            for i in msg.params['input_variables']:
                await self.send_async(Message(
                        to='io',
                        cmd=Command.READ,
                        params={
                            'name': i['name'],
                            'type': i['type']
                        },
                        priority=1
                ), mq, manage, websocket, send_msg, receive)
            mq.put(Message(to='core', cmd=Command.INITIAL_DATA_LOADED, params=None, priority=5))
        elif msg.cmd == Command.READ:
            mq.put(Message(
                    priority=5, to='db', cmd=Command.UPDATE,
                    params={
                        'name':  msg.params['name'],
                        'value': await self.read_variable_ws(
                                msg.params['name'], msg.params['type'], manage,
                                websocket, send_msg, receive
                        )
                    }
            ))
        elif msg.cmd == Command.CHOOSE_INTERFACE:
            await self.choose_interface_ws(msg, mq, manage, websocket, send_msg, receive)

    async def read_variable_ws(
            self, name: str, var_type: VariableInputType, manage: ConnectionManager,
            websocket: WebSocket, send_msg, receive
    ):
        raise NotImplemented

    async def choose_interface_ws(
            self, msg: Message, mq: PriorityQueue[Message], manage: ConnectionManager,
            websocket: WebSocket, send_msg,
            receive
    ):
        raise Exception("NI")

    def convert_variable(self, value, var_type):
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


class CLIOModule(IOModule):

    def read_variable(self, name: str, var_type: VariableInputType) -> Optional[VariableType]:
        value = input(f'Ввеите значение переменной {name} или "None", если значение не известно: ')
        return self.convert_variable(value, var_type)

    def choose_interface(self, mq: PriorityQueue[Message]):
        # todo
        pass


class WSIOModule(IOModule):

    async def read_variable_ws(
            self, name: str, var_type: VariableInputType, manage: ConnectionManager, websocket, send_msg, receive
    ):
        await manage.send_personal_message(f'Ввеите значение переменной {name} или "None", если значение не известно: ',
                                           websocket)
        return self.convert_variable((await websocket.receive_json())['query'], var_type)

    async def choose_interface_ws(
            self, msg: Message, mq: PriorityQueue[Message], manage: ConnectionManager, websocket: WebSocket, send_msg,
            receive
    ):
        await manage.send_personal_message("Выберите вашу роль(0 - конечный пользователь, 1 - эксперт):", websocket)
        resp = int((await websocket.receive_json())['query'])
        mq.put(Message(10, 'core', Command.INTERFACE_CHOSEN, {'interface': resp}))
