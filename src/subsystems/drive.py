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
        self.bl_motor = talonsrx.TalonSRX(Constants.BL_MOTOR_ID)
        self.br_motor = talonsrx.TalonSRX(Constants.BR_MOTOR_ID)
        self.fl_motor = talonsrx.TalonSRX(Constants.FL_MOTOR_ID)
        self.fr_motor = talonsrx.TalonSRX(Constants.FR_MOTOR_ID)

        self.motors = [self.bl_motor, self.br_motor,
                       self.fl_motor, self.fr_motor]

        self.bl_motor.initialize(
            inverted=False, encoder=True, name="Drive Back Left")
        self.br_motor.initialize(
            inverted=True, encoder=False, name="Drive Back Right")
        self.fl_motor.initialize(
            inverted=False, encoder=True, name="Drive Front Left")
        self.fr_motor.initialize(
            inverted=True, encoder=False, name="Drive Front Right")
        self.initPIDF()

    def initPIDF(self):
        self.bl_motor.setVelocityPIDF(
            Constants.BL_VELOCITY_KP, Constants.BL_VELOCITY_KI, Constants.BL_VELOCITY_KD, Constants.BL_VELOCITY_KF)
        self.br_motor.setVelocityPIDF(
            Constants.BR_VELOCITY_KP, Constants.BR_VELOCITY_KI, Constants.BR_VELOCITY_KD, Constants.BR_VELOCITY_KF)
        self.fl_motor.setVelocityPIDF(
            Constants.FL_VELOCITY_KP, Constants.FL_VELOCITY_KI, Constants.FL_VELOCITY_KD, Constants.FL_VELOCITY_KF)
        self.fr_motor.setVelocityPIDF(
            Constants.FR_VELOCITY_KP, Constants.FR_VELOCITY_KI, Constants.FR_VELOCITY_KD, Constants.FR_VELOCITY_KF)

    def zeroSensors(self):
        """Set the encoder positions to 0."""
        for motor in self.motors:
            motor.zero()

    def outputToSmartDashboard(self):
        self.bl_motor.outputToDashboard()
        self.br_motor.outputToDashboard()
        self.fl_motor.outputToDashboard()
        self.fr_motor.outputToDashboard()

    def setPercentOutput(self, bl_signal, br_signal, fl_signal, fr_signal):
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
        bl_signal = x_signal - y_signal + rotation
        br_signal = x_signal + y_signal - rotation
        fl_signal = x_signal + y_signal + rotation
        fr_signal = x_signal - y_signal - rotation

        self.setPercentOutput(bl_signal, br_signal, fl_signal, fr_signal)

    def setVelocityOutput(self, bl_velocity, br_velocity, fl_velocity, fr_velocity):
        self.bl_motor.setVelocitySetpoint(bl_velocity)
        self.br_motor.setVelocitySetpoint(br_velocity)
        self.fl_motor.setVelocitySetpoint(fl_velocity)
        self.fr_motor.setVelocitySetpoint(fr_velocity)

    def initDefaultCommand(self):
        return self.setDefaultCommand(tankdrive.TankDrive())

    def periodic(self):
        self.outputToSmartDashboard()
