from wpilib.command import Subsystem
from constants import Constants
from utils import singleton, talonsrx


class Intake(Subsystem, metaclass=singleton.Singleton):
    """The intake subsystem controlls the cargo intake motors."""

    def __init__(self):
        super().__init__()

    def init(self):
        """Initialize the intake motors. This is not in the constructor to make the calling explicit in the robotInit to the robot simulator."""
        self.l_motor = talonsrx.TalonSRX(Constants.IL_MOTOR_ID)
        self.r_motor = talonsrx.TalonSRX(Constants.IR_MOTOR_ID)
        self.l_motor.initialize(
            inverted=False, encoder=False, name="Intake Left")
        self.r_motor.initialize(
            inverted=False, encoder=False, name="Intake Right")

    def outputToDashboard(self):
        self.l_motor.outputToDashboard()
        self.r_motor.outputToDashboard()

    def setPercentOutput(self, l_signal, r_signal):
        """Set the percent output of the 2 motors."""
        self.l_motor.setPercentOutput(l_signal, max_signal=1)
        self.r_motor.setPercentOutput(r_signal, max_signal=1)

    def stop(self):
        """Stop the intake motors."""
        self.setPercentOutput(0, 0)

    def suck(self, speed=Constants.SUCK_SPEED):
        """Set the intake motors to \"suck\"."""
        self.setPercentOutput(speed, -speed)

    def spit(self, speed=Constants.SPIT_SPEED):
        """Set the intake motors to \"spit\"."""
        self.setPercentOutput(speed, -speed)
