
import wpilib

from wpilib import SmartDashboard
from wpilib.buttons import JoystickButton

class OI:
    
    def __init__(self):
        self.stick = wpilib.Joystick(0)   

    def getJoystick(self):
        return self.stick
        