
import math

import wpilib
from wpilib.command import Subsystem
import constants

class RobotState(Subsystem):
    '''The DriveTrain subsystem incorporates the sensors and actuators attached to
       the robots chassis. These include four drive motors, a left and right robot.drive
       and a gyro.
    '''

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.drive = robot.drive

        self.last_left_ecnoder_distance = 0
        self.last_right_ecnoder_distance = 0

        self.timestamp = 0
        self.last_timestamp = 0

        self.pos_x = 0
        self.pos_y = 0
        self.heading = 0
        self.last_heading = 0

        # self.gyro = wpilib.AnalogGyro(1)

        # wpilib.LiveWindow.addSensor("Drive Train", "Gyro", self.gyro)

    def log(self):
        '''The log method puts interesting information to the SmartDashboard.'''
        wpilib.SmartDashboard.putNumber(
            "Left Distance", self.drive.getDistanceInchesLeft())
        wpilib.SmartDashboard.putNumber(
            "Right Distance", self.drive.getDistanceInchesRight())
        # wpilib.SmartDashboard.putNumber("Gyro", self.gyro.getAngle())

    def reset(self):
        '''Reset the robots sensors to the zero states'''
        # self.gyro.reset()

    def getDistance(self):
        ''' :returns: The distance driven (average of left and right robot.drives)'''
        return (self.robot.drive.getDistanceInchesLeft() + self.robot.drive.getDistanceInchesRight()) / 2.0

    def getDistanceDelta(self):
        ''' :returns: The distance driven (average of left and right robot.drives)'''
        return (((self.last_left_ecnoder_distance-self.robot.drive.getDistanceInchesLeft()) + (self.last_right_ecnoder_distance-self.robot.drive.getDistanceInchesRight())) / 2.0)

    def getEncoderAngle(self):
        return (self.robot.drive.getDistanceInchesLeft() + self.robot.drive.getDistanceInchesRight()) / constants.WHEEL_BASE

    def getEncoderAngleDelta(self):
        ''' :returns: The distance driven (average of left and right robot.drives)'''
        return self.heading-self.last_heading

    def updateState(self, timestamp):
        self.timestamp = timestamp
        delta_time = self.timestamp-self.last_timestamp
        self.heading += self.getEncoderAngleDelta()*delta_time
        self.pos_x += self.getDistanceDelta()*math.cos(self.heading)*delta_time
        self.pos_y += self.getDistanceDelta()*math.sin(self.heading)*delta_time
        self.last_left_ecnoder_distance = self.robot.drive.getDistanceInchesLeft()
        self.last_right_ecnoder_distance = self.robot.drive.getDistanceInchesRight()
        self.last_heading = self.heading
        self.last_timestamp = self.timestamp

    def getState(self):
        return [self.pos_x, self.pos_y, self.heading]
