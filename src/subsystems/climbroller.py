from wpilib.command import Subsystem
from constants import Constants
from utils import singleton, lazytalonsrx
import logging
from commands import rollclimbroller


class ClimbRoller(Subsystem, metaclass=singleton.Singleton):
    """The climb roller subsystem controlls the rollers on the end of the front arm."""

    def __init__(self):
        super().__init__()

    def init(self):
        """Initialize the intake motors. This is not in the constructor to make the calling explicit in the robotInit to the robot simulator."""
        self.l_motor = lazytalonsrx.LazyTalonSRX(Constants.CRL_MOTOR_ID)
        self.r_motor = lazytalonsrx.LazyTalonSRX(Constants.CRR_MOTOR_ID)
        self.l_motor.initialize(
            inverted=False, encoder=False, name="Climb Roller Left")
        self.r_motor.initialize(
            inverted=False, encoder=False, name="Climb Roller Right")

    def outputToDashboard(self):
        self.l_motor.outputToDashboard()
        self.r_motor.outputToDashboard()

    def setPercentOutput(self, l_signal, r_signal):
        """Set the percent output of the 2 motors."""
        self.l_motor.setPercentOutput(l_signal, max_signal=1)
        self.r_motor.setPercentOutput(r_signal, max_signal=1)

    def roll(self, signal):
        """Move the rollers at the same speed."""
        if(signal < 0):
            logging.warn("Will not roll climb rollers backwards")
            return
        self.setPercentOutput(signal, signal)

    def stop(self):
        """Stop the rollers."""
        self.setPercentOutput(0, 0)

    def periodic(self):
        self.outputToDashboard()

    def initDefaultCommand(self):
        return self.setDefaultCommand(rollclimbroller.RollClimbRoller(Constants.CLIMB_ROLLER_SPEED))
