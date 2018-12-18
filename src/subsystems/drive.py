import commands.tankdrive as tankdrive
from commands import tankdrive as tankdrive

import ctre
from wpilib import SmartDashboard as Dash
from wpilib import adxrs450_gyro
from wpilib.command import Subsystem

from constants import Constants
from utils import singleton


class Drive(Subsystem, metaclass=singleton.Singleton):
    """The Drive subsystem controls the drive motors
    and encoders"""

    def __init__(self):
        super().__init__()
        # Set motor ids
        self.left_motor_slave = ctre.WPI_TalonSRX(
            Constants.LEFT_MOTOR_SLAVE_ID)
        self.left_motor_master = ctre.WPI_TalonSRX(
            Constants.LEFT_MOTOR_MASTER_ID)
        self.right_motor_slave = ctre.WPI_TalonSRX(
            Constants.RIGHT_MOTOR_SLAVE_ID)
        self.right_motor_master = ctre.WPI_TalonSRX(
            Constants.RIGHT_MOTOR_MASTER_ID)
        # Set up motors in slave-master config
        self.right_motor_slave.set(ctre.WPI_TalonSRX.ControlMode.Follower,
                                   Constants.RIGHT_MOTOR_MASTER_ID)
        self.left_motor_slave.set(ctre.WPI_TalonSRX.ControlMode.Follower,
                                  Constants.LEFT_MOTOR_MASTER_ID)

    def zeroSensors(self):
        self.left_motor_master.setSelectedSensorPosition(0, 0, 0)
        self.right_motor_master.setSelectedSensorPosition(0, 0, 0)

    def outputToSmartDashboard(self):
        Dash.putNumber("Left Master Voltage",
                       self.getVoltageLeftMaster())
        Dash.putNumber("Right Master Voltage",
                       self.getVoltageRightMaster())
        Dash.putNumber("Left Slave Voltage",
                       self.getVoltageLeftSlave())
        Dash.putNumber("Right Slave Voltage",
                       self.getVoltageRightSlave())

    def setPercentOutput(self, left_signal, right_signal):
        """Set the percent speed of the left and right motors."""
        left_signal = min(max(left_signal, -1), 1)
        right_signal = min(max(right_signal, -1), 1)
        self.left_motor_master.set(
            ctre.WPI_TalonSRX.ControlMode.PercentOutput, left_signal)
        self.right_motor_master.set(
            ctre.WPI_TalonSRX.ControlMode.PercentOutput, right_signal)

    def getVoltageLeftMaster(self):
        """Return the voltage of the left master motor"""
        return self.left_motor_master.getBusVoltage()

    def getVoltageRightMaster(self):
        """Returns the voltage for the right master motor"""
        return self.right_motor_master.getBusVoltage()

    def getVoltageRightSlave(self):
        """Returns the voltage for the right slave motor"""
        return self.right_motor_slave.getBusVoltage()

    def getVoltageLeftSlave(self):
        """Returns the voltage for the left slave motor"""
        return self.left_motor_slave.getBusVoltage()

    def getDistanceTicksLeft(self):
        """Return the distance (in ticks) of the left encoder."""
        return self.left_motor_master.getSelectedSensorPosition(0)

    def getVelocityTicksLeft(self):
        """Return the velocity (in ticks/sec) of the left encoder."""
        return self.left_motor_master.getSelectedSensorVelocity(0)

    def getDistanceTicksRight(self):
        """Return the distance (in ticks) of the right encoder."""
        return self.right_motor_master.getSelectedSensorPosition(0)

    def getVelocityTicksRight(self):
        """Return the velocity (in ticks/sec) of the right encoder."""
        return self.right_motor_master.getSelectedSensorVelocity(0)

    def ticksToInchesLeft(self, ticks):
        """Convert ticks to inches for the left encoder."""
        return (ticks/Constants.DRIVE_ENCODER_TICKS_PER_REVOLUTION_LEFT)*Constants.WHEEL_CIRCUMFERENCE

    def ticksToInchesRight(self, ticks):
        """Convert ticks to inches for the right encoder."""
        return (ticks/Constants.DRIVE_ENCODER_TICKS_PER_REVOLUTION_RIGHT)*Constants.WHEEL_CIRCUMFERENCE

    def getDistanceInchesLeft(self):
        """Return the distance (in inches) of the left encoder."""
        return self.ticksToInchesLeft(self.getDistanceTicksLeft())

    def getVelocityTicksInchesLeft(self):
        """Return the velocity (in inches/sec) of the left encoder."""
        return self.ticksToInchesLeft(self.getVelocityTicksLeft())

    def getDistanceInchesRight(self):
        """Return the distance (in inches) of the right encoder."""
        return self.ticksToInchesRight(self.getDistanceTicksRight())

    def getVelocityTicksInchesRight(self):
        """Return the velocity (in inches/sec) of the right encoder."""
        return self.ticksToInchesRight(self.getVelocityTicksRight())

    def initDefaultCommand(self):
        return self.setDefaultCommand(tankdrive.TankDrive())
