from wpilib.command import Command

from constants import Constants
from subsystems import drive
import odemetry
import wpilib


class DriveForward(Command):
    def __init__(self, distance, speed):
        super().__init__()
        self.drive = drive.Drive()
        self.requires(self.drive)
        self.odemetry = odemetry.Odemetry()
        self.speed = speed
        self.distance = distance

    def initialize(self):
        self.drive.setPercentOutput(self.speed, self.speed)

    def isFinished(self):
        return self.odemetry.getState().x < self.distance

    def end(self):
        self.drive.setPercentOutput(0, 0)
