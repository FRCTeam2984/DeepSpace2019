
import ctre
from wpilib import SmartDashboard as Dash
from wpilib import adxrs450_gyro
from wpilib.command import Subsystem

from constants import Constants
from utils import singleton, units


class Intake(Subsystem, metaclass=singleton.Singleton):
    """Intake subsystem motors."""

    def __init__(self):
        super().__init__()

    def init(self):
        """Initialize left and right intake motors ."""
        self.il_motor = ctre.WPI_TalonSRX(Constants.IL_MOTOR_ID)
        self.ir_motor = ctre.WPI_TalonSRX(Constants.IR_MOTOR_ID)

    def setPercentOutput(self, left_signal, right_signal):
        """Set the percent output of the left and right intake motors."""
        self.il_motor.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput, left_signal)
        self.ir_motor.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput, right_signal)

    def spit(self):
        """Makes intake motors spit."""
        self.setPercentOutput(SPIT_SPEED, -SPIT_SPEED)

    def suck(self):
        """Makes intake motors suck."""
        self.setPercentOutput(-SUCK_SPEED, SUCK_SPEED)
