import json
import logging
import socket

import uvicorn
import websockets
from fastapi import FastAPI, Request, HTTPException
from starlette import status

from config_reader import ConfigReader
from exception_types import ConfigReaderError

app = FastAPI()


@app.post("/api/ui")
async def forward(request: Request):
    try:
        logging.info("Request arrived to the gateway, trying to forward it to the websocket server.")
        request_data = await request.json()
        websocket_host = config.websocket["host"]
        websocket_port = config.websocket["port"]

        async with websockets.connect(f"ws://{websocket_host}:{websocket_port}") as websocket:
            await websocket.send(json.dumps(request_data))
            websocket_raw_response = await websocket.recv()

        websocket_reply = json.loads(websocket_raw_response)
        logging.info("Response arrived to the gateway from the websocket server.")
        return websocket_reply

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="The given data or the received reply from the websocket server is not a valid JSON!")

    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Host and port keys and values are required under the 'websocket' key in the config.json!")

    except socket.gaierror:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Something went wrong while trying to connect to the websocket server.")


if __name__ == "__main__":
    config = ConfigReader()
    logging.basicConfig(level=logging.INFO)
    try:
        uvicorn.run(app, host=config.http["host"], port=config.http["port"])
    except KeyError:
        raise ConfigReaderError("Host and port keys and values are required under the 'http' key in the config.json!")
