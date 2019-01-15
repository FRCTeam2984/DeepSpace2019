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
        power = math.pow(oi.OI().driver.getY(),
                         Constants.TANK_DRIVE_EXPONENT)
        rotation = oi.OI().driver.getZ()
        rotation = rotation if abs(
            rotation) > Constants.JOYSTICK_DEADZONE else 0
        left = power - rotation
        right = power + rotation
        self.drive.setPercentOutput(left, right)

    def isFinished(self):
        return False

    def end(self):
        return
