import json
from json.decoder import JSONDecodeError
from typing import Any

class Config:
    def __init__(self, configurationFile) -> None:
        self.file = configurationFile
        self.configuration = dict()

    def load(self) -> None:
        try:
            with open(self.file, "r") as configurationFile:
                configuration = json.load(configurationFile)
            configurationFile.close()

        except FileNotFoundError as e:
            print(e)


        self.configuration = configuration

    def update(self, var, value, changeStateForbidden = True):
        try:
            category = var.split(".")[0]
            variable = var.split(".")[1]

            # Cant change state of program
            if category == "state" and changeStateForbidden:
                raise PermissionError("PermissionError: You are not allowed to alter the state of the program through setting it directly.")

            # Check if variable exists
            if not category in self.configuration or not variable in self.configuration[category]:
                raise KeyError("KeyError: The variable you are trying to assign does not exist.")

            # Check if variable type is correct
            if not type(value) == type(self.configuration[category][variable]):
                raise ValueError(f"ValueError: Type of variable({ type(self.configuration[category][variable])}) and value({type(value)}) you are trying to assign don't match")

            # Assign variable to copy of current state
            newConfiguration = self.configuration
            newConfiguration[category][variable] = value

            # Write new state to file
            with open(self.file, "w") as configurationFile:
                json.dump(newConfiguration, configurationFile, indent=4)
            configurationFile.close()

            # Update internal state
            self.load()


        except PermissionError as e:
            print(e)
        except IndexError as e:
            print(e)
        except KeyError as e:
            print(e)
        except ValueError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)


    def get(self, var) -> Any:
        try:
            category = var.split(".")[0]
            variable = var.split(".")[1]

            return self.configuration[category][variable]

        except IndexError as e:
            print(e)
        except KeyError as e:
            print(e)

        return None

    def c__set(self, message):
        try:
            args = message.content.split(" ")

            var = args[1]
            category = var.split(".")[0]
            variable = var.split(".")[1]

            prefix_length = len(args[0]) + len(args[1]) + 2

            value = message.content[prefix_length:]
            val = type(self.configuration[category][variable])(value)
            self.update(var, val)

        except IndexError as e:
            return
        except TypeError as e:
            return

