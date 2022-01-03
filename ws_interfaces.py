from typing import NoReturn

from core import Core
from starlette.websockets import WebSocket
from utils import ConnectionManager


async def end_user_interface(manage: ConnectionManager, websocket: WebSocket) \
        -> NoReturn:
    core = Core('./example_data/rules.json')

    async def send_msg(msg: str):
        await manage.send_personal_message(msg, websocket)

    async def receive():
        return await websocket.receive_text()

    await core.loop_async(manage, websocket, send_msg, receive)
