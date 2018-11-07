
import math

import wpilib
from wpilib.command import Subsystem
import constants


class RobotState(Subsystem):
    '''The DriveTrain subsystem incorporates the sensors and actuators attached to
       the robots chassis. These include four drive motors, a left and right encoder
       and a gyro.
    '''

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        self.left_encoder = wpilib.Encoder(1, 2)
        self.right_encoder = wpilib.Encoder(3, 4)
        self.last_left_encoder_distance = 0
        self.last_right_encoder_distance = 0

        self.timestamp = 0
        self.last_timestamp = 0

        self.pos_x = 0
        self.pos_y = 0
        self.heading = 0
        self.last_heading = 0

        self.wheel_base = 1
        self.wheel_diameter = 1
        self.ticks_per_revolution_left = 1000
        self.ticks_per_revolution_right = 1000

        # Encoders may measure differently in the real world and in
        # simulation. In this example the robot moves 0.042 barleycorns
        # per tick in the real world, but the simulated encoders
        # simulate 360 tick encoders. This if statement allows for the
        # real robot to handle this difference in devices.
        if robot.isReal():
            self.left_encoder.setDistancePerPulse(
                6.0*math.pi/self.ticks_per_revolution_left)
            self.right_encoder.setDistancePerPulse(
                6.0*math.pi/self.ticks_per_revolution_right)
        else:
            # Circumference in ft = 4in/12(in/ft)*PI
            self.left_encoder.setDistancePerPulse((4.0/12.0*math.pi) / 360.0)
            self.right_encoder.setDistancePerPulse((4.0/12.0*math.pi) / 360.0)

        self.gyro = wpilib.AnalogGyro(1)

        wpilib.LiveWindow.addSensor(
            "Drive Train", "Left Encoder", self.left_encoder)
        wpilib.LiveWindow.addSensor(
            "Drive Train", "Right Encoder", self.right_encoder)
        wpilib.LiveWindow.addSensor("Drive Train", "Gyro", self.gyro)

    # def initDefaultCommand(self):
    #     '''When no other command is running let the operator drive around
    #        using the PS3 joystick'''
    #     self.setDefaultCommand(TankDriveWithJoystick(self.robot))

    def log(self):
        '''The log method puts interesting information to the SmartDashboard.'''
        wpilib.SmartDashboard.putNumber(
            "Left Distance", self.left_encoder.getDistance())
        wpilib.SmartDashboard.putNumber(
            "Right Distance", self.right_encoder.getDistance())
        wpilib.SmartDashboard.putNumber(
            "Left Speed", self.left_encoder.getRate())
        wpilib.SmartDashboard.putNumber(
            "Right Speed", self.right_encoder.getRate())
        wpilib.SmartDashboard.putNumber("Gyro", self.gyro.getAngle())

    def reset(self):
        '''Reset the robots sensors to the zero states'''
        self.gyro.reset()
        self.left_encoder.reset()
        self.right_encoder.reset()

    def getDistance(self):
        ''' :returns: The distance driven (average of left and right encoders)'''
        return (self.left_encoder.getDistance() + self.right_encoder.getDistance()) / 2.0

    def getDistanceDelta(self):
        ''' :returns: The distance driven (average of left and right encoders)'''
        return (((self.last_left_encoder_distance-self.left_encoder.getDistance()) + (self.last_right_encoder_distance-self.right_encoder.getDistance())) / 2.0)

    def getEncoderAngle(self):
        return (self.left_encoder.getDistance() + self.right_encoder.getDistance()) / self.wheel_base

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
        self.last_left_encoder_distance = self.left_encoder.getDistance()
        self.last_right_encoder_distance = self.right_encoder.getDistance()
        self.last_heading = self.heading

    def getState(self):
        return [self.pos_x, self.pos_y, self.heading]
