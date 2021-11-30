from data import database
from io_module import IOModule, CLIIOMddule
from rules import KnowledgeBase, load_kowledge_base, VariableType


class Core:
    db: dict[str, VariableType]
    kb: KnowledgeBase
    io_mod: IOModule

    def __init__(self, path_to_knowedge_base: str):
        self.db = database.value
        self.kb = load_kowledge_base(path_to_knowedge_base)
        self.io_mod = CLIIOMddule()

    def load_initial_vars(self):
        for i in self.kb['input_variables']:
            self.db[i['name']] = self.io_mod.read_variable(i['name'], i['type'])
        print(self.db)
