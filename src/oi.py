from wpilib import SmartDashboard
from wpilib.buttons import JoystickButton
from wpilib import Joystick


class OI:
    """Deals with anything controller related,
    be it gamepads, joysticks, or steering wheels"""

    def __init__(self):
        self.stick = Joystick(0)

    def getJoystick(self):
        """Return the main joystick used"""
        return self.stick
