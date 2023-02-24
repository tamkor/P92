import json
from pathlib import Path


class ConfigReader:
    CONFIG_FILE_PATH = Path(__file__).resolve().parent / "servers_config.json"

    FILE_NOT_FOUND_ERROR_MSG = f"There is no config file at: {CONFIG_FILE_PATH}"
    JSON_ERROR_MSG = f"The config json file at {CONFIG_FILE_PATH} is invalid."
    KEY_ERROR_MSG = "Missing host, port, http_server or websocket_server value(s) from the config json file."

    def __init__(self):
        try:
            with open(self.CONFIG_FILE_PATH) as file:
                data = json.load(file)

            self.http_host = data["http_server"]["host"]
            self.http_port = data["http_server"]["port"]
            self.ws_host = data["websocket_server"]["host"]
            self.ws_port = data["websocket_server"]["port"]

        except FileNotFoundError:
            raise FileNotFoundError(self.FILE_NOT_FOUND_ERROR_MSG)

        except json.JSONDecodeError:
            raise ValueError(self.JSON_ERROR_MSG)

        except KeyError:
            raise KeyError(self.KEY_ERROR_MSG)
