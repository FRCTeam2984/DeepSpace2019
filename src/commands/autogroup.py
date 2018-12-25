from wpilib.command import CommandGroup
from commands import drivetimed, turntoangle, followpath
import wpilib
import math


class AutonomousCommandGroup(CommandGroup):
    """Robot follows path and set of actions."""

    def __init__(self):
        super().__init__('Autonomous Program')
        self.ds = wpilib.DriverStation.getInstance()

    def getPath(self):
        data = self.ds.getGameSpecificMessage()

        # TODO create and implement actual paths
        if(data == "LLL"):
            self.addSequential(followpath.FollowPath("example.json"))
        elif(data == "RRR"):
            self.addSequential(followpath.FollowPath("example.json"))
        else:
            self.addSequential(followpath.FollowPath("example.json"))
