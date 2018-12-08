from wpilib.command import CommandGroup, Scheduler


class TeleopCommandGroup(CommandGroup):
    """Gets robot following controller input"""

    def __init__(self):
        super().__init__('Teleop Program')
        Scheduler.getInstance().run()
