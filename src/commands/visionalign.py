from wpilib.command import Command

from constants import Constants
from subsystems import drive
from vision import vision
import odemetry
import wpilib
import logging


class VisionAlign(Command):
    def __init__(self):
        super().__init__()
        self.drive = drive.Drive()
        self.requires(self.drive)
        self.vision = vision.Vision()

    def initialize(self):
        pass

    def execute(self):
        logging.info("Vision Number Array: {}".format(
            self.vision.table.getNumberArray("VISION DATA", [])))

    def isFinished(self):
        return self.vision.isAligned()

    def end(self):
        pass
