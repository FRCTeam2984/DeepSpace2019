from wpilib.command import Command

from constants import Constants
from subsystems import climbroller
import wpilib
import oi


class RollClimbRoller(Command):
    def __init__(self):
        super().__init__()
        self.climbroller = climbroller.ClimbRoller()
        self.requires(self.climbroller)

    def execute(self):
        speed = oi.OI().operator.getY()
        self.climbroller.roll(speed)

    def isFinished(self):
        False

    def end(self):
        self.climbroller.stop()
