from wpilib.command import Command, InstantCommand
from subsystems import backarm
from constants import Constants


class SetBackArm(InstantCommand):
    def __init__(self, setpoint):
        super().__init__()
        self.arm = backarm.BackArm()
        self.requires(self.arm)
        self.setpoint = setpoint

    def initialize(self):
        self.arm.setMotion(self.setpoint)

    def end(self):
        pass
