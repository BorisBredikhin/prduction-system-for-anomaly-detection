import json
from typing import Any, Tuple, TypedDict, Optional, Literal, Union

"""
Пакет содержит базовые классы и функции для продукционных правил
"""

VariableInputType = Literal['bool', 'float', 'int', 'str']
VariableType = Union[str, int, float, bool]


class KnowledgeBase(TypedDict):
    rules: list['Rule']
    input_variables: list['InputVariable']


ElementaryAntecedent = list


class Rule(TypedDict):
    antecedent: list[ElementaryAntecedent]  # условие
    consequent: Tuple[str, Any]  # действие
    recommendation: Optional[str]


class InputVariable(TypedDict):
    name: str
    type: VariableInputType
    description: str


def load_kowledge_base(path_to_file) -> KnowledgeBase:
    f = open(path_to_file, 'r')
    kb = json.load(f)
    f.close()
    return kb
