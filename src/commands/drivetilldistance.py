import os
import sys
import time

from wpilib.command import Command
from constants import Constants
from subsystems import drive, distance

class DriveTillDistanceAway(Command):
    def __init__(self):
        super().__init__()
        self.drive = drive.Drive()
        self.distance = distance.DistanceSensor()
        self.distance.init()
        self.requires(self.drive)
        self.requires(self.distance)


    def initialize(self):
        print("INIT")
        self.drive.setPercentOutput(0.1, 0.1)

    def execute(self):
        print("RUNNING - {}".format( self.distance.distanceInches() ))
        pass

    def isFinished(self):
        return self.distance.distanceInches() <= Constants.DISTANCE_SENSOR_THRESHOLD

    def end(self):
        self.drive.setPercentOutput(0, 0)