from wpilib.command import Command

from constants import Constants
from subsystems import drive
from vision import vision
import odemetry
import wpilib


class VisionTest(Command):
    def __init__(self):
        super().__init__()
        self.vision = vision.Vision()

    def initialize(self):
        pass

    def execute(self):
        print("NUMBER IS {}".format(
            self.vision.table.getNumberArray("VISION DATA", [])))

    def isFinished(self):
        return False

    def end(self):
        pass
