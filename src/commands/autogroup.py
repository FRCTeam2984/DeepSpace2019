from wpilib.command import CommandGroup


class AutonomousCommandGroup(CommandGroup):
    """Robot follows path and set of actions"""

    def __init__(self):
        super().__init__('Autonomous Program')
        # TODO add drive forward command
