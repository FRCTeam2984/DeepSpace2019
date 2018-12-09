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
        power = -math.pow(oi.OI().getJoystick().getY(),
                          Constants.TANK_DRIVE_EXPONENT)
        rotation = oi.OI().getJoystick().getZ()
        rotation = (rotation, 0)[abs(rotation) < 0.05]
        left = power - rotation
        right = power + rotation
        self.drive.setPercentOutput(left, right)

    def isFinished(self):
        return False

    def end(self):
        return
