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
            inverted=True, encoder=True, phase=False, name="Back Arm Slave")
        self.m_motor.initialize(
            inverted=False, encoder=True, phase=False, name="Back Arm Master")
        self.s_motor.follow(self.m_motor)
        self.initPIDF()

    def initPIDF(self):
        """Initialize the arm motor pidf gains."""
        self.m_motor.setMotionMagicConfig(
            Constants.BACK_ARM_CRUISE_VELOCITY * (192) * (10/360), Constants.BACK_ARM_ACCELERATION * (192) * (10/360))
        self.m_motor.setPIDF(0, Constants.BACK_ARM_KP, Constants.BACK_ARM_KI,
                             Constants.BACK_ARM_KD, Constants.BACK_ARM_KF)

    def zeroSensors(self):
        """Set the encoder positions to 0."""
        self.m_motor.zero()

    def outputToDashboard(self):
        self.s_motor.outputToDashboard()
        self.m_motor.outputToDashboard()
        Dash.putNumber("Back Arm Angle", self.getAngle())

    def getAngle(self):
        """Get the angle of the arm in degrees."""
        return self.m_motor.getPosition() / (192) / (10/360)

    def setAngle(self, angle):
        """Set the angle of the arm in degrees."""
        ticks = angle * (192) * (10/360)
        self.m_motor.setMotionMagicSetpoint(ticks)

    def periodic(self):
        self.outputToDashboard()

    def reset(self):
        self.m_motor.setPercentOutput(0)
        self.zeroSensors()
        self.initPIDF()
