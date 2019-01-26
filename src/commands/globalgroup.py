from wpilib.command import CommandGroup
from commands import updateodemetry, checkdiagnostics


class GlobalCommandGroup(CommandGroup):
    """Run at the start of all modes."""

    def __init__(self):
        super().__init__('Global Program')
        self.addParallel(updateodemetry.UpdateOdemetry())
        # self.addParallel(checkdiagnostics.CheckDiagnostics())
