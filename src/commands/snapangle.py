import math
import os
import sys

from utils import units
from commands import turntoangle


from wpilib.command import Command
from wpilib.smartdashboard import SmartDashboard

import oi
from constants import Constants
from subsystems import drive


class SnapDrive(Command):
    def __init__(self):
        super().__init__()
        self.drive = drive.Drive()
        self.requires(self.drive)
        self.drive.zeroSensors()


    def initialize(self):
        return


    def execute(self):
        dead_zone = math.hypot(oi.OI().driver.getX(), oi.OI().driver.getY())

        angle = 180 + units.radiansToDegrees(math.atan2(oi.OI().driver.getY(), oi.OI().driver.getX()))

        if angle != 180 and dead_zone >= 0.6:
            print(angle)
            if angle > 0 and angle < 22.5 or angle > 337.5:
                activation_path = 7
            for i in range(7):
                if angle > i * 45 + 22.5 and angle < i * 45 + 67.5:
                    activation_path = i
            if activation_path == 7:
                print("270")
                turntoangle.TurnToAngle(270, relative=False).start()
            if activation_path == 6:
                print("315")
                turntoangle.TurnToAngle(315, relative=False).start()
            if activation_path == 5:
                print("0")
                turntoangle.TurnToAngle(0, relative=False).start()
            if activation_path == 4:
                print("45")
                turntoangle.TurnToAngle(45, relative=False).start()
            if activation_path == 3:
                print("90")
                turntoangle.TurnToAngle(90, relative=False).start()
            if activation_path == 2:
                print("135")
                turntoangle.TurnToAngle(135, relative=False).start()
            if activation_path == 1:
                print("180")
                turntoangle.TurnToAngle(180, relative=False).start()
            if activation_path == 0:
                print("225")
                turntoangle.TurnToAngle(225, relative=False).start()

    def isFinished(self):
        return False

    def end(self):
        return
