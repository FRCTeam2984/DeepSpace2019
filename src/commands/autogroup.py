from wpilib.command import CommandGroup
from commands import drivetimed


class AutonomousCommandGroup(CommandGroup):
    """Robot follows path and set of actions"""

    def __init__(self):
        super().__init__('Autonomous Program')
        self.addSequential(drivetimed.DriveTimed(1, 1, 1000))
