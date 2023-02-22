import logging

from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

app = FastAPI()


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            received_data = await websocket.receive_text()
            logging.info("Data arrived from the gateway, trying to send it back.")
            await websocket.send_text(received_data)
    except WebSocketDisconnect:
        pass  # intentionally - disconnecting after the HTTP reply in the http_server is is expected behavior.
