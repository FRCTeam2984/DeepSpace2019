import json
import math


class Constants:
    """Global constants that are accesed throughout the project"""
    LEFT_MOTOR_SLAVE_ID = 23
    LEFT_MOTOR_MASTER_ID = 28
    RIGHT_MOTOR_SLAVE_ID = 12
    RIGHT_MOTOR_MASTER_ID = 22

    CONSTANTS_JSON_PATH = "/home/lvuser/py_constants.json"

    WHEEL_DIAMETER = 6  # inches
    WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER*math.pi  # inches
    WHEEL_BASE = 27.75  # inches (distance between wheels)

    DRIVE_ENCODER_TICKS_PER_REVOLUTION_LEFT = 4096  # UPDATE
    DRIVE_ENCODER_TICKS_PER_REVOLUTION_RIGHT = 4096  # UPDATE

    TANK_DRIVE_EXPONENT = 3

    @staticmethod
    def updateConstants():
        try:
            json_file = open(Constants.CONSTANTS_JSON_PATH, "r")
            file_dict = json.load(json_file)
            json_file.close()
            for var_name in file_dict.keys():
                if hasattr(Constants, var_name):
                    setattr(Constants, var_name, file_dict[var_name])
        except FileNotFoundError:
            try:
                class_dict = {key: value for key, value in Constants.__dict__.items() if not key.startswith("__")}
                class_dict.pop('updateConstants', None)
                with open(Constants.CONSTANTS_JSON_PATH, "w") as json_file:
                    json.dump(class_dict, json_file)
            except FileNotFoundError:
                print("Failed to dump constants json, probably unit testing")
                return
