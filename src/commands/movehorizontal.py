from wpilib.command import CommandGroup
from subsystems import drive
from commands import driveatcurvature, driveforward


class MoveHorizontal(CommandGroup):
    def __init__(self, distance):
        super().__init__('Move Right')
        self.addSequential(
            driveatcurvature.DriveAtCurvature(distance/2, 0.5, 1000))
        self.addSequential(
            driveatcurvature.DriveAtCurvature(distance/2, -0.5, 1000))
        self.addSequential(driveforward.DriveForward(distance, 0.5))
