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
        self.vision.update()
        x_movement = self.vision.movement[0]
        y_movement = self.vision.movement[1]
        self.drive.setDirectionOutput(x_movement, y_movement, 0)

    def isFinished(self):
        return self.vision.isAligned()

    def end(self):
        pass
