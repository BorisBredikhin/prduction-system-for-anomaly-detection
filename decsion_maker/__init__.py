import typing
from queue import PriorityQueue

from common import ReceiverMixin, Message, Command
from io_module import IOModule
from rules import VariableType, KnowledgeBase, ElementaryAntecedent
from user_interfaces import CLIUserInterface


class DecisionMaker(ReceiverMixin):
    db: dict[str, VariableType]
    io_mod: IOModule
    kb: KnowledgeBase
    mq: PriorityQueue[Message]
    ui: CLIUserInterface

    def __init__(self, ui: CLIUserInterface, db: dict[str, VariableType],
                 kb: KnowledgeBase, mq: PriorityQueue[Message], io_mod: IOModule):
        self.io_mod = io_mod
        self.mq = mq
        self.kb = kb
        self.db = db
        self.ui = ui

    def send(self, msg: Message, mq: PriorityQueue[Message]) -> typing.NoReturn:
        if msg.cmd == Command.BEGIN_INFERENCE:
            self.begin_inference()

    def begin_inference(self):
        while True:
            for rule in self.kb['rules']:
                if self.try_ancetedent(rule['antecedent']):
                    print(f"Применяется правило {rule}")
                    if 'recommendation' in rule.keys():
                        print("**Рекомендация**:", rule['recommendation']) # todo: move to tracer
                    if rule['consequent'][0] == 'result':
                        print(f"ВЫВОД: {rule['consequent'][1]}")
                        return
                    elif not isinstance(rule['consequent'][1], list):
                        print(f"{rule['consequent'][0]} = {rule['consequent'][1]}")
                        self.db[rule['consequent'][0]] = rule['consequent'][1]
                    else:
                        print(f"{rule['consequent'][0]}={rule['consequent'][1]}={self.calculate(rule['consequent'][1])}")
                        self.db[rule['consequent'][0]] = self.calculate(rule['consequent'][1])

    def try_ancetedent(self, antecedent: list[ElementaryAntecedent]) -> bool:
        return all(self.try_elementwary_ancetedent(x) for x in antecedent)

    def try_elementwary_ancetedent(self, elementwary_ancetedent: ElementaryAntecedent) -> bool:
        var_name, op, expr = elementwary_ancetedent
        if var_name not in self.db.keys():
            return False
        var_val = self.db[var_name]
        if op == '<': return var_val < expr
        if op == '<=': return var_val <= expr
        if op == '==': return var_val == expr
        if op == '!=': return var_val != expr
        if op == '>=': return var_val >= expr
        if op == '>': return var_val > expr

    def calculate(self, expr: list):
        fst = self.calculate(expr[1]) if isinstance(expr[1], list) else expr[1]
        snd = self.calculate(expr[2]) if isinstance(expr[2], list) else expr[2]

        if fst[0] == '$': fst = self.db[fst]
        if snd[0] == '$': snd = self.db[snd]

        if expr[0] == '+': return fst + snd
        if expr[0] == '-': return fst - snd
        if expr[0] == '*': return fst * snd
        if expr[0] == '/': return fst / snd

        if expr[0] == '<': return fst < snd
        if expr[0] == '<=': return fst <= snd
        if expr[0] == '==': return fst == snd
        if expr[0] == '!=': return fst != snd
        if expr[0] == '>=': return fst >= snd
        if expr[0] == '>': return fst > snd
