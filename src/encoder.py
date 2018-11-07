import wpilib
import robot
import constants


class Encoder:

    def __init__(self, robot):
        self.robot = robot

    def getDistanceTicksLeft(self):
        return self.robot.leftMotorMaster.getSelectedSensorPosition(0)

    def getVelocityTicksLeft(self):
        return self.robot.leftMotorMaster.getSelectedSensorVeloicty(0)

    def getDistanceTicksRight(self):
        return self.robot.rightMotorMaster.getSelectedSensorPosition(0)

    def getVelocityTicksRight(self):
        return self.robot.rightMotorMaster.getSelectedSensorVeloicty(0)


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

