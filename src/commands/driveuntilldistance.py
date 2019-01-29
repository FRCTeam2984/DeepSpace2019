import os
import sys
import time

from wpilib.command import Command
from constants import Constants
from subsystems import drive, distance


class DriveUntillDistance(Command):
    def __init__(self, distance):
        super().__init__()
        self.drive = drive.Drive()
        self.requires(self.drive)
        self.sensor = distance.DistanceSensor()
        self.requires(self.sensor)
        self.distance = distance

    def initialize(self):
        self.drive.setPercentOutput(0.25, 0.25, 0.25, 0.25)

    def execute(self):
        pass

    def isFinished(self):
        return self.distance.distanceInches() <= self.distance

    def end(self):
        self.drive.setPercentOutput(0, 0, 0, 0)
