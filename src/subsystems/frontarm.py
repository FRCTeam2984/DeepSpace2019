import ctre
from wpilib import SmartDashboard as Dash
from wpilib.command import Subsystem

from constants import Constants
from utils import singleton, units, talonsrx, pidf


class FrontArm(Subsystem, metaclass=singleton.Singleton):
    """The Drive subsystem controls the drive motors
    and encoders."""

    def __init__(self):
        super().__init__()

    def init(self):
        """Initialize the drive motors. This is not in the constructor to make the calling explicit in the robotInit to the robot simulator."""
        self.s_motor = talonsrx.TalonSRX(Constants.FS_MOTOR_ID)
        self.m_motor = talonsrx.TalonSRX(Constants.FM_MOTOR_ID)
        self.s_motor.initialize(inverted=False, encoder=False)
        self.m_motor.initialize(inverted=False, encoder=True)
        self.s_motor.follow(self.m_motor)

    def zeroSensors(self):
        """Set the encoder positions to 0."""
        self.m_motor.zero()

    def outputToSmartDashboard(self):
        pass

    def getAngle(self):
        self.m_motor.getPosition()


    def setPercentOutput(self, b_signal, f_signal):
        """Set the percent output of the left and right motors."""
        self.m_motor.setPercentOutput(b_signal)
        self.m_motor.setPercentOutput(f_signal)
