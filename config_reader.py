import json


class ConfigReader:
    def __init__(self):
        with open("config.json") as file:
            data = json.load(file)

        self.http = data["http"]
        self.websocket = data["websocket"]
