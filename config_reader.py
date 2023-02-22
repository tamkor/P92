import json

from exception_types import ConfigReaderError


class ConfigReader:
    def __init__(self):
        try:
            with open("config.json") as file:
                data = json.load(file)

            self.http = data["http"]
            self.websocket = data["websocket"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            raise ConfigReaderError()


