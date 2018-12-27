import json
import math


class Constants:
    """Global constants that are accesed throughout the project."""
    CONSTANTS_JSON_PATH = "/home/lvuser/py_constants.json"

    # Motion
    THEORETICAL_MAX_SPEED = 10

    # PDP
    PDP_ID = 60

    # Gyro
    GYRO_ID = 7

    # Drive motors
    LS_MOTOR_ID = 1
    LM_MOTOR_ID = 3
    RS_MOTOR_ID = 5
    RM_MOTOR_ID = 2

    # Wheel measurements
    WHEEL_DIAMETER = 6  # inches
    WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi  # inches
    WHEEL_BASE = 27.75  # inches (distance between wheels)

    # Encoder measurements
    DRIVE_ENCODER_TICKS_PER_REVOLUTION_LEFT = 4096  # TODO update
    DRIVE_ENCODER_TICKS_PER_REVOLUTION_RIGHT = 4096  # TODO update

    # Turn to angle pid values
    TURN_TO_ANGLE_KP = 0.006
    TURN_TO_ANGLE_KI = 0.01
    TURN_TO_ANGLE_KD = 0.0001
    TURN_TO_ANGLE_TOLERANCE = 1

    # Pure pursuit values
    LOOKAHEAD_DIST = 1

    # Joystick values
    DRIVER_PORT = 0
    OPERATOR_PORT = 1

    DRIVER_X_MOD = 1
    DRIVER_Y_MOD = 1
    DRIVER_Z_MOD = -1

    OPERATOR_X_MOD = 1
    OPERATOR_Y_MOD = 1
    OPERATOR_Z_MOD = 1

    JOYSTICK_DEADZONE = 0.05
    TANK_DRIVE_EXPONENT = 1

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
                class_dict = {key: value for key, value in Constants.__dict__.items(
                ) if not key.startswith("__")}
                class_dict.pop('updateConstants', None)
                with open(Constants.CONSTANTS_JSON_PATH, "w") as json_file:
                    json.dump(class_dict, json_file)
            except FileNotFoundError:
                print("Failed to dump constants json, probably unit testing")
                return
