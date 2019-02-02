
# import matplotlib.pyplot as plt
from wpilib.command import Command

import odemetry
from autonomous import purepursuit
from constants import Constants
from splines import hermitespline as hs
from subsystems import drive
from utils import pidf, vector2d


class FollowPath(Command):
    def __init__(self, filename):
        super().__init__()
        self.drive = drive.Drive()
        self.odemetry = odemetry.Odemetry()
        self.requires(self.drive)
        self.spline = hs.HermiteSpline(filename=filename)
        self.follower = purepursuit.PurePursuit(self.spline)
        self.follower.computeVelocities()

    def initialize(self):
        return

    def execute(self):
        state = self.odemetry.getState()
        self.follower.update(state)
        self.follower.outputToDashboard()
        velocities = self.follower.target_velocities
        # self.drive.setPercentOutput()

    def isFinished(self):
        return self.follower.isDone()

    def end(self):
        self.drive.setPercentOutput(0, 0, 0, 0)
