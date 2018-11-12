import wpilib as wpi
import ctre
import oi
from commandbased import CommandBasedRobot
from constants import Constants

from commands.autogroup import AutonomousCommandGroup


class Robot(CommandBasedRobot):

    def robotInit(self):
        """Run when the robot turns on"""
        # Update constants from json file on robot
        Constants.updateConstants()
        # Set command group member variables
        self.autonomous = AutonomousCommandGroup

    def disabledInit(self):
        """Run when robot enters disabled mode"""
        pass

    def autonomousInit(self):
        """Run when the robot enters auto mode"""
        self.scheduler.

    def teleopInit(self):
        """Run when the robot enters teleop mode"""
        pass

    def testInit(self):
        """Run when the robot enters test mode"""
        pass


# defining main function
if __name__ == '__main__':
    wpi.run(Robot)
