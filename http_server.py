import json

import uvicorn
import websockets
from fastapi import FastAPI, Request

from config_reader import ConfigReader

app = FastAPI()
config = ConfigReader()


@app.post("/api/ui")
async def forward(request: Request):
    request_data = await request.json()
    websocket_host = config.websocket["host"]
    websocket_port = config.websocket["port"]

    async with websockets.connect(f"ws://{websocket_host}:{websocket_port}") as websocket:
        await websocket.send(json.dumps(request_data))
        websocket_response = await websocket.recv()

    return json.loads(websocket_response)


if __name__ == "__main__":
    uvicorn.run(app, host=config.http["host"], port=config.http["port"])
