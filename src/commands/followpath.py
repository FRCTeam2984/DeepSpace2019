
from wpilib.command import Command
from utils import purepursuit, hermitespline
from subsystems import drive
import odemetry

class FollowPath(Command):
    def __init__(self, filename):
        super().__init__()
        self.drive = drive.Drive()
        self.odemetry = odemetry.Odemetry()
        self.requires(self.drive)
        self.spline = hermitespline.HermiteSpline(filename=filename)
        self.follower = purepursuit.PurePursuit(self.spline.getPoints(), 1)

    def initialize(self):
        return

    def execute(self):
        self.drive.setPercentOutput(1,1)
        pass

    def isFinished(self):
        return self.follower.isDone()

    def end(self):
        return
