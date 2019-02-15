import logging
from wpilib.command import Command

import oi
from commands import turntoangle
from subsystems import drive

class SnapListener(Command):
    def __init__(self, pov_port):
        super().__init__()
        self.drive = drive.Drive()
        self.pov_port = 0
    
    def initialize(self):
        pass
    
    def execute(self):
        pov = oi.OI().driver.getPOV(self.pov_port)
        logging.debug("drive current command: {}".format(self.drive.currentCommand))
        if pov != -1 and not self.drive.currentCommand is SnapListener:
            turntoangle.TurnToAngle(pov).start()
