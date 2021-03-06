import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from utils import ConnectionManager
from ws_interfaces import end_user_interface

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>

"""

manager: ConnectionManager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)


async def start_user_interface(websocket: WebSocket):
    pass


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        data = await websocket.receive_text()
        await manager.send_personal_message(f"Accepted", websocket)
        await websocket.receive_text()
        # await manager.send_personal_message(f"Выберите вашу роль(0 - конечный польователь, 1 - эксперт):", websocket)
        #
        # role = await websocket.receive_json()
        # if role['query'] == '0':
            # end user
        await end_user_interface(manager, websocket)
            # await manager.send_personal_message('Не реализовано', websocket)
        # elif role['query'] == '1':
        #     # expert
        #     await manager.send_personal_message('Не реализовано', websocket)
        # await start_user_interface(websocket)
        pass
    except WebSocketDisconnect:

        manager.disconnect(websocket)

        await manager.broadcast(f"Client #{client_id} left the chat")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
