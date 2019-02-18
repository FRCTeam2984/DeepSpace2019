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
from subsystems import drive, longarm, intake, shortarm, climbroller
from wpilib import watchdog

import logging
import coloredlogs
from wpilib import LiveWindow


class Robot(CommandBasedRobot):

    def robotInit(self):
        """Run when the robot turns on."""
        field_styles = coloredlogs.DEFAULT_FIELD_STYLES
        field_styles['filename'] = {'color': 'cyan'}
        coloredlogs.install(level='DEBUG', 
            fmt="%(asctime)s[%(msecs)d] %(filename)s:%(lineno)d %(name)s %(levelname)s %(message)s", datefmt="%m-%d %H:%M:%S", field_styles=field_styles)  # install to created handler
        Command.getRobot = lambda x=0: self
        # Update constants from json file on robot
        # if self.isReal():
        #     Constants.updateConstants()
        # Update constants for dashboard editing
        Constants.initSmartDashboard()
        # Initialize motor objects
        drive.Drive().init()
        longarm.LongArm().init()
        shortarm.ShortArm().init()
        intake.Intake().init()
        climbroller.ClimbRoller().init()
        # The PDP
        # self.pdp = PDP(7)
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
        self.watchdog = watchdog.Watchdog(
            Constants.WATCHDOG_TIMEOUT, self._watchdogTimeout)
        self.globalInit()
        LiveWindow.disableAllTelemetry()

    def _watchdogTimeout(self):
        logging.warning("Watchdog timeout")

    def globalInit(self):
        """Run on every init."""
        self.watchdog.enable()
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
        logging.debug("Initiating teleop mode")
        self.globalInit()
        self.teleop.start()

    def testInit(self):
        """Run when the robot enters test mode."""
        self.globalInit()
        self.test.start()

    def robotPeriodic(self):
        self.outputToDashboard()

    def outputToDashboard(self):
        pass
        # Dash.putNumber("Total Current", self.pdp.getTotalCurrent())
        # for i in range(16):
        #     Dash.putNumber("Channel {} Current".format(i),
        #                    self.pdp.getCurrent(i))


# defining main function
if __name__ == '__main__':
    wpi.run(Robot)
