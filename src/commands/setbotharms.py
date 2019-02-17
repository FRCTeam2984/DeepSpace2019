from commands import setshortarm, setlongarm

from wpilib.command import CommandGroup


class SetBothArms(CommandGroup):
    """Gets robot following controller input."""

    def __init__(self):
        super().__init__('Arms Program')
        self.addParallel(setshortarm.SetShortArm(30))
        self.addParallel(setlongarm.SetLongArm(30))
