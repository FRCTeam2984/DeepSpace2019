from wpilib.command import InstantCommand

from subsystems import drive


class ZeroSensors(InstantCommand):
    def __init__(self):
        super().__init__()
        self.drive = drive.Drive()
        self.requires(self.drive)

    def initialize(self):
        self.drive.zeroSensors()
