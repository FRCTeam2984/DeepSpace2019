import json
import math
from utils import log
from networktables import NetworkTables


class Constants:
    """Global constants that are accesed throughout the project."""
    CONSTANTS_JSON_PATH = "/home/lvuser/py_constants.json"

    # Motion
    THEORETICAL_MAX_VELOCITY = 60

    # PDP
    PDP_ID = 7

    # Gyro
    GYRO_ID = 6

    # Drive motors
    BL_MOTOR_ID = 1
    BR_MOTOR_ID = 2
    FL_MOTOR_ID = 3
    FR_MOTOR_ID = 4
    MAX_DRIVE_OUTPUT = 1

    # Intake motors
    IL_MOTOR_ID = 5
    IR_MOTOR_ID = 6

    # Arm motors
    BS_MOTOR_ID = 7
    BM_MOTOR_ID = 8
    FS_MOTOR_ID = 9
    FM_MOTOR_ID = 10

    # Wheel measurements
    WHEEL_DIAMETER = 6  # inches TODO update
    WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi  # inches
    # inches (distance between front and back wheels) TODO update
    X_WHEEL_BASE = 27.75
    Y_WHEEL_BASE = 27.75
    # inches (distance between left and right wheels) TODO update
    TRACK_WIDTH = 27.75

    # Encoder measurements
    DRIVE_ENCODER_TICKS_PER_REVOLUTION_LEFT = 1440
    DRIVE_ENCODER_TICKS_PER_REVOLUTION_RIGHT = 1440

    DRIVE_MOTOR_KP = 0
    DRIVE_MOTOR_KI = 0
    DRIVE_MOTOR_KD = 0
    DRIVE_MOTOR_KF = 1.2

    # Turn to angle pidf values
    TURN_TO_ANGLE_KP = 0.4
    TURN_TO_ANGLE_KI = 0.01
    TURN_TO_ANGLE_KD = 0
    TURN_TO_ANGLE_KF = 0

    TURN_TO_ANGLE_MIN_OUTPUT = 0.1
    TURN_TO_ANGLE_TIMEOUT = 1000
    TURN_TO_ANGLE_TOLERANCE = math.radians(5)

    # Pure pursuit values
    MAX_VELOCITY = 60  # inches/sec
    MAX_ACCELERATION = 10  # inches/sec/sec
    # TODO dynamically change lookahead distance based on the curvature of path/velocity of robot
    LOOKAHEAD_DIST = 24  # shorter == more overshoot, longer == longer to correct
    CURVE_VELOCITY = 0.25  # smaller == slower around turns
    CURVATURE_THRESHOLD = 1e-9

    PURE_PURSUIT_KV = 1 / THEORETICAL_MAX_VELOCITY
    PURE_PURSUIT_KA = 0.002
    PURE_PURSUIT_KP = 0.01

    # Joystick values
    DRIVER_PORT = 0
    OPERATOR_PORT = 1

    DRIVER_X_MOD = 1
    DRIVER_Y_MOD = -1
    DRIVER_Z_MOD = 1

    OPERATOR_X_MOD = 1
    OPERATOR_Y_MOD = 1
    OPERATOR_Z_MOD = 1

    JOYSTICK_DEADZONE = 0.05
    TANK_DRIVE_EXPONENT = 3

    # Distance sensor
    DISTANCE_SENSOR_PORT = 0

    # Hatch latch
    HATCH_LATCH_OPENED = 180
    HATCH_LATCH_CLOSED = 0

    # Front arm
    FRONT_ARM_KP = 0
    FRONT_ARM_KI = 0
    FRONT_ARM_KD = 0
    FRONT_ARM_KF = 0

    BACK_ARM_KP = 0
    BACK_ARM_KI = 0
    BACK_ARM_KD = 0
    BACK_ARM_KF = 0

    # Game modes (front arm, intake, back arm)
    GAME_MODE_STOW = [25,  0,  -90]
    GAME_MODE_PLAY = [25,  -90,  0]
    GAME_MODE_START_CLIMB = [0,  0,  0]
    GAME_MODE_END_CLIMB = [-90,  0,  90]
    GAME_MODE_END_GAME = [0,  0,  0]

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
                    json.dump(class_dict, json_file, indent=4)
            except FileNotFoundError:
                log.printerr(
                    "Failed to dump constants json, probably unit testing")
                return

    @staticmethod
    def initSmartDashboard():
        constants_table = NetworkTables.getTable(
            "SmartDashboard").getSubTable("CONSTANTS")
        constants_table.addEntryListener(Constants._valueChanged)
        for key, value in Constants.__dict__.items():
            if not key.startswith("__"):
                if isinstance(value, (int, float)):
                    constants_table.putNumber(key, value)
                elif isinstance(value, str):
                    constants_table.putString(key, value)
                elif isinstance(value, bool):
                    constants_table.putBoolean(key, value)

    @staticmethod
    def _valueChanged(table, key, value, isNew):
        if hasattr(Constants, key):
            setattr(Constants, key, value)
