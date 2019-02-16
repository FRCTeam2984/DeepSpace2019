from wpilib.command import Command

from constants import Constants
from subsystems import drive
import wpilib


class DriveTimed(Command):
    def __init__(self, x_speed, y_speed, rotation, timeout=1):
        super().__init__()
        self.drive = drive.Drive()
        self.requires(self.drive)

        self.timer = wpilib.Timer()
        self.timeout = timeout

        self.x_speed = x_speed
        self.y_speed = y_speed
        self.rotation = rotation

    def initialize(self):
        self.timer.start()
        self.drive.setDirectionOutput(
            self.x_speed, self.y_speed, self.rotation)

    def isFinished(self):
        return self.timer.get() >= self.timeout

    def end(self):
        self.drive.setDirectionOutput(0, 0, 0)
