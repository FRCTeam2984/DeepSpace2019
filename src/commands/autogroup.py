from wpilib.command import CommandGroup
from commands import autopath


class AutonomousCommandGroup(CommandGroup):
    """Robot follows path and set of actions."""

    def __init__(self):
        super().__init__('Autonomous Program')
        self.addSequential(autopath.AutoPath())
