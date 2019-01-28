from commands import tankdrive

import ctre
from wpilib import SmartDashboard as Dash
from wpilib.command import Subsystem

from constants import Constants
from utils import singleton, units, talonsrx


class Drive(Subsystem, metaclass=singleton.Singleton):
    """The Drive subsystem controls the drive motors
    and encoders."""

    def __init__(self):
        super().__init__()

    def init(self):
        """Initialize the drive motors. This is not in the constructor to make the calling explicit in the robotInit to the robot simulator."""
        self.fl_motor = talonsrx.TalonSRX(Constants.FL_MOTOR_ID)
        self.fr_motor = talonsrx.TalonSRX(Constants.FR_MOTOR_ID)
        self.bl_motor = talonsrx.TalonSRX(Constants.BL_MOTOR_ID)
        self.br_motor = talonsrx.TalonSRX(Constants.BR_MOTOR_ID)

        self.motors = [self. fl_motor, self.fr_motor,
                       self.bl_motor, self.br_motor]

        self.fl_motor.initialize(inverted=False, encoder=True)
        self.fr_motor.initialize(inverted=True, encoder=True)
        self.bl_motor.initialize(inverted=False, encoder=True)
        self.br_motor.initialize(inverted=True, encoder=True)

        self.fl_motor.setVeloictyPIDF(0, 0, 0, 1)
        self.fr_motor.setVeloictyPIDF(0, 0, 0, 1)
        self.bl_motor.setVeloictyPIDF(0, 0, 0, 1)
        self.br_motor.setVeloictyPIDF(0, 0, 0, 1)

    def zeroSensors(self):
        """Set the encoder positions to 0."""
        for motor in self.motors:
            motor.zero()

    def _outputMotorToDashboard(self, name, motor):
        Dash.putNumber(f"{name} Voltage", self.fl_motor.getBusVoltage())
        Dash.putNumber(f"{name} PIDF Target",
                       self.fl_motor.getClosedLoopTarget(0))
        Dash.putNumber(f"{name} PIDF Error",
                       self.fl_motor.getClosedLoopError(0))

    def outputToSmartDashboard(self):
        self._outputMotorToDashboard("Front Left", self.fl_motor)
        self._outputMotorToDashboard("Front Right", self.fr_motor)
        self._outputMotorToDashboard("Back Left", self.bl_motor)
        self._outputMotorToDashboard("Back Right", self.br_motor)

    def setPercentOutput(self, fl_signal, fr_signal, bl_signal, br_signal):
        """Set the percent output of the 4 motors."""
        self.bl_motor.setPercentOutput(
            bl_signal, max_signal=Constants.MAX_DRIVE_OUTPUT)
        self.br_motor.setPercentOutput(
            br_signal, max_signal=Constants.MAX_DRIVE_OUTPUT)
        self.fl_motor.setPercentOutput(
            fl_signal, max_signal=Constants.MAX_DRIVE_OUTPUT)
        self.fr_motor.setPercentOutput(
            fr_signal, max_signal=Constants.MAX_DRIVE_OUTPUT)

    def setDirectionOutput(self, x_signal, y_signal, rotation):
        """Set percent output of the 4 motors given an x, y, and rotation inputs."""
        fl_signal = x_signal + y_signal + rotation
        fr_signal = x_signal - y_signal - rotation
        bl_signal = x_signal - y_signal + rotation
        br_signal = x_signal + y_signal - rotation
        self.setPercentOutput(fl_signal, fr_signal, bl_signal, br_signal)

    def setVeloictyOutput(self, fl_velocity, fr_velocity, bl_velocity, br_velocity):
        self.bl_motor.setVelocitySetpoint(bl_velocity)
        self.br_motor.setVelocitySetpoint(br_velocity)
        self.fl_motor.setVelocitySetpoint(fl_velocity)
        self.fr_motor.setVelocitySetpoint(fr_velocity)

    def initDefaultCommand(self):
        return self.setDefaultCommand(tankdrive.TankDrive())
