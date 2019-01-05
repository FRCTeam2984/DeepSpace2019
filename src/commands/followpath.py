
import matplotlib.pyplot as plt
from wpilib.command import Command

import odemetry
from autonomous import purepursuit
from constants import Constants
from splines import hermitespline as hs
from subsystems import drive
from utils import pid, vector2d


class FollowPath(Command):
    def __init__(self, filename):
        super().__init__()
        self.drive = drive.Drive()
        self.odemetry = odemetry.Odemetry()
        self.requires(self.drive)
        self.spline = hs.HermiteSpline(filename=filename)
        self.follower = purepursuit.PurePursuit(self.spline)
        self.follower.computeVelocities()
        # x_list = [p.x for p in self.spline.getPoints()]
        # y_list = [p.y for p in self.spline.getPoints()]
        # v_list = self.follower.velocities
        # c_list = [c * 10000 for c in self.follower.curvatures]
        # plt.gca().invert_yaxis()
        # plt.plot(x_list, y_list, color='red')  # path
        # plt.plot(x_list, c_list, color='green')  # curvature
        # plt.plot(x_list, v_list, color='blue')  # velocities
        # plt.show()

    def initialize(self):
        return

    def execute(self):
        state = self.odemetry.getState()
        self.follower.update(state)
        self.follower.outputToSmartDashboard()
        velocities = self.follower.target_velocities
        self.drive.setPercentOutput(vector=velocities)

    def isFinished(self):
        return self.follower.isDone()

    def end(self):
        self.drive.setPercentOutput(0, 0)
        return
