import wpilib as wpi
import ctre
import oi
from commandbased import CommandBasedRobot
from constants import Constants

from commands import autogroup
from commands import disabledgroup
from commands import teleopgroup
from commands import testgroup
from commands import updateodemetry


class Robot(CommandBasedRobot):

    def robotInit(self):
        """Run when the robot turns on"""
        # Update constants from json file on robot
        Constants.updateConstants()
        # Robot odemetry command
        self.updateodemetry = updateodemetry.UpdateOdemetry()
        # Set command group member variables
        self.autonomous = autogroup.AutonomousCommandGroup()

    def globalInit(self):
        """Run on every init"""
        self.updateodemetry.start()

    def disabledInit(self):
        """Run when robot enters disabled mode"""
        self.globalInit()

    def autonomousInit(self):
        """Run when the robot enters auto mode"""
        self.globalInit()
        self.autonomous.start()

    def teleopInit(self):
        """Run when the robot enters teleop mode"""
        self.globalInit()

    def testInit(self):
        """Run when the robot enters test mode"""
        self.globalInit()


# defining main function
if __name__ == '__main__':
    wpi.run(Robot)
