
import math

import wpilib
from wpilib.command import Subsystem
import constants
import encoder

class RobotState(Subsystem):
    '''The DriveTrain subsystem incorporates the sensors and actuators attached to
       the robots chassis. These include four drive motors, a left and right encoder
       and a gyro.
    '''

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.encoder = encoder.Encoder(self.robot)

        self.last_left_encoder_distance = 0
        self.last_right_encoder_distance = 0

        self.timestamp = 0
        self.last_timestamp = 0

        self.pos_x = 0
        self.pos_y = 0
        self.heading = 0
        self.last_heading = 0

        self.gyro = wpilib.AnalogGyro(1)

        wpilib.LiveWindow.addSensor("Drive Train", "Gyro", self.gyro)

    # def initDefaultCommand(self):
    #     '''When no other command is running let the operator drive around
    #        using the PS3 joystick'''
    #     self.setDefaultCommand(TankDriveWithJoystick(self.robot))

    def log(self):
        '''The log method puts interesting information to the SmartDashboard.'''
        wpilib.SmartDashboard.putNumber(
            "Left Distance", self.encoder.getDistanceInchesLeft())
        wpilib.SmartDashboard.putNumber(
            "Right Distance", self.encoder.getDistanceInchesRight())
        wpilib.SmartDashboard.putNumber("Gyro", self.gyro.getAngle())

    def reset(self):
        '''Reset the robots sensors to the zero states'''
        self.gyro.reset()

    def getDistance(self):
        ''' :returns: The distance driven (average of left and right encoders)'''
        return (self.encoder.getDistanceInchesLeft() + self.encoder.getDistanceInchesRight()) / 2.0

    def getDistanceDelta(self):
        ''' :returns: The distance driven (average of left and right encoders)'''
        return (((self.last_left_encoder_distance-self.encoder.getDistanceInchesLeft()) + (self.last_right_encoder_distance-self.encoder.getDistanceInchesRight())) / 2.0)

    def getEncoderAngle(self):
        return (self.encoder.getDistanceInchesLeft() + self.encoder.getDistanceInchesRight()) / constants.WHEEL_BASE

    def getEncoderAngleDelta(self):
        ''' :returns: The distance driven (average of left and right encoders)'''
        return self.heading-self.last_heading

    def updateState(self, timestamp):
        self.last_timestamp = self.timestamp
        self.timestamp = timestamp
        delta_time = self.timestamp-self.last_timestamp
        self.heading = self.getEncoderAngle()
        self.pos_x += self.getDistanceDelta()*math.cos(self.heading)*delta_time
        self.pos_y += self.getDistanceDelta()*math.sin(self.heading)*delta_time
        self.last_left_encoder_distance = self.encoder.getDistanceInchesLeft()
        self.last_right_encoder_distance = self.encoder.getDistanceInchesRight()
        self.last_heading = self.heading

    def getState(self):
        return [self.pos_x, self.pos_y, self.heading]
