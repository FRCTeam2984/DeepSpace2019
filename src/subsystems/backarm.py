import ctre
from wpilib import SmartDashboard as Dash
from wpilib.command import Subsystem

from constants import Constants
from utils import singleton, units, lazytalonsrx, pidf


class BackArm(Subsystem, metaclass=singleton.Singleton):
    """The back arm subsystem controls the back arm motors and encoders."""

    def __init__(self):
        super().__init__()

    def init(self):
        """Initialize the back arm motors. This is not in the constructor to make the calling explicit in the robotInit to the robot simulator."""
        self.s_motor = lazytalonsrx.LazyTalonSRX(Constants.BS_MOTOR_ID)
        self.m_motor = lazytalonsrx.LazyTalonSRX(Constants.BM_MOTOR_ID)
        self.s_motor.initialize(
            inverted=True, encoder=True, name="Back Arm Slave")
        self.m_motor.initialize(
            inverted=False, encoder=True, name="Back Arm Master")
        self.s_motor.follow(self.m_motor)
        self.initPIDF()

    def initPIDF(self):
        self.m_motor.setMotionMagicConfig(
            Constants.BACK_ARM_CRUISE_VELOCITY, Constants.BACK_ARM_ACCELERATION)
        self.m_motor.setMotionMagicPIDF(
            Constants.BACK_ARM_KP, Constants.BACK_ARM_KI, Constants.BACK_ARM_KD, Constants.BACK_ARM_KF)

    def zeroSensors(self):
        """Set the encoder positions to 0."""
        self.m_motor.zero()

    def outputToDashboard(self):
        self.s_motor.outputToDashboard()
        self.m_motor.outputToDashboard()

    def getAngle(self):
        """Get the angle of the arm in degrees."""
        self.m_motor.getPosition()

    def setAngle(self, angle):
        """Set the angle of the arm in degrees."""

        self.m_motor.setMotionMagicSetpoint(angle)

    def setMotion(self, motion):
        ticks = Constants.BACK_ARM_POS*(192)*(8/360)
        self.m_motor.setMotionMagicSetpoint(ticks)

    def periodic(self):
        self.outputToDashboard()

    def reset(self):
        self.initPIDF()
