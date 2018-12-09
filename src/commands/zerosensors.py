from subsystems import drive
from wpilib.command import Command


class ZeroSensors(Command):
    def __init__(self):
        super().__init__()
        self.drive = drive.Drive()
        self.requires(self.drive)
        self.drive.zeroSensors()

    def initialize(self):
        return

    def execute(self):
        return

    def isFinished(self):
        return True

    def end(self):
        return
