from wpilib.command import CommandGroup
from commands import drivetimed, turntoangle, followpath
import wpilib
import math

class AutonomousCommandGroup(CommandGroup):
    """Robot follows path and set of actions."""

    def __init__(self):
        super().__init__('Autonomous Program')
        self.ds = wpilib.DriverStation.getInstance()
        self.addSequential(followpath.FollowPath("example.json"))

    def initialize(self):
        data = self.ds.getGameSpecificMessage()
        print("Game Data: {}".format(data))