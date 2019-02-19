from wpilib.command import CommandGroup
import math
from commands import teleopgroup


class AutonomousCommandGroup(CommandGroup):
    """Robot follows path and set of actions."""

    def __init__(self):
        super().__init__('Autonomous Program')
        self.addSequential(teleopgroup.TeleopCommandGroup())
