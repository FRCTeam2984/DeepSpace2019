from wpilib.command import InstantCommand
from subsystems import backarm


class SetBackArm(InstantCommand):
    def __init__(self, setpoint):
        super().__init__()
        self.arm = backarm.BackArm()
        self.requires(self.arm)
        self.setpoint = setpoint

    def initialize(self):
        self.arm.setAngle(self.setpoint)

    def end(self):
        pass
