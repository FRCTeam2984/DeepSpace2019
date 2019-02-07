from wpilib.command import CommandGroup
from commands import turntoangle, setbackarm
import math


class AutonomousCommandGroup(CommandGroup):
    """Robot follows path and set of actions."""

    def __init__(self):
        super().__init__('Autonomous Program')
        self.addSequential(setbackarm.SetBackArm(45))
