import math
import os
import sys

from wpilib.command import Command
from wpilib.smartdashboard import SmartDashboard as Dash

import oi
from constants import Constants
from subsystems import drive
import odemetry
from utils import vector2d, units
import logging
from commands import turntoangle


class TankDrive(Command):
    def __init__(self, allocentric=False):
        super().__init__()
        self.allocentric = allocentric
        self.drive = drive.Drive()
        self.requires(self.drive)
        self.drive.zeroSensors()
        self.odemetry = odemetry.Odemetry()
        self.last_snap = 0

    def initialize(self):
        self.drive.initPIDF()
        return

    def execute(self):
        if not oi.OI().snapbutton.get():
            x_speed = math.pow(oi.OI().driver.getY(),
                               Constants.TANK_DRIVE_EXPONENT)
            y_speed = math.pow(oi.OI().driver.getX(),
                               Constants.TANK_DRIVE_EXPONENT)
            rotation = math.pow(oi.OI().driver.getZ(),
                                Constants.TANK_DRIVE_EXPONENT)
            if self.allocentric:
                speed = vector2d.Vector2D(
                    x_speed, y_speed).getRotated(-self.odemetry.getAngle())
                x_speed, y_speed = speed.getValues()

            self.drive.setDirectionOutput(x_speed, y_speed, rotation)
            self.last_snap = -1
        else:
            self.drive.setPercentOutput(0, 0, 0, 0)
            pov = oi.OI().driver.getPOV(0)
            print(pov)
            if pov != -1:
                turntoangle.TurnToAngle(pov).start()
