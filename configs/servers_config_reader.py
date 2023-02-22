import json
from pathlib import Path


class ConfigReader:
    CONFIG_FILE_PATH = Path(__file__).resolve().parent / "servers_config.json"

    def __init__(self):
        try:
            with open(self.CONFIG_FILE_PATH) as file:
                data = json.load(file)

            self.http_host = data["http_server"]["host"]
            self.http_port = data["http_server"]["port"]
            self.ws_host = data["websocket_server"]["host"]
            self.ws_port = data["websocket_server"]["port"]

        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            raise RuntimeError("Something went wrong while handling the configs.json file.")
