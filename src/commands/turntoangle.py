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
    def _setMotors(self, signal):
        signal = signal if abs(
            signal) > Constants.TURN_TO_ANGLE_MIN_OUTPUT else math.copysign(Constants.TURN_TO_ANGLE_MIN_OUTPUT, signal)
        Dash.putNumber("Turn To Angle Output", signal)
        self.drive.setPercentOutput(signal, -signal, signal, -signal)

    def __init__(self, setpoint):
        """Turn to setpoint (degrees)."""
        super().__init__()
        self.drive = drive.Drive()
        self.odemetry = odemetry.Odemetry()
        self.requires(self.drive)
        self.setpoint = setpoint
        src = self.odemetry.pidgyro
        self.PID = PIDController(Constants.TURN_TO_ANGLE_KP, Constants.TURN_TO_ANGLE_KI,
                                 Constants.TURN_TO_ANGLE_KD, src, self._setMotors)
        logging.debug("Turn to angle constructed with angle {}".format(setpoint))
        self.PID.setInputRange(-180.0, 180.0)
        self.PID.setOutputRange(-0.7, 0.7)
        self.PID.setContinuous(True)
        self.PID.setAbsoluteTolerance(Constants.TURN_TO_ANGLE_TOLERANCE)
        self.PID.setPIDSourceType(PIDController.PIDSourceType.kDisplacement)

    def initialize(self):
        self.PID.setP(Constants.TURN_TO_ANGLE_KP)
        self.PID.setI(Constants.TURN_TO_ANGLE_KI)
        self.PID.setD(Constants.TURN_TO_ANGLE_KD)
        self.PID.setAbsoluteTolerance(Constants.TURN_TO_ANGLE_TOLERANCE)
        self.PID.setSetpoint(self.setpoint)
        self.PID.enable()

    def execute(self):
        Dash.putNumber("Turn To Angle Error", self.PID.getError())
        # logging.info(f"Turn To Angle Error {self.PID.getError()}")

    def isFinished(self):
        return self.PID.onTarget()

    def end(self):
        logging.debug("Finished turning to angle {}".format(self.setpoint))
        self.PID.disable()

    def interrupted(self):
        self.end()