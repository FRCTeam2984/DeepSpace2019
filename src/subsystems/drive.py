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

        self.lm_motor.setSensorPhase(True)

        self.lm_motor.configNominalOutputForward(0, 5)
        self.lm_motor.configNominalOutputReverse(0, 5)
        self.lm_motor.configPeakOutputForward(1, 5)
        self.lm_motor.configPeakOutputReverse(-1, 5)

        self.rm_motor.configNominalOutputForward(0, 5)
        self.rm_motor.configNominalOutputReverse(0, 5)
        self.rm_motor.configPeakOutputForward(1, 5)
        self.rm_motor.configPeakOutputReverse(-1, 5)

        self.lm_motor.selectProfileSlot(0, 0)
        self.lm_motor.config_kP(0, Constants.DRIVE_MOTOR_KP, 0)
        self.lm_motor.config_kI(0, Constants.DRIVE_MOTOR_KI, 0)
        self.lm_motor.config_kD(0, Constants.DRIVE_MOTOR_KD, 0)
        self.lm_motor.config_kF(0, Constants.DRIVE_MOTOR_KF, 0)

        self.rm_motor.selectProfileSlot(0, 0)
        self.rm_motor.config_kP(0, Constants.DRIVE_MOTOR_KP, 0)
        self.rm_motor.config_kI(0, Constants.DRIVE_MOTOR_KI, 0)
        self.rm_motor.config_kD(0, Constants.DRIVE_MOTOR_KD, 0)
        self.rm_motor.config_kF(0, Constants.DRIVE_MOTOR_KF, 0)

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
        Dash.putNumber("Left Ticks Velocity", self.getVelocityTicksLeft())
        Dash.putNumber("Right Ticks Velocity", self.getVelocityTicksRight())
        Dash.putNumber("Left Inches Velocity", self.getVelocityInchesLeft())
        Dash.putNumber("Right Inches Velocity", self.getVelocityInchesRight())
        Dash.putNumber("Left Error", self.lm_motor.getClosedLoopError(0))
        Dash.putNumber("Right Error", self.rm_motor.getClosedLoopError(0))

    def setPercentOutput(self, left_signal, right_signal):
        """Set the percent output of the left and right motors."""
        left_signal = min(
            max(left_signal, -Constants.MAX_DRIVE_OUTPUT), Constants.MAX_DRIVE_OUTPUT)
        right_signal = min(
            max(right_signal, -Constants.MAX_DRIVE_OUTPUT), Constants.MAX_DRIVE_OUTPUT)
        self.lm_motor.set(
            ctre.WPI_TalonSRX.ControlMode.PercentOutput, left_signal)
        self.rm_motor.set(
            ctre.WPI_TalonSRX.ControlMode.PercentOutput, right_signal)

    def setVelocitySetpoint(self, left_velocity, right_velocity):
        """Set the velocity setpoint (inches/sec) of the left and right motors."""
        native_left = units.inchesPerSecToTicksPer100msLeft(left_velocity)
        native_right = units.inchesPerSecToTicksPer100msLeft(right_velocity)
        self.lm_motor.set(
            ctre.WPI_TalonSRX.ControlMode.Velocity, native_left)
        self.rm_motor.set(
            ctre.WPI_TalonSRX.ControlMode.Velocity, native_right)

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
        """Return the velocity (in ticks/100ms) of the left encoder."""
        return self.lm_motor.getSelectedSensorVelocity(0)

    def getVelocityTicksRight(self):
        """Return the velocity (in ticks/100ms) of the right encoder."""
        return self.rm_motor.getSelectedSensorVelocity(0)

    def getDistanceInchesLeft(self):
        """Return the distance (in inches) of the left encoder."""
        return units.ticksToInchesLeft(self.getDistanceTicksLeft())

    def getDistanceInchesRight(self):
        """Return the distance (in inches) of the right encoder."""
        return units.ticksToInchesRight(self.getDistanceTicksRight())

    def getVelocityInchesLeft(self):
        """Return the velocity (in inches/sec) of the right encoder."""
        return units.ticksPer100msToInchesPerSecLeft(self.getVelocityTicksLeft())

    def getVelocityInchesRight(self):
        """Return the velocity (in inches/sec) of the right encoder."""
        return units.ticksPer100msToInchesPerSecRight(self.getVelocityTicksRight())

    def initDefaultCommand(self):
        return self.setDefaultCommand(tankdrive.TankDrive())
