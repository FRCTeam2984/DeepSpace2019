import math
import os
import sys

from wpilib.command import Command, InstantCommand
from wpilib.smartdashboard import SmartDashboard

import oi
from constants import Constants
from subsystems import drive


class ZeroSensors(InstantCommand):
    def __init__(self):
        super().__init__()
        self.drive = drive.Drive()
        self.requires(self.drive)

    def initialize(self):
        self.drive.zeroSensors()
