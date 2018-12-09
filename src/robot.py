from commands import (autogroup, disabledgroup, teleopgroup, testgroup,
                      updateodemetry)

import wpilib as wpi
from wpilib.cameraserver import CameraServer
import ctre
import wpilib as wpi
from commandbased import CommandBasedRobot
from wpilib import PowerDistributionPanel
from wpilib import SmartDashboard as Dash

import oi
from constants import Constants


class Robot(CommandBasedRobot):

    def robotInit(self):
        """Run when the robot turns on"""
        # Update constants from json file on robot
        Constants.updateConstants()
        # The PDP
        self.pdp = PowerDistributionPanel(Constants.PDP_ID)
        # Robot odemetry command
        self.updateodemetry = updateodemetry.UpdateOdemetry()
        # Set command group member variables
        self.autonomous = autogroup.AutonomousCommandGroup()
        self.disabled = disabledgroup.DisabledCommandGroup()
        self.teleop = teleopgroup.TeleopCommandGroup()
        self.test = testgroup.TestCommandGroup()
        # Start the camera sever
        CameraServer.launch()

    def globalInit(self):
        """Run on every init"""
        self.updateodemetry.start()

    def disabledInit(self):
        """Run when robot enters disabled mode"""
        self.globalInit()
        self.disabled.start()

    def autonomousInit(self):
        """Run when the robot enters auto mode"""
        self.globalInit()
        self.autonomous.start()

    def teleopInit(self):
        """Run when the robot enters teleop mode"""
        self.globalInit()
        self.teleop.start()

    def testInit(self):
        """Run when the robot enters test mode"""
        self.globalInit()
        self.test.start()

    def outputToSmartDashboard(self):
        for i in range(16):
            Dash.putNumber("channel " + i + " current", self.pdp.getCurrent(i))


# defining main function
if __name__ == '__main__':
    wpi.run(Robot)