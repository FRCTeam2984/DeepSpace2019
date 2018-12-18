from wpilib.command import CommandGroup
from commands import driveforward


class AutonomousCommandGroup(CommandGroup):
    """Robot follows path and set of actions"""

    def __init__(self):
        super().__init__('Autonomous Program')
        self.addSequential(driveforward.DriveForward(1, 1, 1000))
