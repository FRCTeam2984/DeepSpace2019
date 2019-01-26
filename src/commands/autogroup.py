from wpilib.command import CommandGroup
from commands import drivetimed, drivetilldistance, pathchooser, visiontest, turntoangle


class AutonomousCommandGroup(CommandGroup):
    """Robot follows path and set of actions."""

    def __init__(self):
        super().__init__('Autonomous Program')
        self.addSequential(turntoangle.TurnToAngle(90, relative=True))
