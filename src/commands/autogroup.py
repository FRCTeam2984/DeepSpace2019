from wpilib.command import CommandGroup
from commands import pathchooser, turntoangle, drivetimed

import math


class AutonomousCommandGroup(CommandGroup):
    """Robot follows path and set of actions."""

    def __init__(self):
        super().__init__('Autonomous Program')
        self.addSequential(turntoangle.TurnToAngle(math.pi/2, relative=True))
