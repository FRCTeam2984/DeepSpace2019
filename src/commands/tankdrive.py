import math
import sys
import os

import oi
from subsystems import drive
from wpilib.command import Command
from wpilib.smartdashboard import SmartDashboard
import constants

class TankDrive(Command):
    def __init__(self):
        super().__init__()
        self.requires(drive.Drive())

    def initialize(self):
        return

    def execute(self):
        power = -math.pow(oi.OI().getJoystick().getY(), constants.TANK_DRIVE_EXPONENT)
        rotation = -oi.OI().getJoystick().getZ()
        rotation = (rotation, 0)[abs(rotation) < 0.05]
        left = power - rotation
        right = power + rotation
        drive.Drive().setPercentOutput(left, right)

    def isFinished(self):
        return False

    def end(self):
        return

    def interrupted(self):
        self.end()
