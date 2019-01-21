from wpilib.command import Command

from constants import Constants
from diagnostic import Diagnostic
from wpilib.robotbase import hal


class CheckDiagnostics(Command):
    def __init__(self):
        super().__init__()
        self.diagnostic = Diagnostic()

    def initialize(self):
        pass

    def execute(self):
        self.diagnostic.update()
        if not hal.isSimulation(): #TODO no output on update
            self.diagnostic.log()
        self.diagnostic.outputToSmartDashboard()

    def isFinished(self):
        return False

    def end(self):
        pass
