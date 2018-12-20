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
        self.kp = Constants.TURN_TO_ANGLE_KP
        self.ki = Constants.TURN_TO_ANGLE_KI
        self.kd = Constants.TURN_TO_ANGLE_KD
        self.error_tolerance = Constants.TURN_TO_ANGLE_TOLERANCE
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
