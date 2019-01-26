import commands.tankdrive as tankdrive
from commands import tankdrive as tankdrive

import ctre
from wpilib import SmartDashboard as Dash
from wpilib import adxrs450_gyro
from wpilib.command import Subsystem

from constants import Constants
from utils import singleton, units


class Drive(Subsystem, metaclass=singleton.Singleton):
    """The Drive subsystem controls the drive motors
    and encoders."""

    def __init__(self):
        super().__init__()

    def init(self):
        """Initialize the drive motors. This is not in the constructor to make the calling explicit in the robotInit to the robot simulator."""
        self.fl_motor = ctre.WPI_TalonSRX(Constants.FL_MOTOR_ID)
        self.fr_motor = ctre.WPI_TalonSRX(Constants.FR_MOTOR_ID)
        self.bl_motor = ctre.WPI_TalonSRX(Constants.BL_MOTOR_ID)
        self.br_motor = ctre.WPI_TalonSRX(Constants.BR_MOTOR_ID)
        self.br_motor.setInverted(True)
        self.fr_motor.setInverted(True)

        self.motors = [self. fl_motor, self.fr_motor,
                       self.bl_motor, self.br_motor]

        for motor in self.motors:
            motor.configSelectedFeedbackSensor(
                ctre.FeedbackDevice.QuadEncoder, 0, timeoutMs=10)
            motor.configNominalOutputForward(0, 5)
            motor.configNominalOutputReverse(0, 5)
            motor.configPeakOutputForward(1, 5)
            motor.configPeakOutputReverse(-1, 5)

    def zeroSensors(self):
        """Set the encoder positions to 0."""
        for motor in self.motors:
            motor.setSelectedSensorPosition(0, 0, 0)

    def outputToSmartDashboard(self):
        Dash.putNumber("Front Left Voltage",
                       self.getVoltageFrontLeft())
        Dash.putNumber("Front Right Voltage",
                       self.getVoltageFrontRight())
        Dash.putNumber("Back Left Voltage",
                       self.getVoltageBackLeft())
        Dash.putNumber("Back Right Voltage",
                       self.getVoltageBackRight())

    def setPercentOutput(self, fl_signal, fr_signal, bl_signal, br_signal):
        """Set the percent output of the left and right motors."""
        fl_signal = min(max(fl_signal, -1), 1)
        fr_signal = min(max(fr_signal, -1), 1)
        bl_signal = min(max(bl_signal, -1), 1)
        br_signal = min(max(br_signal, -1), 1)
        self.fl_motor.set(
            ctre.WPI_TalonSRX.ControlMode.PercentOutput, fl_signal)
        self.fr_motor.set(
            ctre.WPI_TalonSRX.ControlMode.PercentOutput, fr_signal)
        self.bl_motor.set(
            ctre.WPI_TalonSRX.ControlMode.PercentOutput, bl_signal)
        self.br_motor.set(
            ctre.WPI_TalonSRX.ControlMode.PercentOutput, br_signal)

    def setDirectionOutput(self, x_signal, y_signal, rotation):
        """Set the percent output of the left and right motors."""
        fl_signal = x_signal + y_signal + rotation
        fr_signal = x_signal - y_signal - rotation
        bl_signal = x_signal - y_signal + rotation
        br_signal = x_signal + y_signal - rotation
        self.setPercentOutput(fl_signal, fr_signal, bl_signal, br_signal)

    def getVoltageFrontLeft(self):
        """Return the voltage of the left master motor."""
        return self.fl_motor.getBusVoltage()

    def getVoltageFrontRight(self):
        """Return the voltage of the left master motor."""
        return self.fr_motor.getBusVoltage()

    def getVoltageBackLeft(self):
        """Return the voltage of the left master motor."""
        return self.bl_motor.getBusVoltage()

    def getVoltageBackRight(self):
        """Return the voltage of the left master motor."""
        return self.br_motor.getBusVoltage()

    def initDefaultCommand(self):
        return self.setDefaultCommand(tankdrive.TankDrive())
