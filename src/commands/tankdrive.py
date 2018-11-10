import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from wpilib.command import Command
import math
import oi
from subsystems import drive

class TankDrive(Command):
    def __init__(self):
        super().__init__()
        self.requires(drive.Drive())

    def initialize(self):
        return

    def execute(self):
        power = math.pow(oi.OI().getJoystick().getX(), 3)
        rotation = -oi.OI().getJoystick().getY()
        rotation = (rotation, 0)[abs(rotation) < 0.05]
        left = power - rotation
        right = power + rotation
        drive.Drive().setPercentOutput(left, right)

    def isFinished(self):
        return False 

    def end(self):
        return

    def interrupted(self):
        self.end()
