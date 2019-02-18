from wpilib.command import Command

from constants import Constants
from subsystems import climbroller
import wpilib


class RollClimbRoller(Command):
    def __init__(self, speed):
        super().__init__()
        self.climbroller = climbroller.ClimbRoller()
        self.requires(self.climbroller)
        self.speed = speed
        self.setInterruptible(True)

    def initialize(self):
        pass

    def execute(self):
        self.climbroller.roll(self.speed)

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        self.climbroller.stop()
