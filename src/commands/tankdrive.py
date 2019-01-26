import math
import os
import sys

from wpilib.command import Command
from wpilib.smartdashboard import SmartDashboard as Dash

import oi
from constants import Constants
from subsystems import drive
import odemetry
from utils import vector2d


class TankDrive(Command):
    def __init__(self, allocentric=False):
        super().__init__()
        self.allocentric = allocentric
        self.drive = drive.Drive()
        self.requires(self.drive)
        self.drive.zeroSensors()
        self.odemetry = odemetry.Odemetry()

    def initialize(self):
        return

    def execute(self):
        x_speed = math.pow(oi.OI().getDriver().getY(),
                           Constants.TANK_DRIVE_EXPONENT)
        y_speed = math.pow(oi.OI().getDriver().getX(),
                           Constants.TANK_DRIVE_EXPONENT)
        rotation = math.pow(oi.OI().getDriver().getZ(),
                            Constants.TANK_DRIVE_EXPONENT)
        if self.allocentric:
            speed = vector2d.Vector2D(
                x_speed, y_speed).getRotated(-self.odemetry.getAngle())
            x_speed, y_speed = speed.getValues()

        self.drive.setDirectionOutput(x_speed, y_speed, rotation)

    def isFinished(self):
        return False

    def end(self):
        return
