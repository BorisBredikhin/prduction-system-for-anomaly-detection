from typing import Any, Tuple, TypedDict

"""
Пакет содержит базовые классы и функции для продукционных правил
"""


class KnowledgeBase:
    rules: list['Rule']


class Rule(TypedDict):
    antecedent: list  # условие
    consequent: Tuple[str, Any]  # действие
