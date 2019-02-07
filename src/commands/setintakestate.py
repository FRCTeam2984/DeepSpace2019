from wpilib.command import Command

from subsystems import intake
from utils.intakestate import IntakeState


class SetIntakeState(Command):
    def __init__(self, state):
        super().__init__()
        self.intake = intake.Intake()
        self.requires(self.intake)
        self.state = state
        self.setInterruptible(True)

    def initialize(self):
        pass

    def execute(self):
        if self.state == IntakeState.STOP:
            self.intake.stop()
        elif self.state == IntakeState.SPIT:
            self.intake.spit()
        elif self.state == IntakeState.SUCK:
            self.intake.suck()

    def isFinished(self):
        return False
