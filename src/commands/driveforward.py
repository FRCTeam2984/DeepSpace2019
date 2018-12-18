from wpilib.command import Command

from constants import Constants
from subsystems import drive
import wpilib


class DriveForward(Command):
    def __init__(self, left_signal, right_signal, timeout=1000):
        super().__init__()
        self.drive = drive.Drive()
        self.requires(self.drive)

        self.timer = wpilib.Timer()
        self.timeout = timeout

        self.left_signal = left_signal
        self.right_signal = right_signal

    def initialize(self):
        self.timer.start()
        self.drive.setPercentOutput(self.left_signal, self.right_signal)

    def isFinished(self):
        return self.timer.get()*1000 >= self.timeout

    def end(self):
        self.drive.setPercentOutput(0, 0)
