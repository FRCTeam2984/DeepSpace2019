from wpilib.command import InstantCommand

from subsystems import hatchlatch
from utils.hatchlatchstate import HatchLatchState


class SetHatchLatchState(InstantCommand):
    def __init__(self, state):
        super().__init__()
        self.hatchlatch = hatchlatch.HatchLatch()
        self.requires(self.hatchlatch)
        self.state = state

    def initialize(self):
        if self.state == HatchLatchState.CLOSE:
            self.hatchlatch.close()
        elif self.state == HatchLatchState.OPEN:
            self.hatchlatch.open()
        elif self.state == HatchLatchState.TOGGLE:
            self.hatchlatch.toggle()

    def end(self):
        pass
