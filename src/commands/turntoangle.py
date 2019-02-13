import math
import logging
from wpilib import SmartDashboard as Dash
from wpilib.command import Command
from wpilib import PIDController

from constants import Constants
from subsystems import drive
from utils import pidf, units
import odemetry
import wpilib
from wpilib import PIDController

class TurnToAngle(Command):
    def __init__(self, setpoint, relative=False):
        """Turn to setpoint (degrees)."""
        super().__init__()
        self.drive = drive.Drive()
        self.odemetry = odemetry.Odemetry()
        self.requires(self.drive)
        self.setpoint = units.degreesToRadians(setpoint)
        self.relative = relative
        self.timer = wpilib.Timer()
        self.timestamp = 0
        self.last_timestamp = 0
        self.cur_error = 0

    def initialize(self):
        # self.kp = Constants.TURN_TO_ANGLE_KP
        # self.ki = Constants.TURN_TO_ANGLE_KI
        # self.kd = Constants.TURN_TO_ANGLE_KD
        # self.kf = Constants.TURN_TO_ANGLE_KF
        self.pid_controller = PIDController(Constants.TURN_TO_ANGLE_KP, Constants.TURN_TO_ANGLE_KI, Constants.TURN_TO_ANGLE_KD, source=lambda: units.degreesToRadians(self.odemetry.getAngle()), )
        self.error_tolerance = units.degreesToRadians(
            Constants.TURN_TO_ANGLE_TOLERANCE)
        self.timeout = Constants.TURN_TO_ANGLE_TIMEOUT
        if self.relative:
            self.setpoint += units.degreesToRadians(self.odemetry.getAngle())
        self.controller = pidf.PIDF(
            self.setpoint, self.kp, self.ki, self.kd, self.kf, True, -math.pi, math.pi)
        self.timer.reset()

    def execute(self):
        self.timestamp = self.timeSinceInitialized()
        dt = self.timestamp - self.last_timestamp
        self.last_timestamp = self.timestamp
        angle = math.fmod(self.odemetry.getAngle(), 2 * math.pi)
        output = self.controller.update(angle, dt)
        if abs(output) < Constants.TURN_TO_ANGLE_MIN_OUTPUT:
            output = math.copysign(Constants.TURN_TO_ANGLE_MIN_OUTPUT, output)
        Dash.putNumber("Turn To Angle Output", output)
        Dash.putNumber("Turn To Angle Error",
                       units.radiansToDegrees(self.controller.cur_error))
        self.drive.setVelocityOutput(-output, output, -output, output)

    def isFinished(self):
        # if abs(self.controller.cur_error) <= self.error_tolerance and not self.timer.running:
        #     logging.debug("start")
        #     self.timer.start()
        # if abs(self.controller.cur_error) > self.error_tolerance and self.timer.running:
        #     logging.debug("stop")

        #     self.timer.stop()
        #     self.timer.reset()
        # return self.timer.get()*1000 >= self.timeout
        return False

    def end(self):
        self.drive.setPercentOutput(0, 0, 0, 0)
