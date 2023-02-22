import logging

import uvicorn
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from config_reader import ConfigReader
from exception_types import ConfigReaderError

app = FastAPI()


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logging.info("Websocket connected!")
    try:
        while True:
            received_data = await websocket.receive_text()
            await websocket.send_text(received_data)
    except WebSocketDisconnect:
        logging.info("Websocket disconnected!")


if __name__ == "__main__":
    config = ConfigReader()
    logging.basicConfig(level=logging.INFO)
    try:
        uvicorn.run(app, host=config.websocket["host"], port=config.websocket["port"])
    except KeyError:
        raise ConfigReaderError("Host and port keys and values are required under"
                                "the 'websocket' key in the config.json!")
