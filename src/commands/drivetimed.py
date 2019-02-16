from wpilib.command import Command

from constants import Constants
from subsystems import drive
import wpilib


class DriveTimed(Command):
    def __init__(self, x, y, timeout=1):
        super().__init__()
        self.drive = drive.Drive()
        self.requires(self.drive)

        self.timer = wpilib.Timer()
        self.timeout = timeout

        self.x = x
        self.y = y

    def initialize(self):
        self.timer.start()
        self.drive.setDirectionOutput(self.x, self.y, 0)
        

    def isFinished(self):
        return self.timer.get() >= self.timeout

    def end(self):
        self.drive.setDirectionOutput(0, 0, 0)
