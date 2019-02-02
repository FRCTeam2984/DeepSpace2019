from wpilib.command import Command
from subsystems import backarm


class SetBackArm(Command):
    def __init__(self, setpoint):
        super().__init__()
        self.arm = backarm.BackArm()
        self.requires(self.arm)
        self.setpoint = setpoint

    def initialize(self):
        pass

    def execute(self):
        self.arm.setAngle(self.setpoint)

    def isFinished(self):
        return False

    def end(self):
        pass
