import json
import logging
import math
from networktables import NetworkTables


class Constants:
    """Global constants that are accesed throughout the project."""
    CONSTANTS_JSON_PATH = "/home/lvuser/py_constants.json"

    # Motion
    THEORETICAL_MAX_VELOCITY = 60

    # PDP
    PDP_ID = 1

    # Gyro
    GYRO_ID = 6

    # Drive motors
    BL_MOTOR_ID = 2
    BR_MOTOR_ID = 3
    FL_MOTOR_ID = 4
    FR_MOTOR_ID = 5
    MAX_DRIVE_OUTPUT = 1

    # Intake motors
    IL_MOTOR_ID = 6
    IR_MOTOR_ID = 7
    IW_MOTOR_ID = 8

    # Arm motors
    FS_MOTOR_ID = 9
    FM_MOTOR_ID = 10
    BS_MOTOR_ID = 11
    BM_MOTOR_ID = 12
    CRL_MOTOR_ID = 13
    CRR_MOTOR_ID = 14

    # Intake motor "suck" and "spit" speeds
    SUCK_SPEED = 1
    SPIT_SPEED = 1

    # Wheel measurements
    WHEEL_DIAMETER = 6  # inches TODO update
    WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi  # inches
    # inches (distance between front and back wheels) TODO update
    X_WHEEL_BASE = 27.75
    Y_WHEEL_BASE = 27.75
    # inches (distance between left and right wheels) TODO update
    TRACK_WIDTH = 27.75

    # Encoder measurements
    CPR_DRIVE_BL = 1440
    CPR_DRIVE_BR = 1440
    CPR_DRIVE_FL = 1440
    CPR_DRIVE_FR = 1440
    CPR_ARM_F = 1440
    CPR_ARM_B = 1440
    CPR_INTAKE_W = 1440

    # Drive motor pidf values
    BL_VELOCITY_KP = 0.1
    BL_VELOCITY_KI = 0
    BL_VELOCITY_KD = 0
    BL_VELOCITY_KF = 0.335

    BR_VELOCITY_KP = 0
    BR_VELOCITY_KI = 0
    BR_VELOCITY_KD = 0
    BR_VELOCITY_KF = 1

    FL_VELOCITY_KP = 0
    FL_VELOCITY_KI = 0
    FL_VELOCITY_KD = 0
    FL_VELOCITY_KF = 1

    FR_VELOCITY_KP = 0
    FR_VELOCITY_KI = 0
    FR_VELOCITY_KD = 0
    FR_VELOCITY_KF = 1

    # Turn to angle pidf values
    TURN_TO_ANGLE_KP = 0.16
    TURN_TO_ANGLE_KI = 0.025
    TURN_TO_ANGLE_KD = 0
    TURN_TO_ANGLE_KF = 0

    TURN_TO_ANGLE_MIN_OUTPUT = 0.12
    TURN_TO_ANGLE_TIMEOUT = 200
    TURN_TO_ANGLE_TOLERANCE = 2

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

    # Vision
    VISION_MOVEMENT_KP_X = 1
    VISION_MOVEMENT_KP_Y = -1/40
    VISION_ERROR_THRESH_X = 0.1
    VISION_ERROR_THRESH_Y = 0.1

    # Front arm
    FRONT_ARM_KP = 0
    FRONT_ARM_KI = 0
    FRONT_ARM_KD = 0
    FRONT_ARM_KF = 0

    # Back arm
    BACK_ARM_KP = 0
    BACK_ARM_KI = 0
    BACK_ARM_KD = 0
    BACK_ARM_KF = 0

    # Intake wrist
    INTAKE_WRIST_KP = 0
    INTAKE_WRIST_KI = 0
    INTAKE_WRIST_KD = 0
    INTAKE_WRIST_KF = 0

    # Game modes (front arm, intake, back arm)
    GAME_MODE_STOW = [25,  0,  -90]
    GAME_MODE_PLAY = [25,  -90,  0]
    GAME_MODE_START_CLIMB = [0,  0,  0]
    GAME_MODE_END_CLIMB = [-90,  0,  90]
    GAME_MODE_END_GAME = [0,  0,  0]

    # Snap to angle angles
    FIELD_FRONT = 0
    FIELD_BACK = 180
    FIELD_LEFT = 90
    FIELD_RIGHT = 270
    L_ROCKET_FRONT = 29
    L_ROCKET_BACK = 151
    R_ROCKET_FRONT = 331
    R_ROCKET_BACK = 139

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
            except FileNotFoundError as f:
                logging.error(
                    "Failed to dump constants json: {}".format(str(f)))

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
