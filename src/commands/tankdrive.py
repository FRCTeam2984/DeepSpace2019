import math
import os
import sys

from wpilib.command import Command
from wpilib.smartdashboard import SmartDashboard

import oi
from constants import Constants
from subsystems import drive


class TankDrive(Command):
    def __init__(self):
        super().__init__()
        self.drive = drive.Drive()
        self.requires(self.drive)
        self.drive.zeroSensors()

    def initialize(self):
        return

    def execute(self):
        x_speed = math.pow(oi.OI().getDriver().getY(),
                           Constants.TANK_DRIVE_EXPONENT)
        y_speed = math.pow(oi.OI().getDriver().getX(),
                           Constants.TANK_DRIVE_EXPONENT)
        rotation = math.pow(oi.OI().getDriver().getZ(),
                            Constants.TANK_DRIVE_EXPONENT)
        self.drive.setDirectionOutput(x_speed, y_speed, rotation)

    def isFinished(self):
        return False

    def end(self):
        return
