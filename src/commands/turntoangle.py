import math
from wpilib.command import Command

from constants import Constants
from subsystems import drive
from utils import pid, units
import odemetry
import wpilib


class TurnToAngle(Command):
    def __init__(self, setpoint, relative=False):
        super().__init__()
        self.drive = drive.Drive()
        self.odemetry = odemetry.Odemetry()
        self.requires(self.drive)
        self.setpoint = setpoint
        self.kp = Constants.TURN_TO_ANGLE_KP
        self.ki = Constants.TURN_TO_ANGLE_KI
        self.kd = Constants.TURN_TO_ANGLE_KD
        self.error_tolerance = Constants.TURN_TO_ANGLE_TOLERANCE
        self.timeout = Constants.TURN_TO_ANGLE_TIMEOUT
        self.controller = pid.PID(
            self.setpoint, self.kp, self.ki, self.kd, True, -math.pi, math.pi)
        self.timestamp = 0
        self.last_timestamp = 0
        self.cur_error = 0
        self.relative = relative

        self.timer = wpilib.Timer()
        self.timeout = 1000

    def initialize(self):
        self.timer.reset()
        if self.relative:
            self.setpoint += self.odemetry.getAngle()
            self.controller.setpoint = self.setpoint

    def execute(self):
        self.timestamp = self.timeSinceInitialized()
        dt = self.timestamp - self.last_timestamp
        self.last_timestamp = self.timestamp
        output = self.controller.update(self.odemetry.getAngle(), dt)
        print("Output: {}, Error: {}".format(
            output, units.radiansToDegrees(self.controller.cur_error)))
        self.drive.setDirectionOutput(0, 0, -output)

    def isFinished(self):
        if abs(self.controller.cur_error) < self.error_tolerance and not self.timer.running:
            self.timer.start()
        return self.timer.get()*1000 >= self.timeout

    def end(self):
        self.timer.stop()
        self.drive.setPercentOutput(0, 0, 0, 0)
        return
