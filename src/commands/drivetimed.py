from wpilib.command import Command

from constants import Constants
from subsystems import drive
import wpilib
from utils import units


class DriveTimed(Command):
    def __init__(self, left_velocity, right_velocity, timeout=1000):
        super().__init__()
        self.drive = drive.Drive()
        self.requires(self.drive)

        self.timer = wpilib.Timer()
        self.timeout = timeout

        self.left_velocity = left_velocity
        self.right_velocity = right_velocity

    def initialize(self):
        self.timer.start()
        self.drive.setVelocitySetpoint(self.left_velocity, self.right_velocity)

    def execute(self):
        pass

    def isFinished(self):
        return self.timer.get()*1000 >= self.timeout

    def end(self):
        self.drive.setPercentOutput(0, 0)
