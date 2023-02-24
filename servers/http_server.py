import json
import logging
import socket

import websockets
from fastapi import FastAPI, Request, HTTPException
from starlette import status

from configs.servers_config_reader import ConfigReader

http_server_app = FastAPI()
servers_config = ConfigReader()

JSON_ERROR_MSG = "The given data or the received reply from the websocket server is not a valid JSON!"
WS_ERROR_MSG = "Something went wrong while trying to connect to the websocket server."


@http_server_app.post("/api/ui")
async def forward(request: Request):
    try:
        logging.info("Request arrived to the gateway, trying to forward it to the websocket server.")
        request_data = await request.json()

        async with websockets.connect(f"ws://{servers_config.ws_host}:{servers_config.ws_port}") as websocket:
            await websocket.send(json.dumps(request_data))
            websocket_raw_response = await websocket.recv()

        websocket_reply = json.loads(websocket_raw_response)
        logging.info("Response arrived to the gateway from the websocket server.")
        return websocket_reply

    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=JSON_ERROR_MSG)

    except (socket.gaierror, ConnectionRefusedError):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=WS_ERROR_MSG)
