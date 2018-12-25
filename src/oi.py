from utils import joystick
from constants import Constants


class OI:
    """Deals with anything controller related,
    be it gamepads, joysticks, or steering wheels."""

    def __init__(self):
        self.driver = joystick.Joystick(
            Constants.DRIVER_PORT, Constants.DRIVER_X_MOD, Constants.DRIVER_Y_MOD, Constants.DRIVER_Z_MOD)
        self.operator = joystick.Joystick(
            Constants.OPERATOR_PORT, Constants.OPERATOR_X_MOD, Constants.OPERATOR_Y_MOD, Constants.OPERATOR_Z_MOD)

    def getDriver(self):
        """Return the driver joystick."""
        return self.driver

    def getOperator(self):
        """Return the operator joystick."""
        return self.operator
