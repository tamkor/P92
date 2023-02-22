import uvicorn
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from config_reader import ConfigReader

app = FastAPI()


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Connected!")
    try:
        while True:
            received_data = await websocket.receive_text()
            await websocket.send_text(received_data)
    except WebSocketDisconnect:
        print("Disconnected!")


if __name__ == "__main__":
    config = ConfigReader()
    uvicorn.run(app, host=config.websocket["host"], port=config.websocket["port"])
