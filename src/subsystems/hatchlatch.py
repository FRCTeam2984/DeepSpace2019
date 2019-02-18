import ctre
from wpilib import SmartDashboard as Dash
from wpilib.command import Subsystem
import logging

from utils import singleton, units
from wpilib import Servo
from constants import Constants


class HatchLatch(Subsystem, metaclass=singleton.Singleton):
    """The HatchLatch subsystem controls the latch which grabs hatch panels
    and encoders."""

    def __init__(self):
        super().__init__()
        self.servo = Servo(0)

    def open(self):
        """Open the hatch latch."""
        logging.debug("Opening hatch latch")
        self.servo.setAngle(Constants.HATCH_LATCH_OPENED)

    def close(self):
        """Close the hatch latch."""
        logging.debug("Closing hatch latch")
        self.servo.setAngle(Constants.HATCH_LATCH_CLOSED)

    def toggle(self):
        """Toggle the hatch latch between open and closed
           (if it is not in either state, it will be closed)."""
        if self.servo.getAngle() == Constants.HATCH_LATCH_CLOSED:
            self.open()
        elif self.servo.getAngle() == Constants.HATCH_LATCH_OPENED:
            self.close()
        else:
            self.close()

    def outputToDashboard(self):
        Dash.putNumber("Servo Angle", self.servo.getAngle())

    def periodic(self):
        self.outputToDashboard()
