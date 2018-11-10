import math
import constants

from wpilib import SmartDashboard as Dash
from subsystems import drive
from utils import singleton
from utils import pose


class RobotState(metaclass=singleton.Singleton):

    def __init__(self):
        """Initilize the RobotState class"""
        super().__init__()
        self.drive = drive.Drive()

        self.timestamp = 0
        self.last_timestamp = 0

        self.pose = pose.Pose()

        self.last_left_ecnoder_distance = 0
        self.last_right_ecnoder_distance = 0
        self.last_angle = 0

    def outputToSmartDashboard(self):
        Dash.putNumber(
            "Left Encoder Inches", self.drive.getDistanceInchesLeft())
        Dash.putNumber(
            "Right Encoder Inches", self.drive.getDistanceInchesRight())
        Dash.putNumber("Gyro Angle", self.getAngle())
        Dash.putNumber("Pos X", self.pose.x)
        Dash.putNumber("Pos Y", self.pose.y)
        Dash.putNumber("Heading", self.pose.angle)

    def getDistance(self):
        """Use encoders to return the distance driven in inches."""
        return (self.drive.getDistanceInchesLeft() + self.drive.getDistanceInchesRight()) / 2.0

    def getDistanceDelta(self):
        """Use encoders to return the distance change in inches."""
        return (((self.last_left_ecnoder_distance-self.drive.getDistanceInchesLeft()) + (self.last_right_ecnoder_distance-self.drive.getDistanceInchesRight())) / 2.0)

    def getAngle(self):
        """Use the gyroscope to return the angle in radians."""
        return self.drive.gyro.getAngle()

    def getAngleDelta(self):
        """Use the gyroscope to return the angle change in radians."""
        return self.pose.angle-self.last_angle

    def updateState(self, timestamp):
        """Use odometry to update the robot state."""
        self.timestamp = timestamp
        #delta_time = self.timestamp-self.last_timestamp
        # update angle
        self.pose.angle = self.getAngle()
        # update x and y positions
        self.pose.x += self.getDistanceDelta()*math.cos(self.pose.angle)
        self.pose.y += self.getDistanceDelta()*math.sin(self.pose.angle)
        # update last distances for next periodic
        self.last_left_ecnoder_distance = self.drive.getDistanceInchesLeft()
        self.last_right_ecnoder_distance = self.drive.getDistanceInchesRight()
        # update last angle and timestamp for next periodic
        self.last_angle = self.pose.angle
        self.last_timestamp = self.timestamp

    def getState(self):
        """Return the robot pose (position and orientation)."""
        return self.pose
