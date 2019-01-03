
from wpilib.command import InstantCommand
import wpilib
from commands import followpath


class PathChooser(InstantCommand):
    def __init__(self):
        super().__init__()
        self.ds = wpilib.DriverStation.getInstance()

    def initialize(self):
        data = self.ds.getGameSpecificMessage()
        # TODO create and implement actual paths
        followpath.FollowPath("example3.json").start()

    def end(self):
        pass
