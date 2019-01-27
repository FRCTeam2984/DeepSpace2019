import math
from wpilib import SmartDashboard as Dash
from wpilib.command import Command

from constants import Constants
from subsystems import backarm
from utils import pidf, units
import odemetry
import wpilib


class SetFrontArm(Command):
    def __init__(self, setpoint):
        super().__init__()
        self.arm = backarm.BackArm()
        self.requires(self.arm)
        self.setpoint = setpoint
        self.timestamp = 0
        self.last_timestamp = 0
        self.cur_error = 0

    def initialize(self):
        self.kp = Constants.BACK_ARM_KP
        self.ki = Constants.BACK_ARM_KI
        self.kd = Constants.BACK_ARM_KD
        self.kf = Constants.BACK_ARM_KF
        self.controller = pidf.PIDF(
            self.setpoint, self.kp, self.ki, self.kd, self.kf)

    def execute(self):
        self.timestamp = self.timeSinceInitialized()
        dt = self.timestamp - self.last_timestamp
        self.last_timestamp = self.timestamp
        angle = math.fmod(self.arm.getAngle(), 2*math.pi)
        output = self.controller.update(angle, dt)
        Dash.putNumber("Back Arm Angle", angle)
        Dash.putNumber("Back Arm Output", output)
        Dash.putNumber("Back Arm Error", units.radiansToDegrees(
            self.controller.cur_error))
        self.arm.setPercent(output)

    def isFinished(self):
        return False

    def end(self):
        pass
