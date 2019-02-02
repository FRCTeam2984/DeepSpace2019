from wpilib.command import Command
from subsystems import intakewrist


class SetIntakeWrist(Command):
    def __init__(self, setpoint):
        super().__init__()
        self.wrist = intakewrist.IntakeWrist()
        self.requires(self.wrist)
        self.setpoint = setpoint

    def initialize(self):
        pass

    def execute(self):
        self.wrist.setAngle(self.setpoint)

    def isFinished(self):
        return False

    def end(self):
        pass
