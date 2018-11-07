
import math

import wpilib
from wpilib.command import Subsystem
import constants
import ctre
import oi
import tankdrive

class Drive(Subsystem):
    '''The DriveTrain subsystem incorporates the sensors and actuators attached to
       the robots chassis. These include four drive motors, a left and right encoder
       and a gyro.
    '''

    def __init__(self, robot, left_motor_slave, left_motor_master,  right_motor_slave, right_motor_master):
        super().__init__()

        self.robot = robot
        self.timestamp = 0
        self.last_timestamp = 0

        self.left_motor_slave = left_motor_slave
        self.left_motor_master = left_motor_master
        self.right_motor_slave = right_motor_slave
        self.right_motor_master = right_motor_master

        self.right_motor_slave.set(
            ctre.ControlMode.Follower, constants.RIGHT_MOTOR_MASTER_ID)
        self.left_motor_slave.set(ctre.ControlMode.Follower,
                                constants.LEFT_MOTOR_MASTER_ID)


    def initDefaultCommand(self):
        '''When no other command is running let the operator drive around
           using the PS3 joystick'''
        self.setDefaultCommand(tankdrive.TankDrive(self.robot))

    def log(self):
        '''The log method puts interesting information to the SmartDashboard.'''
        return

    def reset(self):
        '''Reset the robots sensors to the zero states'''
        return

    def setPercentOutput(self, left_signal, right_signal):
        left_signal = min(max(left_signal, -1), 1)
        right_signal = min(max(right_signal, -1), 1)
        self.left_motor_master.set(
            ctre.ControlMode.PercentOutput, left_signal)
        self.right_motor_master.set(
            ctre.ControlMode.PercentOutput, right_signal)

    def getDistanceTicksLeft(self):
        return self.left_motor_master.getSelectedSensorPosition(0)

    def getVelocityTicksLeft(self):
        return self.left_motor_master.getSelectedSensorVeloicty(0)

    def getDistanceTicksRight(self):
        return self.right_motor_master.getSelectedSensorPosition(0)

    def getVelocityTicksRight(self):
        return self.right_motor_master.getSelectedSensorVeloicty(0)


    def ticksToInchesLeft(self, ticks):
        return (ticks/constants.DRIVE_ENCODER_TICKS_PER_REVOLUTION_LEFT)*constants.WHEEL_CIRCUMFERENCE

    def ticksToInchesRight(self, ticks):
        return (ticks/constants.DRIVE_ENCODER_TICKS_PER_REVOLUTION_RIGHT)*constants.WHEEL_CIRCUMFERENCE


    def getDistanceInchesLeft(self):
        return self.ticksToInchesLeft(self.getDistanceTicksLeft())

    def getVelocityTicksInchesLeft(self):
        return self.ticksToInchesLeft(self.getVelocityTicksLeft())

    def getDistanceInchesRight(self):
        return self.ticksToInchesRight(self.getDistanceTicksRight())

    def getVelocityTicksInchesRight(self):
        return self.ticksToInchesRight(self.getVelocityTicksRight())