from commands import snaplistener, tankarm, rollclimbroller, tankdrive

from wpilib.command import CommandGroup


class TeleopCommandGroup(CommandGroup):
    """Gets robot following controller input."""

    def __init__(self):
        super().__init__('Teleop Program')
        self.addParallel(snaplistener.SnapListener(0))
        self.addParallel(tankdrive.TankDrive())
