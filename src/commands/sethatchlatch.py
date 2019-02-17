from wpilib.command import InstantCommand
from enum import Enum

from subsystems import hatchlatch
import logging

class HatchState(Enum):
    OPEN = 1
    CLOSED = 2


class SetHatchLatch(InstantCommand):
    def __init__(self, hatch_state: HatchState):
        super().__init__()
        self.hatchlatch = hatchlatch.HatchLatch()
        self.requires(self.hatchlatch)
        self.hatch_state = hatch_state
    
    def initialize(self):
        logging.debug("Setting hatch latch state")
        if self.hatch_state == HatchState.OPEN:
            self.hatchlatch.setOpen()
        elif self.hatch_state == HatchState.CLOSED:
            self.hatchlatch.setClosed()
        else:
            logging.error("Unexpected state: {}".format(self.hatch_state))

    def end(self):
        pass