from wpilib.command import CommandGroup


class TestCommandGroup(CommandGroup):
    """Run when robot enters testing mode."""

    def __init__(self):
        super().__init__('Test Program')
        # TODO add robot systems test
