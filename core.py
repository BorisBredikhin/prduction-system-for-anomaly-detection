from typing import Any

from data import database
from data._singleton import Singleton
from rules import KnowledgeBase


class Core:
    db: Singleton[dict[str, Any]]
    kb: KnowledgeBase

    def __init__(self):
        self.db = database
        self.kb = ... # todo: ooad knowledge base
