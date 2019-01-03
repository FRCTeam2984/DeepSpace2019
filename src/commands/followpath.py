
from wpilib.command import Command
from utils import purepursuit, hermitespline, vector2d
from subsystems import drive
import odemetry
import matplotlib.pyplot as plt


class FollowPath(Command):
    def __init__(self, filename):
        super().__init__()
        self.drive = drive.Drive()
        self.odemetry = odemetry.Odemetry()
        self.requires(self.drive)
        self.spline = hermitespline.HermiteSpline(filename=filename)
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
        velocities = self.follower.getTargetVelocities()
        self.drive.setPercentOutput(velocities.x, velocities.y)

    def isFinished(self):
        return self.follower.isDone()

    def end(self):
        self.drive.setPercentOutput(0, 0)
        return
