import logging
from wpilib.command import Command
from wpilib import SmartDashboard as Dash

import oi
from commands import turntoangle
from subsystems import drive
from utils import angles

class SnapListener(Command):
    POV_ARRAY = [0, 28.75, 90, 151.25, -179.9, -151.25, -90, -28.75]

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
            pov /= 45
            to_turn_to = SnapListener.POV_ARRAY[pov]
            to_turn_to = int(to_turn_to)
            Dash.putNumber("Snap Turning Target", to_turn_to)
            logging.debug("Starting snap to angle")
            turntoangle.TurnToAngle(to_turn_to).start()
