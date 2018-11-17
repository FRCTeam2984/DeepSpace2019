from wpilib.command import Command

import odemetry


class UpdateOdemetry(Command):
    def __init__(self):
        super().__init__()
        self.odemetry = odemetry.Odemetry()

    def initialize(self):
        self.odemetry.reset()

    def execute(self):
        self.odemetry.updateState(self.timeSinceInitialized())
        self.odemetry.outputToSmartDashboard()

    def isFinished(self):
        return False

    def end(self):
        return
