
import math

import wpilib
from wpilib.command import Subsystem
import constants
import ctre


class Drive(Subsystem):
    '''The DriveTrain subsystem incorporates the sensors and actuators attached to
       the robots chassis. These include four drive motors, a left and right encoder
       and a gyro.
    '''

    def __init__(self, robot, leftMotorSlave, leftMotorMaster,  rightMotorSlave, rightMotorMaster):
        super().__init__()

        self.robot = robot
        self.timestamp = 0
        self.lastTimestamp = 0

        self.leftMotorSlave = leftMotorSlave
        self.leftMotorMaster = leftMotorMaster
        self.rightMotorSlave = rightMotorSlave
        self.rightMotorMaster = rightMotorMaster

        self.rightMotorSlave.set(
            ctre.ControlMode.Follower, constants.RIGHT_MOTOR_MASTER_ID)
        self.leftMotorSlave.set(ctre.ControlMode.Follower,
                                constants.LEFT_MOTOR_MASTER_ID)
    # def initDefaultCommand(self):
    #     '''When no other command is running let the operator drive around
    #        using the PS3 joystick'''
    #     self.setDefaultCommand(TankDriveWithJoystick(self.robot))

    def log(self):
        '''The log method puts interesting information to the SmartDashboard.'''
        return

    def reset(self):
        '''Reset the robots sensors to the zero states'''
        return

    def setPercentOutput(self, left_signal, right_signal):
        left_signal = min(max(left_signal, -1), 1)
        right_signal = min(max(right_signal, -1), 1)
        self.leftMotorMaster.set(
            ctre.ControlMode.PercentOutput, left_signal)
        self.rightMotorMaster.set(
            ctre.ControlMode.PercentOutput, right_signal)
