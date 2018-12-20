import math
from wpilib.command import Command

from constants import Constants
from subsystems import drive
from utils import pidf
import odemetry


class TurnToAngle(Command):
    def __init__(self, setpoint):
        super().__init__()
        self.drive = drive.Drive()
        self.odemetry = odemetry.Odemetry()
        self.requires(self.drive)
        self.setpoint = setpoint
        self.kp = 1
        self.ki = 1
        self.kd = 1
        self.error_tolerance = 1
        self.controller = pidf.PIDF(self.setpoint, self.kp, self.ki, self.kd)
        self.timestamp = 0
        self.last_timestamp = 0
        self.done_time = 0

    def initialize(self):
        return

    def execute(self):
        self.timestamp = self.timeSinceInitialized()
        dt = self.timestamp - self.last_timestamp
        self.last_timestamp = self.timestamp
        output = self.controller.update(self.odemetry.getAngle(), dt)
        print("Output: {}, Error: {}".format(
            output, self.controller.cur_error))
        self.drive.setPercentOutput(output, -output)

    def isFinished(self):
        return self.controller.cur_error < self.error_tolerance and self.controller.has_updated

    def end(self):
        self.drive.setPercentOutput(0, 0)
        return
