import ctre
from wpilib import SmartDashboard as Dash
from wpilib.command import Subsystem

from utils import singleton, units
from wpilib import Servo
from constants import Constants
from utils import oi


class HatchLatch(Subsystem, metaclass=singleton.Singleton):
    """The HatchLatch subsystem controls the latch which grabs hatch panels
    and encoders."""

    def __init__(self):
        super().__init__()
        self.servo = Servo(0)

    def setOpen(self):
        """Open the hatch latch."""
        self.servo.setAngle(Constants.HATCH_LATCH_OPENED)

    def setClosed(self):
        """Close the hatch latch."""
        self.servo.setAngle(Constants.HATCH_LATCH_CLOSED)

    def setToggle(self):
        """Toggle the hatch latch between open and closed
           (if it is not in either state, it will be closed)."""
        if self.servo.getAngle() == Constants.HATCH_LATCH_CLOSED:
            self.setOpen()
        elif self.servo.getAngle() == Constants.HATCH_LATCH_OPENED:
            self.setClosed()
        else:
            self.setClosed()

    def outputToDashboard(self):
        Dash.putNumber("Servo Angle", self.servo.getAngle())

    def periodic(self):
        self.outputToDashboard()

    def controlHatch(self):
        """ Checks each trigger and opens and closes depending on the trigger pressed."""
        if oi.OI.operator_buttons[6].whenPressed():
            self.setOpen()
        elif oi.OI.operator_buttons[5].whenPressed():
            self.setClosed()
