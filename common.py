import typing

Command = typing.Literal['LOAD_INITIAL_DATA', 'INITIAL_DATA_LOADED', 'UPDATE']


class Message(typing.TypedDict):
    to: str
    cmd: Command
    params: typing.Optional[dict]
