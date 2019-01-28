from wpilib.command import Command

from constants import Constants
from subsystems import drive
import wpilib
from utils import units


class DriveTimed(Command):
    def __init__(self,  fl_signal, fr_signal, bl_signal, br_signal, timeout=1000):
        super().__init__()
        self.drive = drive.Drive()
        self.requires(self.drive)

        self.timer = wpilib.Timer()
        self.timeout = timeout

        self.fl_signal = fl_signal
        self.fr_signal = fr_signal
        self.bl_signal = bl_signal
        self.br_signal = br_signal

    def initialize(self):
        self.timer.start()
        self.drive.setPercentOutput(
            self.fl_signal, self.fr_signal, self.bl_signal, self.br_signal)

    def isFinished(self):
        return self.timer.get()*1000 >= self.timeout

    def end(self):
        self.drive.setPercentOutput2(0, 0, 0, 0)
