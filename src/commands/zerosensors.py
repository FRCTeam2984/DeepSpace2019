from wpilib.command import InstantCommand

from subsystems import drive, backarm


class ZeroSensors(InstantCommand):
    def __init__(self):
        super().__init__()
        self.drive = drive.Drive()
        self.backarm = backarm.BackArm()
        self.requires(self.drive)
        self.requires(self.backarm)

    def initialize(self):
        self.drive.reset()
        self.backarm.reset()
