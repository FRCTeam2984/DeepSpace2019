from wpilib.command import CommandGroup


class DisabledCommandGroup(CommandGroup):
    """Commands to run when robot is disabled"""

    def __init__(self):
        super().__init__('Disabled Program')
        # TODO add gyro calibration stuff
