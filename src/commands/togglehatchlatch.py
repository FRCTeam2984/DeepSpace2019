from wpilib.command import InstantCommand

from constants import Constants
from subsystems import hatchlatch
import wpilib
from utils import units


class ToggleHatchLatch(InstantCommand):
    def __init__(self):
        super().__init__()
        self.hatchlatch = hatchlatch.HatchLatch()
        self.requires(self.hatchlatch)

    def initialize(self):
        self.hatchlatch.setToggle()

    def end(self):
        pass
