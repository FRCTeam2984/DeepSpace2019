from wpilib.command import Command

from constants import Constants
from subsystems import drive
import wpilib
import logging


class DriveAtCurvature(Command):
    def __init__(self, radius, velocity, timeout):
        super().__init__()
        self.drive = drive.Drive()
        self.requires(self.drive)

        self.radius = radius
        self.velocity = velocity

        self.timeout = timeout
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.start()
        l_velocity = (self.radius + Constants.TRACK_WIDTH/2)
        r_velocity = (self.radius - Constants.TRACK_WIDTH/2)
        scale = (1/max(abs(l_velocity), abs(r_velocity))) * self.velocity
        l_velocity *= scale
        r_velocity *= scale

        logging.info(
            "Drive Curvature Velocity: {} - {}".format(l_velocity, r_velocity))
        self.drive.setPercentOutput(l_velocity, r_velocity)

    def isFinished(self):
        return self.timer.get()*1000 >= self.timeout

    def end(self):
        self.drive.setPercentOutput(0, 0)
