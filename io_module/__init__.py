import abc
from typing import Optional

from rules import VariableInputType, VariableType

#todo: разделить с интерфейсом пользователя

class IOModule(abc.ABC):
    @abc.abstractmethod
    def read_variable(self, name: str, var_type: VariableInputType) -> Optional[VariableType]:
        pass


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
