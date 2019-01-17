import ctre
from wpilib import SmartDashboard as Dash
from wpilib.command import Subsystem

from utils import singleton, units
from wpilib import Servo
from constants import Constants


class HatchLatch(Subsystem, metaclass=singleton.Singleton):
    """The HatchLatch subsystem controls the latch which grabs hatch panels
    and encoders."""

    def __init__(self):
        super().__init__()
        self.servo = Servo(0)

    def setOpen(self):
        self.servo.setAngle(Constants.HATCH_LATCH_OPENED)

    def setClosed(self):
        self.servo.setAngle(Constants.HATCH_LATCH_CLOSED)

    def setToggle(self):
        if self.servo.getAngle() == Constants.HATCH_LATCH_CLOSED:
            self.setOpen()
        elif self.servo.getAngle() == Constants.HATCH_LATCH_OPENED:
            self.setClosed()
        else:
            self.setClosed()

    def outputToSmartDashboard(self):
        Dash.putNumber("Servo Angle", self.servo.getAngle())
