from wpilib.command import Command, InstantCommand
from subsystems import longarm
from constants import Constants
import math


class SetLongArm(InstantCommand):
    def __init__(self, setpoint):
        super().__init__()
        self.arm = longarm.LongArm()
        self.requires(self.arm)
        self.setpoint = setpoint

    def initialize(self):
        self.arm.setAngle(math.degrees(
            math.asin(Constants.LONG_ARM_ANGLE/27.5)))

    def end(self):
        pass
