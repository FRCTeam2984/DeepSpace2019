import math
from wpilib import SmartDashboard as Dash
from wpilib.command import Command

from constants import Constants
from subsystems import frontarm
from utils import pidf, units
import odemetry
import wpilib


class SetFrontArm(Command):
    def __init__(self, setpoint):
        super().__init__()
        self.arm = frontarm.FrontArm()
        self.requires(self.arm)
        self.setpoint = setpoint
        self.timestamp = 0
        self.last_timestamp = 0
        self.cur_error = 0

    def initialize(self):
        self.kp = Constants.FRONT_ARM_KP
        self.ki = Constants.FRONT_ARM_KI
        self.kd = Constants.FRONT_ARM_KD
        self.kf = Constants.FRONT_ARM_KF
        self.controller = pidf.PIDF(
            self.setpoint, self.kp, self.ki, self.kd, self.kf)

    def execute(self):
        self.timestamp = self.timeSinceInitialized()
        dt = self.timestamp - self.last_timestamp
        self.last_timestamp = self.timestamp
        angle = math.fmod(self.arm.getAngle(), 2*math.pi)
        output = self.controller.update(angle, dt)
        Dash.putNumber("Front Arm Angle", angle)
        Dash.putNumber("Front Arm Output", output)
        Dash.putNumber("Front Arm Error", units.radiansToDegrees(
            self.controller.cur_error))
        self.arm.setPercent(output)

    def isFinished(self):
        return False

    def end(self):
        pass
