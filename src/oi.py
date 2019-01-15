from utils import joystick, singleton
from constants import Constants


class OI(metaclass=singleton.Singleton):
    """Deals with anything controller related,
    be it gamepads, joysticks, or steering wheels."""

    def __init__(self):
        self.driver = joystick.Joystick(
            Constants.DRIVER_PORT, Constants.DRIVER_X_MOD, Constants.DRIVER_Y_MOD, Constants.DRIVER_Z_MOD)
        self.operator = joystick.Joystick(
            Constants.OPERATOR_PORT, Constants.OPERATOR_X_MOD, Constants.OPERATOR_Y_MOD, Constants.OPERATOR_Z_MOD)