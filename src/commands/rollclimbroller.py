from wpilib.command import InstantCommand

from constants import Constants
from subsystems import climbroller
import wpilib
import logging


class RollClimbRoller(InstantCommand):
    def __init__(self, speed):
        super().__init__()
        self.climbroller = climbroller.ClimbRoller()
        self.requires(self.climbroller)
        self.speed = speed

    def initialize(self):
        self.climbroller.roll(self.speed)
