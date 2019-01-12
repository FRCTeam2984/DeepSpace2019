from wpilib.command import CommandGroup
from subsystems import drive
from commands import zerosensors, calibratesensors


class DisabledCommandGroup(CommandGroup):
    """Commands to run when robot is disabled."""

    def __init__(self):
        super().__init__('Disabled Program')
        self.addSequential(calibratesensors.CalibrateSensors())
        self.addSequential(zerosensors.ZeroSensors())
