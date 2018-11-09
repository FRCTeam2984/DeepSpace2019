
import math

import wpilib
from wpilib.command import Subsystem
import constants
from enum import Enum
import drive
import singleton

class RobotState(metaclass=singleton.Singleton):
    '''The DriveTrain subsystem incorporates the sensors and actuators attached to
       the robots chassis. These include four drive motors, a left and right robot.drive
       and a gyro.
    '''

    def __init__(self):
        super().__init__()
        self.drive = drive.Drive()

        self.last_left_ecnoder_distance = 0
        self.last_right_ecnoder_distance = 0

        self.timestamp = 0
        self.last_timestamp = 0

        self.pos_x = 0
        self.pos_y = 0
        self.heading = 0
        self.last_heading = 0

    def outputToSmartDashboard(self):
        wpilib.SmartDashboard.putNumber(
            "Left Encoder Inches", self.drive.getDistanceInchesLeft())
        wpilib.SmartDashboard.putNumber(
            "Right Encoder Inches", self.drive.getDistanceInchesRight())
        wpilib.SmartDashboard.putNumber("Gyro Angle", self.getAngle())
        wpilib.SmartDashboard.putNumber("Pos X", self.getState()[0])
        wpilib.SmartDashboard.putNumber("Pos Y", self.getState()[1])
        wpilib.SmartDashboard.putNumber("Heading", self.getState()[2])

    def getDistance(self):
        return (self.drive.getDistanceInchesLeft() + self.drive.getDistanceInchesRight()) / 2.0

    def getDistanceDelta(self):
        return (((self.last_left_ecnoder_distance-self.drive.getDistanceInchesLeft()) + (self.last_right_ecnoder_distance-self.drive.getDistanceInchesRight())) / 2.0)

    def getAngle(self):
        return self.drive.gyro.getAngle()

    def getAngleDelta(self):
        return self.heading-self.last_heading

    def updateState(self, timestamp):
        self.timestamp = timestamp
        delta_time = self.timestamp-self.last_timestamp
        self.heading += self.getAngleDelta()*delta_time
        self.pos_x += self.getDistanceDelta()*math.cos(self.heading)*delta_time
        self.pos_y += self.getDistanceDelta()*math.sin(self.heading)*delta_time
        self.last_left_ecnoder_distance = self.drive.getDistanceInchesLeft()
        self.last_right_ecnoder_distance = self.drive.getDistanceInchesRight()
        self.last_heading = self.heading
        self.last_timestamp = self.timestamp

    def getState(self):
        return [self.pos_x, self.pos_y, self.heading]
