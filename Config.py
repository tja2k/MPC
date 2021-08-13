import json
from os import read

class Config:
    def __init__(self) -> None:
        self.file = ""

    def load(self, file):
        with open("configuration.json", "r") as readConfiguration:
            configuration = json.load(readConfiguration)
        readConfiguration.close()

        print(configuration)