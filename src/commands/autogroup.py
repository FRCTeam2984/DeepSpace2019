from wpilib.command import CommandGroup
from commands import drivetimed, drivetilldistance
from commands import pathchooser


class AutonomousCommandGroup(CommandGroup):
    """Robot follows path and set of actions."""

    def __init__(self):
        super().__init__('Autonomous Program')
        # self.addSequential(pathchooser.PathChooser())
        self.addSequential(drivetilldistance.DriveTillDistanceAway())

