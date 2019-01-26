#!/usr/bin/env python
from commands import (autogroup, disabledgroup,
                      teleopgroup, testgroup, globalgroup)

import ctre
import wpilib as wpi
from commandbased import CommandBasedRobot
from wpilib import PowerDistributionPanel as PDP
from wpilib import SmartDashboard as Dash

from wpilib.cameraserver import CameraServer
from wpilib.command import Command

import oi
from constants import Constants
from subsystems import drive


class Robot(CommandBasedRobot):

    def robotInit(self):
        Command.getRobot = lambda x=0: self
        """Run when the robot turns on."""
        # Update constants from json file on robot
        if self.isReal():
            Constants.updateConstants()
        # Update constants for dashboard editing
        Constants.initSmartDashboard()
        # Initialize drive objects
        drive.Drive().init()
        # The PDP
        self.pdp = PDP(Constants.PDP_ID)
        # Set command group member variables
        self.autonomous = autogroup.AutonomousCommandGroup()
        self.disabled = disabledgroup.DisabledCommandGroup()
        self.disabled.setRunWhenDisabled(True)
        self.teleop = teleopgroup.TeleopCommandGroup()
        self.test = testgroup.TestCommandGroup()
        self.global_ = globalgroup.GlobalCommandGroup()
        self.global_.setRunWhenDisabled(True)

        # Start the camera sever
        CameraServer.launch()
        self.globalInit()

    def globalInit(self):
        """Run on every init."""
        self.global_.start()

    def disabledInit(self):
        """Run when robot enters disabled mode."""
        self.globalInit()
        self.disabled.start()

    def autonomousInit(self):
        """Run when the robot enters auto mode."""
        self.globalInit()
        self.autonomous.start()

    def teleopInit(self):
        """Run when the robot enters teleop mode."""
        self.globalInit()
        self.teleop.start()

    def testInit(self):
        """Run when the robot enters test mode."""
        self.globalInit()
        self.test.start()


# defining main function
if __name__ == '__main__':
    wpi.run(Robot)
