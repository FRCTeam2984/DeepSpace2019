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
        self.ls_motor = ctre.WPI_TalonSRX(Constants.LS_MOTOR_ID)
        self.lm_motor = ctre.WPI_TalonSRX(Constants.LM_MOTOR_ID)
        self.rs_motor = ctre.WPI_TalonSRX(Constants.RS_MOTOR_ID)
        self.rm_motor = ctre.WPI_TalonSRX(Constants.RM_MOTOR_ID)

        # Set up motors in slave-master config
        self.rs_motor.follow(self.rm_motor)
        self.ls_motor.follow(self.lm_motor)

        self.lm_motor.configSelectedFeedbackSensor(
            ctre.FeedbackDevice.QuadEncoder, 0, timeoutMs=10)
        self.rm_motor.configSelectedFeedbackSensor(
            ctre.FeedbackDevice.QuadEncoder, 0, timeoutMs=10)

    def zeroSensors(self):
        """Set the encoder positions to 0."""
        self.lm_motor.setSelectedSensorPosition(0, 0, 0)
        self.rm_motor.setSelectedSensorPosition(0, 0, 0)

    def outputToSmartDashboard(self):
        Dash.putNumber("Left Master Voltage",
                       self.getVoltageLeftMaster())
        Dash.putNumber("Right Master Voltage",
                       self.getVoltageRightMaster())
        Dash.putNumber("Left Slave Voltage",
                       self.getVoltageLeftSlave())
        Dash.putNumber("Right Slave Voltage",
                       self.getVoltageRightSlave())

    def setPercentOutput(self, left_signal=0, right_signal=0, vector=None):
        """Set the percent output of the left and right motors."""
        if vector != None:
            left_signal = vector.x
            right_signal = vector.y
        left_signal = min(max(left_signal, -1), 1)
        right_signal = min(max(right_signal, -1), 1)
        self.lm_motor.set(
            ctre.WPI_TalonSRX.ControlMode.PercentOutput, left_signal)
        self.rm_motor.set(
            ctre.WPI_TalonSRX.ControlMode.PercentOutput, right_signal)

    def getVoltageLeftMaster(self):
        """Return the voltage of the left master motor."""
        return self.lm_motor.getBusVoltage()

    def getVoltageRightMaster(self):
        """Returns the voltage for the right master motor."""
        return self.rm_motor.getBusVoltage()

    def getVoltageLeftSlave(self):
        """Returns the voltage for the left slave motor."""
        return self.ls_motor.getBusVoltage()

    def getVoltageRightSlave(self):
        """Returns the voltage for the right slave motor."""
        return self.rs_motor.getBusVoltage()

    def getDistanceTicksLeft(self):
        """Return the distance (in ticks) of the left encoder."""
        return self.lm_motor.getSelectedSensorPosition(0)

    def getDistanceTicksRight(self):
        """Return the distance (in ticks) of the right encoder."""
        return self.rm_motor.getSelectedSensorPosition(0)

    def getVelocityTicksLeft(self):
        """Return the velocity (in ticks/sec) of the left encoder."""
        return self.lm_motor.getSelectedSensorVelocity(0)

    def getVelocityTicksRight(self):
        """Return the velocity (in ticks/sec) of the right encoder."""
        return self.rm_motor.getSelectedSensorVelocity(0)

    def getDistanceInchesLeft(self):
        """Return the distance (in inches) of the left encoder."""
        return units.ticksToInchesLeft(self.getDistanceTicksLeft())

    def getDistanceInchesRight(self):
        """Return the distance (in inches) of the right encoder."""
        return units.ticksToInchesRight(self.getDistanceTicksRight())

    def getVelocityInchesLeft(self):
        """Return the velocity (in inches/sec) of the right encoder."""
        return units.ticksToInchesLeft(self.getVelocityTicksLeft())

    def getVelocityInchesRight(self):
        """Return the velocity (in inches/sec) of the right encoder."""
        return units.ticksToInchesRight(self.getVelocityTicksRight())

    def initDefaultCommand(self):
        return self.setDefaultCommand(tankdrive.TankDrive())
