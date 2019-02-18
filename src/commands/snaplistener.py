import logging
from wpilib.command import Command
from wpilib import SmartDashboard as Dash

import oi
from commands import turntoangle
from subsystems import drive
from utils import angles

class SnapListener(Command):
    def __init__(self, pov_port):
        super().__init__()
        self.drive = drive.Drive()
        self.pov_port = 0
    
    def initialize(self):
        pass
    
    def execute(self):
        pov = oi.OI().driver.getPOV(self.pov_port)
        #logging.debug("drive current command: {}".format(self.drive.currentCommand))
        if pov != -1 and not isinstance(self.drive.currentCommand,turntoangle.TurnToAngle):
            pov = angles.positiveAngleToMixedAngle(pov)
            Dash.putNumber("Snap Turning Target", pov)
            logging.debug("Starting snap to angle")
            turntoangle.TurnToAngle(pov).start()
