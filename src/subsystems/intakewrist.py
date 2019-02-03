from wpilib.command import Subsystem
from constants import Constants
from utils import singleton, units, lazytalonsrx


class IntakeWrist(Subsystem, metaclass=singleton.Singleton):
    """The intake wrist subsystem controlls the wrist of the intake and which angle it is at."""

    def __init__(self):
        super().__init__()

    def init(self):
        """Initialize the intake wrist motors. This is not in the constructor to make the calling explicit in the robotInit to the robot simulator."""
        self.w_motor = lazytalonsrx.LazyTalonSRX(Constants.IW_MOTOR_ID)
        self.w_motor.initialize(inverted=False, encoder=False, name="Wrist")
        self.w_motor.setPositionPIDF(Constants.INTAKE_WRIST_KP, Constants.INTAKE_WRIST_KI,
                                     Constants.INTAKE_WRIST_KD, Constants.INTAKE_WRIST_KF)

    def outputToDashboard(self):
        self.w_motor.outputToDashboard()

    def setAngle(self, angle):
        """Set the angle of the wrist."""
        self.w_motor.setPositionSetpoint(
            units.intakeWristDegreesToTicks(angle))

    def periodic(self):
        self.outputToDashboard()
