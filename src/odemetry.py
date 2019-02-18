import math

from ctre.pigeonimu import PigeonIMU
import ctre
from wpilib import PowerDistributionPanel
from wpilib import SmartDashboard as Dash
from wpilib import analoggyro
from wpilib.robotbase import hal

from constants import Constants
from subsystems import drive, intake
from utils import pose, singleton, units, vector2d, pidpigeon, pidanaloggyro, angles


class Odemetry(metaclass=singleton.Singleton):
    """A singleton dealing with the odemetry of the robot."""

    def __init__(self):
        """Initilize the Odemetry class."""
        super().__init__()
        self.drive = drive.Drive()
        self.timestamp = 0
        self.last_timestamp = 0
        self.dt = 0

        # Gyroscope
        if hal.isSimulation():
            self.gyro = analoggyro.AnalogGyro(0)
            self.pidgyro = pidanaloggyro.PIDAnalogGyro(self.gyro)
        else:
            self.gyro = PigeonIMU(intake.Intake().l_motor)
            self.pidgyro = pidpigeon.PIDPigeon(self.gyro)

        self.pose = pose.Pose()

        self.last_left_encoder_distance = 0
        self.last_right_encoder_distance = 0
        self.last_angle = 0

    def reset(self):
        if hal.isSimulation():
            self.gyro.reset()
        else:
            self.gyro.setYaw(0, 0)
            self.pose = pose.Pose()

    def calibrate(self):
        if not hal.isSimulation():
            # TODO how to calibrate pigeon
            pass

    def outputToDashboard(self):
        # Dash.putNumber(
        #     "Left Encoder Ticks", self.drive.getDistanceTicksLeft())
        # Dash.putNumber(
        #     "Right Encoder Ticks", self.drive.getDistanceTicksRight())
        # Dash.putNumber(
        #     "Left Encoder Inches", self.drive.getDistanceInchesLeft())
        # Dash.putNumber(
        #     "Right Encoder Inches", self.drive.getDistanceInchesRight())

        Dash.putNumber("Pos X", self.pose.pos.x)
        Dash.putNumber("Pos Y", self.pose.pos.y)
        Dash.putNumber("Angle", int(units.radiansToDegrees(self.getAngle())))

    def getDistance(self):
        """Use encoders to return the distance driven in inches."""
        return 0
        # return (self.drive.getDistanceInchesLeft() + self.drive.getDistanceInchesRight()) / 2.0

    def getDistanceDelta(self):
        """Use encoders to return the distance change in inches."""
        return 0
        # return (((self.drive.getDistanceInchesLeft()-self.last_left_encoder_distance) + (self.drive.getDistanceInchesRight()-self.last_right_encoder_distance)) / 2.0)

    def getVelocity(self):
        """Use the distance delta to return the velocity in inches/sec."""
        return 0
        # if self.dt != 0:
        #     return self.getDistanceDelta()/self.dt
        # else:
        #     return 0

    def getAngle(self):
        """Use the gyroscope to return the angle in radians."""
        #angles.positiveAngleToMixedAngle(abs(math.fmod(units.radiansToDegrees(  ), 360)))
        if hal.isSimulation():
            return units.degreesToRadians(angles.positiveAngleToMixedAngle(angles.wrapPositiveAngle(-self.gyro.getAngle())))
            #return -units.degreesToRadians(self.gyro.getAngle())
        else:
            return units.degreesToRadians(angles.positiveAngleToMixedAngle(angles.wrapPositiveAngle(-self.gyro.getYawPitchRoll()[0])))
            #return -units.degreesToRadians(self.gyro.getYawPitchRoll()[0])

    def getAngleDelta(self):
        """Use the gyroscope to return the angle change in radians."""
        return self.pose.angle-self.last_angle

    def updateState(self, timestamp):
        """Use odemetry to update the robot state."""
        self.timestamp = timestamp
        self.dt = self.timestamp-self.last_timestamp
        # update angle
        self.pose.angle = self.getAngle()
        # # update x and y positions
        # self.pose.pos.x += self.getDistanceDelta() * math.cos(self.pose.angle)
        # self.pose.pos.y += self.getDistanceDelta() * math.sin(self.pose.angle)
        # # update last distances for next periodic
        # self.last_left_encoder_distance = self.drive.getDistanceInchesLeft()
        # self.last_right_encoder_distance = self.drive.getDistanceInchesRight()
        # # update last angle and timestamp for next periodic
        # self.last_angle = self.pose.angle
        # self.last_timestamp = self.timestamp

    def getState(self):
        """Return the robot pose (position [inches] and orientation [radians])."""
        return self.pose
