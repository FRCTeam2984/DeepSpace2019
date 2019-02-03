from wpilib.command import InstantCommand
from subsystems import frontarm


class SetFrontArm(InstantCommand):
    def __init__(self, setpoint):
        super().__init__()
        self.arm = frontarm.FrontArm()
        self.requires(self.arm)
        self.setpoint = setpoint

    def initialize(self):
        self.arm.setAngle(self.setpoint)

    def end(self):
        pass
