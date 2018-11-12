from wpilib.command import CommandGroup


class TeleopCommandGroup(CommandGroup):
    """Gets robot following controller input"""

    def __init__(self):
        super().__init__('Teleop Program')
        # TODO run tank drive
