import uvicorn
from fastapi import FastAPI, WebSocket

from config_reader import ConfigReader

app = FastAPI()
config = ConfigReader()


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        received_data = await websocket.receive_text()
        await websocket.send_text(received_data)


if __name__ == "__main__":
    uvicorn.run(app, host=config.websocket["host"], port=config.websocket["port"])
