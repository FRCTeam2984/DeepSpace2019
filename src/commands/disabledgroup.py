from wpilib.command import CommandGroup
import subsystems.drive as drive
import commands.zerosensors as zerosensors

class DisabledCommandGroup(CommandGroup):
    """Commands to run when robot is disabled"""

    def __init__(self):
        super().__init__('Disabled Program')
        # TODO add gyro calibration stuff
        self.addSequential(zerosensors.ZeroSensors())

