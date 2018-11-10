
import wpilib

from wpilib import SmartDashboard
from wpilib.buttons import JoystickButton

class OI:
    """Deals with anything controller related,
    be it gamepads, joysticks, or steering wheels"""
    def __init__(self):
        self.stick = wpilib.Joystick(0)   

    def getJoystick(self):
        """Return the main joystick used"""
        return self.stick
        