import typing
from queue import PriorityQueue

from common import ReceiverMixin, Message, Command
from io_module import IOModule
from rules import VariableType, KnowledgeBase, ElementaryAntecedent
from starlette.websockets import WebSocket
from user_interfaces import CLIUserInterface, WSUserInterface
from utils import ConnectionManager


class DecisionMaker(ReceiverMixin):
    async def send_async(
            self, msg: Message, mq: PriorityQueue[Message], manage: ConnectionManager, websocket: WebSocket, send_msg,
            receive
    ):
        if msg.cmd == Command.BEGIN_INFERENCE:
            await self.begin_inference_async(manage, websocket)

    db: dict[str, VariableType]
    io_mod: IOModule
    kb: KnowledgeBase
    mq: PriorityQueue[Message]
    ui: WSUserInterface

    def __init__(
            self, ui: CLIUserInterface, db: dict[str, VariableType],
            kb: KnowledgeBase, mq: PriorityQueue[Message], io_mod: IOModule
    ):
        self.io_mod = io_mod
        self.mq = mq
        self.kb = kb
        self.db = db
        self.ui = ui

    def send(self, msg: Message, mq: PriorityQueue[Message]) -> typing.NoReturn:
        if msg.cmd == Command.BEGIN_INFERENCE:
            self.begin_inference(print)

    async def get_additional_data(self, param, manage, websocket):
        await manage.send_personal_message(
                f"Требуются дополнительные данные:\n"
                f"{param[0]}: {param[1]['type']} ({param[1]['description']})",
                websocket,
        )
        value = self.io_mod.convert_variable((await websocket.receive_json())['query'], param[1]['type'])
        self.db[param[0]] = value

    async def begin_inference_async(self, manage: ConnectionManager, websocket: WebSocket):
        while True:
            used_any_rule = False
            for rule in self.kb['rules']:
                if self.try_ancetedent(rule['antecedent']):
                    used_any_rule = True
                    await manage.send_personal_message(f"Применяется правило {rule}", websocket)
                    if isinstance(rule['consequent'][1], dict) and rule['consequent'][0] not in self.db.keys():
                        await self.get_additional_data(rule['consequent'], manage, websocket)
                    if 'recommendation' in rule.keys():
                        await manage.send_personal_message(f"**Рекомендация**: {rule['recommendation']}",
                                                           websocket)  # todo: move to tracer
                    if rule['consequent'][0] == 'result':
                        await manage.send_personal_message(f"ВЫВОД: {rule['consequent'][1]}", websocket)
                        return
                    elif not isinstance(rule['consequent'][1], list):
                        await manage.send_personal_message(f"{rule['consequent'][0]} = {rule['consequent'][1]}",
                                                           websocket)
                        self.db[rule['consequent'][0]] = rule['consequent'][1]
                    else:
                        await manage.send_personal_message(
                                f"{rule['consequent'][0]}={rule['consequent'][1]}={self.calculate(rule['consequent'][1])}",
                                websocket)
                        self.db[rule['consequent'][0]] = self.calculate(rule['consequent'][1])
            if not used_any_rule:
                await manage.send_personal_message(
                        "Отсутствуют правила для вашего случая. Обратитесь к эксперту для пополнения базы данных",
                        websocket)
                return

    def begin_inference(self, show: typing.Callable[[str], typing.NoReturn]):
        while True:
            for rule in self.kb['rules']:
                if self.try_ancetedent(rule['antecedent']):
                    show(f"Применяется правило {rule}")
                    if 'recommendation' in rule.keys():
                        print("**Рекомендация**:", rule['recommendation'])  # todo: move to tracer
                    if rule['consequent'][0] == 'result':
                        print(f"ВЫВОД: {rule['consequent'][1]}")
                        return
                    elif not isinstance(rule['consequent'][1], list):
                        print(f"{rule['consequent'][0]} = {rule['consequent'][1]}")
                        self.db[rule['consequent'][0]] = rule['consequent'][1]
                    else:
                        print(
                                f"{rule['consequent'][0]}={rule['consequent'][1]}={self.calculate(rule['consequent'][1])}")
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
