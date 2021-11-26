from typing import TypedDict

"""
Пакет содержит базовые классы и функции для продукционных правил
"""

class Rule(TypedDict):
    antecedent # условие
    consequen # действие
