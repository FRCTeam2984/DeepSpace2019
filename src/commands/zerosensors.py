from wpilib.command import InstantCommand

from subsystems import drive, longarm, shortarm


class ZeroSensors(InstantCommand):
    def __init__(self):
        super().__init__()
        self.drive = drive.Drive()
        self.longarm = longarm.LongArm()
        self.shortarm = shortarm.ShortArm()

        self.requires(self.drive)
        self.requires(self.longarm)
        self.requires(self.shortarm)

    def initialize(self):
        self.drive.reset()
        self.longarm.reset()
        self.shortarm.reset()
