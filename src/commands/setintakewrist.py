from wpilib.command import InstantCommand
from subsystems import intakewrist


class SetIntakeWrist(InstantCommand):
    def __init__(self, setpoint):
        super().__init__()
        self.wrist = intakewrist.IntakeWrist()
        self.requires(self.wrist)
        self.setpoint = setpoint

    def initialize(self):
        self.wrist.setAngle(self.setpoint)

    def end(self):
        pass
