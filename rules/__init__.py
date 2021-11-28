from __future__ import annotations

from typing import Any, Tuple, TypedDict, Optional

"""
Пакет содержит базовые классы и функции для продукционных правил
"""


class KnowledgeBase(TypedDict):
    rules: list['Rule']


class ElementaryAntecedent(TypedDict):
    variable_name: str
    op: str
    expr: str | int | float


class Rule(TypedDict):
    antecedent: list[ElementaryAntecedent]  # условие
    consequent: Tuple[str, Any]  # действие
    recommendation: Optional[str]

